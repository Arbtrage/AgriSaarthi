import json
from typing import Optional, AsyncGenerator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llama_index.core.llms import ChatMessage
from app.agents.agent_factory import AgentFactory

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    language: str = "en-IN"
    category: str = "crop_info"
    question: str
    markdown: bool = False


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream chat response from the appropriate agricultural agent.

    Args:
        request: ChatRequest containing language, category, question, and markdown preference

    Returns:
        StreamingResponse with the agent's response as plain text or markdown
    """
    try:
        # Create the appropriate agent based on category, language, and markdown preference
        agent = AgentFactory.create_agent(
            category=request.category,
            language=request.language,
            markdown=request.markdown,
        )

        # Get the FunctionAgent from the specialized agent
        function_agent = agent.get_agent()

        async def token_generator() -> AsyncGenerator[bytes, None]:
            try:
                # Use the correct streaming method for FunctionAgent
                # FunctionAgent.run() returns a workflow handler that has stream_events()
                handler = function_agent.run(request.question)

                async for event in handler.stream_events():
                    if hasattr(event, "delta") and event.delta:
                        # Send the token as plain text, encoded as UTF-8 bytes
                        yield event.delta.encode("utf-8")

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                yield error_msg.encode("utf-8")

        # Use text/plain instead of text/event-stream for plain text streaming
        return StreamingResponse(
            token_generator(), media_type="text/plain; charset=utf-8"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Get complete chat response from the appropriate agricultural agent.

    Args:
        request: ChatRequest containing language, category, question, and markdown preference

    Returns:
        Complete response as JSON
    """
    try:
        # Create the appropriate agent based on category, language, and markdown preference
        agent = AgentFactory.create_agent(
            category=request.category,
            language=request.language,
            markdown=request.markdown,
        )

        # Get the FunctionAgent from the specialized agent
        function_agent = agent.get_agent()

        # Run the agent and collect the complete response
        handler = function_agent.run(request.question)

        # Collect all the streaming content into a single response
        accumulated_text = ""
        async for event in handler.stream_events():
            if hasattr(event, "delta") and event.delta:
                accumulated_text += event.delta

        if not accumulated_text:
            accumulated_text = "No response content received"

        return accumulated_text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")


@router.get("/agents/categories")
async def get_agent_categories():
    """Get available agent categories and their descriptions."""
    categories = AgentFactory.get_available_categories()
    descriptions = {}

    for category in categories:
        descriptions[category] = AgentFactory.get_agent_description(category)

    # Highlight the primary categories
    primary_categories = [
        "crop_info",
        "fertilizers",
        "market_prices",
        "gov_schemes",
        "other",
    ]

    return {
        "primary_categories": primary_categories,
        "all_categories": categories,
        "descriptions": descriptions,
        "total_count": len(categories),
    }


@router.get("/health")
async def health_check():
    """Health check endpoint for the chat service."""
    return {
        "status": "healthy",
        "service": "AgriSaarthi Chat API",
        "available_categories": len(AgentFactory.get_available_categories()),
        "primary_categories": [
            "crop_info",
            "fertilizers",
            "market_prices",
            "gov_schemes",
            "other",
        ],
    }


# Keep the old endpoint for backward compatibility
@router.post("/chat/stream/legacy")
async def chat_stream_legacy(
    message: str, namespace: Optional[str] = None, markdown: bool = False
):
    """Legacy endpoint for backward compatibility."""
    from app.agents.agent import build_agent

    agent = build_agent(namespace=namespace, markdown=markdown)

    async def token_generator() -> AsyncGenerator[bytes, None]:
        try:
            # Use the correct streaming method for FunctionAgent
            # FunctionAgent.run() returns a workflow handler that has stream_events()
            handler = agent.run(message)

            async for event in handler.stream_events():
                if hasattr(event, "delta") and event.delta:
                    # Send the token as plain text, encoded as UTF-8 bytes
                    yield event.delta.encode("utf-8")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            yield error_msg.encode("utf-8")

    # Use text/plain instead of text/event-stream for plain text streaming
    return StreamingResponse(token_generator(), media_type="text/plain; charset=utf-8")
