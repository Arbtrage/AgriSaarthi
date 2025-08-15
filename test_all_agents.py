#!/usr/bin/env python3
"""
Test script to verify all required agents are working correctly.
"""

from app.agents.agent_factory import AgentFactory


def test_agent_categories():
    """Test that all required agent categories are available."""
    print("Testing Agent Categories...")
    print("=" * 50)

    # Required categories
    required_categories = [
        "crop_info",
        "fertilizers",
        "market_prices",
        "gov_schemes",
        "other",
    ]

    # Get available categories from factory
    available_categories = AgentFactory.get_available_categories()

    print(f"Available categories: {len(available_categories)}")
    print(f"Required categories: {len(required_categories)}")
    print()

    # Check each required category
    for category in required_categories:
        if category in available_categories:
            print(f"✅ {category}: Available")
            # Test agent creation
            try:
                agent = AgentFactory.create_agent(category, "en-US")
                description = AgentFactory.get_agent_description(category)
                print(f"   Description: {description}")
                print(f"   Agent Type: {type(agent).__name__}")
            except Exception as e:
                print(f"   ❌ Error creating agent: {e}")
        else:
            print(f"❌ {category}: Missing")
        print()

    # Show all available categories
    print("All available categories:")
    for i, category in enumerate(available_categories, 1):
        print(f"  {i}. {category}")

    print("\n" + "=" * 50)

    # Test agent creation for each required category
    print("Testing Agent Creation...")
    print("=" * 50)

    for category in required_categories:
        try:
            agent = AgentFactory.create_agent(category, "en-US")
            print(f"✅ Successfully created {category} agent: {type(agent).__name__}")

            # Test agent methods
            if hasattr(agent, "get_agent_description"):
                desc = agent.get_agent_description()
                print(f"   Description: {desc}")

            if hasattr(agent, "get_specialized_tools"):
                tools = agent.get_specialized_tools()
                print(f"   Tools: {tools}")

        except Exception as e:
            print(f"❌ Failed to create {category} agent: {e}")
        print()


if __name__ == "__main__":
    test_agent_categories()
