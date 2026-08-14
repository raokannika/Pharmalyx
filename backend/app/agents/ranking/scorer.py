import math
from datetime import datetime
from typing import Dict, Optional
from app.models.document import Document, EQSComponents

class EQSScorer:
    """Calculates Evidence Quality Score (EQS) and its 5 components for documents.

    Governing Formula (from docs.md):
        EQS(d) = α · Sim(q,d) + β · IF(d) + γ · Rec(d) + δ · Cite(d) + ε · StudyType(d)

    Default weights:
        α = 0.35 (Semantic Similarity)
        β = 0.20 (Journal Impact Factor)
        γ = 0.15 (Publication Recency)
        δ = 0.15 (Citation Impact)
        ε = 0.15 (Study Methodology Quality)
    """

    STUDY_TYPE_WEIGHTS: Dict[str, float] = {
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

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "sim": 0.35,
        "if": 0.20,
        "rec": 0.15,
        "cite": 0.15,
        "stype": 0.15
    }

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        current_year: Optional[int] = None
    ):
        self.weights = weights or self.DEFAULT_WEIGHTS
        self.current_year = current_year or datetime.now().year

    def compute_components(
        self,
        doc: Document,
        max_if: float = 1.0,
        max_cite: int = 1
    ) -> EQSComponents:
        # 1. Semantic Similarity: Sim(q,d) in [0, 1]
        sim = float(doc.retrieval_score) if doc.retrieval_score is not None else 0.0
        sim_norm = min(max(sim, 0.0), 1.0)

        # 2. Journal Impact Factor: IF(d) = impact_factor / max(max_if, 1) in [0, 1]
        if_val = float(doc.impact_factor) if doc.impact_factor is not None else 0.0
        if_norm = min(if_val / max(max_if, 1.0), 1.0) if max_if > 0 else 0.0
        if_norm = max(if_norm, 0.0)

        # 3. Recency: Rec(d) = exp(-0.1 * (current_year - publication_year)) in [0, 1]
        year = doc.publication_year if doc.publication_year is not None else self.current_year
        years_diff = max(self.current_year - year, 0)
        rec_norm = math.exp(-0.1 * years_diff)

        # 4. Citation Impact: Cite(d) = log(1 + citations) / log(1 + max_citations) in [0, 1]
        cite_count = max(doc.citation_count, 0) if doc.citation_count is not None else 0
        if max_cite > 0:
            cite_norm = math.log1p(cite_count) / math.log1p(max_cite)
        else:
            cite_norm = 0.0
        cite_norm = min(max(cite_norm, 0.0), 1.0)

        # 5. Study Quality: StudyType(d) weight mapping in [0, 1]
        stype = (doc.study_type or "unknown").lower()
        stype_norm = self.STUDY_TYPE_WEIGHTS.get(stype, self.STUDY_TYPE_WEIGHTS["unknown"])

        return EQSComponents(
            semantic_similarity=round(sim_norm, 4),
            journal_impact=round(if_norm, 4),
            recency=round(float(rec_norm), 4),
            citation_impact=round(float(cite_norm), 4),
            study_quality=round(stype_norm, 4)
        )

    def calculate_eqs(self, components: EQSComponents) -> float:
        w = self.weights
        eqs = (
            w["sim"] * components.semantic_similarity +
            w["if"] * components.journal_impact +
            w["rec"] * components.recency +
            w["cite"] * components.citation_impact +
            w["stype"] * components.study_quality
        )
        return round(eqs, 4)
