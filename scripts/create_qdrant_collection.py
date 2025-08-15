#!/usr/bin/env python3
"""
Script to create Qdrant collection for RAG application.
This script sets up the necessary collection structure for storing document embeddings.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to Python path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import after loading environment variables
from app.core.qdrant_client import create_collection, get_qdrant_client


async def main():
    """Create Qdrant collection with proper schema"""
    print("Setting up Qdrant collection for RAG application...")

    # Check required environment variables
    required_vars = ["QDRANT_URL", "QDRANT_COLLECTION"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please set these in your .env file:")
        for var in missing_vars:
            print(f"  {var}=your_value")
        return

    try:
        # Test Qdrant connection
        print("Testing Qdrant connection...")
        await get_qdrant_client()
        print("✓ Connected to Qdrant successfully")

        # Create collection
        collection_name = os.getenv("QDRANT_COLLECTION", "rag_documents")
        await create_collection(collection_name)
        print(f"✓ Collection '{collection_name}' created successfully")

        print("\n🎉 Qdrant collection setup completed!")
        print(f"Collection name: {collection_name}")

    except Exception as e:
        print(f"❌ Error setting up Qdrant collection: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
