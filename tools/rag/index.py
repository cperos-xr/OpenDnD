"""
Simple indexer: walks a folder of text files, splits into fixed-size chunks,
and writes `tools/rag/chunks.jsonl` with one JSON object per chunk:
{ "id": ..., "source": "path/to/file", "text": "..." }

This keeps indexing simple and avoids embedding during indexing. The
service will compute embeddings on demand (using Ollama nomic/embed if
available) or fall back to a TF-IDF retriever.

Usage:
  python3 tools/rag/index.py /path/to/docs_folder

"""
import os
import sys
import json
from pathlib import Path

CHUNK_SIZE = 2000  # characters per chunk
CHUNK_OVERLAP = 200


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    start = 0
    L = len(text)
    while start < L:
        end = start + size
        yield text[start:end]
        if end >= L:
            break
        start = end - overlap


def index_folder(folder, out_file):
    folder = Path(folder)
    chunks = []
    idx = 0
    for p in folder.rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        for i, chunk in enumerate(chunk_text(text)):
            obj = {
                "id": f"{p.name}#{i}",
                "source": str(p.relative_to(folder)),
                "text": chunk.strip()
            }
            chunks.append(obj)
            idx += 1
    for p in folder.rglob("*.txt"):
        text = p.read_text(encoding="utf-8")
        for i, chunk in enumerate(chunk_text(text)):
            obj = {
                "id": f"{p.name}#{i}",
                "source": str(p.relative_to(folder)),
                "text": chunk.strip()
            }
            chunks.append(obj)
            idx += 1
    with open(out_file, "w", encoding="utf-8") as fh:
        for c in chunks:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote {len(chunks)} chunks to {out_file}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 tools/rag/index.py /path/to/docs_folder")
        sys.exit(1)
    docs = sys.argv[1]
    out = Path(__file__).parent / "chunks.jsonl"
    index_folder(docs, out)
