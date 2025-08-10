#!/usr/bin/env python3
"""
Script to create Milvus collection for RAG application.
Run this script to set up the collection before using the RAG service.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the parent directory to Python path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from app.core.milvus_client import create_collection, get_milvus_client
from app.core.llm import get_embedding_dimension

load_dotenv()


async def main():
    """Create Milvus collection with proper schema"""
    print("Setting up Milvus collection for RAG application...")

    # Check environment variables
    required_vars = ["MILVUS_URI", "MILVUS_COLLECTION"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Error: Missing required environment variables: {missing_vars}")
        print("Please set them in your .env file")
        sys.exit(1)

    try:
        # Test connection
        print("Testing Milvus connection...")
        await get_milvus_client()
        print("✓ Connected to Milvus successfully")

        # Get collection name from environment
        collection_name = os.getenv("MILVUS_COLLECTION", "rag_documents")

        # Get embedding dimension from the model
        print("Getting embedding model dimension...")
        dimension = get_embedding_dimension()
        print(f"✓ Embedding dimension: {dimension}")

        # Create collection
        print(f"Creating collection '{collection_name}'...")
        collection = await create_collection(collection_name, dimension)

        print(f"\n✓ Collection '{collection_name}' created successfully!")
        print(f"✓ Vector dimension: {dimension}")
        print(f"✓ Simplified schema: embedding, text, metadata")
        print(f"✓ Index created for 'embedding' field with COSINE similarity")
        print(
            f"\nYou can now run the RAG service with: uv run uvicorn main:app --reload"
        )

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
