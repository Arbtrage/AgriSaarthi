#!/usr/bin/env python3
"""
Test script for the AgriSaarthi modular agent system.
This script tests the creation and basic functionality of all agents.
"""

import asyncio
import json
from app.agents.agent_factory import AgentFactory
from app.agents.base_agent import BaseAgent


def test_agent_creation():
    """Test that all agents can be created successfully."""
    print("Testing agent creation...")

    # Test categories
    categories = AgentFactory.get_available_categories()
    print(f"Available categories: {categories}")

    # Test agent creation for each category
    for category in [
        "weather_info",
        "crop_info",
        "market_info",
        "finance_info",
        "soil_info",
    ]:
        try:
            agent = AgentFactory.create_agent(category=category, language="en-US")
            print(f"✓ Successfully created {category} agent")

            # Verify it's a BaseAgent instance
            assert isinstance(
                agent, BaseAgent
            ), f"{category} agent is not a BaseAgent instance"

            # Verify it has the required methods
            assert hasattr(
                agent, "get_agent"
            ), f"{category} agent missing get_agent method"
            assert hasattr(
                agent, "language"
            ), f"{category} agent missing language attribute"

        except Exception as e:
            print(f"✗ Failed to create {category} agent: {e}")
            return False

    return True


def test_language_support():
    """Test that agents support different languages."""
    print("\nTesting language support...")

    languages = ["en-US", "hi-IN", "pa-IN"]
    category = "crop_info"

    for language in languages:
        try:
            agent = AgentFactory.create_agent(category=category, language=language)
            print(f"✓ Successfully created {category} agent with language {language}")

            # Verify language is set correctly
            assert (
                agent.language == language
            ), f"Language mismatch: expected {language}, got {agent.language}"

        except Exception as e:
            print(f"✗ Failed to create {category} agent with language {language}: {e}")
            return False

    return True


def test_agent_descriptions():
    """Test that agent descriptions are available."""
    print("\nTesting agent descriptions...")

    for category in [
        "weather_info",
        "crop_info",
        "market_info",
        "finance_info",
        "soil_info",
    ]:
        try:
            description = AgentFactory.get_agent_description(category)
            print(f"✓ {category}: {description}")

            # Verify description is not empty
            assert description, f"Empty description for {category}"

        except Exception as e:
            print(f"✗ Failed to get description for {category}: {e}")
            return False

    return True


def test_unknown_category():
    """Test that unknown categories fall back to default agent."""
    print("\nTesting unknown category handling...")

    try:
        agent = AgentFactory.create_agent(category="unknown_category", language="en-US")
        print("✓ Successfully handled unknown category with fallback")

        # Should default to CropScienceAgent
        assert "CropScienceAgent" in str(
            type(agent)
        ), "Did not fall back to CropScienceAgent"

    except Exception as e:
        print(f"✗ Failed to handle unknown category: {e}")
        return False

    return True


async def main():
    """Run all tests."""
    print("🧪 AgriSaarthi Agent System Test Suite")
    print("=" * 50)

    tests = [
        ("Agent Creation", test_agent_creation),
        ("Language Support", test_language_support),
        ("Agent Descriptions", test_agent_descriptions),
        ("Unknown Category Handling", test_unknown_category),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The agent system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    exit(0 if success else 1)
