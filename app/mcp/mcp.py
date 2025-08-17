from fastmcp import FastMCP
from app.core.qdrant_client import search_similar
import json
from app.agents.tools import build_web_search_tool

# Create MCP instance
mcp = FastMCP(name="Agents MCP Server")


@mcp.tool(
    name="search_knowledgebase",
    description="Search the knowledgebase for a given query.",
)
async def search_knowledgebase(query: str) -> str:
    try:
        results = await search_similar(query, top_k=5)
        return json.dumps(results)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="web_search",
    description="Search the web for a given query.",
)
async def search_web(query: str) -> str:
    try:
        results = await build_web_search_tool(query)
        return results
    except Exception as e:
        return f"Error performing web search: {str(e)}"


if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http", port=8005)
    except KeyboardInterrupt:
        print("\n🔄 MCP server shutdown requested")
    except Exception as e:
        print(f"❌ MCP server error: {e}")
