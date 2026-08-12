import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "pharmalyx"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Google Gemini Configuration (google-genai SDK)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # External APIs
    PUBMED_API_KEY: str = ""
    PUBMED_BASE_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    CLINICALTRIALS_BASE_URL: str = "https://clinicaltrials.gov/api/v2"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
