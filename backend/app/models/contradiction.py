from typing import List, Optional
from pydantic import BaseModel, Field

class ContradictionPair(BaseModel):
    claim_1_text: str
    claim_1_source: str
    claim_1_pmid: Optional[str] = None
    claim_2_text: str
    claim_2_source: str
    claim_2_pmid: Optional[str] = None
    shared_entity: str
    contra_score: float = Field(ge=0.0, le=1.0)
    nli_label: str = Field(default="contradiction", description="contradiction | neutral")
    nli_confidence: float = 0.0
    topic_overlap: float = 0.0
    explanation: str = ""
    severity: str = Field(default="medium", description="high | medium | low")

class ContradictionReport(BaseModel):
    contradiction_pairs: List[ContradictionPair] = Field(default_factory=list)
    contradiction_alert: bool = False
    contradiction_count: int = 0
    high_confidence_count: int = 0
