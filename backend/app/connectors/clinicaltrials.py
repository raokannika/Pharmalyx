import re
import logging
from typing import List, Dict, Optional, Any
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

class ClinicalTrialsConnector:
    """Async connector for ClinicalTrials.gov REST API v2."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        client: Optional[httpx.AsyncClient] = None
    ):
        self.base_url = (base_url or settings.CLINICALTRIALS_BASE_URL).rstrip("/")
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
    async def _fetch_page(self, params: Dict[str, Any]) -> Dict[str, Any]:
        client = await self._get_client()
        url = f"{self.base_url}/studies"
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def search(
        self,
        condition: Optional[str] = None,
        intervention: Optional[str] = None,
        max_results: int = 20
    ) -> List[Document]:
        """Search ClinicalTrials.gov API v2 for studies matching condition/intervention."""
        params: Dict[str, Any] = {
            "format": "json",
            "pageSize": min(max_results, 100)
        }

        if condition and condition.strip():
            params["query.cond"] = condition.strip()
        if intervention and intervention.strip():
            params["query.intr"] = intervention.strip()

        # If neither is provided, don't send empty parameters, but log warning
        if "query.cond" not in params and "query.intr" not in params:
            logger.warning("ClinicalTrials search called without condition or intervention parameters.")

        documents: List[Document] = []
        next_page_token: Optional[str] = None

        while len(documents) < max_results:
            current_params = dict(params)
            if next_page_token:
                current_params["pageToken"] = next_page_token

            data = await self._fetch_page(current_params)
            studies = data.get("studies", [])
            if not studies:
                break

            for study in studies:
                doc = self._parse_study(study)
                if doc:
                    documents.append(doc)
                    if len(documents) >= max_results:
                        break

            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return documents

    def _parse_study(self, study: Dict[str, Any]) -> Optional[Document]:
        try:
            proto = study.get("protocolSection", {})
            ident = proto.get("identificationModule", {})
            nct_id = ident.get("nctId")
            if not nct_id:
                return None

            title = ident.get("officialTitle") or ident.get("briefTitle") or f"Clinical Trial {nct_id}"

            desc = proto.get("descriptionModule", {})
            brief_summary = desc.get("briefSummary", "")
            detailed_desc = desc.get("detailedDescription", "")

            status_mod = proto.get("statusModule", {})
            overall_status = status_mod.get("overallStatus", "UNKNOWN")
            last_update = status_mod.get("lastUpdatePostDateStruct", {}).get("date")
            start_date = status_mod.get("startDateStruct", {}).get("date")

            pub_date_str = last_update or start_date
            pub_year: Optional[int] = None
            if pub_date_str:
                match = re.search(r"\b(19|20)\d{2}\b", pub_date_str)
                if match:
                    pub_year = int(match.group(0))

            design = proto.get("designModule", {})
            raw_study_type = design.get("studyType", "INTERVENTIONAL")
            phases = design.get("phases", [])
            phase_str = ", ".join(phases) if phases else "N/A"

            sponsors_mod = proto.get("sponsorCollaboratorsModule", {})
            lead_sponsor = sponsors_mod.get("leadSponsor", {}).get("name")
            authors = [lead_sponsor] if lead_sponsor else []

            # Mapped study type
            mapped_type = self._map_study_type(raw_study_type, phases)

            journal_str = f"ClinicalTrials.gov (Phase: {phase_str}, Status: {overall_status})"

            eligibility = proto.get("eligibilityModule", {}).get("eligibilityCriteria")
            full_text_content = detailed_desc or eligibility

            return Document(
                source="clinicaltrials",
                external_id=nct_id,
                nct_id=nct_id,
                title=title,
                abstract=brief_summary,
                full_text=full_text_content,
                authors=authors,
                journal=journal_str,
                publication_date=pub_date_str,
                publication_year=pub_year,
                study_type_raw=raw_study_type,
                study_type=mapped_type,
                url=f"https://clinicaltrials.gov/study/{nct_id}",
                retrieval_method="api_keyword"
            )
        except Exception as e:
            logger.warning(f"Error parsing ClinicalTrials study JSON: {e}")
            return None

    def _map_study_type(self, raw_type: str, phases: List[str]) -> str:
        raw_upper = raw_type.upper()
        if "INTERVENTIONAL" in raw_upper or any("PHASE" in p.upper() for p in phases):
            return "RCT"
        if "OBSERVATIONAL" in raw_upper:
            return "cohort"
        return "unknown"
