#!/usr/bin/env python3
"""
Test script for Tavily web search integration
"""

import asyncio
import json
import os
from app.agents.tools import build_web_search_tool


async def test_tavily_search():
    """Test the Tavily web search tool"""

    # Check if API key is set
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ TAVILY_API_KEY environment variable not set")
        print("Please set it with: export TAVILY_API_KEY='your_api_key_here'")
        return

    print("✅ TAVILY_API_KEY found")

    # Build the web search tool
    web_search_tool = build_web_search_tool()
    print(f"✅ Web search tool created: {web_search_tool.name}")
    print(f"📝 Description: {web_search_tool.description}")

    # Test search
    print("\n🔍 Testing web search...")
    try:
        result = await web_search_tool.fn(
            query="latest agricultural technology trends 2024",
            search_depth="basic",
            max_results=3,
        )

        # Parse and display results
        parsed_result = json.loads(result)

        if "error" in parsed_result:
            print(f"❌ Error: {parsed_result['error']}")
        else:
            print(
                f"✅ Search successful! Found {parsed_result.get('total_results', 0)} results"
            )
            print(f"📊 Source: {parsed_result.get('source')}")
            print(f"🔎 Query: {parsed_result.get('query')}")

            print("\n📋 Results:")
            for i, result_item in enumerate(parsed_result.get("results", []), 1):
                if not result_item.startswith("Search performed using Tavily"):
                    print(f"\n{i}. {result_item}")

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")


if __name__ == "__main__":
    print("🧪 Testing Tavily Web Search Integration")
    print("=" * 50)

    asyncio.run(test_tavily_search())
