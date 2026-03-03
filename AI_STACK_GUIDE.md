# The AI Stack — Complete Build Guide
### What We Built, How It Works, and How to Test It

> **Who this is for:** Constantine's brother (and anyone watching the video).
> You do not need to be technical to follow the bold sections.
> The smaller grey-text sections below each topic are for the curious — skip them freely.

---

## 🗺️ THE BIG PICTURE

> **We built a personal AI server that lives entirely on a portable USB drive.**
> Plug the drive into a Mac, run one command, and three independent AI assistants come to life — each with its own personality, memory, and purpose.
> Two of those assistants run completely offline using AI models stored on the same drive. No internet required. No API fees for local use.

```
┌─────────────────────────────────────────────────────┐
│         EMTEC X210 256GB SSD  (/Volumes/ai-stack)   │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │  Instance 1  │  │  Instance 2  │  │Instance 3 │ │
│  │  (Personal)  │  │  (Zeek/Dev)  │  │ (OpenDnD) │ │
│  │  Port 18781  │  │  Port 18783  │  │Port 18785 │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  Ollama  —  Local AI Engine  (Port 11434)   │   │
│  │  phi4-mini (2.5GB) · qwen2.5-coder:3b (1.9GB)  │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🖥️ THE HARDWARE

> **A Mac Mini with an Apple M2 chip and a tiny portable SSD.**
> The M2 chip has a built-in AI accelerator (called Metal / Neural Engine). This is what makes local AI fast — no GPU needed.

| Component | Detail |
|---|---|
| Machine | Mac Mini, Apple M2 |
| RAM | 8GB unified memory |
| External Drive | EMTEC X210 256GB SSD |
| Drive Mount | `/Volumes/ai-stack` |
| Drive Format | APFS (Mac native — required for symlinks + permissions) |

**Why a portable drive?**
Every file, every AI model, every conversation history, and every config lives on the SSD. Unplug it, carry it anywhere, plug into another Mac — everything works exactly the same. No setup required on the new machine.

<details>
<summary>Technical: drive setup details</summary>

- Drive was reformatted from ExFAT → APFS using Disk Utility, named `ai-stack`
- A symlink was created: `/Users/cperos/ai-stack` → `/Volumes/ai-stack` for backward compatibility
- Docker Desktop is configured with virtiofs mount access to `/Volumes`, so containers see the drive directly

</details>

---

## 📦 WHAT IS OPENCLAW?

> **OpenClaw is the AI assistant software — think of it like a brain for each agent.**
> It connects to AI models (like GPT-4, Gemini, or local Ollama models), gives them a personality and memory, and lets you chat with them via a web browser or phone apps.

Each running copy of OpenClaw is called an **instance**. We run 3 instances, each isolated from the others, each with their own:
- Conversation history
- Personality files (`SOUL.md`, `AGENTS.md`)
- Skills and tools
- Web UI at their own port

<details>
<summary>Technical: how instances run</summary>

- OpenClaw runs inside Docker containers using the image `openclaw:local` (4.08GB, shared across all instances — no duplication)
- Each instance uses `docker compose` with a dedicated `.env.instanceN` file
- Instance data stored at `/Volumes/ai-stack/openclaw-data-N/`
- Source code at `/Volumes/ai-stack/openclaw/`

</details>

---

## 🤖 THE THREE INSTANCES

### Instance 1 — Personal Assistant
| | |
|---|---|
| **Web UI** | http://localhost:18781 |
| **Bridge** | http://localhost:18782 |
| **Data** | `/Volumes/ai-stack/openclaw-data-1/` |
| **Model** | Google Gemini (primary) |

### Instance 2 — Zeek's Dev Instance
| | |
|---|---|
| **Web UI** | http://localhost:18783 |
| **Bridge** | http://localhost:18784 |
| **Data** | `/Volumes/ai-stack/openclaw-data-2/` |
| **Model** | Google Gemini (primary) |
| **Extra** | Has Zeek's skills folder + SAM server skill |

### Instance 3 — OpenDnD (The Focus of This Guide)
| | |
|---|---|
| **Web UI** | http://localhost:18785 |
| **Bridge** | http://localhost:18786 |
| **Data** | `/Volumes/ai-stack/openclaw-data-3/` |
| **GitHub** | https://github.com/cperos-xr/OpenDnD |
| **Special** | Has 3 agents including 2 local Ollama models |

---

## 🧠 WHAT IS OLLAMA?

> **Ollama is software that runs AI models directly on your Mac — no internet, no subscription, no data leaving your machine.**
> It's like having ChatGPT but it runs entirely in your living room.

We installed Ollama natively (not in Docker) so it gets full access to the M2 chip's AI hardware. This makes it **5-10x faster** than running it in a container.

**Models we downloaded (stored on the SSD at `/Volumes/ai-stack/ollama/models/`):**

| Model | Size | Made By | Good At |
|---|---|---|---|
| `phi4-mini` | 2.5 GB | Microsoft | General reasoning, creative writing, D&D! |
| `qwen2.5-coder:3b` | 1.9 GB | Alibaba | Writing code, debugging, technical tasks |

**Total local AI storage: ~4.4 GB on the SSD. Both fit in 8GB RAM with room to spare.**

<details>
<summary>Technical: Ollama configuration</summary>

- Installed via `brew install ollama`
- Service configured at `~/Library/LaunchAgents/homebrew.mxcl.ollama.plist`
- Environment variables set:
  - `OLLAMA_MODELS=/Volumes/ai-stack/ollama/models` — models live on the SSD
  - `OLLAMA_HOST=0.0.0.0:11434` — accessible from Docker containers
  - `OLLAMA_FLASH_ATTENTION=1` — M2 optimization
  - `OLLAMA_KV_CACHE_TYPE=q8_0` — M2 optimization
- Docker containers reach Ollama via `http://host.docker.internal:11434`
- Ollama loads one model at a time; switching agents triggers ~5s model swap

