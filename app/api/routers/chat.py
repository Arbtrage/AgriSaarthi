import json
from typing import Optional, AsyncGenerator
from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
from llama_index.core.llms import ChatMessage
from app.agents.agent import build_agent

router = APIRouter()


@router.post("/chat/stream")
async def chat_stream(message: str = Form(...), namespace: Optional[str] = Form(None)):
    agent = build_agent(namespace=namespace)

    async def token_generator() -> AsyncGenerator[bytes, None]:
        try:
            # Use the correct streaming method for FunctionAgent
            # FunctionAgent.run() returns a workflow handler that has stream_events()
            handler = agent.run(message)

            accumulated_text = ""
            async for event in handler.stream_events():
                # Handle different event types
                if hasattr(event, "delta") and event.delta:
                    # This is an AgentStream event with text content
                    accumulated_text += event.delta
                    yield f"data: {event.delta}".encode("utf-8")
                elif hasattr(event, "tool_output") and event.tool_output:
                    # This is a ToolCallResult event
                    tool_content = str(event.tool_output.content)
                    yield f"data: [TOOL] {tool_content}".encode("utf-8")
                elif hasattr(event, "tool_name") and event.tool_name:
                    # This is a ToolCall event
                    yield f"data: [CALLING] {event.tool_name}".encode("utf-8")

            # If no streaming events were received, send a completion message
            if not accumulated_text:
                yield f"data: [COMPLETE] No streaming content received".encode("utf-8")

            yield b"data: [DONE]\n\n"
        except Exception as e:
            err = json.dumps({"error": str(e)})
            yield f"data: {err}\n\n".encode("utf-8")

    return StreamingResponse(token_generator(), media_type="text/event-stream")
