import io
from fastapi import UploadFile
from pypdf import PdfReader


def read_file_to_text(upload: UploadFile) -> str:
    filename = upload.filename or ""
    content = upload.file.read()
    if filename.lower().endswith(".pdf"):
        with io.BytesIO(content) as buf:
            reader = PdfReader(buf)
            texts = []
            for page in reader.pages:
                texts.append(page.extract_text() or "")
            return "\n".join(texts)
    try:
        return content.decode("utf-8")
    except Exception:
        return content.decode("latin-1", errors="ignore")
