import uuid
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    doc_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str = Field(description="pubmed | clinicaltrials | drugbank | patent")
    external_id: Optional[str] = None
    pmid: Optional[str] = None
    doi: Optional[str] = None
    nct_id: Optional[str] = None
    title: str
    abstract: str = ""
    full_text: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    journal: Optional[str] = None
    publication_date: Optional[str] = None
    publication_year: Optional[int] = None
    study_type_raw: Optional[str] = None
    study_type: str = Field(
        default="unknown",
        description="meta_analysis | systematic_review | RCT | cohort | case_control | cross_sectional | review_narrative | in_vitro | computational | case_report | unknown"
    )
    mesh_terms: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    citation_count: int = 0
    impact_factor: float = 0.0
    url: str = ""
    retrieval_score: float = 0.0
    retrieval_method: str = Field(default="api_keyword", description="faiss | bm25 | api_keyword")

class EQSComponents(BaseModel):
    semantic_similarity: float = 0.0
    journal_impact: float = 0.0
    recency: float = 0.0
    citation_impact: float = 0.0
    study_quality: float = 0.0

class RankedDocument(Document):
    eqs_score: float = 0.0
    eqs_components: EQSComponents = Field(default_factory=EQSComponents)
