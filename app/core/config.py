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

    milvus_uri: Optional[str]
    milvus_token: Optional[str]
    milvus_collection: str

    @staticmethod
    def load() -> "Settings":
        return Settings(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            embed_model_name=os.getenv("EMBED_MODEL_NAME", "text-embedding-004"),
            milvus_uri=os.getenv("MILVUS_URI"),
            milvus_token=os.getenv("MILVUS_TOKEN"),
            milvus_collection=os.getenv("MILVUS_COLLECTION", "rag_documents"),
        )


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings
