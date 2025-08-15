from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.ingest import router as ingest_router
from app.api.routers.chat import router as chat_router
import threading
from app.mcp.mcp import mcp

app = FastAPI(title="Agrisathi RAG Service", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def run_mcp_server():
    """Run the MCP server in a separate thread"""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    # Start MCP server in a separate thread
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()

    # Note: When running in Docker, uvicorn is started via the CMD
    # This section is kept for local development outside Docker
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
