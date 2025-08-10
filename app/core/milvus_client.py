import json
import time
from typing import List, Dict, Any, Optional
from pymilvus import MilvusClient, DataType
from app.core.config import get_settings
from app.core.llm import get_embedding_dimension

_milvus_client = None


async def get_milvus_client():
    global _milvus_client
    if _milvus_client is None:
      

        # Create MilvusClient with URI and token
        _milvus_client = MilvusClient(
            host="localhost", port=19530,alias="default"
        )

    return _milvus_client


async def create_collection(collection_name: str, dimension: int = 768):
    """Create Milvus collection with simplified schema for RAG documents"""
    milvus_client = await get_milvus_client()

    # Check if collection exists and drop it
    if milvus_client.has_collection(collection_name):
        milvus_client.drop_collection(collection_name)
        print(f"Dropped existing collection {collection_name}")

    print(f"Creating collection schema for {collection_name}")
    schema = milvus_client.create_schema()
    schema.add_field(
        "id", DataType.INT64, is_primary=True, auto_id=True, description="Primary key"
    )
    schema.add_field(
        "embedding",
        DataType.FLOAT_VECTOR,
        dim=dimension,
        description="Document embedding",
    )
    schema.add_field(
        "text", DataType.VARCHAR, max_length=65535, description="Document text"
    )
    schema.add_field(
        "metadata",
        DataType.VARCHAR,
        max_length=65535,
        description="Document metadata as JSON",
    )

    print("Preparing index parameters")
    index_params = milvus_client.prepare_index_params()
    index_params.add_index("embedding", metric_type="COSINE")

    print(f"Creating collection: {collection_name}")
    milvus_client.create_collection(
        collection_name, schema=schema, index_params=index_params
    )

    collection_property = milvus_client.describe_collection(collection_name)
    print(f"Collection created successfully: {collection_property}")

    return collection_name


async def get_collection(collection_name: str) -> str:
    """Get existing collection or create if doesn't exist"""
    milvus_client = await get_milvus_client()

    if milvus_client.has_collection(collection_name):
        print(f"Collection '{collection_name}' already exists")
        return collection_name
    else:
        # Get embedding dimension from the model
        dimension = get_embedding_dimension()
        return await create_collection(collection_name, dimension)


async def insert_documents(
    texts: List[str],
    metadatas: List[Dict[str, Any]],
):
    """Insert documents directly into Milvus with simplified schema"""
    settings = get_settings()
    collection_name = await get_collection(settings.milvus_collection)
    milvus_client = await get_milvus_client()

    # Generate embeddings
    from app.core.llm import get_embed_model

    embed_model = get_embed_model()
    embeddings = embed_model.get_text_embedding_batch(texts)

    # Prepare data for insertion using MilvusClient format
    rows = []
    for i, (text, metadata, embedding) in enumerate(zip(texts, metadatas, embeddings)):
        rows.append(
            {"text": text, "metadata": json.dumps(metadata), "embedding": embedding}
        )

    print(f"Inserting {len(texts)} entities into collection '{collection_name}'")

    # Insert data
    t0 = time.time()
    milvus_client.insert(collection_name, rows)
    insert_time = time.time() - t0

    print(f"Insert completed in {round(insert_time, 4)} seconds")

    # Flush to ensure data is persisted
    print("Flushing collection...")
    flush_start = time.time()
    milvus_client.flush(collection_name)
    flush_time = time.time() - flush_start
    print(f"Flush completed in {round(flush_time, 4)} seconds")

    print(f"Successfully inserted {len(texts)} documents")


async def get_collection_stats(collection_name: str = None):
    """Get collection statistics to verify data insertion"""
    settings = get_settings()
    if collection_name is None:
        collection_name = settings.milvus_collection

    milvus_client = await get_milvus_client()

    if not milvus_client.has_collection(collection_name):
        print(f"Collection '{collection_name}' does not exist")
        return None

    # Get collection statistics
    collection_property = milvus_client.describe_collection(collection_name)
    print(f"Collection '{collection_name}' details:")
    print(f"  - Schema: {collection_property}")

    return collection_property


async def search_similar(
    query: str, top_k: int = 5, namespace: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for similar documents using vector similarity"""
    settings = get_settings()
    collection_name = await get_collection(settings.milvus_collection)
    milvus_client = await get_milvus_client()

    # Generate query embedding
    from app.core.llm import get_embed_model

    embed_model = get_embed_model()
    query_embedding = embed_model.get_text_embedding(query)

    print(f"Searching for similar documents with query: {query[:50]}...")

    t0 = time.time()
    try:
        # Perform search with different approaches based on namespace
        if namespace:
            # Search with namespace filtering
            search_expr = f'JSON_EXTRACT(metadata, "$.namespace") == "{namespace}"'
            results = milvus_client.search(
                collection_name,
                data=[query_embedding],
                limit=top_k,
                anns_field="embedding",
                expr=search_expr,
                output_fields=["text", "metadata"],
            )
        else:
            # Search without namespace filtering (no expr parameter)
            results = milvus_client.search(
                collection_name,
                data=[query_embedding],
                limit=top_k,
                anns_field="embedding",
                output_fields=["text", "metadata"],
            )

        search_time = time.time() - t0

        # Format results
        formatted_results = []
        for hits in results:
            for hit in hits:
                metadata = json.loads(hit.get("metadata", "{}"))
                formatted_results.append(
                    {
                        "text": hit.get("text"),
                        "score": hit.get("score"),
                        "metadata": metadata,
                    }
                )

        print(f"Search completed in {round(search_time, 4)} seconds")
        print(f"Found {len(formatted_results)} results")
        return formatted_results

    except Exception as e:
        print(f"Error during search: {str(e)}")
        # Fallback: try without any expr parameter
        try:
            print("Attempting fallback search without expr parameter...")
            results = milvus_client.search(
                collection_name,
                data=[query_embedding],
                limit=top_k,
                anns_field="embedding",
                output_fields=["text", "metadata"],
            )

            # Format results
            formatted_results = []
            for hits in results:
                for hit in hits:
                    metadata = json.loads(hit.get("metadata", "{}"))
                    formatted_results.append(
                        {
                            "text": hit.get("text"),
                            "score": hit.get("score"),
                            "metadata": metadata,
                        }
                    )

            print(f"Fallback search completed successfully")
            print(f"Found {len(formatted_results)} results")
            return formatted_results

        except Exception as fallback_error:
            print(f"Fallback search also failed: {str(fallback_error)}")
            raise e  # Re-raise the original error
