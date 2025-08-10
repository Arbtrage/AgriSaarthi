from typing import Optional
from app.core.config import get_settings
from app.core.llm import get_llm, get_embed_model
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext, VectorStoreIndex

_vector_store: Optional[MilvusVectorStore] = None
_storage_context: Optional[StorageContext] = None


def get_vector_store() -> MilvusVectorStore:
    global _vector_store
    if _vector_store is None:
        settings = get_settings()
        if not settings.milvus_uri:
            raise RuntimeError(
                "MILVUS_URI is required in environment (Zilliz Cloud endpoint)"
            )
        _vector_store = MilvusVectorStore(
            uri=settings.milvus_uri,
            token=settings.milvus_token or None,
            collection_name=settings.milvus_collection,
        )
    return _vector_store


def get_storage_context() -> StorageContext:
    global _storage_context
    if _storage_context is None:
        _storage_context = StorageContext.from_defaults(vector_store=get_vector_store())
    return _storage_context


def get_index() -> VectorStoreIndex:
    return VectorStoreIndex.from_vector_store(
        vector_store=get_vector_store(),
        storage_context=get_storage_context(),
        embed_model=get_embed_model(),
        llm=get_llm(),
    )
