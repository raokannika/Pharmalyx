import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_pydantic_schemas():
    print("=== PHARMALYX CORE SCHEMAS & DATA MODELS TEST ===")

    from app.models import (
        StructuredQuery, Entity, TemporalFilter,
        Document, RankedDocument,
        ContradictionPair, ContradictionReport,
        EvidenceSummary, KeyFinding, RecommendedReading,
        QueryResult, EvidenceCard, ContradictionAlert
    )

    # 1. Test StructuredQuery
    sq = StructuredQuery(
        raw_query="Does metformin reduce liver fibrosis in NAFLD?",
        intent="evidence_retrieval",
        entities=[
            Entity(entity_text="metformin", entity_type="Drug", canonical_name="metformin"),
            Entity(entity_text="NAFLD", entity_type="Disease", canonical_name="Non-alcoholic fatty liver disease")
        ],
        pubmed_query_string='("metformin"[MH] OR "metformin"[TIAB]) AND ("Non-alcoholic fatty liver disease"[MH] OR "NAFLD"[TIAB])'
    )
    print(f"[SUCCESS] StructuredQuery model validated: {sq.entities[0].canonical_name} ({sq.intent})")

    # 2. Test RankedDocument
    doc = RankedDocument(
        source="pubmed",
        external_id="34567890",
        pmid="34567890",
        title="Metformin in Non-Alcoholic Fatty Liver Disease: A Randomized Controlled Trial",
        abstract="We investigated the effects of metformin on liver histology...",
        authors=["Smith J", "Doe A"],
        journal="Journal of Hepatology",
        publication_year=2023,
        study_type="RCT",
        citation_count=45,
        impact_factor=15.2,
        retrieval_score=0.89,
        eqs_score=0.8432,
        eqs_components={"semantic_similarity": 0.89, "journal_impact": 0.76, "recency": 0.90, "citation_impact": 0.65, "study_quality": 0.80}
    )
    print(f"[SUCCESS] RankedDocument validated: PMID {doc.pmid}, EQS={doc.eqs_score}")

    # 3. Test ContradictionPair & Report
    cp = ContradictionPair(
        claim_1_text="Metformin significantly improved liver histology after 48 weeks.",
        claim_1_source="Smith et al., 2023 [PMID: 34567890]",
        claim_1_pmid="34567890",
        claim_2_text="Metformin showed no significant effect on liver fibrosis scores compared to placebo.",
        claim_2_source="Jones et al., 2021 [PMID: 31234567]",
        claim_2_pmid="31234567",
        shared_entity="metformin",
        contra_score=0.82,
        nli_label="contradiction",
        nli_confidence=0.91,
        topic_overlap=0.90,
        explanation="Study 1 evaluated 48-week high dose (2000mg/day) in biospied patients, whereas Study 2 evaluated 24-week standard dose (1000mg/day)."
    )
    cr = ContradictionReport(
        contradiction_pairs=[cp],
        contradiction_alert=True,
        contradiction_count=1,
        high_confidence_count=1
    )
    print(f"[SUCCESS] ContradictionReport validated: ContraScore={cr.contradiction_pairs[0].contra_score}")

    # 4. Test EvidenceSummary
    summary = EvidenceSummary(
        main_summary="Current evidence presents mixed conclusions regarding metformin efficacy in NAFLD [1], [2].",
        key_findings=[
            KeyFinding(finding="Metformin improves insulin resistance in NAFLD patients [1].", citation="Smith et al., 2023", pmid="34567890", evidence_level="High")
        ],
        study_populations="Adult patients with biopsy-confirmed non-alcoholic steatohepatitis (NASH).",
        methodological_limitations="Heterogeneity in treatment duration and histological scoring systems across studies.",
        evidence_strength="Moderate",
        recommended_readings=[
            RecommendedReading(title="Metformin in NAFLD RCT", citation="Smith et al., 2023", pmid="34567890", justification="Highest quality RCT assessing histological outcomes.")
        ]
    )
    print(f"[SUCCESS] EvidenceSummary validated: Evidence Strength={summary.evidence_strength}")

    # 5. Test QueryResult JSON serialization
    qr = QueryResult(
        raw_query=sq.raw_query,
        response_text="Metformin demonstrates clear metabolic benefits but conflicting histological outcomes in NAFLD.",
        intent_label=sq.intent,
        entity_labels=["metformin", "NAFLD"],
        evidence_cards=[
            EvidenceCard(
                doc_id=doc.doc_id,
                title=doc.title,
                authors_short="Smith et al.",
                journal=doc.journal or "",
                year=doc.publication_year or 2023,
                pmid=doc.pmid,
                url=f"https://pubmed.ncbi.nlm.nih.gov/{doc.pmid}/",
                abstract_excerpt=doc.abstract[:100],
                study_type=doc.study_type,
                eqs_score=doc.eqs_score,
                has_contradiction=True,
                contradiction_badge="⚠ Conflicting Findings"
            )
        ],
        contradiction_alerts=[
            ContradictionAlert(
                severity="high",
                entity=cp.shared_entity,
                headline="Conflict regarding histological fibrosis improvement",
                claim_1_excerpt=cp.claim_1_text,
                claim_1_source=cp.claim_1_source,
                claim_2_excerpt=cp.claim_2_text,
                claim_2_source=cp.claim_2_source,
                contra_score=cp.contra_score,
                explanation=cp.explanation
            )
        ],
        evidence_summary=summary,
        follow_up_suggestions=[
            "What is the impact of pioglitazone compared to metformin in NAFLD?",
            "What are the long-term histological endpoints of GLP-1 receptor agonists in NASH?"
        ],
        evidence_strength="Moderate",
        total_sources_retrieved=45,
        sources_analysed=10,
        processing_time_ms=3420
    )

    # Test serialization to JSON
    json_bytes = qr.model_dump_json()
    assert len(json_bytes) > 0
    print(f"[SUCCESS] QueryResult serialized to JSON ({len(json_bytes)} bytes)")

    print("\n=== STEP 2 VERIFICATION PASSED ===")

if __name__ == "__main__":
    test_pydantic_schemas()
