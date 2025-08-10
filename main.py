from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.ingest import router as ingest_router
from app.api.routers.chat import router as chat_router

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
