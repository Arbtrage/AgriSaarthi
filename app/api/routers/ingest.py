from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.utils.parsing import read_file_to_text
from app.utils.chunking import chunk_text
from app.core.milvus_client import insert_documents, get_collection_stats

router = APIRouter()


@router.post("/ingest")
async def ingest(
    files: List[UploadFile] = File(...), namespace: Optional[str] = Form(None)
):
    try:
        all_texts = []
        all_metadatas = []

        for f in files:
            text = read_file_to_text(f)
            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):
                all_texts.append(chunk)

                # Store all metadata in a single JSON field
                metadata = {
                    "source": f.filename,
                    "chunk_id": i,
                    "file_size": len(text),
                    "chunk_size": len(chunk),
                    "namespace": namespace,
                    "total_chunks": len(chunks),
                }
                all_metadatas.append(metadata)

        if not all_texts:
            raise HTTPException(status_code=400, detail="No content to ingest")

        # Insert directly into Milvus with simplified schema
        await insert_documents(texts=all_texts, metadatas=all_metadatas)

        # Verify insertion by getting collection stats
        stats = await get_collection_stats()

        return JSONResponse(
            {
                "status": "ok",
                "ingested_chunks": len(all_texts),
                "files_processed": len(files),
                "collection_stats": stats,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
