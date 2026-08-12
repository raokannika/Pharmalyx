import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.connectors.pubmed import PubMedConnector
from app.connectors.clinicaltrials import ClinicalTrialsConnector

async def test_connectors():
    print("=== PHARMALYX EXTERNAL CONNECTORS TEST ===")

    # -------------------------------------------------------------
    # 1. Test PubMed Connector
    # -------------------------------------------------------------
    print("\n[INFO] Testing PubMed connector...")
    pubmed = PubMedConnector()
    try:
        pmids = await pubmed.search("metformin liver fibrosis", max_results=5)
        if not pmids:
            print("[FAIL] PubMed search returned 0 PMIDs.")
            sys.exit(1)

        print(f"[SUCCESS] PubMed search returned {len(pmids)} PMIDs: {pmids}")

        docs = await pubmed.fetch_articles(pmids)
        if not docs:
            print("[FAIL] PubMed fetch_articles returned 0 documents.")
            sys.exit(1)

        print(f"[SUCCESS] PubMed article fetch returned {len(docs)} documents.")

        # Validate normalization
        sample = docs[0]
        assert sample.source == "pubmed", f"Expected source 'pubmed', got '{sample.source}'"
        assert sample.pmid is not None, "PMID should be populated"
        assert len(sample.title) > 0, "Title should not be empty"
        assert sample.url.startswith("https://pubmed.ncbi.nlm.nih.gov/"), "URL should point to PubMed"

        print(f"[SUCCESS] PubMed normalization verified for PMID {sample.pmid}: '{sample.title[:60]}...'")
    finally:
        await pubmed.close()

    # -------------------------------------------------------------
    # 2. Test ClinicalTrials.gov Connector
    # -------------------------------------------------------------
    print("\n[INFO] Testing ClinicalTrials.gov connector...")
    ct = ClinicalTrialsConnector()
    try:
        ct_docs = await ct.search(condition="diabetes", intervention="metformin", max_results=5)
        if not ct_docs:
            print("[FAIL] ClinicalTrials search returned 0 documents.")
            sys.exit(1)

        print(f"[SUCCESS] ClinicalTrials.gov search returned {len(ct_docs)} studies.")

        # Validate normalization
        ct_sample = ct_docs[0]
        assert ct_sample.source == "clinicaltrials", f"Expected source 'clinicaltrials', got '{ct_sample.source}'"
        assert ct_sample.nct_id is not None, "NCT ID should be populated"
        assert len(ct_sample.title) > 0, "Title should not be empty"
        assert ct_sample.url.startswith("https://clinicaltrials.gov/study/"), "URL should point to ClinicalTrials.gov"

        print(f"[SUCCESS] ClinicalTrials.gov normalization verified for {ct_sample.nct_id}: '{ct_sample.title[:60]}...'")
    finally:
        await ct.close()

    print("\n=== STEP 3 VERIFICATION PASSED ===")

if __name__ == "__main__":
    asyncio.run(test_connectors())
