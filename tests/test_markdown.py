#!/usr/bin/env python3
"""
Test script to verify markdown functionality in agents.
"""

from app.agents.agent_factory import AgentFactory


def test_markdown_functionality():
    """Test that agents handle markdown parameter correctly."""
    print("Testing Markdown Functionality...")
    print("=" * 50)

    test_categories = ["crop_info", "fertilizers", "market_prices"]

    for category in test_categories:
        print(f"\n🔍 Testing {category} agent...")

        # Test with markdown=False (plain text)
        try:
            agent_plain = AgentFactory.create_agent(category, "en-US", markdown=False)
            print(f"✅ Created {category} agent with markdown=False")

            # Check if the agent has the markdown attribute
            assert hasattr(
                agent_plain, "markdown"
            ), f"{category} agent missing markdown attribute"
            assert (
                agent_plain.markdown == False
            ), f"{category} agent markdown attribute should be False"

            # Check if the system prompt contains plain text instruction
            system_prompt = agent_plain.system_prompt
            assert (
                "plain text only" in system_prompt.lower()
            ), f"{category} agent should have plain text instruction"
            assert (
                "text-to-speech" in system_prompt.lower()
            ), f"{category} agent should mention text-to-speech"

        except Exception as e:
            print(f"❌ Failed to test {category} agent with markdown=False: {e}")
            continue

        # Test with markdown=True
        try:
            agent_markdown = AgentFactory.create_agent(category, "en-US", markdown=True)
            print(f"✅ Created {category} agent with markdown=True")

            # Check if the agent has the markdown attribute
            assert hasattr(
                agent_markdown, "markdown"
            ), f"{category} agent missing markdown attribute"
            assert (
                agent_markdown.markdown == True
            ), f"{category} agent markdown attribute should be True"

            # Check if the system prompt contains markdown instruction
            system_prompt = agent_markdown.system_prompt
            assert (
                "proper markdown" in system_prompt.lower()
            ), f"{category} agent should have markdown instruction"
            assert (
                "headers" in system_prompt.lower()
            ), f"{category} agent should mention markdown headers"

        except Exception as e:
            print(f"❌ Failed to test {category} agent with markdown=True: {e}")
            continue

        # Test confidence instruction
        try:
            system_prompt = agent_plain.system_prompt
            assert (
                "never say" in system_prompt.lower()
            ), f"{category} agent should have confidence instruction"
            assert (
                "i don't know" in system_prompt.lower()
            ), f"{category} agent should mention not saying 'I don't know'"
            assert (
                "i'm not confident" in system_prompt.lower()
            ), f"{category} agent should mention not saying 'I'm not confident'"
            print(f"✅ {category} agent has proper confidence instructions")

        except Exception as e:
            print(
                f"❌ Failed to verify confidence instructions for {category} agent: {e}"
            )
            continue

    print("\n" + "=" * 50)
    print("✅ Markdown functionality test completed!")


def test_language_markdown_combination():
    """Test markdown functionality with different languages."""
    print("\nTesting Language + Markdown Combinations...")
    print("=" * 50)

    languages = ["en-US", "hi-IN", "pa-IN"]
    category = "crop_info"

    for language in languages:
        for markdown in [False, True]:
            try:
                agent = AgentFactory.create_agent(category, language, markdown=markdown)
                print(
                    f"✅ Created {category} agent with {language} and markdown={markdown}"
                )

                # Verify both attributes are set correctly
                assert (
                    agent.language == language
                ), f"Language mismatch: expected {language}, got {agent.language}"
                assert (
                    agent.markdown == markdown
                ), f"Markdown mismatch: expected {markdown}, got {agent.markdown}"

            except Exception as e:
                print(
                    f"❌ Failed to create {category} agent with {language} and markdown={markdown}: {e}"
                )


if __name__ == "__main__":
    test_markdown_functionality()
    test_language_markdown_combination()
