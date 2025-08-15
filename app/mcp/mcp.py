from fastmcp import FastMCP
from app.core.qdrant_client import search_similar
import json

mcp = FastMCP(name="Agents MCP Server", port=3005)


@mcp.tool(
    name="search_knowledgebase",
    description="Search the knowledgebase for a given query.",
)
async def search_knowledgebase(query: str) -> str:
    results = await search_similar(query, top_k=5)
    return json.dumps(results)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
