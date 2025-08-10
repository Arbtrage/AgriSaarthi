import json
from typing import Optional
from llama_index.core.tools import FunctionTool
from app.core.milvus_client import search_similar


def build_vector_search_tool(namespace: Optional[str] = None) -> FunctionTool:
    async def vector_search(query: str, top_k: int = 5) -> str:
        # Use direct Milvus search
        results = await search_similar(query, top_k=top_k, namespace=namespace)
        return json.dumps(results)

    return FunctionTool.from_defaults(
        fn=vector_search,
        name="vector_search",
        description="Search the Milvus vector database for relevant context.",
    )
