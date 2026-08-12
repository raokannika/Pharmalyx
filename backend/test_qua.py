import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.agents.qua import QueryUnderstandingAgent
from app.models.query import StructuredQuery

async def test_qua_agent():
    print("=== PHARMALYX QUERY UNDERSTANDING AGENT (QUA) TEST ===")

    qua = QueryUnderstandingAgent()
    print("[SUCCESS] QUA initialized.")

    # -----------------------------------------------------------------
    # TEST 1: Evidence Retrieval Query
    # -----------------------------------------------------------------
    q1 = "Does metformin reduce liver fibrosis in non-alcoholic fatty liver disease?"
    print(f"\n[INFO] Test 1 Query: '{q1}'")
    sq1 = await qua.process(q1)

    assert isinstance(sq1, StructuredQuery), "Output must be StructuredQuery instance"
    assert sq1.intent == "evidence_retrieval", f"Expected intent 'evidence_retrieval', got '{sq1.intent}'"
    assert len(sq1.entities) >= 2, f"Expected at least 2 entities, got {len(sq1.entities)}"

    entity_names = [e.canonical_name.lower() for e in sq1.entities]
    entity_types = [e.entity_type for e in sq1.entities]

    assert any("metformin" in name for name in entity_names), "Metformin must be extracted as Drug entity"
    assert "Drug" in entity_types, "Drug entity type must be present"
    assert len(sq1.pubmed_query_string) > 0, "PubMed query string must be generated"

    print("[SUCCESS] Evidence retrieval query processed.")
    print("[SUCCESS] Biomedical entities extracted.")
    print(f"         Extracted Entities: {[f'{e.canonical_name} ({e.entity_type})' for e in sq1.entities]}")
    print(f"         PubMed Query String: {sq1.pubmed_query_string}")

    # -----------------------------------------------------------------
    # TEST 2: Clinical Trial Query
    # -----------------------------------------------------------------
    q2 = "What clinical trials are studying pembrolizumab for melanoma?"
    print(f"\n[INFO] Test 2 Query: '{q2}'")
    sq2 = await qua.process(q2)

    assert sq2.intent == "clinical_trial", f"Expected intent 'clinical_trial', got '{sq2.intent}'"
    assert len(sq2.clinicaltrials_params) > 0, "ClinicalTrials params must be generated"
    print("[SUCCESS] Clinical trial query processed.")
    print(f"         ClinicalTrials Params: {sq2.clinicaltrials_params}")

    # -----------------------------------------------------------------
    # TEST 3: Drug Comparison Query
    # -----------------------------------------------------------------
    q3 = "Compare metformin and pioglitazone for type 2 diabetes."
    print(f"\n[INFO] Test 3 Query: '{q3}'")
    sq3 = await qua.process(q3)

    assert sq3.intent == "drug_comparison", f"Expected intent 'drug_comparison', got '{sq3.intent}'"
    assert sq3.comparison_mode is True, "comparison_mode must be True"
    assert len(sq3.comparison_entities) >= 2, "comparison_entities must contain at least 2 drugs"

    comp_lower = [c.lower() for c in sq3.comparison_entities]
    assert any("metformin" in c for c in comp_lower), "Metformin should be in comparison entities"
    assert any("pioglitazone" in c for c in comp_lower), "Pioglitazone should be in comparison entities"

    print("[SUCCESS] Drug comparison detected.")
    print(f"         Comparison Entities: {sq3.comparison_entities}")

    # -----------------------------------------------------------------
    # TEST 4: Temporal Filter Query
    # -----------------------------------------------------------------
    q4 = "Show me studies from the last 5 years about aspirin and colorectal cancer."
    print(f"\n[INFO] Test 4 Query: '{q4}'")
    sq4 = await qua.process(q4)

    assert sq4.temporal_filter is not None, "Temporal filter must be present"
    assert sq4.temporal_filter.from_year is not None, "from_year should be set"
    assert sq4.temporal_filter.from_year >= 2020, f"Expected from_year >= 2020, got {sq4.temporal_filter.from_year}"
    assert sq4.temporal_filter.recency_bias is True, "recency_bias should be True"

    print("[SUCCESS] Temporal filter processed.")
    print(f"         Temporal Filter: {sq4.temporal_filter.from_year} to {sq4.temporal_filter.to_year}")

    # -----------------------------------------------------------------
    # TEST 5: Follow-Up Query Resolution
    # -----------------------------------------------------------------
    history = [
        {"role": "user", "content": "Does metformin help with type 2 diabetes?"},
        {"role": "assistant", "content": "Metformin is a primary first-line oral antihyperglycemic medication for type 2 diabetes..."}
    ]
    q5 = "What about liver fibrosis?"
    print(f"\n[INFO] Test 5 Follow-up Query: '{q5}' with history context.")

    sq5 = await qua.process(q5, session_context={"conversation_history": history})

    assert sq5.is_followup is True, "is_followup must be True"
    assert sq5.resolved_from_history is True, "resolved_from_history must be True"

    resolved_names = [e.canonical_name.lower() for e in sq5.entities]
    assert any("metformin" in n for n in resolved_names), "Metformin should be resolved from history context"

    print("[SUCCESS] Follow-up query resolution processed.")
    print(f"         Resolved Entities: {[f'{e.canonical_name} ({e.entity_type})' for e in sq5.entities]}")

    print("\n=== STEP 4 VERIFICATION PASSED ===")

if __name__ == "__main__":
    asyncio.run(test_qua_agent())
