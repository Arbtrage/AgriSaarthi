import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    google_api_key: Optional[str]
    gemini_model: str
    embed_model_name: str

    qdrant_url: Optional[str]
    qdrant_api_key: Optional[str]
    qdrant_collection: str

    tavily_api_key: Optional[str]

    @staticmethod
    def load() -> "Settings":
        return Settings(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            embed_model_name=os.getenv("EMBED_MODEL_NAME", "text-embedding-004"),
            qdrant_url=os.getenv("QDRANT_URL"),
            qdrant_api_key=os.getenv("QDRANT_API_KEY"),
            qdrant_collection="argisathi",
            tavily_api_key=os.getenv("TAVILY_API_KEY"),
        )


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings
