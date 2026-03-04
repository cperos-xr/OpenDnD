"""
Minimal RAG service.

Endpoints:
- POST /index { "path": "/path/to/docs" }  -> runs indexer (writes chunks.jsonl)
- GET  /query?q=...&k=4                  -> returns top-k retrieved chunks (TF-IDF fallback)
- POST /rag-chat { "q": "...", "k": 4 } -> returns generated answer using Llama-3.2

Behavior:
- Tries to use Ollama nomic/embed-3-small via local HTTP for embeddings if available.
  If that fails, falls back to a TF-IDF retriever (scikit-learn).
- Calls Ollama Llama 3.2 model via HTTP to generate the final answer.

Notes:
- This is intentionally minimal and suitable for small corpora.
- See README.md for configuration and usage.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import json
from pathlib import Path
import requests
import os

APP = FastAPI()
BASE_DIR = Path(__file__).parent
CHUNKS_FILE = BASE_DIR / "chunks.jsonl"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.environ.get("RAG_EMBED_MODEL", "nomic-embed-text")
GEN_MODEL = os.environ.get("RAG_GEN_MODEL", "phi4-mini")

# Simple in-memory corpus loaded from chunks.jsonl
CORPUS = []


def load_corpus():
    global CORPUS
    CORPUS = []
    if CHUNKS_FILE.exists():
        with open(CHUNKS_FILE, "r", encoding="utf-8") as fh:
            for line in fh:
                CORPUS.append(json.loads(line))
    return len(CORPUS)


class IndexRequest(BaseModel):
    path: str


class RagRequest(BaseModel):
    q: str
    k: int = 4


@APP.post("/index")
def do_index(req: IndexRequest):
    # call indexer script
    idx_path = Path(__file__).parent / "index.py"
    if not idx_path.exists():
        raise HTTPException(status_code=500, detail="index.py missing")
    cmd = f"python3 {idx_path} {req.path}"
    rc = os.system(cmd)
    if rc != 0:
        raise HTTPException(status_code=500, detail="indexing failed")
    n = load_corpus()
    return {"status": "ok", "chunks": n}


def try_ollama_embed(texts: List[str]):
    """Try to get embeddings from Ollama (nomic embed). Returns list of vectors or None."""
    try:
        url = f"{OLLAMA_HOST}/api/embed"
        payload = {"model": EMBED_MODEL, "input": texts}
        r = requests.post(url, json=payload, timeout=20)
        if r.status_code == 200:
            data = r.json()
            # expected: { "embeddings": [[...], ...] }
            if "embeddings" in data:
                return data["embeddings"]
        return None
    except Exception:
        return None


# TF-IDF fallback
TFIDF_VECT = None
VECT_MATRIX = None
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def build_tfidf():
    global TFIDF_VECT, VECT_MATRIX
    texts = [c["text"] for c in CORPUS]
    TFIDF_VECT = TfidfVectorizer(stop_words="english", max_features=20000)
    VECT_MATRIX = TFIDF_VECT.fit_transform(texts)
    return VECT_MATRIX.shape[0]


def retrieve_tfidf(q, k=4):
    if TFIDF_VECT is None:
        build_tfidf()
    qv = TFIDF_VECT.transform([q])
    sims = (VECT_MATRIX @ qv.T).toarray()[:, 0]
    idxs = np.argsort(-sims)[:k]
    results = [CORPUS[i] for i in idxs]
    return results


def call_ollama_generate(prompt, max_tokens=512):
    # Ollama generation via HTTP /api/generate
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": GEN_MODEL,
        "prompt": prompt,
        "max_tokens": max_tokens
    }
    try:
        r = requests.post(url, json=payload, timeout=60)
        if r.status_code == 200:
            data = r.json()
            # Ollama returns streaming chunks in some versions; try to extract text
            if "text" in data:
                return data["text"]
            # else return raw json
            return json.dumps(data)
        else:
            raise Exception(f"status {r.status_code}: {r.text}")
    except Exception as e:
        raise


@APP.get("/query")
def query(q: str, k: int = 4):
    if not CORPUS:
        load_corpus()
    # Try Ollama embeddings
    ids = []
    embeds = try_ollama_embed([q])
    if embeds is not None:
        # naive brute-force: embed each doc text (costly) — try small corpora only
        doc_texts = [c["text"] for c in CORPUS]
        doc_embeds = try_ollama_embed(doc_texts)
        if doc_embeds is None:
            results = retrieve_tfidf(q, k)
        else:
            qe = np.array(embeds[0])
            dob = np.array(doc_embeds)
            sims = dob @ qe
            idxs = np.argsort(-sims)[:k]
            results = [CORPUS[i] for i in idxs]
    else:
        results = retrieve_tfidf(q, k)
    return {"results": results}


@APP.post("/rag-chat")
def rag_chat(req: RagRequest):
    if not CORPUS:
        load_corpus()
    # retrieve
    try:
        got = query(req.q, k=req.k)
    except Exception:
        got = query(req.q, k=req.k)
    passages = got.get("results", [])
    # build prompt
    sys_instr = (
        "System: You are an assistant. Use only the provided sources to answer. "
        "Cite sources as [source:filename#chunk]. If none are relevant, say 'I don't know'.\n\n"
    )
    srcs = []
    for i, p in enumerate(passages, 1):
        t = p.get("text", "")
        src = p.get("source", "unknown")
        srcs.append(f"Source {i} ({src}):\n{t}\n")
    prompt = sys_instr + "\n\n".join(srcs) + f"\nQuestion: {req.q}\nAnswer:" 
    # call generator
    try:
        out = call_ollama_generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"answer": out, "sources": [p.get("source") for p in passages]}


if __name__ == '__main__':
    load_corpus()
    uvicorn.run(APP, host="127.0.0.1", port=8765)
