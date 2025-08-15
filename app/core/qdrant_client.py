import json
import time
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from app.core.config import get_settings
from app.core.llm import get_embedding_dimension

_qdrant_client = None


async def get_qdrant_client():
    global _qdrant_client
    if _qdrant_client is None:
        settings = get_settings()
        if not settings.qdrant_url:
            raise RuntimeError("QDRANT_URL is required in environment")

        # Create QdrantClient with URL and API key
        _qdrant_client = QdrantClient(
            url=settings.qdrant_url, api_key=settings.qdrant_api_key
        )

    return _qdrant_client


async def create_collection(collection_name: str, dimension: int = 768):
    """Create Qdrant collection with simplified schema for RAG documents"""
    qdrant_client = await get_qdrant_client()

    # Check if collection exists and delete it
    try:
        qdrant_client.delete_collection(collection_name)
        print(f"Deleted existing collection {collection_name}")
    except:
        pass

    print(f"Creating collection schema for {collection_name}")

    # Create collection with vector configuration
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
    )

    # Create index on metadata.namespace for filtering
    try:
        qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="metadata.namespace",
            field_schema="keyword",
        )
        print(f"Created index on metadata.namespace field")
    except Exception as e:
        print(f"Warning: Could not create index on metadata.namespace: {e}")

    print(f"Collection created successfully: {collection_name}")
    return collection_name


async def get_collection(collection_name: str) -> str:
    """Get existing collection or create if doesn't exist"""
    qdrant_client = await get_qdrant_client()

    try:
        # Check if collection exists
        collection_info = qdrant_client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists")
        return collection_name
    except:
        # Get embedding dimension from the model
        dimension = get_embedding_dimension()
        return await create_collection(collection_name, dimension)


async def insert_documents(
    texts: List[str],
    metadatas: List[Dict[str, Any]],
):
    """Insert documents directly into Qdrant with simplified schema"""
    settings = get_settings()
    collection_name = await get_collection(settings.qdrant_collection)
    qdrant_client = await get_qdrant_client()

    # Generate embeddings
    from app.core.llm import get_embed_model

    embed_model = get_embed_model()
    embeddings = embed_model.get_text_embedding_batch(texts)

    # Prepare data for insertion using Qdrant format
    points = []
    for i, (text, metadata, embedding) in enumerate(zip(texts, metadatas, embeddings)):
        points.append(
            PointStruct(
                id=i, vector=embedding, payload={"text": text, "metadata": metadata}
            )
        )

    print(f"Inserting {len(texts)} entities into collection '{collection_name}'")

    # Insert data
    t0 = time.time()
    qdrant_client.upsert(collection_name=collection_name, points=points)
    insert_time = time.time() - t0

    print(f"Insert completed in {round(insert_time, 4)} seconds")
    print(f"Successfully inserted {len(texts)} documents")


async def get_collection_stats(collection_name: str = None):
    """Get collection statistics to verify data insertion"""
    settings = get_settings()
    if collection_name is None:
        collection_name = settings.qdrant_collection

    qdrant_client = await get_qdrant_client()

    try:
        # Get collection information
        collection_info = qdrant_client.get_collection(collection_name)
        print(f"Collection '{collection_name}' details:")
        print(f"  - Vectors count: {collection_info.vectors_count}")
        print(f"  - Points count: {collection_info.points_count}")

        # Return a JSON serializable dictionary
        return {
            "collection_name": collection_name,
            "vectors_count": collection_info.vectors_count,
            "points_count": collection_info.points_count,
            "status": str(collection_info.status),
            "optimizers_status": (
                str(collection_info.optimizers_status)
                if hasattr(collection_info, "optimizers_status")
                else None
            ),
            "payload_schema": (
                str(collection_info.payload_schema)
                if hasattr(collection_info, "payload_schema")
                else None
            ),
        }
    except Exception as e:
        print(f"Collection '{collection_name}' does not exist: {e}")
        return None


async def search_similar(
    query: str, top_k: int = 5, namespace: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for similar documents using vector similarity"""
    settings = get_settings()
    collection_name = await get_collection(settings.qdrant_collection)
    qdrant_client = await get_qdrant_client()

    # Generate query embedding
    from app.core.llm import get_embed_model

    embed_model = get_embed_model()
    query_embedding = embed_model.get_text_embedding(query)

    print(f"Searching for similar documents with query: {query[:50]}...")

    t0 = time.time()
    try:
        # Use the correct search method with proper parameters
        search_params = {
            "collection_name": collection_name,
            "query_vector": query_embedding,
            "limit": top_k,
            "with_payload": True,
        }

        # Add namespace filtering if provided
        if namespace:
            search_params["query_filter"] = Filter(
                must=[
                    FieldCondition(
                        key="metadata.namespace", match=MatchValue(value=namespace)
                    )
                ]
            )

        # Perform search using the search method (which is still supported)
        results = qdrant_client.search(**search_params)
        search_time = time.time() - t0

        # Format results
        formatted_results = []
        for hit in results:
            formatted_results.append(
                {
                    "text": hit.payload.get("text"),
                    "score": hit.score,
                    "metadata": hit.payload.get("metadata", {}),
                }
            )

        print(f"Search completed in {round(search_time, 4)} seconds")
        print(f"Found {len(formatted_results)} results")
        return formatted_results

    except Exception as e:
        print(f"Error during search: {str(e)}")
        # If namespace filtering fails, try without it
        if namespace:
            print(f"Namespace filtering failed, trying without namespace filter...")
            try:
                # Remove filter and try again
                search_params.pop("query_filter", None)
                results = qdrant_client.search(**search_params)

                formatted_results = []
                for hit in results:
                    formatted_results.append(
                        {
                            "text": hit.payload.get("text"),
                            "score": hit.score,
                            "metadata": hit.payload.get("metadata", {}),
                        }
                    )

                print(f"Search without namespace filter completed successfully")
                print(f"Found {len(formatted_results)} results")
                return formatted_results

            except Exception as fallback_error:
                print(f"Fallback search also failed: {str(fallback_error)}")

        raise e
