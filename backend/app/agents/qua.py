import json
import re
import time
import logging
from typing import Dict, Any, Optional, List

from app.services.gemini_service import GeminiService
from app.models.query import StructuredQuery, Entity, TemporalFilter

logger = logging.getLogger(__name__)

QUA_SYSTEM_PROMPT = """SYSTEM: You are a pharmaceutical research query analyst integrated into Pharmalyx, a scientific evidence intelligence platform.

Your task is to analyze a researcher's natural-language query and extract structured pharmaceutical research information into valid JSON.

RULES & INSTRUCTIONS:

1. INTENT CLASSIFICATION:
   Classify intent into EXACTLY ONE of:
   - "evidence_retrieval": Default for queries seeking scientific evidence, efficacy, safety, mechanism of action.
   - "drug_interaction": Queries about drug-drug, drug-disease, or drug-food interactions.
   - "clinical_trial": Queries asking about ongoing/completed clinical trials, phases, enrollment, or NCT IDs.
   - "contradiction_check": Queries explicitly asking about conflicting evidence, disputes, controversy, or debates in literature.
   - "drug_comparison": Queries comparing two or more drugs, therapies, or interventions side-by-side.
   - "general_summary": Broad background or introductory overviews.

2. BIOMEDICAL ENTITY EXTRACTION & CANONICALIZATION:
   Extract all biomedical entities mentioned. For each entity provide:
   - "entity_text": Exact substring from query.
   - "entity_type": EXACTLY ONE of ["Drug", "Disease", "Gene", "Protein", "Outcome", "Population", "Procedure"].
   - "canonical_name": Standardized scientific name (e.g. "Glucophage" -> "metformin", "fatty liver" -> "Non-alcoholic fatty liver disease (NAFLD)", "T2D" -> "Type 2 Diabetes Mellitus", "Keytruda" -> "pembrolizumab").
   - "confidence": Float 0.0 to 1.0 (default 1.0).
   - "mesh_id": Optional MeSH Descriptor ID if known, otherwise null.
   - "umls_cui": Optional UMLS CUI if known, otherwise null.

3. QUERY EXPANSION:
   Provide "expanded_terms" mapping canonical names to lists of relevant synonyms, brand names, or MeSH terms.

4. TEMPORAL FILTERING:
   If query specifies temporal boundaries (e.g. "last 5 years", "since 2020", "recent studies"):
   - Set "from_year" and "to_year" in "temporal_filter". Assume current year is 2026.
   - Set "recency_bias": true if recent literature is requested.

5. COMPARISON MODE:
   If intent is "drug_comparison" or query compares treatments:
   - Set "comparison_mode": true.
   - List compared drug/treatment canonical names in "comparison_entities".

6. SEARCH QUERY SYNTAX GENERATION:
   - "pubmed_query_string": Generate a MeSH-formatted query using [MH] for MeSH headings and [TIAB] for Title/Abstract (e.g. `("metformin"[MH] OR "metformin"[TIAB]) AND ("Non-alcoholic fatty liver disease"[MH] OR "NAFLD"[TIAB])`).
   - "clinicaltrials_params": Object with "condition" and/or "intervention" strings suitable for ClinicalTrials.gov API v2.

7. CONVERSATION HISTORY & FOLLOW-UP RESOLUTION:
   Inspect CONVERSATION HISTORY (if provided).
   If CURRENT QUERY is a follow-up (e.g. "What about liver fibrosis?", "Are there side effects?"):
   - Set "is_followup": true.
   - Set "resolved_from_history": true.
   - Resolve implied drug/disease entities from history into the current entities list, PubMed query, and ClinicalTrials parameters.
   - Do NOT override if the user starts a completely new query topic.

8. OUTPUT FORMAT:
   Return ONLY raw valid JSON conforming to the StructuredQuery schema structure without preamble or markdown formatting wrapper. Be very careful to close all objects with curly braces }} and arrays with square brackets ].

JSON SCHEMA STRUCTURE:
{{
  "raw_query": "string",
  "intent": "evidence_retrieval | drug_interaction | clinical_trial | contradiction_check | drug_comparison | general_summary",
  "entities": [
    {{
      "entity_text": "string",
      "entity_type": "Drug | Disease | Gene | Protein | Outcome | Population | Procedure",
      "canonical_name": "string",
      "mesh_id": "string or null",
      "umls_cui": "string or null",
      "confidence": 1.0
    }}
  ],
  "expanded_terms": {{
    "canonical_name": ["synonym1", "synonym2"]
  }},
  "temporal_filter": {{
    "from_year": 1990,
    "to_year": 2026,
    "recency_bias": true
  }},
  "comparison_mode": false,
  "comparison_entities": ["string"],
  "pubmed_query_string": "string",
  "clinicaltrials_params": {{
    "condition": "string",
    "intervention": "string"
  }},
  "is_followup": false,
  "resolved_from_history": false
}}

CONVERSATION HISTORY:
{history_json}

USER PREFERENCES:
{preferences_json}

CURRENT QUERY:
"{raw_query}"
"""

