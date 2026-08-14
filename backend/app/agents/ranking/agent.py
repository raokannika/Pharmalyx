import logging
from typing import List, Dict, Optional, Any, Union
from app.models.document import Document, RankedDocument
from .scorer import EQSScorer

logger = logging.getLogger(__name__)

class EvidenceRankingAgent:
    """Agent 3: Evidence Ranking Agent (ERA).
    Ranks retrieved candidate documents using composite Evidence Quality Score (EQS).
    """

    def __init__(
        self,
        scorer: Optional[EQSScorer] = None,
        weights: Optional[Dict[str, float]] = None
    ):
        self.scorer = scorer or EQSScorer(weights=weights)

    async def process(
        self,
        documents: List[Union[Document, Dict[str, Any]]],
        weights: Optional[Dict[str, float]] = None
    ) -> List[RankedDocument]:
        """Process candidate documents, compute EQS scores and components, and return descending sorted RankedDocuments."""
        if not documents:
            return []

        # Convert dictionary inputs to Document Pydantic models if needed
        doc_objects: List[Document] = []
        for d in documents:
            if isinstance(d, Document):
                doc_objects.append(d)
            elif isinstance(d, dict):
                try:
                    doc_objects.append(Document(**d))
                except Exception as exc:
                    logger.warning(f"Failed to parse Document dict in ERA: {exc}")
            else:
                logger.warning(f"Unexpected document type in ERA: {type(d)}")

        if not doc_objects:
            return []

        # Dynamically set weights/scorer if custom weights passed
        if weights:
            scorer = EQSScorer(weights=weights, current_year=self.scorer.current_year)
        else:
            scorer = self.scorer

        # Find maximum bounds across candidate set for IF and citation normalization
        max_if = max((d.impact_factor for d in doc_objects if d.impact_factor is not None), default=0.0)
        max_cite = max((d.citation_count for d in doc_objects if d.citation_count is not None), default=0)

        ranked_docs: List[RankedDocument] = []

        for doc in doc_objects:
            components = scorer.compute_components(doc, max_if=max_if, max_cite=max_cite)
            eqs_score = scorer.calculate_eqs(components)

            # Dump document to dict and inject EQS score and components
            doc_dict = doc.model_dump()
            doc_dict["eqs_score"] = eqs_score
            doc_dict["eqs_components"] = components

            ranked_docs.append(RankedDocument(**doc_dict))

        # Sort descending by EQS score
        ranked_docs.sort(key=lambda d: d.eqs_score, reverse=True)
        return ranked_docs
