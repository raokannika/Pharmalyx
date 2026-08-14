import os
import sys
import asyncio
from datetime import datetime

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.models.document import Document, RankedDocument, EQSComponents
from app.agents.ranking import EvidenceRankingAgent, EQSScorer

async def test_evidence_ranking_agent():
    print("=== PHARMALYX EVIDENCE RANKING AGENT (ERA) TEST ===")

    # 1. Initialize ERA and Scorer
    current_yr = 2026
    scorer = EQSScorer(current_year=current_yr)
    era = EvidenceRankingAgent(scorer=scorer)
    print("[SUCCESS] EvidenceRankingAgent & EQSScorer initialized.")

    # 2. Construct deterministic test documents
    doc_meta = Document(
        source="pubmed",
        external_id="1001",
        pmid="1001",
        title="Meta-Analysis of Metformin in NAFLD Patients",
        abstract="Pooled analysis of 15 RCTs showing significant ALT reduction...",
        study_type="meta_analysis",
        publication_year=2025,
        citation_count=120,
        impact_factor=18.5,
        retrieval_score=0.92
    )

    doc_rct_recent = Document(
        source="pubmed",
        external_id="1002",
        pmid="1002",
        title="Randomized Controlled Trial of Metformin vs Placebo in NASH",
        abstract="Double-blind RCT investigating liver histology endpoints...",
        study_type="RCT",
        publication_year=2024,
        citation_count=45,
        impact_factor=12.0,
        retrieval_score=0.85
    )

    doc_case_old = Document(
        source="pubmed",
        external_id="1003",
        pmid="1003",
        title="Case Report of Metformin-Associated Lactic Acidosis",
        abstract="A single patient case description from 1998...",
        study_type="case_report",
        publication_year=1998,
        citation_count=2,
        impact_factor=1.5,
        retrieval_score=0.70
    )

    doc_missing_metadata = Document(
        source="clinicaltrials",
        external_id="NCT999999",
        nct_id="NCT999999",
        title="Observational Study of Metformin in Liver Disease",
        abstract="Brief summary with minimal metadata...",
        study_type="cohort",
        publication_year=None,     # Missing publication year
        citation_count=0,          # 0 citations
        impact_factor=0.0,         # Missing impact factor
        retrieval_score=0.60
    )

    docs = [doc_case_old, doc_meta, doc_missing_metadata, doc_rct_recent]

    # 3. Test Scorer component calculation directly
    components_meta = scorer.compute_components(doc_meta, max_if=18.5, max_cite=120)
    assert components_meta.semantic_similarity == 0.92
    assert components_meta.journal_impact == 1.0       # 18.5 / 18.5
    assert components_meta.citation_impact == 1.0      # log1p(120) / log1p(120)
    assert components_meta.study_quality == 1.0         # meta_analysis weight = 1.0

    eqs_meta = scorer.calculate_eqs(components_meta)
    print(f"[SUCCESS] EQS components and score verified for Meta-Analysis (EQS = {eqs_meta:.4f})")

    # 4. Test ERA process execution
    ranked_docs = await era.process(docs)
    assert len(ranked_docs) == 4, f"Expected 4 ranked docs, got {len(ranked_docs)}"
    print(f"[SUCCESS] Processed {len(ranked_docs)} documents into RankedDocument instances.")

    # 5. Verify descending sort order
    for i in range(len(ranked_docs) - 1):
        assert ranked_docs[i].eqs_score >= ranked_docs[i+1].eqs_score, \
            f"Sorting error: index {i} EQS {ranked_docs[i].eqs_score} < index {i+1} EQS {ranked_docs[i+1].eqs_score}"

    print("[SUCCESS] Documents sorted in descending EQS order:")
    for idx, rdoc in enumerate(ranked_docs, 1):
        print(f"   #{idx} EQS={rdoc.eqs_score:.4f} | StudyType={rdoc.study_type:<15} | Title='{rdoc.title[:55]}...'")

    # Verify expected top document is Meta-Analysis and lowest is old Case Report
    assert ranked_docs[0].external_id == "1001", "Top-ranked document must be Meta-Analysis"
    assert ranked_docs[-1].external_id == "1003", "Lowest-ranked document must be old Case Report"
    print("[SUCCESS] Top-ranked and lowest-ranked documents match theoretical expectations.")

    # 6. Verify missing metadata handling
    missing_doc_ranked = next(r for r in ranked_docs if r.external_id == "NCT999999")
    assert missing_doc_ranked.eqs_components.journal_impact == 0.0, "Missing IF should result in 0.0 journal impact"
    assert missing_doc_ranked.eqs_components.citation_impact == 0.0, "0 citations should result in 0.0 citation impact"
    assert missing_doc_ranked.eqs_components.recency == 1.0, "Missing publication year defaults to current year (recency = 1.0)"
    print("[SUCCESS] Missing/optional metadata handled safely without exceptions.")

    # 7. Verify Pydantic JSON serialization
    serialized_json = ranked_docs[0].model_dump_json()
    assert len(serialized_json) > 0
    print(f"[SUCCESS] RankedDocument successfully serialized to JSON ({len(serialized_json)} bytes).")

    print("\n=== STEP 5 VERIFICATION PASSED ===")

if __name__ == "__main__":
    asyncio.run(test_evidence_ranking_agent())