</details>

---

## 🎭 THE THREE AGENTS IN INSTANCE 3

> **Instance 3 has three distinct personalities you can chat with. Two run 100% offline.**

### Agent: `main` — The General Assistant
- **Model:** Google Gemini (cloud, requires internet)
- **Fallback:** phi4-mini (local, if Gemini is unavailable)
- **Personality:** Default helpful assistant
- **Workspace:** `/Volumes/ai-stack/openclaw-data-3/workspace/`

### Agent: `dm` — The Dungeon Master 🎲
- **Model:** phi4-mini (LOCAL — no internet needed)
- **Personality:** Imaginative, "yes, and…" storyteller. Vivid descriptions. Tracks world lore.
- **Best for:** D&D campaign help, NPC creation, location descriptions, encounter ideas
- **Workspace:** `/Volumes/ai-stack/openclaw-data-3/workspace-dm/`

### Agent: `coder` — The Code Specialist 💻
- **Model:** qwen2.5-coder:3b (LOCAL — no internet needed)
- **Personality:** Terse, efficient engineer. Code-first. No filler.
- **Best for:** Writing functions, debugging, reviewing code, shell scripts
- **Workspace:** `/Volumes/ai-stack/openclaw-data-3/workspace-coder/`

---

## ✅ HOW TO START EVERYTHING

> **Before running tests, make sure everything is running.**

### Step 1 — Check the drive is mounted
```bash
ls /Volumes/ai-stack
```
You should see folders like `openclaw`, `openclaw-data-1`, `ollama`, etc.
If not, replug the EMTEC drive.

### Step 2 — Check Ollama is running
```bash
curl http://localhost:11434/
```
Expected output: `Ollama is running`

If not running:
```bash
brew services start ollama
```

### Step 3 — Check the containers are up
```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep openclaw
```
Expected output (all three should show `Up`):
```
openclaw1-openclaw-gateway-1   Up X minutes
openclaw2-openclaw-gateway-1   Up X minutes
openclaw3-openclaw-gateway-1   Up X minutes
```

If any are down, start them all:
```bash
cd /Volumes/ai-stack/openclaw
docker compose -p openclaw1 --env-file .env.instance1 up -d openclaw-gateway
docker compose -p openclaw2 --env-file .env.instance2 up -d openclaw-gateway
docker compose -p openclaw3 --env-file .env.instance3 up -d openclaw-gateway
```

### Step 4 — Check the models are available
```bash
ollama list
```
Expected output:
```
NAME                ID              SIZE      MODIFIED
qwen2.5-coder:3b    f72c60cabf62    1.9 GB    ...
phi4-mini:latest    78fad5d182a7    2.5 GB    ...
```

