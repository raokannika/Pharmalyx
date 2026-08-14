import os
import logging
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from app.core.config import settings

logger = logging.getLogger(__name__)

def _is_rate_limit_error(exc: Exception) -> bool:
    err_str = str(exc).lower()
    return "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str

class GeminiService:
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL

        if not self.api_key:
            self.api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=2, max=15),
        retry=retry_if_exception(_is_rate_limit_error),
        reraise=True
    )
    def generate_text(self, prompt: str, temperature: float = 0.1) -> str:
        if not self.client:
            raise ValueError("GEMINI_API_KEY is not configured in .env.local or environment.")

        config = types.GenerateContentConfig(
            temperature=temperature,
        )
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )
        return response.text

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=2, max=15),
        retry=retry_if_exception(_is_rate_limit_error),
        reraise=True
    )
    def generate_json(self, prompt: str) -> str:
        if not self.client:
            raise ValueError("GEMINI_API_KEY is not configured in .env.local or environment.")

        config = types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
        )
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )
        return response.text
