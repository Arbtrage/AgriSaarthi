import json
import requests
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
        name="knowledge_base_search",
        description="Search the knowledge base for relevant agricultural information and context.",
    )


def build_web_search_tool() -> FunctionTool:
    async def web_search(query: str) -> str:
        """Search the web for current agricultural information and news."""
        try:
            # This is a placeholder - you'll need to implement actual web search
            # You could use DuckDuckGo, Google Custom Search, or other APIs
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Extract relevant information from DuckDuckGo response
                results = []
                if data.get("Abstract"):
                    results.append(f"Summary: {data['Abstract']}")
                if data.get("RelatedTopics"):
                    for topic in data["RelatedTopics"][:3]:
                        if isinstance(topic, dict) and topic.get("Text"):
                            results.append(f"Related: {topic['Text']}")
                return json.dumps({"results": results, "source": "web_search"})
            else:
                return json.dumps(
                    {"error": "Web search failed", "status": response.status_code}
                )
        except Exception as e:
            return json.dumps({"error": f"Web search error: {str(e)}"})

    return FunctionTool.from_defaults(
        fn=web_search,
        name="web_search",
        description="Search the web for current agricultural information, market prices, weather updates, and news.",
    )
