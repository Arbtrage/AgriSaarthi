import os
from typing import Optional
from app.core.config import get_settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

_llm: Optional[GoogleGenAI] = None
_embed_model: Optional[GoogleGenAIEmbedding] = None


def get_llm() -> GoogleGenAI:
    global _llm
    if _llm is None:
        settings = get_settings()
        if settings.google_api_key:
            os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)
        _llm = GoogleGenAI(model=settings.gemini_model)
    return _llm


def get_embed_model() -> GoogleGenAIEmbedding:
    global _embed_model
    if _embed_model is None:
        settings = get_settings()
        if settings.google_api_key:
            os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)
        _embed_model = GoogleGenAIEmbedding(model_name=settings.embed_model_name)
    return _embed_model


def get_embedding_dimension() -> int:
    """Get the embedding dimension from the model"""
    embed_model = get_embed_model()
    # Google GenAI embeddings typically have 768 dimensions
    # This is a fallback if the model doesn't expose embed_dim
    return getattr(embed_model, "embed_dim", 768)
