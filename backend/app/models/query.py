from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Entity(BaseModel):
    entity_text: str
    entity_type: str = Field(description="Drug | Disease | Gene | Protein | Outcome | Population | Procedure")
    canonical_name: str
    mesh_id: Optional[str] = None
    umls_cui: Optional[str] = None
    confidence: float = 1.0

class TemporalFilter(BaseModel):
    from_year: Optional[int] = 1990
    to_year: Optional[int] = 2026
    recency_bias: bool = True

class StructuredQuery(BaseModel):
    raw_query: str
    intent: str = Field(
        default="evidence_retrieval",
        description="evidence_retrieval | drug_interaction | clinical_trial | contradiction_check | drug_comparison | general_summary"
    )
    entities: List[Entity] = Field(default_factory=list)
    expanded_terms: Dict[str, List[str]] = Field(default_factory=dict)
    temporal_filter: TemporalFilter = Field(default_factory=TemporalFilter)
    comparison_mode: bool = False
    comparison_entities: List[str] = Field(default_factory=list)
    pubmed_query_string: str = ""
    clinicaltrials_params: Dict[str, str] = Field(default_factory=dict)
    is_followup: bool = False
    resolved_from_history: bool = False
    processing_time_ms: int = 0
