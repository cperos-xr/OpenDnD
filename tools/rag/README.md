RAG toolset — indexer + retriever + simple chat service

Overview
--------
This folder provides a minimal Retrieval-Augmented-Generation (RAG) toolset:

- `index.py` — simple chunker that writes `chunks.jsonl`
- `service.py` — FastAPI service with endpoints to retrieve and perform RAG
- `requirements.txt` — Python dependencies

Design notes
------------
- The service prefers using a local Ollama embedding model (`nomic/embed-3-small`) when the Ollama HTTP embed endpoint is available. If embedding calls fail, the service falls back to a TF-IDF retriever (scikit-learn).
- The generator model defaults to `ollama/llama-3.2-3b` (configurable via `RAG_GEN_MODEL` env var).

Quickstart
----------
1. Install dependencies (recommend a venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r tools/rag/requirements.txt
```

2. Pull models into Ollama:

```bash
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull nomic/embed-3-small
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull ollama/llama-3.2-3b
```

3. Index a folder of docs (markdown or text):

```bash
python3 tools/rag/index.py /Volumes/ai-stack/openclaw-data-3/workspace
```

4. Start the service:

```bash
RAG_GEN_MODEL=ollama/llama-3.2-3b RAG_EMBED_MODEL=nomic/embed-3-small python3 tools/rag/service.py
```

5. Test a RAG query (local):

```bash
curl -s -X POST http://127.0.0.1:8765/rag-chat -H "Content-Type: application/json" -d '{"q":"Describe how to start instance 3","k":3}' | jq
```

Notes & caveats
----------------
- Ollama embedding HTTP endpoints vary by version. If the Ollama embed endpoint is not available, the service will fall back to TF-IDF. For best retrieval quality, run `nomic/embed-3-small` and verify your Ollama version supports embeddings via HTTP.
- This project provides a minimal, local-first RAG workflow. For larger corpora consider a dedicated vector DB like Chroma or FAISS and precomputing embeddings.

