from typing import Optional
from llama_index.core.agent import FunctionAgent
from app.core.llm import get_llm
from app.agents.tools import build_vector_search_tool


def build_agent(namespace: Optional[str] = None) -> FunctionAgent:
    system_prompt = (
        "You are a helpful assistant that uses the vector_search tool to ground answers. "
        "If using retrieved text, cite the 'source' fields from metadata."
    )
    tool = build_vector_search_tool(namespace=namespace)
    agent = FunctionAgent(
        tools=[tool],
        llm=get_llm(),
        system_prompt=system_prompt,
    )
    return agent
