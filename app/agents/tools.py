import json
import requests
from typing import List, Dict, Any, Optional
from llama_index.core.tools import FunctionTool
from app.core.llm import get_embed_model
from app.core.qdrant_client import search_similar
from app.core.config import get_settings
from tavily import TavilyClient


def build_vector_search_tool(namespace: Optional[str] = None) -> FunctionTool:
    async def vector_search(query: str, top_k: int = 5) -> str:
        # Use direct Qdrant search
        results = await search_similar(query, top_k=top_k, namespace=namespace)
        return json.dumps(results)

    return FunctionTool.from_defaults(
        fn=vector_search,
        name="knowledge_base_search",
        description="Search the knowledge base for relevant agricultural information and context.",
    )


def build_web_search_tool() -> FunctionTool:
    async def web_search(
        query: str, search_depth: str = "basic", max_results: int = 5
    ) -> str:
        """Search the web for current agricultural information and news using Tavily."""
        try:
            settings = get_settings()
            if not settings.tavily_api_key:
                return json.dumps(
                    {
                        "error": "Tavily API key not configured. Please set TAVILY_API_KEY environment variable."
                    }
                )

            # Initialize Tavily client
            tavily_client = TavilyClient(api_key=settings.tavily_api_key)

            # Perform web search with agricultural context
            search_result = tavily_client.search(
                query=query,
                search_depth=search_depth,  # "basic" or "advanced"
                max_results=max_results,
                include_answer=True,
                include_raw_content=False,
                include_images=False,
            )

            # Extract and format results
            results = []

            # Add answer if available
            if search_result.get("answer"):
                results.append(f"Answer: {search_result['answer']}")

            # Add search results
            if search_result.get("results"):
                for i, result in enumerate(search_result["results"][:max_results], 1):
                    title = result.get("title", "No title")
                    content = result.get("content", "No content")
                    url = result.get("url", "No URL")

                    result_text = f"{i}. {title}\n   Content: {content[:200]}...\n   Source: {url}"
                    results.append(result_text)

            # Add source information
            results.append(f"\nSearch performed using Tavily. Query: '{query}'")

            return json.dumps(
                {
                    "results": results,
                    "source": "tavily_web_search",
                    "query": query,
                    "total_results": len(results) - 1,  # Exclude the source info line
                }
            )

        except Exception as e:
            return json.dumps(
                {"error": f"Web search error: {str(e)}", "source": "tavily_web_search"}
            )

    return FunctionTool.from_defaults(
        fn=web_search,
        name="web_search",
        description="Search the web for current agricultural information, market prices, weather updates, and news using Tavily. Accepts query string, search_depth (basic/advanced), and max_results (default 5).",
    )
