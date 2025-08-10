from typing import List

try:
    from chonkie import TokenChunker
except Exception:
    TokenChunker = None  # type: ignore

from llama_index.core.node_parser import TokenTextSplitter


def chunk_text(text: str) -> List[str]:
    if TokenChunker is not None:
        chunker = TokenChunker(chunk_size=800, chunk_overlap=120)
        return [c.text for c in chunker.chunk(text) if c.text.strip()]
    splitter = TokenTextSplitter(chunk_size=800, chunk_overlap=120)
    return splitter.split_text(text)
