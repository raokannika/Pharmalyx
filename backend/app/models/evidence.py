from typing import List, Optional
from pydantic import BaseModel, Field

class KeyFinding(BaseModel):
    finding: str
    citation: str
    pmid: Optional[str] = None
    evidence_level: str = Field(default="Moderate", description="High | Moderate | Low")

class RecommendedReading(BaseModel):
    title: str
    citation: str
    pmid: Optional[str] = None
    justification: str

class EvidenceSummary(BaseModel):
    main_summary: str = ""
    key_findings: List[KeyFinding] = Field(default_factory=list)
    study_populations: str = ""
    methodological_limitations: str = ""
    conflict_summary: Optional[str] = None
    evidence_strength: str = Field(default="Moderate", description="Strong | Moderate | Weak | Insufficient")
    evidence_strength_rationale: str = ""
    recommended_readings: List[RecommendedReading] = Field(default_factory=list)
    processing_time_ms: int = 0
