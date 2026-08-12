import re
import logging
from typing import List, Dict, Optional, Any
from xml.etree import ElementTree as ET
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from app.core.config import settings
from app.models.document import Document

logger = logging.getLogger(__name__)

def _is_transient_error(exc: Exception) -> bool:
    if isinstance(exc, (httpx.NetworkError, httpx.TimeoutException)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in (429, 500, 502, 503, 504)
    return False

class PubMedConnector:
    """Async connector for NCBI PubMed E-utilities REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        email: Optional[str] = None,
        tool: Optional[str] = None,
        client: Optional[httpx.AsyncClient] = None
    ):
        self.base_url = (base_url or settings.PUBMED_BASE_URL).rstrip("/")
        raw_key = api_key if api_key is not None else settings.PUBMED_API_KEY
        # Sanitize API key (ignore empty or comment lines)
        if raw_key and not raw_key.startswith("#") and raw_key.strip():
            self.api_key = raw_key.strip()
        else:
            self.api_key = None

        self.email = email or settings.PUBMED_EMAIL
        self.tool = tool or settings.PUBMED_TOOL
        self._client = client
        self._owns_client = client is None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
            self._owns_client = True
        return self._client

    async def close(self):
        if self._owns_client and self._client and not self._client.is_closed:
            await self._client.aclose()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception(_is_transient_error),
        reraise=True
    )
    async def _request(self, endpoint: str, params: Dict[str, Any]) -> httpx.Response:
        client = await self._get_client()
        req_params = dict(params)
        if self.email:
            req_params["email"] = self.email
        if self.tool:
            req_params["tool"] = self.tool
        if self.api_key:
            req_params["api_key"] = self.api_key

        url = f"{self.base_url}/{endpoint}"
        response = await client.get(url, params=req_params)
        response.raise_for_status()
        return response

    async def search(
        self,
        query: str,
        max_results: int = 20,
        date_range: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Search PubMed via esearch.fcgi and return list of PMIDs."""
        if not query or not query.strip():
            return []

        params: Dict[str, Any] = {
            "db": "pubmed",
            "term": query.strip(),
            "retmax": max_results,
            "sort": "relevance",
            "retmode": "json"
        }

        if date_range:
            params["datetype"] = "pdat"
            from_yr = date_range.get("from_year") or date_range.get("from")
            to_yr = date_range.get("to_year") or date_range.get("to")
            if from_yr:
                params["mindate"] = str(from_yr)[:4]
            if to_yr:
                params["maxdate"] = str(to_yr)[:4]

        response = await self._request("esearch.fcgi", params)
        data = response.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        return id_list

    async def fetch_articles(self, pmids: List[str]) -> List[Document]:
        """Fetch article metadata and abstracts for a list of PMIDs via efetch.fcgi."""
        if not pmids:
            return []

        documents: List[Document] = []
        batch_size = 200

        for i in range(0, len(pmids), batch_size):
            batch = pmids[i:i + batch_size]
            params = {
                "db": "pubmed",
                "id": ",".join(batch),
                "retmode": "xml",
                "rettype": "abstract"
            }

            response = await self._request("efetch.fcgi", params)
            parsed_docs = self._parse_xml(response.text)
            documents.extend(parsed_docs)

        return documents

    def _parse_xml(self, xml_text: str) -> List[Document]:
        documents: List[Document] = []
        if not xml_text or not xml_text.strip():
            return documents

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            logger.error(f"PubMed XML Parse Error: {e}")
            return documents

        for article in root.findall(".//PubmedArticle"):
            doc = self._parse_single_article(article)
            if doc:
                documents.append(doc)

        return documents

    def _parse_single_article(self, article: ET.Element) -> Optional[Document]:
        try:
            medline = article.find("MedlineCitation")
            if medline is None:
                return None

            pmid_elem = medline.find("PMID")
            pmid = pmid_elem.text.strip() if pmid_elem is not None and pmid_elem.text else None
            if not pmid:
                return None

            art = medline.find("Article")
            if art is None:
                return None

            title_elem = art.find("ArticleTitle")
            title = "".join(title_elem.itertext()).strip() if title_elem is not None else f"PubMed Article {pmid}"

            abstract_text = ""
            abstract_elem = art.find("Abstract")
            if abstract_elem is not None:
                abstract_parts = []
                for abs_text in abstract_elem.findall("AbstractText"):
                    label = abs_text.attrib.get("Label")
                    text_content = "".join(abs_text.itertext()).strip()
                    if text_content:
                        if label:
                            abstract_parts.append(f"{label}: {text_content}")
                        else:
                            abstract_parts.append(text_content)
                abstract_text = "\n\n".join(abstract_parts)

            authors: List[str] = []
            author_list = art.find("AuthorList")
            if author_list is not None:
                for a in author_list.findall("Author"):
                    last_name = a.findtext("LastName")
                    fore_name = a.findtext("ForeName") or a.findtext("Initials")
                    collective = a.findtext("CollectiveName")
                    if last_name:
                        name = f"{last_name} {fore_name}" if fore_name else last_name
                        authors.append(name.strip())
                    elif collective:
                        authors.append(collective.strip())

            journal_elem = art.find(".//Journal/Title") or art.find(".//Journal/ISOAbbreviation")
            journal = journal_elem.text.strip() if journal_elem is not None and journal_elem.text else None

            pub_date = art.find(".//JournalIssue/PubDate")
            pub_year: Optional[int] = None
            pub_date_str: Optional[str] = None

            if pub_date is not None:
                year_elem = pub_date.find("Year")
                month_elem = pub_date.find("Month")
                day_elem = pub_date.find("Day")
                medline_date = pub_date.find("MedlineDate")

                if year_elem is not None and year_elem.text:
                    try:
                        pub_year = int(year_elem.text.strip()[:4])
                    except ValueError:
                        pass

                if medline_date is not None and medline_date.text:
                    pub_date_str = medline_date.text.strip()
                    if pub_year is None:
                        match = re.search(r"\b(19|20)\d{2}\b", pub_date_str)
                        if match:
                            pub_year = int(match.group(0))
                elif year_elem is not None and year_elem.text:
                    m_str = month_elem.text.strip() if month_elem is not None and month_elem.text else ""
                    d_str = day_elem.text.strip() if day_elem is not None and day_elem.text else ""
                    pub_date_str = f"{year_elem.text.strip()}-{m_str}-{d_str}".rstrip("-")

            doi: Optional[str] = None
            for elem in art.findall(".//ELocationID"):
                if elem.attrib.get("EIdType") == "doi" and elem.text:
                    doi = elem.text.strip()
                    break
            if not doi:
                article_ids = article.find(".//PubmedData/ArticleIdList")
                if article_ids is not None:
                    for aid in article_ids.findall("ArticleId"):
                        if aid.attrib.get("IdType") == "doi" and aid.text:
                            doi = aid.text.strip()
                            break

            mesh_terms: List[str] = []
            mesh_list = medline.find("MeshHeadingList")
            if mesh_list is not None:
                for mh in mesh_list.findall("MeshHeading"):
                    desc = mh.find("DescriptorName")
                    if desc is not None and desc.text:
                        mesh_terms.append(desc.text.strip())

            pub_types: List[str] = []
            pub_type_list = art.find("PublicationTypeList")
            if pub_type_list is not None:
                for pt in pub_type_list.findall("PublicationType"):
                    if pt.text:
                        pub_types.append(pt.text.strip())

            raw_study_type = ", ".join(pub_types) if pub_types else None
            mapped_study_type = self._map_study_type(pub_types)

            return Document(
                source="pubmed",
                external_id=pmid,
                pmid=pmid,
                doi=doi,
                title=title,
                abstract=abstract_text,
                authors=authors,
                journal=journal,
                publication_date=pub_date_str,
                publication_year=pub_year,
                study_type_raw=raw_study_type,
                study_type=mapped_study_type,
                mesh_terms=mesh_terms,
                url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                retrieval_method="api_keyword"
            )

        except Exception as e:
            logger.warning(f"Error parsing PubMed article XML: {e}")
            return None

    def _map_study_type(self, pub_types: List[str]) -> str:
        text = " ".join(pub_types).lower()
        if "meta-analysis" in text:
            return "meta_analysis"
        if "systematic review" in text:
            return "systematic_review"
        if "randomized controlled trial" in text or "clinical trial" in text:
            return "RCT"
        if "cohort studies" in text or "longitudinal study" in text:
            return "cohort"
        if "case-control studies" in text:
            return "case_control"
        if "cross-sectional" in text:
            return "cross_sectional"
        if "review" in text:
            return "review_narrative"
        if "case reports" in text or "case report" in text:
            return "case_report"
        return "unknown"
