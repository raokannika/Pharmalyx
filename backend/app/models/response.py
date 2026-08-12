import uuid
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from .evidence import EvidenceSummary

class EvidenceCard(BaseModel):
    doc_id: str
    title: str
    authors_short: str = ""
    journal: str = ""
    year: int = 2024
    pmid: Optional[str] = None
    doi: Optional[str] = None
    url: str = ""
    abstract_excerpt: str = ""
    study_type: str = "unknown"
    eqs_score: float = 0.0
    eqs_components: Dict[str, float] = Field(default_factory=dict)
    source: str = "pubmed"
    has_contradiction: bool = False
    contradiction_badge: Optional[str] = None

class ContradictionAlert(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    severity: str = "medium"
    entity: str
    headline: str
    claim_1_excerpt: str
    claim_1_source: str
    claim_2_excerpt: str
    claim_2_source: str
    contra_score: float
    explanation: str

class QueryResult(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    raw_query: str
    response_text: str = ""
    intent_label: str = "evidence_retrieval"
    entity_labels: List[str] = Field(default_factory=list)
    evidence_cards: List[EvidenceCard] = Field(default_factory=list)
    contradiction_alerts: List[ContradictionAlert] = Field(default_factory=list)
    evidence_summary: Optional[EvidenceSummary] = None
    follow_up_suggestions: List[str] = Field(default_factory=list)
    evidence_strength: str = "Moderate"
    total_sources_retrieved: int = 0
    sources_analysed: int = 0
    processing_time_ms: int = 0
    export_payload: Dict[str, Any] = Field(default_factory=dict)