---

## 🧪 COPY-PASTE TESTS

> **Run these in your terminal (the Terminal app, or iTerm). Each one talks to a different AI.**
> These are the exact tests we ran to verify everything works.

---

### TEST 1 — Verify Ollama is alive
```bash
curl http://localhost:11434/
```
**Expected output:**
```
Ollama is running
```

---

### TEST 2 — List available local models
```bash
ollama list
```
**Expected output:**
```
NAME                ID              SIZE      MODIFIED
qwen2.5-coder:3b    f72c60cabf62    1.9 GB    ...
phi4-mini:latest    78fad5d182a7    2.5 GB    ...
```

---

### TEST 3 — phi4-mini: Introduce yourself
```bash
ollama run phi4-mini "Hello, what can you do?"
```
**What to watch for:** The model describes its capabilities. No internet. Runs on M2 Metal.

**Example output we got:**
```
Hello! I'm Phi, an AI digital assistant. I'm designed to help you
with a variety of tasks, including:
1. Answering general knowledge questions.
2. Providing explanations on a wide range of topics.
...
```

---

### TEST 4 — phi4-mini as Dungeon Master: scene description
```bash
ollama run phi4-mini "You are a Dungeon Master. Describe the entrance to a goblin cave in 3 sentences."
```
**What to watch for:** Evocative, atmospheric writing. This is the `dm` agent's model.

**Example output we got:**
```
The entrance to the goblin cave is a gaping maw in a sheer cliffside,
cloaked in shadows and moss. Jagged teeth of rock jut out like menacing
teeth, glowing faintly in the dim light. Beyond the entrance lies a
winding tunnel, filled with the echoing sounds of dripping water and
distant goblin chatter.
```

---

### TEST 5 — phi4-mini: D&D campaign ideas
```bash
ollama run phi4-mini "what are some ideas you have for d&d 5e games"
```
**What to watch for:** The model generates a list of creative campaign concepts with different settings. This is 100% local — no data sent anywhere.

---

### TEST 6 — qwen2.5-coder: Write a dice roller function
```bash
ollama run qwen2.5-coder:3b "Write a Python function that rolls XdY dice and returns the total."
```
**What to watch for:** Clean Python code with docstring and explanation. This is the `coder` agent's model.

**Example output we got:**
```python
import random

def roll_dice(x, y):
    """
    Rolls XdY dice and returns the total.
    """
    total = 0
    for _ in range(x):
        roll = random.randint(1, y)
        total += roll
    return total
```

---

### TEST 7 — qwen2.5-coder: Debug code
```bash
ollama run qwen2.5-coder:3b "Here is broken Python code. Find and fix the bug:
def add_numbers(a, b)
    return a + b
print(add_numbers(3, 4))"
```
**What to watch for:** The coder correctly identifies the missing colon after the function definition.

---

### TEST 8 — Interactive D&D session (multi-turn)
Start an interactive session with the DM model:
```bash
ollama run phi4-mini
```
Then type these one at a time and press Enter after each:
```
You are a Dungeon Master running a D&D 5e campaign. I am a level 3 rogue named Kira. I enter a tavern. What do I see?
```
Then follow up with:
```
I approach the cloaked figure in the corner and ask if they have work for a skilled rogue.
```
Press `Ctrl+D` or type `/bye` to exit.

---

### TEST 9 — Check all three agents are configured in Instance 3
```bash
docker exec openclaw3-openclaw-gateway-1 node -e "
const fs = require('fs');
const c = JSON.parse(fs.readFileSync('/home/node/.openclaw/openclaw.json'));
const agents = c.agents?.list?.map(a => a.id + ' → ' + (a.model || 'default'));
console.log('Agents:', agents);
"
```
**Expected output:**
```
Agents: [ 'main → default', 'dm → ollama/phi4-mini', 'coder → ollama/qwen2.5-coder:3b' ]
```

---

### TEST 10 — Verify Instance 3 container can reach Ollama
```bash
docker exec openclaw3-openclaw-gateway-1 curl -s http://host.docker.internal:11434/api/tags | python3 -c "
import sys, json
models = json.load(sys.stdin).get('models', [])
for m in models:
    print(m['name'], '-', round(m['size']/1024/1024), 'MB')
"
```
**Expected output:**
```
qwen2.5-coder:3b - 1840 MB
phi4-mini:latest - 2376 MB
```