class QueryUnderstandingAgent:
    """Agent 1: Query Understanding Agent (QUA).
    Transforms natural language pharmaceutical research queries into StructuredQuery objects.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        self.gemini = gemini_service or GeminiService()

    async def process(
        self,
        raw_query: str,
        session_context: Optional[Dict[str, Any]] = None
    ) -> StructuredQuery:
        start_time = time.perf_counter()

        if not raw_query or not raw_query.strip():
            raise ValueError("Raw query cannot be empty.")

        query_str = raw_query.strip()
        session_context = session_context or {}
        history = session_context.get("conversation_history", [])
        preferences = session_context.get("user_preferences", {})

        history_json = json.dumps(history, indent=2) if history else "[]"
        preferences_json = json.dumps(preferences, indent=2) if preferences else "{}"

        prompt = QUA_SYSTEM_PROMPT.format(
            raw_query=query_str,
            history_json=history_json,
            preferences_json=preferences_json
        )

        try:
            raw_response = self.gemini.generate_json(prompt)
        except Exception as exc:
            logger.error(f"Gemini API call failed in QUA: {exc}")
            raise RuntimeError(f"QUA failed to contact Gemini API: {exc}") from exc

        parsed_data = self._clean_and_parse_json(raw_response)

        # Force raw_query to match original input
        parsed_data["raw_query"] = query_str

        # Measure processing time
        end_time = time.perf_counter()
        processing_time_ms = int((end_time - start_time) * 1000)
        parsed_data["processing_time_ms"] = processing_time_ms

        try:
            structured_query = StructuredQuery(**parsed_data)
            return structured_query
        except Exception as exc:
            logger.error(f"Failed to validate StructuredQuery schema: {exc}. Raw JSON: {parsed_data}")
            raise ValueError(f"QUA model validation error: {exc}") from exc

    def _clean_and_parse_json(self, raw_text: str) -> Dict[str, Any]:
        if not raw_text or not raw_text.strip():
            raise ValueError("Gemini returned empty response text.")

        text = raw_text.strip()
        # Remove potential markdown fences ```json ... ``` or ``` ... ```
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
            text = text.strip()

        try:
            data = json.loads(text)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        # Robust repair logic for common LLM JSON syntax issues
        # Fix 1: Trailing commas before } or ]
        repaired = re.sub(r",\s*([\}\]])", r"\1", text)
        # Fix 2: Object closing bracket mismatch: { ... ], -> { ... },
        repaired = re.sub(r"(\{[^{}]*?)\],", r"\1},", repaired, flags=re.DOTALL)

        try:
            data = json.loads(repaired)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError as exc:
            logger.error(f"JSONDecodeError parsing Gemini output: {exc}. Text was:\n{text}")
            raise ValueError(f"Malformed JSON from Gemini API: {exc}") from exc

        raise ValueError("Failed to parse valid JSON object dictionary from response.")
