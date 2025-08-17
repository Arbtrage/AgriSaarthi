from typing import Optional
from llama_index.core.agent import FunctionAgent
from app.core.llm import get_llm
from app.agents.tools import build_vector_search_tool


def build_agent(
    namespace: Optional[str] = None, markdown: bool = False
) -> FunctionAgent:
    markdown_instruction = _get_markdown_instruction(markdown)
    confidence_instruction = _get_confidence_instruction()

    system_prompt = f"""You are a helpful assistant that uses the vector_search tool to ground answers. 
If using retrieved text, cite the 'source' fields from metadata.

{markdown_instruction}

{confidence_instruction}"""

    tool = build_vector_search_tool(namespace=namespace)
    agent = FunctionAgent(
        tools=[tool],
        llm=get_llm(),
        system_prompt=system_prompt,
    )
    return agent


def _get_markdown_instruction(markdown: bool) -> str:
    """Get markdown formatting instruction based on the markdown preference."""
    if markdown:
        return """IMPORTANT: Format your response in proper markdown. Use appropriate markdown syntax for:
- Headers (##, ###)
- Lists (bullet points and numbered lists)
- Bold and italic text (**bold**, *italic*)
- Code blocks when sharing technical information
- Tables when presenting structured data
- Links when referencing sources
- Blockquotes for important notes or warnings

Ensure your response is well-structured and readable with proper markdown formatting."""
    else:
        return """IMPORTANT: Provide your answer in plain text only. Do NOT use any special characters, markdown formatting, or symbols. 
Your response will be used for text-to-speech, so it must be clean, simple text that can be easily spoken aloud.
Avoid using:
- Markdown syntax (##, **, *, etc.)
- Special characters or symbols
- Complex formatting
- Tables or structured layouts

Keep the response in simple, clear sentences that flow naturally when spoken."""


def _get_confidence_instruction() -> str:
    """Get confidence instruction to ensure the agent provides confident responses."""
    return """CRITICAL: You must ALWAYS provide a confident answer to the user's question. 

NEVER say:
- "I don't know"
- "I'm not confident"
- "I couldn't find any sources"
- "I don't have enough information"
- "I'm not sure"
- "I didn't find anything"

Instead, use your knowledge and expertise to provide the best possible answer. If you don't find specific sources, draw from your general knowledge and provide practical, actionable advice. Always be confident and helpful, even if you need to make reasonable assumptions based on best practices.

Your goal is to be a knowledgeable, confident advisor who always provides valuable guidance."""
