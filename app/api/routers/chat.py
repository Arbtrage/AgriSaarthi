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

    language: str = "en-US"
    category: str = (
        "crop_info"  # Default to crop_info, other options: fertilizers, market_prices, gov_schemes, other
    )
    question: str


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream chat response from the appropriate agricultural agent.

    Args:
        request: ChatRequest containing language, category, and question

    Returns:
        StreamingResponse with the agent's response
    """
    try:
        # Create the appropriate agent based on category and language
        agent = AgentFactory.create_agent(
            category=request.category, language=request.language
        )

        # Get the FunctionAgent from the specialized agent
        function_agent = agent.get_agent()

        async def token_generator() -> AsyncGenerator[bytes, None]:
            try:
                # Use the correct streaming method for FunctionAgent
                # FunctionAgent.run() returns a workflow handler that has stream_events()
                handler = function_agent.run(request.question)

                accumulated_text = ""
                async for event in handler.stream_events():
                    if hasattr(event, "delta") and event.delta:
                        accumulated_text += event.delta
                        yield f"{event.delta}"
                if not accumulated_text:
                    yield f"[COMPLETE] No streaming content received"

            except Exception as e:
                err = json.dumps({"error": str(e)})
                yield f"data: {err}\n\n".encode("utf-8")

        return StreamingResponse(token_generator(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Get complete chat response from the appropriate agricultural agent.

    Args:
        request: ChatRequest containing language, category, and question

    Returns:
        Complete response as JSON
    """
    try:
        # Create the appropriate agent based on category and language
        agent = AgentFactory.create_agent(
            category=request.category, language=request.language
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
async def chat_stream_legacy(message: str, namespace: Optional[str] = None):
    """Legacy endpoint for backward compatibility."""
    from app.agents.agent import build_agent

    agent = build_agent(namespace=namespace)

    async def token_generator() -> AsyncGenerator[bytes, None]:
        try:
            # Use the correct streaming method for FunctionAgent
            # FunctionAgent.run() returns a workflow handler that has stream_events()
            handler = agent.run(message)

            accumulated_text = ""
            async for event in handler.stream_events():
                if hasattr(event, "delta") and event.delta:
                    accumulated_text += event.delta
                    yield f"{event.delta}"
            if not accumulated_text:
                yield f"[COMPLETE] No streaming content received"

        except Exception as e:
            err = json.dumps({"error": str(e)})
            yield f"data: {err}\n\n".encode("utf-8")

    return StreamingResponse(token_generator(), media_type="text/event-stream")
