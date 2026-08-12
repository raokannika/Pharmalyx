import os
from google import genai
from google.genai import types
from app.core.config import settings

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
