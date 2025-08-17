from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.ingest import router as ingest_router
from app.api.routers.chat import router as chat_router
import threading
from app.mcp.mcp import mcp

app = FastAPI(title="AgriSaarthi RAG Service", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
app.include_router(chat_router)


def run_mcp_server():
    """Run the MCP server on port 8005"""
    try:
        print("🚀 Starting MCP server on port 8005...")
        mcp.run(transport="streamable-http", port=8005)
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")


@app.on_event("startup")
async def startup_event():
    """Start MCP server when FastAPI starts"""
    print("🚀 Starting AgriSaarthi services...")

    # Start MCP server in a separate thread
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()

    print("✅ MCP server started in background on port 8005")
    print("✅ FastAPI app ready on port 8000")


@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "AgriSaarthi RAG Service",
        "version": "0.2.0",
        "endpoints": {
            "chat": "/chat",
            "chat_stream": "/chat/stream",
            "agents_categories": "/agents/categories",
            "health": "/health",
        },
        "mcp_server": {
            "status": "running",
            "port": 8005,
            "tools": ["search_knowledgebase", "web_search"],
        },
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AgriSaarthi RAG Service",
        "mcp_server": "running on port 8005",
    }


if __name__ == "__main__":
    import uvicorn

    print("🌾 AgriSaarthi - AI-Powered Agricultural Assistant")
    print("=" * 60)
    print("Starting services...")

    # Start MCP server in a separate thread
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()

    print("✅ MCP server started on port 8005")
    print("✅ Starting FastAPI app on port 8000")
    print("=" * 60)

    # Start FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
