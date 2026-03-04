# Setup Guide — Running Instance 3 (OpenDnD) Locally

This folder contains everything you need to run the OpenDnD OpenClaw instance on your own Mac.

**What's in this repo (no secrets):** All 7 agent personalities (SOUL.md + AGENTS.md), RAG tools, workspace docs, and this setup guide.
**What you get from Constantine separately:** `.env.instance3` (API keys) and `openclaw.json` (gateway token + model config).

---

## Prerequisites
- macOS with Apple Silicon (M1/M2/M3) or Intel
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- [Homebrew](https://brew.sh) installed
- An `OLLAMA_MODELS` path — default is `/Volumes/ai-stack/ollama/models` (EMTEC SSD). Change this if your drive has a different name.

---

## Step 1 — Install Ollama
```bash
brew install ollama
brew services start ollama
```

Verify it's running:
```bash
curl http://localhost:11434/
# Expected: Ollama is running
```

---

## Step 2 — Download AI models (~17 GB total)

Pull the small models first (fast), then the larger ones:

```bash
# Small/medium models (~9 GB)
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull phi4-mini
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull qwen2.5-coder:3b
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull llama3.2:3b
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull phi3:mini
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull nomic-embed-text

# Larger models (~8 GB — fine to run overnight)
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull codellama:7b
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull llama3.1:8b
```

| Model | Size | Agent | Purpose |
|---|---|---|---|
| `phi4-mini` | 2.5 GB | `dm` | Dungeon Master / D&D storytelling |
| `qwen2.5-coder:3b` | 1.9 GB | `coder` | Code writing, debugging |
| `llama3.2:3b` | 2.0 GB | `llama32` | Everyday chat, Q&A |
| `phi3:mini` | 2.2 GB | `phi3` | Step-by-step reasoning, math |
| `codellama:7b` | 3.8 GB | `codellama` | Multi-language code, SQL |
| `llama3.1:8b` | 4.9 GB | `llama31` | Long-form writing, best quality |
| `nomic-embed-text` | 0.3 GB | *(RAG only)* | Embeddings for semantic search |

> RAM note: `llama3.1:8b` uses ~5 GB RAM. Close other apps before chatting with the `llama31` agent.

---

## Step 3 — Get your secrets from Constantine

Ask Constantine to send you (via Signal or encrypted channel):
1. **`.env.instance3`** — gateway token + API keys (Gemini, OpenAI, etc.)
2. **`openclaw.json`** — gateway token, agent configs, model settings

Where to put them:
```bash
# .env goes in the openclaw source folder
cp .env.instance3 /path/to/openclaw/.env.instance3

# openclaw.json goes in this repo root (one level up from setup/)
cp openclaw.json /path/to/OpenDnD/openclaw.json
```

If Constantine only sent `openclaw.json.template`, copy and fill it in:
```bash
cp ../openclaw.json.template ../openclaw.json
# Edit ../openclaw.json and replace all YOUR_*_HERE placeholders
```

---

## Step 4 — Get the OpenClaw source and build the Docker image

You need the OpenClaw source to build the Docker image (ask Constantine for access):

```bash
cd /path/to/openclaw-source

# Build the image (~5 minutes first time, ~30 seconds after)
docker build -t openclaw:local --build-arg OPENCLAW_ACCENT_COLOR='#A020F0' .
```

---

## Step 5 — Start Instance 3

```bash
cd /path/to/openclaw-source
docker compose -p openclaw3 --env-file .env.instance3 up -d openclaw-gateway
```

Check it's running:
```bash
docker ps --filter name=openclaw3
```

---

## Step 6 — Open the UI

Go to: **http://localhost:18785**

You should see the OpenClaw Control UI with all 7 agents ready.

---

## How to chat with a specific agent

The browser UI connects to the `main` agent by default. To switch agents, type one of these commands in the chat input and press Enter:

| Agent | Type in chat | Model |
|---|---|---|
| Dungeon Master | `/session agent:dm:main` | phi4-mini |
| Code Specialist | `/session agent:coder:main` | qwen2.5-coder:3b |
| Everyday Chat | `/session agent:llama32:main` | llama3.2:3b |
| Reasoning Engine | `/session agent:phi3:main` | phi3:mini |
| Code Expert | `/session agent:codellama:main` | codellama:7b |
| Deep Thinker | `/session agent:llama31:main` | llama3.1:8b |
| Back to main | `/session agent:main:main` | Gemini/phi4-mini |

The UI header updates to confirm the active agent.

---

## Quick tests

See `workspace/AI_STACK_GUIDE.md` for all copy-paste terminal tests and browser chat test messages for every agent.