---

### TEST 11 — Open the Instance 3 web UI in the browser

Open your browser and go to:
```
http://localhost:18785
```
You should see the OpenClaw Control UI. From there you can chat with agents and switch between `main`, `dm`, and `coder` using the agent selector in the UI.

---

## 🌐 WHAT'S CONNECTED TO THE INTERNET vs. WHAT'S LOCAL

| Feature | Internet? | Notes |
|---|---|---|
| `phi4-mini` model | ❌ No | Runs entirely on M2 chip |
| `qwen2.5-coder:3b` model | ❌ No | Runs entirely on M2 chip |
| Google Gemini (Instance 3 `main`) | ✅ Yes | Requires GEMINI_API_KEY |
| OpenAI GPT (fallback) | ✅ Yes | Requires OPENAI_API_KEY |
| GitHub (OpenDnD repo) | ✅ Yes | Only for pushing/pulling code |

**The entire Ollama setup costs $0/month and works with no internet.**

---

## 📁 WHERE EVERYTHING LIVES ON THE DRIVE

```
/Volumes/ai-stack/
├── openclaw/               ← Source code for all 3 instances
│   ├── .env.instance1
│   ├── .env.instance2
│   └── .env.instance3
├── openclaw-data-1/        ← Instance 1 data (conversations, settings)
├── openclaw-data-2/        ← Instance 2 data (Zeek's instance)
├── openclaw-data-3/        ← Instance 3 data (OpenDnD)
│   ├── workspace/          ← main agent workspace
│   ├── workspace-dm/       ← DM agent workspace
│   │   ├── SOUL.md         ← DM personality
│   │   └── AGENTS.md       ← DM operating instructions
│   └── workspace-coder/    ← Coder agent workspace
│       ├── SOUL.md         ← Coder personality
│       └── AGENTS.md       ← Coder operating instructions
├── ollama/
│   └── models/             ← phi4-mini (2.5GB) + qwen2.5-coder:3b (1.9GB)
└── deployment-kit/         ← Scripts to spin up new instances
    └── deploy-instance.sh
```

---

## 🚀 WHAT'S NEXT / FUTURE IDEAS

- [ ] Give the `dm` agent campaign notes to remember between sessions (it already has a workspace for this)
- [ ] Pull a larger model like `llama3.2:7b` when you want more capability (requires ~5GB, fits on 8GB M2 with tight margins)
- [ ] Connect Instance 3 to Discord so your brother can DM the AI from his phone
- [ ] Record a video walkthrough using these tests as the shot list
- [ ] Deploy a 4th instance for a new project using `deployment-kit/deploy-instance.sh`

---

## 🔧 QUICK REFERENCE CHEAT SHEET

```bash
# --- OLLAMA ---
ollama list                          # See installed models
ollama run phi4-mini                 # Chat with DM model (interactive)
ollama run qwen2.5-coder:3b          # Chat with coder model (interactive)
brew services start ollama           # Start Ollama if it's not running
brew services stop ollama            # Stop Ollama

# --- DOCKER INSTANCES ---
docker ps                            # See running containers
cd /Volumes/ai-stack/openclaw

# Start all 3 instances
docker compose -p openclaw1 --env-file .env.instance1 up -d openclaw-gateway
docker compose -p openclaw2 --env-file .env.instance2 up -d openclaw-gateway
docker compose -p openclaw3 --env-file .env.instance3 up -d openclaw-gateway

# Stop all 3 instances
docker compose -p openclaw1 --env-file .env.instance1 stop openclaw-gateway
docker compose -p openclaw2 --env-file .env.instance2 stop openclaw-gateway
docker compose -p openclaw3 --env-file .env.instance3 stop openclaw-gateway

# Restart just instance 3
docker compose -p openclaw3 --env-file .env.instance3 restart openclaw-gateway

# View instance 3 logs
docker logs openclaw3-openclaw-gateway-1 --tail 30 -f

# --- WEB UIs ---
# Instance 1: http://localhost:18781
# Instance 2: http://localhost:18783
# Instance 3: http://localhost:18785   ← OpenDnD with DM + Coder agents
```

---

*Built on March 3, 2026 · Apple M2 Mac Mini · EMTEC X210 256GB SSD · Ollama 0.17.5 · OpenClaw v2026.2.25*
