# PHARMALYX — Complete Product & Engineering Reference

> **AI-Powered Pharmaceutical Research Intelligence System**
> Production-Grade Build Reference for Antigravity
> Version 1.0 | Phase 1 → Phase 2 Implementation Guide

---

## TABLE OF CONTENTS

1. [Product Overview](#1-product-overview)
2. [System Architecture](#2-system-architecture)
3. [Agent Specifications](#3-agent-specifications)
4. [API Design & Endpoints](#4-api-design--endpoints)
5. [Database Schema](#5-database-schema)
6. [Data Pipeline Design](#6-data-pipeline-design)
7. [AI/ML Components](#7-aiml-components)
8. [Frontend Architecture](#8-frontend-architecture)
9. [Infrastructure & DevOps](#9-infrastructure--devops)
10. [Folder Structure](#10-folder-structure)
11. [Environment Configuration](#11-environment-configuration)
12. [Backend Requirements (requirements.txt)](#12-backend-requirements)
13. [Frontend Requirements (package.json)](#13-frontend-requirements)
14. [Docker & Compose Setup](#14-docker--compose-setup)
15. [Security Architecture](#15-security-architecture)
16. [Testing Strategy](#16-testing-strategy)
17. [Performance & Scalability](#17-performance--scalability)
18. [Monitoring & Observability](#18-monitoring--observability)
19. [Implementation Roadmap](#19-implementation-roadmap)

---

# 1. PRODUCT OVERVIEW

## 1.1 What Pharmalyx Is

Pharmalyx is a **production-grade, multi-agent AI research intelligence platform** for pharmaceutical researchers, drug discovery scientists, and clinical research analysts. It aggregates evidence from multiple scientific data sources, performs deep semantic analysis, detects contradictions between research findings, and delivers structured, citation-backed research synthesis through a natural language interface.

**Core value proposition:** Ask a research question in plain English → receive a structured, ranked, contradiction-aware evidence report in under 8 seconds.

## 1.2 Key Differentiators

| Feature | Pharmalyx | PubMed | Semantic Scholar | Elsevier |
|---|---|---|---|---|
| Semantic similarity search | ✅ | ❌ | ✅ | Partial |
| Multi-source aggregation | ✅ | ❌ | ❌ | Partial |
| AI-generated summaries | ✅ | ❌ | Partial | ❌ |
| **Contradiction detection** | ✅ | ❌ | ❌ | ❌ |
| Evidence quality ranking (EQS) | ✅ | ❌ | Partial | Partial |
| Drug interaction intelligence | ✅ | ❌ | ❌ | ❌ |
| Natural language interface | ✅ | ❌ | Partial | ❌ |
| Citation-backed answers | ✅ | ❌ | Partial | ❌ |
| Conversational session memory | ✅ | ❌ | ❌ | ❌ |

## 1.3 Target Users

- **Primary:** Pharmaceutical researchers, drug discovery scientists (PhD level)
- **Secondary:** Clinical research analysts, biotech R&D teams, medical affairs
- **Tertiary:** Academic researchers, medical students, health economists

## 1.4 Core Capabilities

1. **Multi-source evidence retrieval** from PubMed, ClinicalTrials.gov, DrugBank, and USPTO patent database
2. **Semantic search** using BioBERT/PubMedBERT vector embeddings
3. **Evidence quality ranking** using composite EQS score
4. **Contradiction detection** using NLI-based ContraScore algorithm
5. **Abstractive summarisation** with inline citations
6. **Multi-turn conversational interface** with session memory
7. **Export** to PDF, BibTeX, CSV, and structured JSON
8. **Team workspaces** with shared research sessions
9. **Drug interaction intelligence** via DrugBank integration
10. **Clinical trial matching** via ClinicalTrials.gov integration

---

# 2. SYSTEM ARCHITECTURE

## 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PHARMALYX PLATFORM                              │
│                                                                         │
│  ┌──────────────────┐          ┌──────────────────────────────────────┐ │
│  │   React Frontend  │◄────────►│         FastAPI Gateway              │ │
│  │   (TypeScript)    │   REST   │      (API Router + Auth)            │ │
│  └──────────────────┘  /WS     └─────────────┬────────────────────────┘ │
│                                               │                         │
│                         ┌─────────────────────▼──────────────────────┐  │
│                         │           ORCHESTRATOR SERVICE              │  │
│                         │     (Agent Pipeline Manager + Session)      │  │
│                         └──┬──────┬──────┬──────┬──────┬─────────────┘  │
│                            │      │      │      │      │                 │
│              ┌─────────────▼─┐  ┌─▼──┐ ┌▼───┐ ┌▼───┐ ┌▼──────────┐   │
│              │  Agent 1: QUA  │  │RA  │ │ERA │ │CDA │ │SA   │RGA  │   │
│              │Query Understanding│ │Ret.│ │Rank│ │Cont│ │Sum. │Resp.│   │
│              └───────────────┘  └─┬──┘ └────┘ └────┘ └──────────┘   │
│                                   │                                     │
│           ┌───────────────────────▼───────────────────────────────────┐ │
│           │                   DATA LAYER                               │ │
│           │  ┌─────────┐ ┌──────────┐ ┌───────┐ ┌─────────────────┐  │ │
│           │  │PostgreSQL│ │ MongoDB  │ │ Redis │ │  FAISS Index    │  │ │
│           │  │(metadata)│ │(raw docs)│ │(cache)│ │(vector search)  │  │ │
│           │  └─────────┘ └──────────┘ └───────┘ └─────────────────┘  │ │
│           └───────────────────────────────────────────────────────────┘ │
│                                                                         │
│           ┌───────────────────────────────────────────────────────────┐ │
│           │              EXTERNAL DATA SOURCES                         │ │
│           │  ┌──────────┐ ┌──────────────────┐ ┌──────┐ ┌────────┐  │ │
│           │  │  PubMed  │ │ClinicalTrials.gov │ │Drug  │ │ USPTO  │  │ │
│           │  │ Entrez   │ │     REST API      │ │ Bank │ │Patents │  │ │
│           │  └──────────┘ └──────────────────┘ └──────┘ └────────┘  │ │
│           └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Service Architecture (Microservices)

```
pharmalyx/
├── api-gateway/          ← FastAPI: auth, routing, rate limiting
├── orchestrator/         ← Agent pipeline manager
├── agents/
│   ├── qua/              ← Query Understanding Agent
│   ├── retrieval/        ← Retrieval Agent
│   ├── ranking/          ← Evidence Ranking Agent
│   ├── contradiction/    ← Contradiction Detection Agent
│   ├── summarisation/    ← Summarisation Agent
│   └── response/         ← Response Generation Agent
├── data-pipeline/        ← Airflow ETL pipeline
├── vector-service/       ← FAISS index management
├── ml-service/           ← Model serving (embeddings, NLI, classification)
└── frontend/             ← React 18 dashboard
```

## 2.3 Request Lifecycle

```
User Query (HTTP POST /api/v1/query)
    │
    ▼
API Gateway
  → JWT validation
  → Rate limit check
  → Session load from Redis
    │
    ▼
Orchestrator
  → Start pipeline trace (OpenTelemetry)
  → Invoke Agent 1 (QUA)
    │
    ▼
Agent 1: QUA
  → BioBERT NER → entity extraction
  → Intent classifier → intent label
  → MeSH expansion → expanded terms
  → Output: structured_query{}
    │
    ▼
Agent 2: Retrieval Agent
  → FAISS semantic search (top 100)
  → PubMed API fetch
  → ClinicalTrials API fetch
  → DrugBank API fetch
  → Document normalisation → unified schema
  → Output: D_raw[]
    │
    ▼
Agent 3: Evidence Ranking Agent [PARALLEL with Agent 4 start]
  → Study type classification
  → Impact factor lookup (OpenAlex)
  → Citation count (OpenAlex)
  → EQS computation for each doc
  → Sort descending
  → Output: D_ranked[]
    │
    ▼
Agent 4: Contradiction Detection Agent
  → Claim sentence extraction
  → Entity overlap grouping
  → NLI pairwise inference
  → ContraScore computation
  → Threshold filtering (θ=0.72)
  → Output: contradiction_report{}
    │
    ▼
Agent 5: Summarisation Agent
  → SciFive/LLM summarisation (top 10 docs)
  → Citation injection
  → Evidence strength assessment
  → Output: evidence_summary{}
    │
    ▼
Agent 6: Response Generation Agent
  → Gemini API call with assembled context
  → Response formatting by intent
  → Follow-up suggestion generation
  → Session history update
  → Output: final_response{}
    │
    ▼
API Gateway → HTTP Response (JSON)
    │
    ▼
React Frontend → Render research cards + contradiction alerts
```

---

# 3. AGENT SPECIFICATIONS

## Agent 1: Query Understanding Agent (QUA)

### Purpose
Transforms raw natural language pharmaceutical queries into structured query objects that downstream agents can act upon. Performs intent classification, biomedical NER, query expansion, and disambiguation.

### Input Schema
```json
{
  "raw_query": "string",
  "session_id": "string",
  "conversation_history": [
    {
      "role": "user | assistant",
      "content": "string",
      "timestamp": "ISO8601"
    }
  ],
  "user_preferences": {
    "verbosity": "brief | standard | detailed",
    "temporal_preference": "recent | all",
    "study_type_preference": ["RCT", "meta_analysis", "all"]
  }
}
```

### Output Schema
```json
{
  "intent": "evidence_retrieval | drug_interaction | clinical_trial | contradiction_check | drug_comparison | general_summary",
  "entities": [
    {
      "entity_text": "string",
      "entity_type": "Drug | Disease | Gene | Protein | Outcome | Population | Procedure",
      "canonical_name": "string",
      "mesh_id": "string",
      "umls_cui": "string",
      "confidence": 0.0
    }
  ],
  "expanded_terms": {
    "entity_canonical_name": ["synonym1", "synonym2", "mesh_term"]
  },
  "temporal_filter": {
    "from_year": 2018,
    "to_year": 2024,
    "recency_bias": true
  },
  "comparison_mode": false,
  "comparison_entities": [],
  "pubmed_query_string": "string",
  "clinicaltrials_params": {},
  "is_followup": false,
  "resolved_from_history": false,
  "processing_time_ms": 0
}
```

### Models Used
- **NER:** `allenai/scibert_scivocab_uncased` fine-tuned on BC5CDR + NCBI Disease
- **Intent classifier:** `microsoft/BiomedNLP-BiomedBERT-base-uncased` fine-tuned, 6-class
- **Query expansion:** MeSH synonym table (SQLite local DB) + embedding nearest-neighbour

### System Prompt (Gemini API)
```
SYSTEM: You are a pharmaceutical research query analyst integrated into
Pharmalyx, a scientific evidence intelligence platform.

Your task: Analyse the researcher's query and extract structured information.

RULES:
- Extract ALL biomedical entities mentioned (drugs, diseases, genes, outcomes,
  populations, procedures).
- Use canonical drug names (e.g. "metformin" not "Glucophage").
- Map diseases to their standard names (e.g. "fatty liver" → "Non-alcoholic
  fatty liver disease (NAFLD)").
- If this is a follow-up query, resolve co-references from the conversation
  history provided.
- If the query is ambiguous, choose the most pharmaceutical-research-relevant
  interpretation.
- Generate MeSH-formatted PubMed query string using [MH] for MeSH terms and
  [TIAB] for title/abstract.
- DO NOT add information not present in the query.
- Respond ONLY in valid JSON matching the output schema exactly.
- No preamble. No explanation. No markdown fences. Raw JSON only.

CONVERSATION HISTORY: {conversation_history}
CURRENT QUERY: {raw_query}
USER PREFERENCES: {user_preferences}
```

### Implementation
```python
# agents/qua/agent.py
import json
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from services.mesh_service import MeSHSynonymService
from services.gemini_service import GeminiService
from models.query_schema import StructuredQuery

class QueryUnderstandingAgent:
    def __init__(self):
        self.ner_pipeline = pipeline(
            "ner",
            model="pruas/BENT-PubMedBERT-NER-Gene",
            aggregation_strategy="simple"
        )
        self.intent_classifier = pipeline(
            "text-classification",
            model="models/intent_classifier",  # fine-tuned locally
            top_k=1
        )
        self.mesh_service = MeSHSynonymService()
        self.gemini = GeminiService()

    async def process(self, raw_query: str, session_context: dict) -> StructuredQuery:
        # Step 1: NER
        entities = self.ner_pipeline(raw_query)
        
        # Step 2: Intent classification
        intent = self.intent_classifier(raw_query)[0]['label']
        
        # Step 3: MeSH expansion
        expanded = {}
        for ent in entities:
            expanded[ent['word']] = self.mesh_service.get_synonyms(ent['word'])
        
        # Step 4: Gemini for structured output + PubMed query generation
        prompt = self._build_prompt(raw_query, session_context)
        response = await self.gemini.generate(prompt)
        structured = json.loads(response)
        
        return StructuredQuery(**structured)

    def _build_prompt(self, query: str, context: dict) -> str:
        return QUA_SYSTEM_PROMPT.format(
            raw_query=query,
            conversation_history=json.dumps(context.get('history', []), indent=2),
            user_preferences=json.dumps(context.get('preferences', {}), indent=2)
        )
```

---

## Agent 2: Retrieval Agent (RA)

### Purpose
Executes multi-source document retrieval, normalises documents to a unified schema, generates embeddings, performs FAISS semantic search, and assembles the raw candidate document set.

### Input Schema
```json
{
  "structured_query": "StructuredQuery object from Agent 1",
  "retrieval_config": {
    "max_pubmed_results": 100,
    "max_clinical_trials": 20,
    "max_drugbank_entries": 10,
    "max_patents": 15,
    "faiss_top_k": 50,
    "use_bm25_fallback": true,
    "date_range": {
      "from": "1990-01-01",
      "to": "2024-12-31"
    }
  }
}
```

### Output Schema
```json
{
  "documents": [
    {
      "doc_id": "uuid",
      "source": "pubmed | clinicaltrials | drugbank | patent",
      "pmid": "string | null",
      "doi": "string | null",
      "nct_id": "string | null",
      "title": "string",
      "abstract": "string",
      "full_text": "string | null",
      "authors": ["string"],
      "journal": "string | null",
      "publication_date": "ISO8601",
      "publication_year": 2024,
      "study_type_raw": "string",
      "mesh_terms": ["string"],
      "keywords": ["string"],
      "citation_count_raw": 0,
      "impact_factor_raw": 0.0,
      "url": "string",
      "embedding": [0.0],
      "retrieval_score": 0.0,
      "retrieval_method": "faiss | bm25 | api_keyword",
      "chunks": [
        {
          "chunk_id": "uuid",
          "text": "string",
          "chunk_index": 0,
          "embedding": [0.0]
        }
      ]
    }
  ],
  "retrieval_stats": {
    "pubmed_fetched": 0,
    "clinicaltrials_fetched": 0,
    "drugbank_fetched": 0,
    "patents_fetched": 0,
    "faiss_returned": 0,
    "total_after_dedup": 0,
    "retrieval_time_ms": 0
  }
}
```

### Sub-Components

#### PubMed Connector
```python
# agents/retrieval/connectors/pubmed.py
import httpx
from xml.etree import ElementTree as ET
from tenacity import retry, stop_after_attempt, wait_exponential

class PubMedConnector:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    API_KEY = settings.PUBMED_API_KEY  # 10 req/sec with key vs 3/sec without

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def search(self, query: str, max_results: int = 100,
                     date_range: dict = None) -> list[str]:
        """Returns list of PMIDs"""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "sort": "relevance",
            "api_key": self.API_KEY,
            "retmode": "json"
        }
        if date_range:
            params["datetype"] = "pdat"
            params["mindate"] = date_range["from"][:4]
            params["maxdate"] = date_range["to"][:4]

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{self.BASE_URL}/esearch.fcgi", params=params)
            r.raise_for_status()
            return r.json()["esearchresult"]["idlist"]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def fetch_abstracts(self, pmids: list[str]) -> list[dict]:
        """Fetch full abstract data for list of PMIDs in batches of 200"""
        results = []
        for i in range(0, len(pmids), 200):
            batch = pmids[i:i+200]
            params = {
                "db": "pubmed",
                "id": ",".join(batch),
                "retmode": "xml",
                "rettype": "abstract",
                "api_key": self.API_KEY
            }
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.get(f"{self.BASE_URL}/efetch.fcgi", params=params)
                r.raise_for_status()
                results.extend(self._parse_xml(r.text))
        return results

    def _parse_xml(self, xml_text: str) -> list[dict]:
        root = ET.fromstring(xml_text)
        articles = []
        for article in root.findall('.//PubmedArticle'):
            try:
                medline = article.find('MedlineCitation')
                art = medline.find('Article')
                abstract_elem = art.find('.//AbstractText')
                pub_date = medline.find('.//PubDate')
                year_elem = pub_date.find('Year') if pub_date is not None else None

                articles.append({
                    "pmid": medline.find('PMID').text,
                    "title": art.find('ArticleTitle').text or "",
                    "abstract": abstract_elem.text if abstract_elem is not None else "",
                    "journal": art.find('.//Title').text or "",
                    "publication_year": int(year_elem.text) if year_elem is not None else None,
                    "authors": [
                        f"{a.find('LastName').text} {a.find('ForeName').text if a.find('ForeName') is not None else ''}"
                        for a in medline.findall('.//Author')
                        if a.find('LastName') is not None
                    ],
                    "mesh_terms": [
                        m.find('DescriptorName').text
                        for m in medline.findall('.//MeshHeading')
                        if m.find('DescriptorName') is not None
                    ]
                })
            except Exception:
                continue
        return articles
```

#### ClinicalTrials Connector
```python
# agents/retrieval/connectors/clinicaltrials.py
class ClinicalTrialsConnector:
    BASE_URL = "https://clinicaltrials.gov/api/v2"

    async def search(self, condition: str, intervention: str,
                     max_results: int = 20) -> list[dict]:
        params = {
            "query.cond": condition,
            "query.intr": intervention,
            "pageSize": max_results,
            "format": "json",
            "fields": "NCTId,BriefTitle,OfficialTitle,BriefSummary,"
                      "DetailedDescription,OverallStatus,Phase,StudyType,"
                      "StartDate,CompletionDate,EnrollmentCount,"
                      "PrimaryOutcomeMeasure,EligibilityCriteria,"
                      "LeadSponsorName,LastUpdatePostDate"
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{self.BASE_URL}/studies", params=params)
            r.raise_for_status()
            studies = r.json().get("studies", [])
            return [self._normalise(s) for s in studies]

    def _normalise(self, study: dict) -> dict:
        proto = study.get("protocolSection", {})
        ident = proto.get("identificationModule", {})
        desc = proto.get("descriptionModule", {})
        status = proto.get("statusModule", {})
        design = proto.get("designModule", {})
        outcomes = proto.get("outcomesModule", {})

        return {
            "nct_id": ident.get("nctId"),
            "title": ident.get("officialTitle") or ident.get("briefTitle", ""),
            "abstract": desc.get("briefSummary", ""),
            "full_text": desc.get("detailedDescription", ""),
            "status": status.get("overallStatus"),
            "phase": design.get("phases", []),
            "study_type": design.get("studyType"),
            "enrollment": design.get("enrollmentInfo", {}).get("count"),
            "primary_outcomes": [
                o.get("measure") for o in outcomes.get("primaryOutcomes", [])
            ],
            "source": "clinicaltrials",
            "url": f"https://clinicaltrials.gov/study/{ident.get('nctId')}"
        }
```

#### DrugBank Connector
```python
# agents/retrieval/connectors/drugbank.py
class DrugBankConnector:
    BASE_URL = "https://api.drugbank.com/v1"

    async def get_drug(self, drug_name: str) -> dict | None:
        headers = {"Authorization": f"Bearer {settings.DRUGBANK_API_KEY}"}
        async with httpx.AsyncClient(timeout=20) as client:
            # Search by name
            r = await client.get(
                f"{self.BASE_URL}/drugs",
                params={"q": drug_name, "fuzzy": "true"},
                headers=headers
            )
            if r.status_code != 200 or not r.json():
                return None

            drug_id = r.json()[0]["drugbank_id"]

            # Get full profile
            r2 = await client.get(
                f"{self.BASE_URL}/drugs/{drug_id}",
                headers=headers
            )
            return self._normalise(r2.json())

    async def get_interactions(self, drug_name: str) -> list[dict]:
        headers = {"Authorization": f"Bearer {settings.DRUGBANK_API_KEY}"}
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(
                f"{self.BASE_URL}/ddi",
                params={"drug": drug_name},
                headers=headers
            )
            return r.json() if r.status_code == 200 else []

    def _normalise(self, drug: dict) -> dict:
        return {
            "drugbank_id": drug.get("drugbank_id"),
            "name": drug.get("name"),
            "abstract": drug.get("description", ""),
            "mechanism_of_action": drug.get("mechanism_of_action", ""),
            "pharmacokinetics": drug.get("pharmacokinetics", ""),
            "indication": drug.get("indication", ""),
            "contraindications": drug.get("contraindications", ""),
            "drug_interactions": drug.get("drug_interactions", []),
            "source": "drugbank",
            "url": f"https://go.drugbank.com/drugs/{drug.get('drugbank_id')}"
        }
```

#### FAISS Service
```python
# services/vector_service/faiss_service.py
import faiss
import numpy as np
import pickle
from pathlib import Path

class FAISSService:
    def __init__(self, index_path: str, dimension: int = 768):
        self.dimension = dimension
        self.index_path = Path(index_path)
        self.index = self._load_or_create_index()
        self.doc_id_map = self._load_id_map()

    def _load_or_create_index(self) -> faiss.Index:
        if self.index_path.exists():
            return faiss.read_index(str(self.index_path))
        # IVF index for large-scale approximate search
        quantizer = faiss.IndexFlatL2(self.dimension)
        index = faiss.IndexIVFFlat(quantizer, self.dimension, 1024)
        index.nprobe = 32
        return index

    def search(self, query_embedding: np.ndarray, top_k: int = 50) -> list[dict]:
        """Returns list of {doc_id, score} dicts"""
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        distances, indices = self.index.search(
            query_norm.reshape(1, -1).astype(np.float32), top_k
        )
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1:
                doc_id = self.doc_id_map.get(int(idx))
                if doc_id:
                    results.append({
                        "doc_id": doc_id,
                        "score": float(1 - dist)  # convert L2 to similarity
                    })
        return results

    def add_documents(self, embeddings: np.ndarray, doc_ids: list[str]):
        """Add new document embeddings to the index"""
        if not self.index.is_trained:
            self.index.train(embeddings)
        
        start_idx = self.index.ntotal
        self.index.add(embeddings.astype(np.float32))
        
        # Update ID map
        for i, doc_id in enumerate(doc_ids):
            self.doc_id_map[start_idx + i] = doc_id
        
        self._save()

    def _save(self):
        faiss.write_index(self.index, str(self.index_path))
        with open(str(self.index_path) + '.ids', 'wb') as f:
            pickle.dump(self.doc_id_map, f)

    def _load_id_map(self) -> dict:
        id_map_path = str(self.index_path) + '.ids'
        if Path(id_map_path).exists():
            with open(id_map_path, 'rb') as f:
                return pickle.load(f)
        return {}
```

---

## Agent 3: Evidence Ranking Agent (ERA)

### Purpose
Re-ranks candidate documents using the composite Evidence Quality Score (EQS), incorporating semantic relevance, journal authority, publication recency, citation impact, and study methodology type.

### Governing Equation
```
EQS(d) = α·Sim(q,d) + β·IF(d) + γ·Rec(d) + δ·Cite(d) + ε·StudyType(d)

Default weights: α=0.35, β=0.20, γ=0.15, δ=0.15, ε=0.15

Where:
  Sim(q,d)   = cosine_similarity(q_embedding, d_embedding) ∈ [0,1]
  IF(d)      = journal_impact_factor_normalised ∈ [0,1]
  Rec(d)     = exp(-0.1 × (2024 - publication_year)) ∈ [0,1]
  Cite(d)    = log(1 + citations) / log(1 + max_citations) ∈ [0,1]
  StudyType(d) = {meta_analysis:1.0, systematic_review:0.9, RCT:0.8,
                  cohort:0.6, case_control:0.5, cross_sectional:0.4,
                  in_vitro:0.3, computational:0.25, case_report:0.2,
                  review_narrative:0.35} ∈ [0,1]
```

### Implementation
```python
# agents/ranking/agent.py
import numpy as np
from services.openalex_service import OpenAlexService
from models.document import RankedDocument

class EvidenceRankingAgent:
    STUDY_TYPE_WEIGHTS = {
        "meta_analysis": 1.0,
        "systematic_review": 0.9,
        "RCT": 0.8,
        "cohort": 0.6,
        "case_control": 0.5,
        "cross_sectional": 0.4,
        "review_narrative": 0.35,
        "in_vitro": 0.3,
        "computational": 0.25,
        "case_report": 0.2,
        "unknown": 0.15
    }
    WEIGHTS = {"sim": 0.35, "if": 0.20, "rec": 0.15, "cite": 0.15, "stype": 0.15}
    CURRENT_YEAR = 2024

    def __init__(self):
        self.openalex = OpenAlexService()
        self.study_type_classifier = StudyTypeClassifier()

    async def process(self, documents: list[dict], query_embedding: np.ndarray,
                      weights: dict = None) -> list[RankedDocument]:
        w = weights or self.WEIGHTS

        # Enrich with OpenAlex metadata (citation counts, impact factors)
        enriched = await self._enrich_metadata(documents)

        # Normalisation bounds
        max_if = max((d.get("impact_factor", 0) or 0 for d in enriched), default=1)
        max_cite = max((d.get("citation_count", 0) or 0 for d in enriched), default=1)

        ranked = []
        for doc in enriched:
            # Classify study type if not already known
            if not doc.get("study_type"):
                doc["study_type"] = await self.study_type_classifier.classify(
                    doc.get("title", ""), doc.get("abstract", "")
                )

            sim = float(doc.get("retrieval_score", 0))
            if_norm = min((doc.get("impact_factor") or 0) / max(max_if, 1), 1.0)
            year = doc.get("publication_year") or self.CURRENT_YEAR
            rec = np.exp(-0.1 * (self.CURRENT_YEAR - year))
            cite = np.log1p(doc.get("citation_count") or 0) / np.log1p(max_cite)
            stype = self.STUDY_TYPE_WEIGHTS.get(doc.get("study_type", "unknown"), 0.15)

            eqs = (w["sim"] * sim + w["if"] * if_norm + w["rec"] * rec +
                   w["cite"] * cite + w["stype"] * stype)

            ranked.append(RankedDocument(
                **doc,
                eqs_score=round(eqs, 4),
                eqs_components={
                    "semantic_similarity": round(sim, 4),
                    "journal_impact": round(if_norm, 4),
                    "recency": round(float(rec), 4),
                    "citation_impact": round(float(cite), 4),
                    "study_quality": round(stype, 4)
                }
            ))

        return sorted(ranked, key=lambda d: d.eqs_score, reverse=True)

    async def _enrich_metadata(self, documents: list[dict]) -> list[dict]:
        """Batch enrich documents with OpenAlex citation counts and journal IFs"""
        dois = [d.get("doi") for d in documents if d.get("doi")]
        pmids = [d.get("pmid") for d in documents if d.get("pmid")]
        metadata = await self.openalex.batch_fetch(dois=dois, pmids=pmids)

        for doc in documents:
            key = doc.get("doi") or doc.get("pmid")
            if key and key in metadata:
                doc.update(metadata[key])
        return documents
```

### System Prompt (Gemini — Study Type Classification)
```
SYSTEM: You are a biomedical research methodology expert.

Given a paper title and abstract, classify the study design into EXACTLY
ONE category:

CATEGORIES:
- meta_analysis: Statistical pooling of results from multiple primary studies
- systematic_review: Structured literature synthesis without meta-analysis
- RCT: Randomised controlled trial with prospective intervention allocation
- cohort: Prospective/retrospective follow-up of defined patient groups
- case_control: Retrospective case vs control comparison
- cross_sectional: Single time-point measurement study
- review_narrative: Unsystematic expert opinion review
- in_vitro: Cell/tissue/molecular laboratory experiments
- computational: Bioinformatics, modelling, simulation, AI/ML studies
- case_report: 1–5 individual patient case descriptions

TITLE: {title}
ABSTRACT: {abstract}

Respond with ONLY the category label. No punctuation. No explanation.
Example: RCT
```

---

## Agent 4: Contradiction Detection Agent (CDA)

### Purpose
The most novel agent. Identifies pairs of research claims from different studies that make conflicting assertions about the same pharmaceutical entity and outcome, using NLI + entity overlap scoring.

### Governing Equations
```
ContraScore(c_i, c_j) = P(Contradiction | NLI(c_i, c_j)) × TopicOverlap(c_i, c_j)

TopicOverlap(c_i, c_j) = |E(c_i) ∩ E(c_j)| / |E(c_i) ∪ E(c_j)|  [Jaccard]

Threshold: θ = 0.72
Flag contradiction if ContraScore > θ
```

### Implementation
```python
# agents/contradiction/agent.py
from transformers import pipeline
import itertools
from models.contradiction import ContradictionReport, ContradictionPair

class ContradictionDetectionAgent:
    NLI_MODEL = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
    THRESHOLD = 0.72
    MAX_CLAIMS_PER_DOC = 5
    MIN_TOPIC_OVERLAP = 0.30

    def __init__(self):
        self.nli_pipeline = pipeline(
            "zero-shot-classification",
            model=self.NLI_MODEL,
            device=0  # GPU
        )
        self.ner_pipeline = pipeline(
            "ner",
            model="allenai/scibert_scivocab_uncased",
            aggregation_strategy="simple"
        )
        self.gemini = GeminiService()

    async def process(self, ranked_documents: list[dict],
                      top_n: int = 20) -> ContradictionReport:
        docs = ranked_documents[:top_n]

        # Step 1: Extract claim sentences from each document
        all_claims = []
        for doc in docs:
            claims = self._extract_claims(doc)
            all_claims.extend(claims)

        # Step 2: Group claims by shared pharmaceutical entities
        entity_groups = self._group_by_entity(all_claims)

        # Step 3: Run NLI on cross-document pairs within entity groups
        contradiction_pairs = []
        for entity, claims in entity_groups.items():
            cross_doc_pairs = [
                (c1, c2) for c1, c2 in itertools.combinations(claims, 2)
                if c1["source_id"] != c2["source_id"]
            ]
            for c1, c2 in cross_doc_pairs:
                score, pair = await self._compare_claims(c1, c2, entity)
                if score >= self.THRESHOLD:
                    contradiction_pairs.append(pair)

        # Step 4: Sort by ContraScore descending
        contradiction_pairs.sort(key=lambda p: p.contra_score, reverse=True)

        # Step 5: Generate explanations for top pairs
        if contradiction_pairs:
            for pair in contradiction_pairs[:5]:
                pair.explanation = await self._generate_explanation(pair)

        return ContradictionReport(
            contradiction_pairs=contradiction_pairs,
            contradiction_alert=len(contradiction_pairs) > 0,
            contradiction_count=len(contradiction_pairs),
            high_confidence_count=sum(1 for p in contradiction_pairs
                                      if p.contra_score >= 0.85)
        )

    def _extract_claims(self, doc: dict) -> list[dict]:
        """Extract sentences likely to be key claims (contain entity + outcome)"""
        text = doc.get("abstract", "") or doc.get("full_text", "")
        sentences = self._sentence_split(text)
        outcome_keywords = {
            "significantly", "reduced", "increased", "improved", "no effect",
            "effective", "ineffective", "associated", "correlated", "prevented",
            "caused", "inhibited", "enhanced", "p<", "p =", "OR", "RR", "HR",
            "confidence interval", "statistically"
        }
        claims = []
        for sent in sentences:
            sent_lower = sent.lower()
            entities = self.ner_pipeline(sent)
            has_pharma_entity = any(
                e["entity_group"] in ["Chemical", "Disease", "Gene"]
                for e in entities
            )
            has_outcome = any(kw in sent_lower for kw in outcome_keywords)

            if has_pharma_entity and has_outcome and len(sent.split()) >= 8:
                pharma_entities = {
                    e["word"].lower() for e in entities
                    if e["entity_group"] in ["Chemical", "Disease"]
                }
                claims.append({
                    "text": sent,
                    "source_id": doc["doc_id"],
                    "source_pmid": doc.get("pmid"),
                    "source_title": doc.get("title"),
                    "source_citation": self._format_citation(doc),
                    "entities": pharma_entities,
                    "eqs_score": doc.get("eqs_score", 0)
                })
        return claims[:self.MAX_CLAIMS_PER_DOC]

    def _group_by_entity(self, claims: list[dict]) -> dict[str, list]:
        """Group claims by shared pharmaceutical entity"""
        groups = {}
        for claim in claims:
            for entity in claim["entities"]:
                if entity not in groups:
                    groups[entity] = []
                groups[entity].append(claim)
        # Only keep groups with ≥2 claims from different documents
        return {
            e: c for e, c in groups.items()
            if len(set(cl["source_id"] for cl in c)) >= 2
        }

    async def _compare_claims(self, c1: dict, c2: dict,
                               shared_entity: str) -> tuple[float, ContradictionPair]:
        # Topic overlap (Jaccard on entity sets)
        e1, e2 = c1["entities"], c2["entities"]
        topic_overlap = len(e1 & e2) / len(e1 | e2) if (e1 | e2) else 0

        # NLI inference
        nli_result = self.nli_pipeline(
            c1["text"],
            candidate_labels=["entailment", "neutral", "contradiction"],
            hypothesis_template=c2["text"]
        )
        label_scores = dict(zip(nli_result["labels"], nli_result["scores"]))
        contra_prob = label_scores.get("contradiction", 0)

        contra_score = contra_prob * topic_overlap

        pair = ContradictionPair(
            claim_1_text=c1["text"],
            claim_1_source=c1["source_citation"],
            claim_1_pmid=c1.get("source_pmid"),
            claim_2_text=c2["text"],
            claim_2_source=c2["source_citation"],
            claim_2_pmid=c2.get("source_pmid"),
            shared_entity=shared_entity,
            contra_score=round(contra_score, 4),
            nli_label="contradiction" if contra_prob > 0.5 else "neutral",
            nli_confidence=round(contra_prob, 4),
            topic_overlap=round(topic_overlap, 4),
            explanation=""
        )
        return contra_score, pair

    async def _generate_explanation(self, pair: ContradictionPair) -> str:
        prompt = CDA_EXPLANATION_PROMPT.format(
            claim_1=pair.claim_1_text,
            source_1=pair.claim_1_source,
            claim_2=pair.claim_2_text,
            source_2=pair.claim_2_source,
            entity=pair.shared_entity,
            nli_confidence=pair.nli_confidence,
            contra_score=pair.contra_score
        )
        return await self.gemini.generate(prompt)
```

### System Prompt (Gemini — Contradiction Explanation)
```
SYSTEM: You are a pharmaceutical research analyst specialising in
identifying and explaining contradictory evidence between scientific
studies for Pharmalyx, an evidence intelligence platform.

Two research claims have been flagged as contradictory by a biomedical
NLI model (ContraScore: {contra_score}, NLI confidence: {nli_confidence}).

CLAIM FROM STUDY 1: "{claim_1}"
SOURCE 1: {source_1}

CLAIM FROM STUDY 2: "{claim_2}"
SOURCE 2: {source_2}

SHARED PHARMACEUTICAL ENTITY: {entity}

Write a precise 2–3 sentence explanation for a PhD-level pharmaceutical
researcher:
1. Sentence 1: State exactly what Study 1 claims vs Study 2 claims
   about {entity}.
2. Sentence 2: Note contextual differences that may explain the conflict
   (population, dosage, duration, endpoint definition, study design,
   era of publication).
3. Sentence 3: Advise on how to interpret this conflict given the relative
   evidence quality of the two studies.

RULES:
- Be specific and factual. No hedging language like "it appears".
- Do not make clinical recommendations.
- Do not speculate beyond what is in the claims.
- Write at PhD researcher level.
- Maximum 80 words total.
- Return ONLY the explanation text. No preamble.
```

---

## Agent 5: Summarisation Agent (SA)

### Purpose
Generates structured, abstractive summaries of ranked evidence. Synthesises across multiple studies, injects citations, produces conflict summaries, and assesses overall evidence strength.

### Input Schema
```json
{
  "ranked_documents": "top 10 RankedDocument objects",
  "contradiction_report": "ContradictionReport from Agent 4",
  "structured_query": "StructuredQuery from Agent 1",
  "verbosity": "brief | standard | detailed"
}
```

### Output Schema
```json
{
  "main_summary": "string (200-400 words, inline citations)",
  "key_findings": [
    {
      "finding": "string",
      "citation": "string",
      "pmid": "string",
      "evidence_level": "High | Moderate | Low"
    }
  ],
  "study_populations": "string",
  "methodological_limitations": "string",
  "conflict_summary": "string | null",
  "evidence_strength": "Strong | Moderate | Weak | Insufficient",
  "evidence_strength_rationale": "string",
  "recommended_readings": [
    {
      "title": "string",
      "citation": "string",
      "pmid": "string",
      "justification": "string"
    }
  ],
  "processing_time_ms": 0
}
```

### System Prompt (Gemini API)
```
SYSTEM: You are a pharmaceutical research intelligence analyst for
Pharmalyx. Your task is to synthesise evidence from multiple scientific
studies into a structured research summary.

RESEARCH QUERY: {original_query}
DETECTED ENTITIES: {entity_list}
DETECTED INTENT: {intent}
VERBOSITY LEVEL: {verbosity}

RANKED EVIDENCE DOCUMENTS (JSON, ordered by Evidence Quality Score,
highest first — respect this ordering in your synthesis):
{ranked_documents_json}

CONTRADICTION ALERTS FROM ANALYSIS:
{contradiction_summary}

TASK: Generate a structured research summary with the following EXACT
sections in this EXACT order:

## MAIN SUMMARY
Write {word_count_by_verbosity} words synthesising what the evidence
COLLECTIVELY shows. Do NOT list papers one by one. Synthesise across
studies — identify consensus, uncertainty, and key debates. Use inline
citation markers [1], [2], etc. referencing document positions in the
ranked list. Lead with the strongest/most relevant evidence. Mention
contradiction alerts if present.

## KEY FINDINGS
List {findings_count} specific, discrete findings. Each finding must be:
- One complete sentence
- Include inline citation [n]
- State direction and magnitude where available
- Format: "Finding statement [n]."

## STUDY POPULATIONS
One paragraph: types of patients/subjects studied, dosages, clinical
settings, countries, time periods, inclusion/exclusion criteria mentioned
across the top studies.

## METHODOLOGICAL LIMITATIONS
One paragraph: key weaknesses in this evidence base
(heterogeneity, small samples, surrogate endpoints, industry funding,
follow-up duration, publication bias).

## EVIDENCE STRENGTH: [Strong / Moderate / Weak / Insufficient]
One sentence justifying the rating based on study types and consistency.

## RECOMMENDED READINGS
Exactly 3 entries. Format:
[n] Author et al. (Year). "Title." Journal. — Justification (one line).

RULES:
- Do NOT add information not in the provided documents.
- Do NOT make clinical recommendations.
- Do NOT use second person ("you should").
- Write at PhD pharmaceutical researcher level.
- Respect the EQS ranking — weight top-ranked documents more heavily.
- If contradiction_summary is non-empty, always include it in MAIN SUMMARY.
- Do NOT use markdown headers that start with # — use plain text section
  labels as shown above.
```

---

## Agent 6: Response Generation Agent (RGA)

### Purpose
Final agent. Assembles outputs of all prior agents into a coherent, formatted, intent-appropriate research response. Manages conversational context for multi-turn sessions, formats output for the React dashboard.

### Input Schema
```json
{
  "original_query": "string",
  "conversation_history": [],
  "structured_query": "StructuredQuery",
  "ranked_documents": "list[RankedDocument] (top 20)",
  "contradiction_report": "ContradictionReport",
  "evidence_summary": "EvidenceSummary",
  "user_preferences": {},
  "session_id": "string"
}
```

### Output Schema
```json
{
  "response_text": "string",
  "intent_label": "string",
  "entity_labels": ["string"],
  "evidence_cards": [
    {
      "doc_id": "string",
      "title": "string",
      "authors_short": "string",
      "journal": "string",
      "year": 2024,
      "pmid": "string",
      "doi": "string",
      "url": "string",
      "abstract_excerpt": "string",
      "study_type": "string",
      "eqs_score": 0.0,
      "eqs_components": {},
      "source": "string",
      "has_contradiction": false,
      "contradiction_badge": "string | null"
    }
  ],
  "contradiction_alerts": [
    {
      "alert_id": "uuid",
      "severity": "high | medium | low",
      "entity": "string",
      "headline": "string",
      "claim_1_excerpt": "string",
      "claim_1_source": "string",
      "claim_2_excerpt": "string",
      "claim_2_source": "string",
      "contra_score": 0.0,
      "explanation": "string"
    }
  ],
  "follow_up_suggestions": ["string", "string", "string"],
  "evidence_strength": "string",
  "total_sources_retrieved": 0,
  "sources_analysed": 0,
  "processing_time_ms": 0,
  "session_id": "string",
  "export_payload": {
    "pdf_data": {},
    "bibtex": "string",
    "csv_rows": []
  }
}
```

### System Prompt (Gemini API)
```
SYSTEM: You are Pharmalyx, an AI-powered pharmaceutical research
intelligence assistant. You respond to pharmaceutical researchers,
drug discovery scientists, and clinical research analysts.

SESSION CONTEXT:
  Query: {user_query}
  Intent: {intent}
  Primary entities: {entity_list}
  Conversation history (last 5 turns): {conversation_history}

PIPELINE OUTPUTS AVAILABLE TO YOU:
  Evidence Summary: {evidence_summary}
  Top 10 ranked documents (title, year, EQS, study type): {top_docs_brief}
  Contradiction alerts ({contra_count} detected): {contradiction_alerts}
  Evidence strength: {evidence_strength}
  Total sources: {total_sources} ({sources_analysed} analysed in detail)

RESPONSE RULES:

TONE: Professional, precise, scientific. PhD-level audience.

FORMAT BY INTENT:
  evidence_retrieval → Lead with synthesis → evidence quality → contradictions
  contradiction_check → Lead with contradiction findings → explain each → context
  drug_interaction → Lead with interaction summary → mechanism → evidence strength
  clinical_trial → Lead with trial status → primary outcomes → evidence quality
  drug_comparison → Side-by-side analysis → evidence for each → conclusion
  general_summary → Balanced overview of current knowledge state

ALWAYS DO:
  - Begin with a direct answer to the query (1–2 sentences).
  - Include inline citations [Author, Year, PMID] for specific claims.
  - If contradictions exist: include "⚠ CONFLICTING EVIDENCE" section,
    name the specific studies, summarise the conflict, explain likely cause.
  - State the evidence strength (Strong/Moderate/Weak/Insufficient) and
    briefly explain why.
  - End with exactly 3 follow-up research questions labelled
    "SUGGESTED NEXT QUERIES:"

NEVER DO:
  - Make prescriptive clinical recommendations.
  - Add information not in the pipeline outputs.
  - Express false certainty about unclear evidence.
  - Omit detected contradictions.
  - Use hedge language like "it seems" or "one might argue".
  - Address the researcher as "you" in a condescending way.

RESPONSE LENGTH: {length_by_verbosity}
```

---

# 4. API DESIGN & ENDPOINTS

## 4.1 Base URL Structure

```
Production: https://api.pharmalyx.com/v1
Staging:    https://staging-api.pharmalyx.com/v1
Local:      http://localhost:8000/api/v1
```

## 4.2 Authentication

All endpoints (except `/auth/*` and `/health`) require a JWT Bearer token in the Authorization header.

```
Authorization: Bearer <jwt_token>
```

JWT payload:
```json
{
  "sub": "user_id",
  "org_id": "org_id",
  "role": "researcher | team_lead | admin",
  "plan": "free | pro | enterprise",
  "exp": 1234567890,
  "iat": 1234567890
}
```

## 4.3 Complete Endpoint Reference

### Auth Endpoints
```
POST   /auth/register          → Create new user account
POST   /auth/login             → Login, returns JWT + refresh token
POST   /auth/refresh           → Refresh JWT using refresh token
POST   /auth/logout            → Invalidate refresh token
POST   /auth/forgot-password   → Send password reset email
POST   /auth/reset-password    → Reset password with token
GET    /auth/me                → Get current user profile
PATCH  /auth/me                → Update user profile
```

### Query Endpoints
```
POST   /query                  → Main research query endpoint (streaming SSE)
POST   /query/sync             → Synchronous query (for testing/simple clients)
GET    /query/{query_id}       → Get query result by ID
GET    /query/history          → Get query history for current user
DELETE /query/{query_id}       → Delete query from history
POST   /query/{query_id}/feedback → Submit relevance feedback (thumbs up/down)
```

#### POST /query — Request Body
```json
{
  "query": "string (required, max 1000 chars)",
  "session_id": "string (optional, for multi-turn)",
  "config": {
    "max_results": 50,
    "include_patents": true,
    "include_clinical_trials": true,
    "date_range": {
      "from_year": 1990,
      "to_year": 2024
    },
    "study_type_filter": [],
    "verbosity": "brief | standard | detailed",
    "stream": true
  }
}
```

#### POST /query — SSE Response Stream
```
data: {"event": "agent_start", "agent": "qua", "message": "Analysing query..."}
data: {"event": "agent_complete", "agent": "qua", "data": {...structured_query}}
data: {"event": "agent_start", "agent": "retrieval", "message": "Searching databases..."}
data: {"event": "retrieval_progress", "source": "pubmed", "count": 47}
data: {"event": "retrieval_progress", "source": "clinicaltrials", "count": 12}
data: {"event": "agent_complete", "agent": "retrieval", "data": {"total": 59}}
data: {"event": "agent_start", "agent": "ranking", "message": "Ranking evidence..."}
data: {"event": "agent_complete", "agent": "ranking", "data": {...top_10_preview}}
data: {"event": "agent_start", "agent": "contradiction", "message": "Checking for conflicts..."}
data: {"event": "contradiction_found", "count": 2, "entity": "metformin"}
data: {"event": "agent_complete", "agent": "contradiction", "data": {...}}
data: {"event": "agent_start", "agent": "summarisation", "message": "Synthesising evidence..."}
data: {"event": "agent_complete", "agent": "summarisation", "data": {...}}
data: {"event": "generating_response", "message": "Generating research report..."}
data: {"event": "response_token", "token": "The"}
data: {"event": "response_token", "token": " evidence"}
...
data: {"event": "complete", "data": {...full_response_object}}
```

### Session Endpoints
```
POST   /sessions               → Create new research session
GET    /sessions               → List user's sessions
GET    /sessions/{session_id}  → Get session with full history
PATCH  /sessions/{session_id}  → Update session (rename, add tags)
DELETE /sessions/{session_id}  → Delete session
POST   /sessions/{session_id}/share → Generate shareable link
```

### Document Endpoints
```
GET    /documents/{doc_id}         → Get full document details
GET    /documents/{doc_id}/full-text → Fetch full text if available
POST   /documents/save             → Save document to library
GET    /documents/library          → Get user's saved library
DELETE /documents/library/{doc_id} → Remove from library
```

### Export Endpoints
```
POST   /export/pdf         → Generate PDF report from query result
POST   /export/bibtex      → Generate BibTeX for citations
POST   /export/csv         → Export evidence data as CSV
POST   /export/json        → Full JSON export of query result
```

### Admin Endpoints
```
GET    /admin/users        → List all users (admin only)
PATCH  /admin/users/{id}   → Update user (role, plan)
GET    /admin/stats        → Platform usage statistics
POST   /admin/reindex      → Trigger FAISS index rebuild
GET    /admin/pipeline/status → Check all agent service health
```

### Health Endpoints
```
GET    /health             → Basic health check (no auth)
GET    /health/detailed    → Detailed service health (admin auth)
GET    /metrics            → Prometheus metrics endpoint
```

---

# 5. DATABASE SCHEMA

## 5.1 PostgreSQL Schema (Relational Metadata)

```sql
-- ─── USERS & AUTH ─────────────────────────────────────────────────────────

CREATE TABLE organisations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    plan            VARCHAR(50) NOT NULL DEFAULT 'free',
    api_key_hash    VARCHAR(255),
    max_queries_day INTEGER NOT NULL DEFAULT 100,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id          UUID REFERENCES organisations(id) ON DELETE SET NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255),
    role            VARCHAR(50) NOT NULL DEFAULT 'researcher',
    plan            VARCHAR(50) NOT NULL DEFAULT 'free',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    email_verified  BOOLEAN NOT NULL DEFAULT FALSE,
    last_login_at   TIMESTAMPTZ,
    preferences     JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE refresh_tokens (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash  VARCHAR(255) NOT NULL UNIQUE,
    expires_at  TIMESTAMPTZ NOT NULL,
    revoked     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─── SESSIONS & QUERIES ────────────────────────────────────────────────────

CREATE TABLE sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           VARCHAR(500),
    tags            TEXT[] DEFAULT '{}',
    is_shared       BOOLEAN NOT NULL DEFAULT FALSE,
    share_token     VARCHAR(255) UNIQUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE queries (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id          UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    raw_query           TEXT NOT NULL,
    structured_query    JSONB,
    intent              VARCHAR(100),
    entities            JSONB,
    status              VARCHAR(50) NOT NULL DEFAULT 'pending',
    -- Status values: pending, processing, complete, error
    error_message       TEXT,
    total_docs_retrieved INTEGER DEFAULT 0,
    total_docs_ranked    INTEGER DEFAULT 0,
    contradiction_count  INTEGER DEFAULT 0,
    evidence_strength    VARCHAR(50),
    processing_time_ms   INTEGER,
    agent_timings        JSONB DEFAULT '{}',
    user_feedback        INTEGER CHECK (user_feedback IN (-1, 0, 1)),
    feedback_notes       TEXT,
    config               JSONB NOT NULL DEFAULT '{}',
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at         TIMESTAMPTZ
);

CREATE TABLE query_results (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id            UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    response_text       TEXT,
    evidence_summary    JSONB,
    contradiction_report JSONB,
    evidence_cards      JSONB,
    follow_up_suggestions TEXT[],
    export_payload      JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─── DOCUMENTS & KNOWLEDGE BASE ────────────────────────────────────────────

CREATE TABLE documents (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source              VARCHAR(50) NOT NULL,
    -- Source values: pubmed, clinicaltrials, drugbank, patent
    external_id         VARCHAR(255),
    -- PMID, NCT ID, DrugBank ID, Patent number
    doi                 VARCHAR(255),
    title               TEXT NOT NULL,
    abstract_text       TEXT,
    full_text           TEXT,
    authors             JSONB DEFAULT '[]',
    journal             VARCHAR(500),
    publication_year    INTEGER,
    publication_date    DATE,
    study_type          VARCHAR(100),
    mesh_terms          TEXT[] DEFAULT '{}',
    keywords            TEXT[] DEFAULT '{}',
    impact_factor       FLOAT,
    citation_count      INTEGER,
    url                 TEXT,
    is_indexed          BOOLEAN NOT NULL DEFAULT FALSE,
    faiss_index_id      BIGINT,
    metadata            JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source, external_id)
);

CREATE INDEX idx_documents_source ON documents(source);
CREATE INDEX idx_documents_year ON documents(publication_year);
CREATE INDEX idx_documents_doi ON documents(doi) WHERE doi IS NOT NULL;
CREATE INDEX idx_documents_pmid ON documents(external_id) WHERE source = 'pubmed';
CREATE INDEX idx_documents_study_type ON documents(study_type);
CREATE INDEX idx_documents_is_indexed ON documents(is_indexed);

CREATE TABLE document_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id     UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index     INTEGER NOT NULL,
    chunk_text      TEXT NOT NULL,
    faiss_index_id  BIGINT,
    is_indexed      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (document_id, chunk_index)
);

CREATE INDEX idx_chunks_document_id ON document_chunks(document_id);
CREATE INDEX idx_chunks_faiss_id ON document_chunks(faiss_index_id)
    WHERE faiss_index_id IS NOT NULL;

-- ─── QUERY–DOCUMENT RELATIONSHIP ───────────────────────────────────────────

CREATE TABLE query_documents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id        UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    document_id     UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    retrieval_rank  INTEGER,
    eqs_score       FLOAT,
    eqs_components  JSONB,
    retrieval_score FLOAT,
    study_type      VARCHAR(100),
    included_in_summary BOOLEAN DEFAULT FALSE,
    user_saved      BOOLEAN DEFAULT FALSE,
    UNIQUE (query_id, document_id)
);

-- ─── CONTRADICTIONS ────────────────────────────────────────────────────────

CREATE TABLE contradictions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id        UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    doc_1_id        UUID NOT NULL REFERENCES documents(id),
    doc_2_id        UUID NOT NULL REFERENCES documents(id),
    claim_1_text    TEXT NOT NULL,
    claim_2_text    TEXT NOT NULL,
    shared_entity   VARCHAR(255) NOT NULL,
    contra_score    FLOAT NOT NULL,
    nli_label       VARCHAR(50),
    nli_confidence  FLOAT,
    topic_overlap   FLOAT,
    explanation     TEXT,
    severity        VARCHAR(20) NOT NULL DEFAULT 'medium',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contradictions_query ON contradictions(query_id);
CREATE INDEX idx_contradictions_entity ON contradictions(shared_entity);

-- ─── USER LIBRARY ──────────────────────────────────────────────────────────

CREATE TABLE user_library (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    notes       TEXT,
    tags        TEXT[] DEFAULT '{}',
    saved_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, document_id)
);

-- ─── PIPELINE ANALYTICS ────────────────────────────────────────────────────

CREATE TABLE pipeline_events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id    UUID REFERENCES queries(id) ON DELETE SET NULL,
    agent_name  VARCHAR(100) NOT NULL,
    event_type  VARCHAR(100) NOT NULL,
    duration_ms INTEGER,
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pipeline_events_query ON pipeline_events(query_id);
CREATE INDEX idx_pipeline_events_agent ON pipeline_events(agent_name);
CREATE INDEX idx_pipeline_events_created ON pipeline_events(created_at);

-- ─── RATE LIMITING ─────────────────────────────────────────────────────────

CREATE TABLE rate_limit_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    endpoint    VARCHAR(255) NOT NULL,
    window_start TIMESTAMPTZ NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 1,
    UNIQUE (user_id, endpoint, window_start)
);
```

## 5.2 MongoDB Schema (Raw Documents Store)

```javascript
// Collection: raw_documents
{
  _id: ObjectId,
  doc_uuid: "uuid string",  // links to PostgreSQL documents.id
  source: "pubmed|clinicaltrials|drugbank|patent",
  external_id: "PMID|NCT|DB|patent_number",
  raw_content: {
    // Original API response - source-specific structure preserved
    pubmed_record: {},
    clinicaltrials_record: {},
    drugbank_record: {},
    patent_record: {}
  },
  processed: {
    title: "string",
    abstract: "string",
    full_text: "string",
    sections: [
      {
        heading: "Introduction|Methods|Results|Discussion|Conclusion",
        text: "string"
      }
    ],
    claims: [
      {
        text: "string",
        sentence_index: 0,
        entities: ["string"],
        is_result: true
      }
    ],
    entities_extracted: [
      {
        text: "string",
        type: "Drug|Disease|Gene|Outcome",
        start: 0,
        end: 0,
        confidence: 0.0
      }
    ]
  },
  embedding_metadata: {
    model: "pubmedbert-base-embeddings",
    dimension: 768,
    embedded_at: ISODate,
    faiss_ids: [0]  // chunk FAISS index IDs
  },
  created_at: ISODate,
  updated_at: ISODate
}

// Collection: pipeline_cache
{
  _id: ObjectId,
  cache_key: "sha256_of_query_params",
  query_hash: "string",
  result_type: "retrieval|ranking|contradiction|summary",
  result_data: {},
  expires_at: ISODate,
  created_at: ISODate
}

// Collection: agent_logs
{
  _id: ObjectId,
  query_id: "uuid",
  session_id: "uuid",
  agent: "qua|retrieval|ranking|contradiction|summarisation|response",
  input_snapshot: {},
  output_snapshot: {},
  duration_ms: 0,
  model_calls: [
    {
      model: "string",
      prompt_tokens: 0,
      completion_tokens: 0,
      latency_ms: 0
    }
  ],
  errors: [],
  created_at: ISODate
}
```

---

# 6. DATA PIPELINE DESIGN

## 6.1 Apache Airflow DAGs

### DAG 1: pubmed_daily_ingest
```python
# pipeline/dags/pubmed_ingest.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'pharmalyx-data',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['data-alerts@pharmalyx.com'],
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
    'pubmed_daily_ingest',
    default_args=default_args,
    description='Daily PubMed incremental ingestion',
    schedule_interval='0 2 * * *',  # 2AM UTC daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['pubmed', 'ingestion']
) as dag:

    fetch_new_pmids = PythonOperator(
        task_id='fetch_new_pmids',
        python_callable=fetch_pubmed_new_publications,
        op_kwargs={'days_back': 2}
    )

    download_abstracts = PythonOperator(
        task_id='download_abstracts',
        python_callable=batch_download_pubmed_abstracts
    )

    normalise_documents = PythonOperator(
        task_id='normalise_documents',
        python_callable=normalise_to_unified_schema
    )

    deduplicate = PythonOperator(
        task_id='deduplicate',
        python_callable=semantic_deduplication
    )

    generate_embeddings = PythonOperator(
        task_id='generate_embeddings',
        python_callable=batch_generate_embeddings,
        op_kwargs={'model': 'pubmedbert-base-embeddings', 'batch_size': 64}
    )

    update_faiss_index = PythonOperator(
        task_id='update_faiss_index',
        python_callable=incremental_faiss_update
    )

    update_postgres_metadata = PythonOperator(
        task_id='update_postgres_metadata',
        python_callable=upsert_document_metadata
    )

    enrich_openalex = PythonOperator(
        task_id='enrich_openalex',
        python_callable=fetch_openalex_metrics,
        op_kwargs={'batch_size': 100}
    )

    (fetch_new_pmids >> download_abstracts >> normalise_documents >>
     deduplicate >> generate_embeddings >>
     [update_faiss_index, update_postgres_metadata] >>
     enrich_openalex)
```

### DAG 2: clinicaltrials_weekly_sync
```python
with DAG(
    'clinicaltrials_weekly_sync',
    schedule_interval='0 3 * * 1',  # Monday 3AM UTC
    ...
) as dag:
    # Similar structure: fetch → normalise → embed → index
    pass
```

### DAG 3: document_enrichment
```python
# Continuously enriches documents with OpenAlex citation counts and journal IFs
with DAG(
    'document_enrichment',
    schedule_interval='0 4 * * *',
    ...
) as dag:
    # Fetch citation counts for documents > 30 days old with no citation data
    # Fetch journal impact factors via CrossRef or OpenAlex
    pass
```

## 6.2 Document Processing Pipeline

```python
# pipeline/processors/document_processor.py
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class DocumentProcessor:
    CHUNK_SIZE = 512  # tokens
    CHUNK_OVERLAP = 64  # tokens

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
        )
        self.model = AutoModel.from_pretrained(
            "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
        )
        self.model.eval()

    def process(self, document: dict) -> dict:
        text = self._get_primary_text(document)
        chunks = self.chunk_text(text)
        embeddings = self.embed_chunks(chunks)
        document["chunks"] = chunks
        document["chunk_embeddings"] = embeddings
        document["doc_embedding"] = embeddings[0] if embeddings else None
        return document

    def chunk_text(self, text: str) -> list[dict]:
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        for i in range(0, len(tokens), self.CHUNK_SIZE - self.CHUNK_OVERLAP):
            chunk_tokens = tokens[i:i + self.CHUNK_SIZE]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append({
                "chunk_index": len(chunks),
                "text": chunk_text,
                "token_count": len(chunk_tokens),
                "start_token": i
            })
        return chunks

    @torch.no_grad()
    def embed_chunks(self, chunks: list[dict]) -> list[np.ndarray]:
        embeddings = []
        batch_size = 32
        texts = [c["text"] for c in chunks]

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            inputs = self.tokenizer(
                batch,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            )
            outputs = self.model(**inputs)
            # Use CLS token embedding
            batch_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
            # L2 normalise
            batch_embeddings = batch_embeddings / np.linalg.norm(
                batch_embeddings, axis=1, keepdims=True
            )
            embeddings.extend(batch_embeddings)

        return embeddings

    def semantic_deduplicate(self, new_docs: list[dict],
                              similarity_threshold: float = 0.97) -> list[dict]:
        """Remove near-duplicate documents using embedding cosine similarity"""
        unique_docs = []
        seen_embeddings = []

        for doc in new_docs:
            emb = doc.get("doc_embedding")
            if emb is None:
                unique_docs.append(doc)
                continue

            is_duplicate = False
            for seen_emb in seen_embeddings:
                sim = np.dot(emb, seen_emb)
                if sim >= similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_docs.append(doc)
                seen_embeddings.append(emb)

        return unique_docs

    def _get_primary_text(self, document: dict) -> str:
        parts = []
        if document.get("title"):
            parts.append(document["title"])
        if document.get("abstract"):
            parts.append(document["abstract"])
        if document.get("full_text"):
            parts.append(document["full_text"][:4000])  # limit full text
        return " ".join(parts)
```

---

# 7. AI/ML COMPONENTS

## 7.1 Model Registry

| Model | Task | Source | Size | Deployment |
|---|---|---|---|---|
| `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext` | Embeddings, NER | HuggingFace | 440MB | GPU pod |
| `allenai/scibert_scivocab_uncased` | NER (backup) | HuggingFace | 440MB | GPU pod |
| `pruas/BENT-PubMedBERT-NER-Gene` | Gene/chemical NER | HuggingFace | 440MB | GPU pod |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | Re-ranking | HuggingFace | 90MB | GPU pod |
| `razent/SciFive-large-Pubmed_PMC` | Summarisation | HuggingFace | 3GB | GPU pod |
| `custom/intent_classifier` | Intent (6-class) | Local fine-tune | 440MB | GPU pod |
| `custom/study_type_classifier` | Study type (10-class) | Local fine-tune | 440MB | GPU pod |
| `custom/nli_biomed` | Contradiction NLI | Fine-tuned on MedNLI | 440MB | GPU pod |
| Gemini 1.5 Flash | Structured output, explanation | Google API | API | Cloud |

## 7.2 ML Service

```python
# services/ml_service/embedding_service.py
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from functools import lru_cache

class EmbeddingService:
    MODEL_NAME = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModel.from_pretrained(self.MODEL_NAME)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def embed(self, texts: list[str]) -> np.ndarray:
        """Returns L2-normalised embeddings, shape (N, 768)"""
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True
        ).to(self.device)

        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()

        # L2 normalise
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / np.maximum(norms, 1e-12)

    def embed_single(self, text: str) -> np.ndarray:
        return self.embed([text])[0]
```

## 7.3 Gemini API Integration

```python
# services/gemini_service.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import json

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.1,  # Low temperature for factual, consistent outputs
                top_p=0.9,
                max_output_tokens=4096,
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_MEDICAL", "threshold": "BLOCK_NONE"},
            ]
        )
        self.json_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.0,
                response_mime_type="application/json",
                max_output_tokens=2048,
            )
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
    async def generate(self, prompt: str, json_mode: bool = False) -> str:
        model = self.json_model if json_mode else self.model
        response = await model.generate_content_async(prompt)
        return response.text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
    async def generate_json(self, prompt: str) -> dict:
        response = await self.json_model.generate_content_async(prompt)
        text = response.text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)

    async def stream(self, prompt: str):
        """Async generator for streaming token-by-token responses"""
        async for chunk in await self.model.generate_content_async(
            prompt, stream=True
        ):
            if chunk.text:
                yield chunk.text
```

---

# 8. FRONTEND ARCHITECTURE

## 8.1 Technology Stack

```
React 18 + TypeScript
TailwindCSS (styling)
Zustand (state management)
TanStack Query (server state, caching)
React Router v6 (routing)
Framer Motion (animations)
D3.js (contradiction graph, EQS visualisation)
Axios (HTTP client)
EventSource API (SSE streaming)
Recharts (analytics charts)
React PDF Renderer (PDF export)
```

## 8.2 Page Structure

```
/                       → Landing page (public)
/auth/login             → Login
/auth/register          → Register
/auth/reset-password    → Password reset
/dashboard              → Main research dashboard (protected)
/query/{queryId}        → Query result detail view
/sessions               → Research session history
/sessions/{sessionId}   → Session detail with full conversation
/library                → Saved documents library
/export/{queryId}       → Export centre
/settings               → User preferences
/settings/team          → Team management (team_lead role)
/admin                  → Admin panel (admin role only)
```

## 8.3 Key Components

```typescript
// components/query/QueryInterface.tsx
// Main query input with streaming response

// components/query/AgentProgressBar.tsx
// Real-time agent pipeline progress (SSE updates)

// components/evidence/EvidenceCard.tsx
// Individual evidence card with EQS score, study type badge,
// source badge, abstract excerpt, contradiction warning badge

// components/evidence/EvidenceGrid.tsx
// Ranked grid of evidence cards

// components/contradiction/ContradictionAlert.tsx
// Prominent alert card showing two conflicting claims side-by-side
// with ContraScore gauge and explanation

// components/contradiction/ContradictionGraph.tsx
// D3.js force-directed graph showing document nodes connected
// by contradiction edges (edge weight = ContraScore)

// components/charts/EQSBreakdown.tsx
// Horizontal bar chart showing the 5 EQS component contributions
// for a selected document

// components/summary/EvidenceSummary.tsx
// Structured summary with expandable sections

// components/export/ExportPanel.tsx
// Export to PDF, BibTeX, CSV, JSON with preview

// components/session/SessionSidebar.tsx
// Left sidebar showing conversation history within a session
```

## 8.4 State Management (Zustand)

```typescript
// store/queryStore.ts
interface QueryState {
  currentQuery: string;
  sessionId: string | null;
  streamingStatus: 'idle' | 'streaming' | 'complete' | 'error';
  agentProgress: {
    qua: 'pending' | 'running' | 'complete';
    retrieval: 'pending' | 'running' | 'complete';
    ranking: 'pending' | 'running' | 'complete';
    contradiction: 'pending' | 'running' | 'complete';
    summarisation: 'pending' | 'running' | 'complete';
    response: 'pending' | 'running' | 'complete';
  };
  retrievalStats: {
    pubmed: number;
    clinicaltrials: number;
    drugbank: number;
    patents: number;
    total: number;
  };
  streamingResponse: string;
  finalResult: QueryResult | null;
  contradictionAlerts: ContradictionAlert[];
  evidenceCards: EvidenceCard[];
  followUpSuggestions: string[];
}
```

---

# 9. INFRASTRUCTURE & DEVOPS

## 9.1 Service Map

```yaml
Services:
  api-gateway:      FastAPI, port 8000, 2-4 replicas
  orchestrator:     FastAPI, port 8001, 2 replicas
  ml-service:       FastAPI, port 8002, 1-2 GPU replicas
  qua-agent:        FastAPI, port 8010, 2 replicas
  retrieval-agent:  FastAPI, port 8011, 2-4 replicas (network heavy)
  ranking-agent:    FastAPI, port 8012, 2 replicas
  contra-agent:     FastAPI, port 8013, 1-2 GPU replicas
  summ-agent:       FastAPI, port 8014, 1-2 GPU replicas
  response-agent:   FastAPI, port 8015, 2 replicas
  data-pipeline:    Airflow, port 8080, 1 scheduler + 4 workers
  vector-service:   FastAPI, port 8020, 1 replica (FAISS)
  frontend:         Nginx, port 3000

Databases:
  postgres:         PostgreSQL 16, port 5432
  mongodb:          MongoDB 7, port 27017
  redis:            Redis 7, port 6379
  faiss-storage:    NFS/EBS volume for FAISS index files

Monitoring:
  prometheus:       port 9090
  grafana:          port 3001
  jaeger:           port 16686 (distributed tracing)
  flower:           port 5555 (Celery monitoring)
```

---

# 10. FOLDER STRUCTURE

```
pharmalyx/
│
├── README.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── docker-compose.dev.yml
├── Makefile
├── .env.example
├── .env.local
├── .gitignore
│
├── ── BACKEND ──────────────────────────────────────────────────────────────
│
├── api-gateway/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                    ← FastAPI app entrypoint
│   ├── config.py                  ← Settings (pydantic-settings)
│   ├── dependencies.py            ← FastAPI dependency injection
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py                ← JWT validation middleware
│   │   ├── rate_limiter.py        ← Redis-based rate limiting
│   │   ├── cors.py                ← CORS configuration
│   │   ├── logging.py             ← Request logging
│   │   └── tracing.py             ← OpenTelemetry tracing
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                ← /auth/* endpoints
│   │   ├── query.py               ← /query endpoints (main SSE endpoint)
│   │   ├── sessions.py            ← /sessions endpoints
│   │   ├── documents.py           ← /documents endpoints
│   │   ├── export.py              ← /export endpoints
│   │   ├── health.py              ← /health endpoints
│   │   └── admin.py               ← /admin endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                ← User Pydantic models
│   │   ├── query.py               ← Query request/response models
│   │   ├── session.py             ← Session models
│   │   ├── document.py            ← Document models
│   │   └── auth.py                ← Auth models (JWT, tokens)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py        ← JWT creation, validation, refresh
│   │   ├── user_service.py        ← User CRUD
│   │   ├── session_service.py     ← Session management
│   │   └── orchestrator_client.py ← HTTP client for orchestrator service
│   └── db/
│       ├── __init__.py
│       ├── postgres.py            ← SQLAlchemy async engine setup
│       ├── redis.py               ← Redis connection pool
│       └── migrations/
│           ├── env.py             ← Alembic config
│           └── versions/          ← Migration files
│
├── orchestrator/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── orchestrator.py            ← Main pipeline orchestration logic
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── pipeline.py            ← Agent invocation and sequencing
│   │   ├── context.py             ← PipelineContext dataclass
│   │   ├── sse_manager.py         ← Server-Sent Events streaming manager
│   │   └── cache.py               ← Pipeline result caching (Redis)
│   ├── agents/
│   │   ├── __init__.py
│   │   └── base_agent.py          ← Abstract base agent class
│   └── services/
│       ├── __init__.py
│       └── agent_clients.py       ← HTTP clients for each agent service
│
├── agents/
│   ├── shared/
│   │   ├── __init__.py
│   │   ├── base.py                ← BaseAgent abstract class
│   │   ├── schemas.py             ← Shared Pydantic models across agents
│   │   └── utils.py               ← Shared utilities
│   │
│   ├── qua/                       ← Query Understanding Agent
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   ├── agent.py               ← QUA main logic
│   │   ├── prompts.py             ← QUA system prompts
│   │   ├── models/
│   │   │   ├── intent_classifier.py
│   │   │   └── ner_pipeline.py
│   │   └── services/
│   │       └── mesh_service.py    ← MeSH synonym lookup
│   │
│   ├── retrieval/                 ← Retrieval Agent
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   ├── agent.py               ← RA orchestration
│   │   ├── prompts.py
│   │   ├── connectors/
│   │   │   ├── __init__.py
│   │   │   ├── pubmed.py          ← PubMed Entrez API connector
│   │   │   ├── clinicaltrials.py  ← ClinicalTrials.gov API connector
│   │   │   ├── drugbank.py        ← DrugBank API connector
│   │   │   └── patents.py         ← USPTO API connector
│   │   └── services/
│   │       ├── faiss_client.py    ← FAISS service HTTP client
│   │       └── deduplication.py   ← Semantic dedup logic
│   │
│   ├── ranking/                   ← Evidence Ranking Agent
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   ├── agent.py               ← ERA main logic
│   │   ├── prompts.py
│   │   ├── eqs/
│   │   │   ├── __init__.py
│   │   │   ├── scorer.py          ← EQS computation
│   │   │   └── weights.py         ← Weight management + learning
│   │   └── services/
│   │       ├── openalex_service.py ← Citation count + IF fetching
│   │       └── study_classifier.py ← Study type classification
│   │
│   ├── contradiction/             ← Contradiction Detection Agent
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   ├── agent.py               ← CDA main logic
│   │   ├── prompts.py
│   │   ├── nli/
│   │   │   ├── __init__.py
│   │   │   ├── model.py           ← NLI model wrapper
│   │   │   └── contra_score.py    ← ContraScore computation
│   │   └── services/
│   │       └── claim_extractor.py ← Sentence-level claim extraction
│   │
│   ├── summarisation/             ← Summarisation Agent
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   ├── agent.py               ← SA main logic
│   │   ├── prompts.py
│   │   └── services/
│   │       ├── scifive_service.py ← SciFive summarisation model
│   │       └── citation_injector.py ← Inline citation injection
│   │
│   └── response/                  ← Response Generation Agent
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── main.py
│       ├── agent.py               ← RGA main logic
│       ├── prompts.py
│       └── services/
│           ├── formatter.py       ← Response formatting by intent
│           ├── followup_generator.py ← Follow-up question generation
│           └── export_builder.py  ← PDF/BibTeX/CSV builder
│
├── services/
│   │
│   ├── ml-service/                ← Centralised ML model serving
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   ├── config.py
│   │   └── routers/
│   │       ├── embed.py           ← POST /embed (batch embedding)
│   │       ├── classify.py        ← POST /classify (intent, study type)
│   │       └── nli.py             ← POST /nli (pairwise NLI inference)
│   │
│   └── vector-service/            ← FAISS index management
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── main.py
│       ├── config.py
│       ├── faiss_service.py       ← FAISS index: search, add, rebuild
│       └── routers/
│           ├── search.py          ← POST /search
│           ├── index.py           ← POST /index/add, POST /index/rebuild
│           └── health.py
│
├── pipeline/                      ← Apache Airflow data pipeline
│   ├── Dockerfile.airflow
│   ├── requirements.txt
│   ├── airflow.cfg
│   ├── dags/
│   │   ├── __init__.py
│   │   ├── pubmed_ingest.py       ← Daily PubMed ingestion DAG
│   │   ├── clinicaltrials_sync.py ← Weekly ClinicalTrials DAG
│   │   ├── drugbank_sync.py       ← Monthly DrugBank DAG
│   │   ├── patent_sync.py         ← Weekly USPTO patent DAG
│   │   └── document_enrichment.py ← Daily OpenAlex enrichment DAG
│   ├── operators/
│   │   ├── __init__.py
│   │   ├── pubmed_operator.py
│   │   ├── embedding_operator.py
│   │   └── faiss_operator.py
│   └── processors/
│       ├── __init__.py
│       ├── document_processor.py  ← Chunking + embedding generation
│       ├── normaliser.py          ← Unified schema normalisation
│       └── deduplicator.py        ← Semantic deduplication
│
├── shared/                        ← Shared libraries across all services
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            ← Global settings (pydantic-settings)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── postgres.py            ← Async SQLAlchemy setup
│   │   ├── mongodb.py             ← Motor (async MongoDB) setup
│   │   └── redis.py               ← Redis connection setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py            ← Document, RankedDocument, Chunk
│   │   ├── query.py               ← StructuredQuery, QueryResult
│   │   ├── contradiction.py       ← ContradictionReport, ContradictionPair
│   │   ├── evidence.py            ← EvidenceSummary, EvidenceCard
│   │   └── session.py             ← Session, ConversationTurn
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py      ← Shared Gemini API service
│   └── utils/
│       ├── __init__.py
│       ├── text_utils.py          ← Text cleaning, sentence splitting
│       ├── citation_utils.py      ← Citation formatting (APA, IEEE, BibTeX)
│       └── logging_utils.py       ← Structured JSON logging
│
├── ── FRONTEND ─────────────────────────────────────────────────────────────
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── vite.config.ts
│   ├── index.html
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── public/
│   │   └── logo.svg
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── router.tsx             ← React Router configuration
│       │
│       ├── api/
│       │   ├── client.ts          ← Axios instance with interceptors
│       │   ├── auth.ts            ← Auth API calls
│       │   ├── query.ts           ← Query API calls + SSE stream handler
│       │   ├── sessions.ts        ← Session API calls
│       │   ├── documents.ts       ← Document API calls
│       │   └── export.ts          ← Export API calls
│       │
│       ├── store/
│       │   ├── authStore.ts       ← Auth state (Zustand)
│       │   ├── queryStore.ts      ← Query/streaming state (Zustand)
│       │   ├── sessionStore.ts    ← Session state (Zustand)
│       │   └── uiStore.ts         ← UI state, sidebar, modals
│       │
│       ├── hooks/
│       │   ├── useQuery.ts        ← Custom hook for query + SSE streaming
│       │   ├── useSession.ts      ← Session management hook
│       │   ├── useExport.ts       ← Export functionality hook
│       │   └── useAuth.ts         ← Auth hook
│       │
│       ├── pages/
│       │   ├── Landing.tsx
│       │   ├── auth/
│       │   │   ├── Login.tsx
│       │   │   ├── Register.tsx
│       │   │   └── ResetPassword.tsx
│       │   ├── dashboard/
│       │   │   ├── Dashboard.tsx   ← Main research interface
│       │   │   └── QueryResult.tsx ← Full result detail page
│       │   ├── sessions/
│       │   │   ├── Sessions.tsx
│       │   │   └── SessionDetail.tsx
│       │   ├── Library.tsx
│       │   ├── Export.tsx
│       │   ├── settings/
│       │   │   ├── Settings.tsx
│       │   │   └── Team.tsx
│       │   └── admin/
│       │       └── Admin.tsx
│       │
│       ├── components/
│       │   ├── layout/
│       │   │   ├── AppLayout.tsx
│       │   │   ├── Sidebar.tsx
│       │   │   ├── TopBar.tsx
│       │   │   └── MobileNav.tsx
│       │   │
│       │   ├── query/
│       │   │   ├── QueryInterface.tsx     ← Main query input component
│       │   │   ├── QueryInput.tsx         ← Text input with suggestions
│       │   │   ├── AgentProgressBar.tsx   ← Pipeline progress visualiser
│       │   │   ├── StreamingResponse.tsx  ← Real-time token streaming display
│       │   │   └── FollowUpSuggestions.tsx
│       │   │
│       │   ├── evidence/
│       │   │   ├── EvidenceCard.tsx       ← Individual evidence card
│       │   │   ├── EvidenceGrid.tsx       ← Grid of ranked evidence cards
│       │   │   ├── EvidenceBadge.tsx      ← Study type badge component
│       │   │   ├── SourceBadge.tsx        ← PubMed/CT/DrugBank badge
│       │   │   └── EQSBreakdown.tsx       ← EQS component bar chart
│       │   │
│       │   ├── contradiction/
│       │   │   ├── ContradictionBanner.tsx  ← Top-level warning banner
│       │   │   ├── ContradictionAlert.tsx   ← Individual conflict card
│       │   │   ├── ContradictionGraph.tsx   ← D3 force graph
│       │   │   └── ContraScoreGauge.tsx     ← Score gauge component
│       │   │
│       │   ├── summary/
│       │   │   ├── EvidenceSummary.tsx    ← Full structured summary
│       │   │   ├── KeyFindings.tsx        ← Key findings list
│       │   │   └── EvidenceStrength.tsx   ← Strength indicator
│       │   │
│       │   ├── session/
│       │   │   ├── SessionSidebar.tsx     ← Conversation history sidebar
│       │   │   ├── ConversationTurn.tsx   ← Single Q&A turn
│       │   │   └── SessionCard.tsx        ← Session list card
│       │   │
│       │   ├── export/
│       │   │   ├── ExportPanel.tsx        ← Export options panel
│       │   │   └── ExportButton.tsx       ← Individual export trigger
│       │   │
│       │   └── ui/                        ← Reusable UI primitives
│       │       ├── Button.tsx
│       │       ├── Input.tsx
│       │       ├── Card.tsx
│       │       ├── Modal.tsx
│       │       ├── Badge.tsx
│       │       ├── Tooltip.tsx
│       │       ├── Spinner.tsx
│       │       ├── Alert.tsx
│       │       └── Tabs.tsx
│       │
│       └── types/
│           ├── query.ts
│           ├── document.ts
│           ├── contradiction.ts
│           ├── session.ts
│           └── auth.ts
│
├── ── INFRASTRUCTURE ───────────────────────────────────────────────────────
│
├── infra/
│   ├── nginx/
│   │   ├── nginx.conf             ← Main Nginx config
│   │   └── upstream.conf          ← Upstream service configs
│   ├── prometheus/
│   │   └── prometheus.yml         ← Scrape configs
│   ├── grafana/
│   │   └── dashboards/
│   │       ├── pharmalyx_overview.json
│   │       └── agent_performance.json
│   └── airflow/
│       └── airflow.cfg
│
├── ── TESTING ──────────────────────────────────────────────────────────────
│
├── tests/
│   ├── unit/
│   │   ├── test_qua_agent.py
│   │   ├── test_retrieval_agent.py
│   │   ├── test_eqs_scorer.py
│   │   ├── test_contra_score.py
│   │   ├── test_claim_extractor.py
│   │   └── test_document_processor.py
│   ├── integration/
│   │   ├── test_pipeline_end_to_end.py
│   │   ├── test_pubmed_connector.py
│   │   ├── test_faiss_service.py
│   │   └── test_api_endpoints.py
│   ├── benchmarks/
│   │   ├── test_retrieval_precision.py  ← Precision@k, Recall, MRR, nDCG
│   │   ├── test_nli_accuracy.py         ← MedNLI accuracy, F1
│   │   └── test_latency.py              ← End-to-end latency benchmarks
│   └── fixtures/
│       ├── sample_queries.json
│       ├── sample_documents.json
│       └── sample_contradictions.json
│
└── ── SCRIPTS & TOOLING ────────────────────────────────────────────────────
    ├── scripts/
    │   ├── init_db.py             ← Create PostgreSQL tables (Alembic)
    │   ├── seed_data.py           ← Seed development data
    │   ├── build_faiss_index.py   ← Build initial FAISS index from scratch
    │   ├── fine_tune_intent.py    ← Fine-tune intent classifier
    │   ├── fine_tune_nli.py       ← Fine-tune NLI model on MedNLI
    │   ├── fine_tune_study_type.py ← Fine-tune study type classifier
    │   └── benchmark.py           ← Run evaluation benchmarks
    └── Makefile                   ← Common dev commands
```

---

# 11. ENVIRONMENT CONFIGURATION

```bash
# .env.example — Copy to .env.local for development

# ─── APPLICATION ───────────────────────────────────────────────
APP_ENV=development               # development | staging | production
APP_NAME=pharmalyx
APP_VERSION=1.0.0
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
DEBUG=true
LOG_LEVEL=INFO

# ─── API GATEWAY ───────────────────────────────────────────────
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
ALLOWED_ORIGINS=http://localhost:3000,https://app.pharmalyx.com
JWT_SECRET=your-jwt-secret-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# ─── DATABASE — POSTGRESQL ─────────────────────────────────────
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pharmalyx
POSTGRES_USER=pharmalyx_user
POSTGRES_PASSWORD=your-postgres-password
DATABASE_URL=postgresql+asyncpg://pharmalyx_user:password@localhost:5432/pharmalyx
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# ─── DATABASE — MONGODB ────────────────────────────────────────
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=pharmalyx_docs
MONGODB_USER=pharmalyx_user
MONGODB_PASSWORD=your-mongodb-password
MONGODB_URL=mongodb://pharmalyx_user:password@localhost:27017/pharmalyx_docs

# ─── DATABASE — REDIS ──────────────────────────────────────────
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_URL=redis://:password@localhost:6379/0
REDIS_CACHE_TTL_SECONDS=3600
REDIS_SESSION_TTL_SECONDS=86400

# ─── FAISS ─────────────────────────────────────────────────────
FAISS_INDEX_PATH=/data/faiss/pharmalyx.index
FAISS_DIMENSION=768
FAISS_NPROBE=32
FAISS_TOP_K=50

# ─── EXTERNAL APIs ─────────────────────────────────────────────
PUBMED_API_KEY=your-ncbi-api-key
PUBMED_BASE_URL=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
PUBMED_RATE_LIMIT=10            # requests per second with API key

CLINICALTRIALS_BASE_URL=https://clinicaltrials.gov/api/v2
CLINICALTRIALS_RATE_LIMIT=5

DRUGBANK_API_KEY=your-drugbank-api-key
DRUGBANK_BASE_URL=https://api.drugbank.com/v1

USPTO_API_KEY=your-uspto-api-key
USPTO_BASE_URL=https://api.patentsview.org/patents

OPENALEX_EMAIL=your-email@domain.com  # For polite pool (higher rate limit)
OPENALEX_BASE_URL=https://api.openalex.org

# ─── GOOGLE GEMINI ─────────────────────────────────────────────
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_OUTPUT_TOKENS=4096
GEMINI_TEMPERATURE=0.1

# ─── ML MODELS ─────────────────────────────────────────────────
ML_SERVICE_URL=http://localhost:8002
EMBEDDING_MODEL=microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext
NLI_MODEL_PATH=models/nli_biomed
INTENT_MODEL_PATH=models/intent_classifier
STUDY_TYPE_MODEL_PATH=models/study_type_classifier
SUMMARISATION_MODEL=razent/SciFive-large-Pubmed_PMC
USE_GPU=true
TORCH_DEVICE=cuda                # cpu | cuda | mps

# ─── AGENT SERVICES ────────────────────────────────────────────
ORCHESTRATOR_URL=http://localhost:8001
QUA_AGENT_URL=http://localhost:8010
RETRIEVAL_AGENT_URL=http://localhost:8011
RANKING_AGENT_URL=http://localhost:8012
CONTRADICTION_AGENT_URL=http://localhost:8013
SUMMARISATION_AGENT_URL=http://localhost:8014
RESPONSE_AGENT_URL=http://localhost:8015
VECTOR_SERVICE_URL=http://localhost:8020

# ─── PIPELINE (AIRFLOW) ────────────────────────────────────────
AIRFLOW_HOME=/opt/airflow
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:password@localhost:5432/airflow
AIRFLOW__CELERY__BROKER_URL=redis://:password@localhost:6379/1
AIRFLOW__CELERY__RESULT_BACKEND=redis://:password@localhost:6379/2
AIRFLOW__CORE__FERNET_KEY=your-fernet-key

# ─── EMAIL ─────────────────────────────────────────────────────
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
FROM_EMAIL=noreply@pharmalyx.com

# ─── RATE LIMITING ─────────────────────────────────────────────
RATE_LIMIT_FREE_QUERIES_PER_DAY=10
RATE_LIMIT_PRO_QUERIES_PER_DAY=200
RATE_LIMIT_ENTERPRISE_QUERIES_PER_DAY=2000
RATE_LIMIT_REQUESTS_PER_MINUTE=30

# ─── MONITORING ────────────────────────────────────────────────
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
JAEGER_HOST=localhost
JAEGER_PORT=6831
SENTRY_DSN=your-sentry-dsn        # Production error tracking
```

---

# 12. BACKEND REQUIREMENTS

## requirements.txt (Shared Base)
```
# ─── WEB FRAMEWORK ─────────────────────────────────────────────
fastapi==0.115.0
uvicorn[standard]==0.32.0
python-multipart==0.0.12
sse-starlette==2.1.3              # Server-Sent Events for streaming
httpx==0.28.0                      # Async HTTP client
tenacity==9.0.0                    # Retry logic with backoff

# ─── CONFIGURATION ─────────────────────────────────────────────
pydantic==2.10.0
pydantic-settings==2.6.0
python-dotenv==1.0.1

# ─── DATABASE ──────────────────────────────────────────────────
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0                    # Async PostgreSQL driver
alembic==1.14.0                    # PostgreSQL migrations
motor==3.6.0                       # Async MongoDB driver
pymongo==4.10.0
redis[hiredis]==5.2.0              # Async Redis client

# ─── AUTHENTICATION ────────────────────────────────────────────
python-jose[cryptography]==3.3.0   # JWT
passlib[bcrypt]==1.7.4             # Password hashing
python-multipart==0.0.12

# ─── AI / ML ───────────────────────────────────────────────────
torch==2.5.1                       # PyTorch
transformers==4.46.0               # HuggingFace Transformers
sentence-transformers==3.3.1       # Sentence embeddings
accelerate==1.1.1                  # Model training/inference acceleration
tokenizers==0.20.3                 # Fast tokenisation
datasets==3.1.0                    # HuggingFace datasets (for fine-tuning)
evaluate==0.4.3                    # Model evaluation metrics

# ─── VECTOR SEARCH ─────────────────────────────────────────────
faiss-gpu==1.9.0                   # Use faiss-cpu if no GPU
numpy==2.1.3

# ─── DATA PROCESSING ───────────────────────────────────────────
pandas==2.2.3
scipy==1.14.1
scikit-learn==1.5.2
spacy==3.8.2
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# ─── NLP UTILITIES ─────────────────────────────────────────────
nltk==3.9.1
biopython==1.84                    # For PubMed XML parsing (Entrez)

# ─── EXTERNAL API CLIENTS ──────────────────────────────────────
# (Using httpx for all HTTP — no specific client SDKs needed)

# ─── GOOGLE GEMINI ─────────────────────────────────────────────
google-generativeai==0.8.3

# ─── CACHING ───────────────────────────────────────────────────
aiocache==0.12.3
msgpack==1.1.0

# ─── MONITORING & OBSERVABILITY ────────────────────────────────
prometheus-client==0.21.0
opentelemetry-api==1.28.0
opentelemetry-sdk==1.28.0
opentelemetry-instrumentation-fastapi==0.49b0
opentelemetry-exporter-jaeger==1.21.0
sentry-sdk[fastapi]==2.19.0
structlog==24.4.0

# ─── UTILITIES ─────────────────────────────────────────────────
python-ulid==3.0.0
uuid7==0.1.0
orjson==3.10.11                    # Fast JSON serialisation
aiofiles==24.1.0                   # Async file I/O
Pillow==11.0.0                     # Image processing (PDF export)
weasyprint==62.3                   # HTML to PDF conversion
bibtexparser==1.4.1                # BibTeX generation/parsing
python-docx==1.1.2                 # Optional: Word export

# ─── EMAIL ─────────────────────────────────────────────────────
aiosmtplib==3.0.2
jinja2==3.1.4                      # Email templates

# ─── TESTING ───────────────────────────────────────────────────
pytest==8.3.3
pytest-asyncio==0.24.0
pytest-cov==6.0.0
httpx==0.28.0                      # Async test client
factory-boy==3.3.1                 # Test fixtures
faker==33.1.0

# ─── DEVELOPMENT ───────────────────────────────────────────────
black==24.10.0
ruff==0.8.0
mypy==1.13.0
pre-commit==4.0.1
```

## requirements-pipeline.txt (Airflow data pipeline)
```
apache-airflow==2.10.3
apache-airflow-providers-postgres==5.12.0
apache-airflow-providers-mongo==4.3.0
apache-airflow-providers-redis==3.8.0
apache-airflow-providers-celery==3.8.2

# Reuse shared requirements above plus:
xmltodict==0.14.2
lxml==5.3.0
requests==2.32.3                   # Sync HTTP for Airflow operators
beautifulsoup4==4.12.3
```

---

# 13. FRONTEND REQUIREMENTS

## package.json
```json
{
  "name": "pharmalyx-frontend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.28.0",

    "zustand": "^5.0.2",
    "@tanstack/react-query": "^5.62.0",
    "@tanstack/react-query-devtools": "^5.62.0",

    "axios": "^1.7.9",

    "d3": "^7.9.0",
    "recharts": "^2.13.3",
    "framer-motion": "^11.11.17",

    "@headlessui/react": "^2.2.0",
    "@heroicons/react": "^2.2.0",
    "lucide-react": "^0.468.0",

    "tailwindcss": "^3.4.16",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",

    "@react-pdf/renderer": "^4.1.5",

    "clsx": "^2.1.1",
    "date-fns": "^4.1.0",
    "zod": "^3.23.8",
    "react-hook-form": "^7.54.1",
    "@hookform/resolvers": "^3.9.1",

    "react-hot-toast": "^2.4.1",
    "react-markdown": "^9.0.1",
    "remark-gfm": "^4.0.0",

    "highlight.js": "^11.10.0",
    "react-syntax-highlighter": "^15.6.1",

    "lodash-es": "^4.17.21"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@types/d3": "^7.4.3",
    "@types/lodash-es": "^4.17.12",
    "@types/react-syntax-highlighter": "^15.5.13",

    "@typescript-eslint/eslint-plugin": "^8.15.0",
    "@typescript-eslint/parser": "^8.15.0",
    "eslint": "^9.15.0",
    "eslint-plugin-react-hooks": "^5.0.0",
    "eslint-plugin-react-refresh": "^0.4.14",

    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.0.1",
    "typescript": "^5.7.2",

    "vitest": "^2.1.6",
    "@vitest/ui": "^2.1.6",
    "@vitest/coverage-v8": "^2.1.6",
    "@testing-library/react": "^16.0.1",
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/user-event": "^14.5.2",

    "prettier": "^3.3.3",
    "prettier-plugin-tailwindcss": "^0.6.9"
  }
}
```

---

# 14. DOCKER & COMPOSE SETUP

## docker-compose.yml (Development)
```yaml
version: '3.9'

services:

  # ─── DATABASES ────────────────────────────────────────────────
  postgres:
    image: postgres:16-alpine
    container_name: pharmalyx-postgres
    environment:
      POSTGRES_DB: pharmalyx
      POSTGRES_USER: pharmalyx_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pharmalyx_user -d pharmalyx"]
      interval: 10s
      timeout: 5s
      retries: 5

  mongodb:
    image: mongo:7-jammy
    container_name: pharmalyx-mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: pharmalyx_user
      MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_PASSWORD}
      MONGO_INITDB_DATABASE: pharmalyx_docs
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: pharmalyx-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--pass", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ─── API GATEWAY ──────────────────────────────────────────────
  api-gateway:
    build:
      context: ./api-gateway
      dockerfile: Dockerfile
    container_name: pharmalyx-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
      - ORCHESTRATOR_URL=http://orchestrator:8001
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./api-gateway:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # ─── ORCHESTRATOR ─────────────────────────────────────────────
  orchestrator:
    build:
      context: ./orchestrator
      dockerfile: Dockerfile
    container_name: pharmalyx-orchestrator
    ports:
      - "8001:8001"
    environment:
      - REDIS_URL=${REDIS_URL}
      - MONGODB_URL=${MONGODB_URL}
      - QUA_AGENT_URL=http://qua-agent:8010
      - RETRIEVAL_AGENT_URL=http://retrieval-agent:8011
      - RANKING_AGENT_URL=http://ranking-agent:8012
      - CONTRADICTION_AGENT_URL=http://contradiction-agent:8013
      - SUMMARISATION_AGENT_URL=http://summarisation-agent:8014
      - RESPONSE_AGENT_URL=http://response-agent:8015
    depends_on:
      - redis
    volumes:
      - ./orchestrator:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8001 --reload

  # ─── ML SERVICE ───────────────────────────────────────────────
  ml-service:
    build:
      context: ./services/ml-service
      dockerfile: Dockerfile
    container_name: pharmalyx-ml
    ports:
      - "8002:8002"
    environment:
      - EMBEDDING_MODEL=${EMBEDDING_MODEL}
      - NLI_MODEL_PATH=${NLI_MODEL_PATH}
      - USE_GPU=${USE_GPU}
    volumes:
      - ./services/ml-service:/app
      - model_cache:/root/.cache/huggingface
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    command: uvicorn main:app --host 0.0.0.0 --port 8002 --workers 1

  # ─── VECTOR SERVICE ───────────────────────────────────────────
  vector-service:
    build:
      context: ./services/vector-service
      dockerfile: Dockerfile
    container_name: pharmalyx-vector
    ports:
      - "8020:8020"
    environment:
      - FAISS_INDEX_PATH=/data/faiss/pharmalyx.index
      - FAISS_DIMENSION=768
    volumes:
      - faiss_data:/data/faiss
      - ./services/vector-service:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8020 --reload

  # ─── AGENTS ───────────────────────────────────────────────────
  qua-agent:
    build:
      context: ./agents/qua
      dockerfile: Dockerfile
    container_name: pharmalyx-qua
    ports:
      - "8010:8010"
    environment:
      - ML_SERVICE_URL=http://ml-service:8002
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - ml-service
    volumes:
      - ./agents/qua:/app
      - ./agents/shared:/app/shared
    command: uvicorn main:app --host 0.0.0.0 --port 8010 --reload

  retrieval-agent:
    build:
      context: ./agents/retrieval
      dockerfile: Dockerfile
    container_name: pharmalyx-retrieval
    ports:
      - "8011:8011"
    environment:
      - ML_SERVICE_URL=http://ml-service:8002
      - VECTOR_SERVICE_URL=http://vector-service:8020
      - PUBMED_API_KEY=${PUBMED_API_KEY}
      - CLINICALTRIALS_BASE_URL=${CLINICALTRIALS_BASE_URL}
      - DRUGBANK_API_KEY=${DRUGBANK_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MONGODB_URL=${MONGODB_URL}
    depends_on:
      - ml-service
      - vector-service
      - mongodb
    volumes:
      - ./agents/retrieval:/app
      - ./agents/shared:/app/shared
    command: uvicorn main:app --host 0.0.0.0 --port 8011 --reload

  ranking-agent:
    build:
      context: ./agents/ranking
      dockerfile: Dockerfile
    container_name: pharmalyx-ranking
    ports:
      - "8012:8012"
    environment:
      - ML_SERVICE_URL=http://ml-service:8002
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENALEX_EMAIL=${OPENALEX_EMAIL}
    depends_on:
      - ml-service
    volumes:
      - ./agents/ranking:/app
      - ./agents/shared:/app/shared
    command: uvicorn main:app --host 0.0.0.0 --port 8012 --reload

  contradiction-agent:
    build:
      context: ./agents/contradiction
      dockerfile: Dockerfile
    container_name: pharmalyx-contradiction
    ports:
      - "8013:8013"
    environment:
      - ML_SERVICE_URL=http://ml-service:8002
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - ml-service
    volumes:
      - ./agents/contradiction:/app
      - ./agents/shared:/app/shared
    command: uvicorn main:app --host 0.0.0.0 --port 8013 --reload

  summarisation-agent:
    build:
      context: ./agents/summarisation
      dockerfile: Dockerfile
    container_name: pharmalyx-summ
    ports:
      - "8014:8014"
    environment:
      - ML_SERVICE_URL=http://ml-service:8002
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - ml-service
    volumes:
      - ./agents/summarisation:/app
      - ./agents/shared:/app/shared
    command: uvicorn main:app --host 0.0.0.0 --port 8014 --reload

  response-agent:
    build:
      context: ./agents/response
      dockerfile: Dockerfile
    container_name: pharmalyx-response
    ports:
      - "8015:8015"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - redis
    volumes:
      - ./agents/response:/app
      - ./agents/shared:/app/shared
    command: uvicorn main:app --host 0.0.0.0 --port 8015 --reload

  # ─── DATA PIPELINE ────────────────────────────────────────────
  airflow-webserver:
    build:
      context: ./pipeline
      dockerfile: Dockerfile.airflow
    container_name: pharmalyx-airflow-web
    ports:
      - "8080:8080"
    environment:
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:${POSTGRES_PASSWORD}@postgres:5432/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://:${REDIS_PASSWORD}@redis:6379/1
      - AIRFLOW__CELERY__RESULT_BACKEND=redis://:${REDIS_PASSWORD}@redis:6379/2
    depends_on:
      - postgres
      - redis
    volumes:
      - ./pipeline/dags:/opt/airflow/dags
      - ./pipeline/processors:/opt/airflow/processors
    command: webserver

  airflow-scheduler:
    build:
      context: ./pipeline
      dockerfile: Dockerfile.airflow
    container_name: pharmalyx-airflow-scheduler
    environment:
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:${POSTGRES_PASSWORD}@postgres:5432/airflow
    depends_on:
      - postgres
    volumes:
      - ./pipeline/dags:/opt/airflow/dags
    command: scheduler

  # ─── FRONTEND ─────────────────────────────────────────────────
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: pharmalyx-frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1
      - VITE_APP_ENV=development
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host 0.0.0.0

  # ─── MONITORING ───────────────────────────────────────────────
  prometheus:
    image: prom/prometheus:v2.55.1
    container_name: pharmalyx-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./infra/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:11.3.2
    container_name: pharmalyx-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./infra/grafana/dashboards:/etc/grafana/provisioning/dashboards

volumes:
  postgres_data:
  mongodb_data:
  redis_data:
  faiss_data:
  model_cache:
  prometheus_data:
  grafana_data:

networks:
  default:
    name: pharmalyx-network
```

## Makefile
```makefile
.PHONY: up down build logs shell-api shell-db migrate seed test lint

# Start all services
up:
	docker-compose -f docker-compose.yml up -d

# Stop all services
down:
	docker-compose -f docker-compose.yml down

# Rebuild all images
build:
	docker-compose -f docker-compose.yml build --no-cache

# View logs
logs:
	docker-compose -f docker-compose.yml logs -f $(service)

# Database migrations
migrate:
	docker-compose exec api-gateway alembic upgrade head

# Seed development data
seed:
	docker-compose exec api-gateway python scripts/seed_data.py

# Build initial FAISS index (run after data pipeline first ingest)
build-index:
	docker-compose exec vector-service python scripts/build_faiss_index.py

# Fine-tune models (run once with training data)
fine-tune-intent:
	docker-compose exec ml-service python scripts/fine_tune_intent.py

fine-tune-nli:
	docker-compose exec ml-service python scripts/fine_tune_nli.py

# Run tests
test:
	docker-compose exec api-gateway pytest tests/ -v --cov=.

# Run linting
lint:
	docker-compose exec api-gateway ruff check .
	docker-compose exec api-gateway black --check .

# Shell access
shell-api:
	docker-compose exec api-gateway bash

shell-db:
	docker-compose exec postgres psql -U pharmalyx_user -d pharmalyx

# Frontend
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev
```

---

# 15. SECURITY ARCHITECTURE

## 15.1 Authentication & Authorization

```python
# JWT-based auth with refresh token rotation
# RBAC: researcher < team_lead < admin

# Rate limiting per plan:
# free:       10 queries/day, 30 req/min
# pro:        200 queries/day, 60 req/min
# enterprise: 2000 queries/day, unlimited req/min

# Password policy:
# - Minimum 10 characters
# - Bcrypt with cost factor 12
# - No plaintext storage anywhere

# Token security:
# - Access tokens: 60-minute expiry
# - Refresh tokens: 30-day expiry, rotated on each use
# - Refresh tokens stored as bcrypt hash in DB
```

## 15.2 Data Security

```
- All data in transit: TLS 1.3 (Let's Encrypt certificates in prod)
- All data at rest: AES-256 (PostgreSQL + MongoDB encrypted volumes)
- API keys: Stored as SHA-256 hashes, never in plaintext
- Environment variables: Never committed to git, injected via Docker secrets
- Gemini API calls: No patient data ever included in prompts
- PII: Email stored, no medical records or patient data stored
- FAISS index: Contains only document embeddings, no PII
```

## 15.3 API Security

```python
# Security headers via middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

---

# 16. TESTING STRATEGY

## 16.1 Unit Tests

```python
# tests/unit/test_eqs_scorer.py
import pytest
import numpy as np
from agents.ranking.eqs.scorer import EQSScorer

class TestEQSScorer:
    @pytest.fixture
    def scorer(self):
        return EQSScorer()

    def test_eqs_meta_analysis_ranked_above_case_report(self, scorer):
        query_emb = np.random.rand(768)
        query_emb /= np.linalg.norm(query_emb)

        meta_analysis_doc = {
            "study_type": "meta_analysis",
            "publication_year": 2023,
            "citation_count": 150,
            "impact_factor": 8.5,
            "retrieval_score": 0.85
        }
        case_report_doc = {
            "study_type": "case_report",
            "publication_year": 2023,
            "citation_count": 2,
            "impact_factor": 1.2,
            "retrieval_score": 0.85  # Same semantic similarity
        }
        meta_score = scorer.compute(meta_analysis_doc, query_emb)
        case_score = scorer.compute(case_report_doc, query_emb)
        assert meta_score > case_score

    def test_recent_doc_ranked_above_old_doc(self, scorer):
        query_emb = np.random.rand(768)
        query_emb /= np.linalg.norm(query_emb)

        recent = {"study_type": "RCT", "publication_year": 2023,
                  "citation_count": 10, "impact_factor": 5.0,
                  "retrieval_score": 0.80}
        old = {"study_type": "RCT", "publication_year": 1995,
               "citation_count": 10, "impact_factor": 5.0,
               "retrieval_score": 0.80}
        assert scorer.compute(recent, query_emb) > scorer.compute(old, query_emb)

    def test_eqs_in_valid_range(self, scorer):
        query_emb = np.random.rand(768)
        query_emb /= np.linalg.norm(query_emb)
        doc = {"study_type": "cohort", "publication_year": 2020,
               "citation_count": 50, "impact_factor": 3.5,
               "retrieval_score": 0.75}
        score = scorer.compute(doc, query_emb)
        assert 0.0 <= score <= 1.0
```

```python
# tests/unit/test_contra_score.py
import pytest
from agents.contradiction.nli.contra_score import ContraScoreComputer

class TestContraScore:
    def test_identical_entity_sets_gives_max_overlap(self):
        comp = ContraScoreComputer()
        e1 = {"metformin", "nafld"}
        e2 = {"metformin", "nafld"}
        assert comp.topic_overlap(e1, e2) == 1.0

    def test_disjoint_entity_sets_gives_zero_overlap(self):
        comp = ContraScoreComputer()
        e1 = {"metformin"}
        e2 = {"atorvastatin"}
        assert comp.topic_overlap(e1, e2) == 0.0

    def test_contra_score_zero_when_no_topic_overlap(self):
        comp = ContraScoreComputer()
        # Even with high NLI contradiction prob, if no topic overlap
        # ContraScore should be 0
        score = comp.compute(nli_contra_prob=0.95, e1={"metformin"}, e2={"aspirin"})
        assert score == 0.0

    def test_flagged_above_threshold(self):
        comp = ContraScoreComputer(threshold=0.72)
        score = comp.compute(nli_contra_prob=0.90, e1={"metformin", "nafld"},
                             e2={"metformin", "nafld"})
        assert score >= 0.72
        assert comp.is_contradiction(score) is True
```

## 16.2 Integration Tests

```python
# tests/integration/test_pipeline_end_to_end.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_query_returns_evidence_cards():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Login first
        login_r = await client.post("/api/v1/auth/login", json={
            "email": "test@pharmalyx.com",
            "password": "testpassword123"
        })
        token = login_r.json()["access_token"]

        # Submit query
        query_r = await client.post(
            "/api/v1/query/sync",
            json={"query": "metformin type 2 diabetes", "config": {"stream": False}},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert query_r.status_code == 200
        result = query_r.json()
        assert len(result["evidence_cards"]) > 0
        assert result["evidence_cards"][0]["eqs_score"] > 0
        assert result["response_text"] is not None

@pytest.mark.asyncio
async def test_contradiction_detected_for_conflicting_topic():
    """Test that contradiction detection fires on a known conflicting topic"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Use a topic known to have conflicting evidence in the test corpus
        token = await get_test_token(client)
        r = await client.post(
            "/api/v1/query/sync",
            json={"query": "contradictions metformin NAFLD liver histology",
                  "config": {"stream": False}},
            headers={"Authorization": f"Bearer {token}"}
        )
        result = r.json()
        # Should detect contradictions if test corpus has conflicting docs
        assert "contradiction_alerts" in result
```

## 16.3 Benchmark Tests

```python
# tests/benchmarks/test_retrieval_precision.py
# Evaluates against BioASQ dataset

def test_precision_at_10():
    """Precision@10 should exceed 0.65 on BioASQ pharmaceutical queries"""
    from benchmarks.bioasq_evaluator import BioASQEvaluator
    evaluator = BioASQEvaluator(dataset_path="tests/fixtures/bioasq_pharma.json")
    results = evaluator.evaluate_retrieval(top_k=10)
    assert results["precision_at_10"] >= 0.65
    assert results["recall_at_10"] >= 0.55
    assert results["ndcg_at_10"] >= 0.60

def test_response_latency():
    """End-to-end query latency must be under 8 seconds (P95)"""
    import statistics
    from tests.helpers import time_query
    latencies = [time_query("metformin type 2 diabetes") for _ in range(20)]
    p95 = sorted(latencies)[int(0.95 * len(latencies))]
    assert p95 < 8000  # milliseconds
```

---

# 17. PERFORMANCE & SCALABILITY

## 17.1 Latency Budget (per query)

| Agent | Target Latency | Notes |
|---|---|---|
| Agent 1 (QUA) | < 800ms | NER + intent + Gemini structured output |
| Agent 2 (Retrieval) | < 2000ms | 4 API calls in parallel + FAISS |
| Agent 3 (Ranking) | < 600ms | EQS scoring, OpenAlex lookup cached |
| Agent 4 (Contradiction) | < 1500ms | NLI on top-20 docs, GPU accelerated |
| Agent 5 (Summarisation) | < 1200ms | Gemini API call |
| Agent 6 (Response) | < 800ms | Gemini API call + formatting |
| **Total P95** | **< 8000ms** | Agents 3 + 4 run partially parallel |

## 17.2 Caching Strategy

```python
# Cache layers:
# 1. Redis query cache: Cache full pipeline results for identical queries (1h TTL)
# 2. Redis session cache: Cache conversation history (24h TTL)
# 3. Redis OpenAlex cache: Cache citation counts + IFs (7d TTL)
# 4. FAISS index: Pre-built, rebuilt weekly, serves all queries
# 5. In-memory model cache: ML models loaded once per service instance

# Cache key construction for query results:
import hashlib, json

def make_cache_key(structured_query: dict, config: dict) -> str:
    key_data = {
        "entities": sorted(structured_query.get("entities", []),
                           key=lambda e: e["canonical_name"]),
        "intent": structured_query.get("intent"),
        "temporal_filter": structured_query.get("temporal_filter"),
        "study_type_filter": sorted(config.get("study_type_filter", []))
    }
    return "query:" + hashlib.sha256(
        json.dumps(key_data, sort_keys=True).encode()
    ).hexdigest()[:16]
```

## 17.3 Scaling Strategy

```
Horizontal scaling (stateless services):
  api-gateway: 2–4 replicas behind Nginx load balancer
  orchestrator: 2 replicas
  qua-agent: 2 replicas (CPU-bound, fast)
  retrieval-agent: 2–4 replicas (network-bound, most concurrent)
  ranking-agent: 2 replicas
  response-agent: 2 replicas

GPU services (scale by GPU count):
  ml-service: 1–2 GPU replicas (handles embedding + NLI)
  contradiction-agent: 1–2 GPU replicas

Vertical scaling:
  FAISS vector service: Single replica with NFS volume (not horizontally scalable in Phase 1)
  → Phase 2: Migrate to Milvus or Weaviate for distributed vector search
```

---

# 18. MONITORING & OBSERVABILITY

## 18.1 Metrics to Track (Prometheus)

```python
# Key metrics per service:

# API Gateway
pharmalyx_query_total{status, intent}
pharmalyx_query_duration_seconds{quantile}
pharmalyx_auth_attempts_total{result}
pharmalyx_rate_limit_hits_total{plan}

# Each Agent
pharmalyx_agent_duration_seconds{agent, quantile}
pharmalyx_agent_errors_total{agent, error_type}
pharmalyx_agent_model_calls_total{agent, model}
pharmalyx_agent_token_usage_total{agent, model}

# Retrieval Agent specifically
pharmalyx_docs_retrieved_total{source}
pharmalyx_faiss_search_duration_seconds{quantile}
pharmalyx_api_calls_total{source, status}

# Contradiction Agent
pharmalyx_contradictions_detected_total
pharmalyx_nli_inference_duration_seconds{quantile}
pharmalyx_contra_score_distribution (histogram)

# Data Pipeline
pharmalyx_pipeline_run_duration_seconds{dag}
pharmalyx_docs_ingested_total{source}
pharmalyx_faiss_index_size (gauge)
pharmalyx_embedding_errors_total
```

## 18.2 Grafana Dashboards

```
Dashboard 1: Pharmalyx Overview
  - Query volume over time
  - P50/P95/P99 end-to-end latency
  - Active users (last 24h)
  - Error rate
  - Contradiction detection rate

Dashboard 2: Agent Performance
  - Per-agent latency breakdown (stacked bar)
  - Per-agent error rate
  - Gemini API token usage and cost
  - ML model inference latency

Dashboard 3: Data Pipeline
  - Documents ingested per day by source
  - FAISS index size over time
  - Deduplication rate
  - Failed DAG runs

Dashboard 4: Infrastructure
  - CPU/Memory per service
  - GPU utilisation (ml-service, contradiction-agent)
  - Database connection pool usage
  - Redis cache hit rate
```

## 18.3 Structured Logging

```python
# All services use structlog for JSON-structured logging
import structlog

logger = structlog.get_logger()

# Example: Orchestrator pipeline log
logger.info(
    "pipeline_complete",
    query_id=str(query_id),
    session_id=str(session_id),
    intent=structured_query.intent,
    total_docs=len(ranked_docs),
    contradiction_count=contradiction_report.contradiction_count,
    evidence_strength=evidence_summary.evidence_strength,
    total_duration_ms=total_ms,
    agent_timings={
        "qua_ms": qua_ms,
        "retrieval_ms": retrieval_ms,
        "ranking_ms": ranking_ms,
        "contradiction_ms": contra_ms,
        "summarisation_ms": summ_ms,
        "response_ms": response_ms
    }
)
```

---

# 19. IMPLEMENTATION ROADMAP

## Phase 2 Sprint Plan

| Sprint | Weeks | Focus | Key Deliverables |
|---|---|---|---|
| **Sprint 1** | 1–3 | Data infrastructure | PostgreSQL schema, MongoDB setup, Airflow DAGs, PubMed + ClinicalTrials connectors live, initial document ingest (~50K papers) |
| **Sprint 2** | 4–6 | Vector search | BioBERT embedding pipeline, FAISS index built, semantic search functional, basic retrieval API |
| **Sprint 3** | 7–9 | RAG pipeline | QUA agent, Retrieval agent, Ranking agent, full RAG pipeline with citation injection, Gemini integration |
| **Sprint 4** | 10–12 | Contradiction engine | NLI fine-tuning on MedNLI, CDA agent, ContraScore algorithm, contradiction alerts in API response |
| **Sprint 5** | 13–14 | Summarisation + Response | SA agent, RGA agent, follow-up suggestions, SSE streaming response |
| **Sprint 6** | 15–16 | Frontend | React dashboard, agent progress bar, evidence cards, contradiction alert UI, D3 graph |
| **Sprint 7** | 17–18 | Evaluation | BioASQ benchmarks, latency profiling, NLI accuracy on held-out MedNLI, load testing |
| **Sprint 8** | 19–20 | Production | Docker Compose prod setup, monitoring stack, export (PDF, BibTeX), documentation |

## Quick Start Commands

```bash
# 1. Clone and setup
git clone https://github.com/your-org/pharmalyx.git
cd pharmalyx
cp .env.example .env.local
# Edit .env.local with your API keys

# 2. Start infrastructure
make up

# 3. Run database migrations
make migrate

# 4. Seed initial data (dev only)
make seed

# 5. Build FAISS index (after first data ingest)
make build-index

# 6. Fine-tune models (optional, use pre-trained for dev)
make fine-tune-nli

# 7. Run tests
make test

# 8. Open frontend
open http://localhost:3000

# 9. API docs (FastAPI auto-generated Swagger)
open http://localhost:8000/docs

# 10. Airflow (trigger data pipeline)
open http://localhost:8080
```

---

*End of Pharmalyx Complete Product & Engineering Reference*
*Version 1.0 | For Antigravity Build Reference*