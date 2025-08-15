# Migration from Milvus to Qdrant Cloud

This document outlines the changes made to migrate the AgriSaarthi project from Milvus to Qdrant Cloud.

## Overview of Changes

The project has been completely migrated from using Milvus (local or Zilliz Cloud) to Qdrant Cloud for vector storage and similarity search.

## Files Modified

### 1. Dependencies (`pyproject.toml`)

- **Removed**: `pymilvus>=2.6.0`
- **Added**: `qdrant-client>=1.7.0`
- **Updated**: Project description to reflect Qdrant instead of Milvus

### 2. Configuration (`app/core/config.py`)

- **Removed**: `milvus_uri`, `milvus_token`, `milvus_collection`
- **Added**: `qdrant_url`, `qdrant_api_key`, `qdrant_collection`

### 3. Vector Client (`app/core/milvus_client.py` → `app/core/qdrant_client.py`)

- **Renamed**: File from `milvus_client.py` to `qdrant_client.py`
- **Replaced**: All Milvus-specific code with Qdrant equivalents
- **Updated**: Function implementations to use Qdrant client API
- **Maintained**: Same function signatures for backward compatibility

### 4. Vector Store (`app/core/vector_store.py`)

- **Replaced**: `MilvusVectorStore` with `QdrantVectorStore`
- **Updated**: Configuration parameters to use Qdrant settings

### 5. API Routes (`app/api/routers/ingest.py`)

- **Updated**: Import statement to use new Qdrant client
- **Updated**: Comment to reflect Qdrant instead of Milvus

### 6. Agent Tools (`app/agents/tools.py`)

- **Updated**: Import statement to use new Qdrant client
- **Updated**: Comment to reflect Qdrant instead of Milvus

### 7. MCP Integration (`app/mcp/mcp.py`)

- **Updated**: Import statement to use new Qdrant client

### 8. Collection Creation Script (`scripts/create_milvus_collection.py` → `scripts/create_qdrant_collection.py`)

- **Renamed**: File from `create_milvus_collection.py` to `create_qdrant_collection.py`
- **Updated**: All Milvus references to Qdrant
- **Updated**: Environment variable requirements
- **Simplified**: Collection creation logic

### 9. Docker Configuration (`docker-compose.yml`)

- **Removed**: All Milvus-related services (etcd, minio, standalone)
- **Added**: Comments explaining the change to Qdrant Cloud

### 10. Documentation

- **Updated**: `README.md` - All Milvus references replaced with Qdrant
- **Updated**: `AGENT_SYSTEM_README.md` - Updated tool descriptions

## Environment Variables

### Old (Milvus)

```bash
MILVUS_URI=grpc://your-zilliz-endpoint:19530
MILVUS_TOKEN=your_zilliz_api_key_or_user:pass
MILVUS_COLLECTION=rag_documents
```

### New (Qdrant Cloud)

```bash
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=rag_documents
```

## Key Differences in Implementation

### Collection Creation

- **Milvus**: Required complex schema definition with field types and index parameters
- **Qdrant**: Simplified collection creation with vector configuration only

### Data Insertion

- **Milvus**: Used `insert()` method with row-based data format
- **Qdrant**: Uses `upsert()` method with `PointStruct` objects

### Search Operations

- **Milvus**: Complex search with `anns_field` and `expr` parameters
- **Qdrant**: Simplified search with `query_vector` and optional `query_filter`

### Namespace Filtering

- **Milvus**: Used JSON extraction expressions
- **Qdrant**: Uses structured filters with `FieldCondition` and `MatchValue`

## Benefits of Migration

1. **Simplified Setup**: No need for local infrastructure (etcd, minio, etc.)
2. **Cloud-Native**: Managed service with automatic scaling and maintenance
3. **Better Performance**: Optimized vector search algorithms
4. **Easier Management**: Web-based dashboard for monitoring and management
5. **Reduced Complexity**: Simpler API and configuration

## Migration Steps for Users

1. **Update Environment Variables**: Replace Milvus variables with Qdrant equivalents
2. **Install Dependencies**: Run `uv sync` to install Qdrant client
3. **Create Collection**: Run `uv run python scripts/create_qdrant_collection.py`
4. **Test Functionality**: Verify that document ingestion and search work correctly

## Backward Compatibility

The migration maintains the same function signatures and API endpoints, ensuring that existing code continues to work with minimal changes. Only the underlying vector database implementation has changed.

## Notes

- The old Milvus client file has been completely removed
- Docker services are no longer needed for local development
- All documentation has been updated to reflect the new architecture
- The migration preserves the existing RAG functionality while improving the infrastructure
