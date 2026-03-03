# Setup Guide — Running Instance 3 (OpenDnD) Locally

This folder contains everything you need to run the OpenDnD OpenClaw instance on your own Mac.

## Prerequisites
- macOS with Apple Silicon (M1/M2/M3) or Intel
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- [Homebrew](https://brew.sh) installed
- The EMTEC X210 SSD (or agree on a different path with Constantine)

## Step 1 — Install Ollama
```bash
brew install ollama
brew services start ollama
```

## Step 2 — Download AI models (4.4 GB total)
```bash
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull phi4-mini
OLLAMA_MODELS=/Volumes/ai-stack/ollama/models ollama pull qwen2.5-coder:3b
```

## Step 3 — Get your secrets from Constantine
Ask Constantine to send you (via Signal or encrypted channel):
- The `.env.instance3` file with all real API keys filled in

Copy it to:
```bash
cp .env.instance3 /Volumes/ai-stack/openclaw/.env.instance3
```

Also copy `openclaw.json.template` to `openclaw.json` in the data dir and fill in your tokens:
```bash
cp ../openclaw.json.template ../openclaw.json
# Then edit ../openclaw.json and replace YOUR_*_HERE placeholders
```

## Step 4 — Build the Docker image
```bash
cd /Volumes/ai-stack/openclaw
docker build -t openclaw:local --build-arg OPENCLAW_ACCENT_COLOR='#A020F0' .
```
*(This takes ~5 minutes the first time, ~30 seconds after that)*

## Step 5 — Start Instance 3
```bash
cd /Volumes/ai-stack/openclaw
docker compose -p openclaw3 --env-file .env.instance3 up -d openclaw-gateway
```

## Step 6 — Open the UI
Go to: **http://localhost:18785**

## Quick tests
See `AI_STACK_GUIDE.md` in the workspace folder for all copy-paste tests.
