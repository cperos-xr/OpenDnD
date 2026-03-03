# Ollama Model Selection Guide — 2025 Edition
> Top 20 Models: Pros, Cons, Storage & Best Use Cases | Helping you pick the right model — one big vs. many small

---

## Strategy: One Big Model vs. Many Small Models?

### ONE BIG MODEL — Best When:
- You have a single primary use case (e.g., deep coding, or research, or writing)
- You want one model that handles everything reasonably well without switching
- You have strong hardware: 32–64 GB RAM or 24 GB+ VRAM
- Example: Llama 3.3 70B handles coding, writing, research, and multilingual all in one

### MANY SMALL MODELS — Best When:
- You have multiple distinct workloads (chat vs. code vs. embeddings vs. vision)
- You want each task to run as fast as possible on modest hardware
- You're building pipelines or automations where different agents handle different jobs
- Example: Mistral 7B for chat speed + DeepSeek Coder for code + Nomic Embed for RAG + Phi-3 Mini for mobile

### Recommended Starter Stacks:
| Tier | Hardware | Recommended Stack |
|---|---|---|
| Budget | 8–16 GB RAM | Llama 3.1 8B + Nomic Embed Text |
| Mid-range | 32 GB RAM | Llama 3.3 70B (quantized) + DeepSeek Coder V2 16B + Nomic Embed |
| High-end | 64+ GB RAM / strong GPU | Llama 3.3 70B + DeepSeek-R1 70B + Llama 3.2-Vision 11B + Nomic Embed |
| Offline/Edge | Any | Phi-3 Mini + TinyLlama |

---

## Hardware Requirements at a Glance

| Model Size | Min RAM | Recommended RAM | Example Models |
|---|---|---|---|
| 1B – 3B | 4 GB | 8 GB | TinyLlama, Phi-3 Mini, Llama 3.2 1B/3B |
| 7B – 8B | 8 GB | 16 GB | Llama 3.1 8B, Mistral 7B, Gemma 3 9B |
| 13B – 14B | 16 GB | 32 GB | CodeLlama 13B, Phi-4 14B, Qwen2.5 14B |
| 27B – 35B | 32 GB | 48 GB | Gemma 3 27B, Command-R 35B, Mixtral 8x7B |
| 70B | 48 GB | 64 GB | Llama 3.1 70B, Llama 3.3 70B, DeepSeek-R1 70B |
| 100B+ | 80 GB+ | 128 GB+ | Command-R+ 104B, Mixtral 8x22B, full DeepSeek-V3 |

---

## Top 20 Models — Detailed Breakdown

---

### 1. Llama 3.3 (70B)
**Category:** General Purpose — Flagship | **Params:** 70B | **Size:** 43 GB | **RAM:** 64 GB RAM or 24 GB VRAM | **Context:** 128K tokens

**Best For:** Deep research, complex analysis, enterprise knowledge management, long-form writing, multilingual tasks

| ✅ Pros | ❌ Cons |
|---|---|
| Near GPT-4 quality at open-source price | Requires high-end hardware (RTX 4090 or M2 Max+) |
| Massive 128K context window | Slow on CPUs |
| Excellent multilingual support (8 languages) | 43 GB download is large |
| Strong on coding & reasoning benchmarks | Needs 64 GB RAM for comfortable use |
| Very efficient for its size | Not ideal for true edge/mobile deployment |

> **Verdict:** Best single model if you have the hardware

---

### 2. Llama 3.1 (8B)
**Category:** General Purpose — Workhorse | **Params:** 8B | **Size:** 4.9 GB | **RAM:** 8 GB VRAM or 16 GB RAM | **Context:** 128K tokens

**Best For:** Everyday professional work, document summarization, code generation, content drafting, chatbots

| ✅ Pros | ❌ Cons |
|---|---|
| 108M+ downloads — most popular Ollama model | Noticeably weaker than 70B on complex reasoning |
| Runs on modest hardware | Struggles with very deep logic chains |
| Strong tool use & function calling | Not ideal for nuanced multilingual work |
| Excellent context length for the size | Can hallucinate on niche topics |
| Best balance of quality vs. accessibility | Limited compared to newer Llama 3.3 |

> **Verdict:** The go-to starting point for most users

---

### 3. Llama 3.2 (1B / 3B)
**Category:** Edge / Mobile | **Params:** 1B or 3B | **Size:** 1.3 GB / 2.0 GB | **RAM:** 4–8 GB RAM | **Context:** 128K tokens

**Best For:** Mobile apps, IoT devices, offline tools, quick prototyping, edge deployment

| ✅ Pros | ❌ Cons |
|---|---|
| Runs on almost any hardware | Limited depth for complex tasks |
| Tiny download size | Struggles with nuanced reasoning |
| Surprisingly capable 128K context | Not suitable for coding or research work |
| Great for on-device / privacy-first apps | Often gives shallow or incomplete answers |
| Near-instant responses | Weak multilingual performance |

> **Verdict:** Best for resource-constrained or always-on scenarios

---

### 4. Llama 3.2-Vision (11B / 90B)
**Category:** Multimodal | **Params:** 11B / 90B | **Size:** 7.8 GB / 55 GB | **RAM:** 16 GB VRAM / 64 GB+ | **Context:** 128K tokens

**Best For:** Image analysis, OCR, chart understanding, document processing, visual Q&A, accessibility tools

| ✅ Pros | ❌ Cons |
|---|---|
| First Llama with true vision capabilities | Image+text mode is English-only |
| High-res image support (up to 1120x1120) | 90B requires serious hardware |
| Handles OCR, handwriting, and charts | Slower than text-only models |
| Preserves all text capabilities from Llama 3.1 | Limited compared to cloud vision APIs on complex tasks |
| 11B is a great sweet spot for most users | Not ideal for real-time video or streaming input |

> **Verdict:** Best local multimodal option

---

### 5. DeepSeek-R1
**Category:** Reasoning / Math | **Params:** 1.5B – 671B | **Size:** 1.1 GB – 404 GB | **RAM:** 4 GB+ (8B distill) to 400 GB+ (671B full) | **Context:** 128K tokens

**Best For:** Complex reasoning, step-by-step math, logic puzzles, research analysis, scientific problems

| ✅ Pros | ❌ Cons |
|---|---|
| 75M+ downloads | Larger variants need extreme hardware |
| Performance approaching OpenAI o3 / Gemini 2.5 Pro | Chain-of-thought can be verbose and slow |
| Excellent chain-of-thought reasoning | Some safety guardrails are inconsistent |
| Available in many sizes via distillation | Full 671B is not practical for local use |
| Open weights allow full inspection | Overthinks simple tasks with unnecessary steps |

> **Verdict:** Best for reasoning-heavy tasks

---

### 6. Qwen3 (Alibaba)
**Category:** General Purpose — Modern | **Params:** 0.6B – 235B MoE | **Size:** 0.5 GB – 150 GB+ | **RAM:** 4 GB (small) to 80 GB+ (large MoE) | **Context:** 128K tokens

**Best For:** Multilingual tasks, coding, long-context work, agentic workflows, Chinese/English bilingual use

| ✅ Pros | ❌ Cons |
|---|---|
| Latest-gen Qwen architecture | Very large MoE models need specialized hardware |
| Dense and MoE variants available | Less English community documentation |
| Exceptional Chinese + English quality | MoE can be slower on consumer hardware |
| Very strong coding performance | Newer — less extensively tested than Llama |
| Scales well from tiny to massive | Licensing has some commercial restrictions |

> **Verdict:** Top pick for multilingual and bilingual work

---

### 7. Qwen2.5 (Alibaba)
**Category:** General Purpose | **Params:** 0.5B – 72B | **Size:** 0.4 GB – 47 GB | **RAM:** 4 GB (small) to 48 GB (72B) | **Context:** 128K tokens

**Best For:** Coding, multilingual chat, summarization, data analysis, structured output

| ✅ Pros | ❌ Cons |
|---|---|
| Pretrained on 18 trillion tokens | Slightly behind Qwen3 on benchmarks |
| Excellent coding and math performance | Large model sizes for top tier variants |
| Strong multilingual support | Less popular than Llama in Western communities |
| Good context and instruction handling | Limited tooling ecosystem compared to Meta models |
| Multiple practical size options | Some fine-tuned versions have inconsistent quality |

> **Verdict:** Excellent all-rounder, especially for code

---

### 8. Mistral 7B (v0.3)
**Category:** General Purpose — Fast | **Params:** 7B | **Size:** 4.1 GB | **RAM:** 8 GB RAM | **Context:** 32K tokens

**Best For:** Quick responses, chatbots, summarization, light coding, everyday tasks where speed matters

| ✅ Pros | ❌ Cons |
|---|---|
| Extremely fast generation speed | Smaller context window (32K vs 128K) |
| Low memory footprint | Weaker than newer models on benchmarks |
| Well-rounded general capability | Not ideal for deep reasoning tasks |
| Great for real-time applications | Limited multilingual performance |
| Active development and community | Superseded by Mistral Nemo / Mistral Large for complex work |

> **Verdict:** Best when speed is more important than depth

---

### 9. Gemma 3 (Google)
**Category:** General Purpose — Efficient | **Params:** 1B – 27B | **Size:** 0.8 GB – 17 GB | **RAM:** 4 GB (1B) to 16 GB (27B) | **Context:** 128K tokens

**Best For:** Conversational AI, simple chat tools, content generation, research assistance, on-device apps

| ✅ Pros | ❌ Cons |
|---|---|
| 28M+ downloads | Weaker than Llama 3.1 8B on complex tasks |
| Highly memory efficient (Flash Attention) | Less community support than Meta models |
| Strong instruction following | Tends toward shorter responses |
| Multiple practical sizes | Not ideal for specialized coding tasks |
| Good for privacy-first deployment | Limited tool use compared to Llama 3.1 |

> **Verdict:** Great lightweight option with Google quality

---

### 10. Phi-4 (Microsoft)
**Category:** Small but Mighty | **Params:** 14B | **Size:** 8.9 GB | **RAM:** 16 GB RAM | **Context:** 16K tokens

**Best For:** Reasoning, STEM tasks, structured problem-solving, offline use on mid-tier hardware

| ✅ Pros | ❌ Cons |
|---|---|
| Punches well above its weight class | Smaller context window (16K) |
| State-of-the-art for the 14B range | Less strong on open-ended creative tasks |
| Strong math and scientific reasoning | Not as broadly general as Llama models |
| Fast on consumer hardware | Limited multilingual capability |
| Good structured output | Smaller ecosystem and community |

> **Verdict:** Best reasoning per GB for mid-tier hardware

---

### 11. Phi-3 Mini (Microsoft)
**Category:** Edge / Efficient | **Params:** 3.8B | **Size:** 2.2 GB | **RAM:** 4 GB RAM | **Context:** 128K tokens

**Best For:** Offline apps, edge devices, quick Q&A, field use, low-bandwidth environments

| ✅ Pros | ❌ Cons |
|---|---|
| Matches much larger models on MMLU benchmarks | Struggles with complex multi-step reasoning |
| Runs on phones and Raspberry Pi-class hardware | Limited creative writing ability |
| Very long context for its size (128K) | Not suited for heavy coding projects |
| Great for offline deployments | Small community vs. Meta |
| Consistently good instruction following | Can feel shallow on open-ended prompts |

> **Verdict:** Best tiny model for real-world offline use

---

### 12. DeepSeek Coder V2
**Category:** Coding Specialist | **Params:** 16B / 236B MoE | **Size:** 9 GB / 133 GB | **RAM:** 16 GB / 80 GB+ | **Context:** 128K tokens

**Best For:** Code generation, debugging, cross-file refactoring, code review, multi-language projects

| ✅ Pros | ❌ Cons |
|---|---|
| Supports 300+ programming languages | MoE version needs serious hardware |
| Trained on 2 trillion code tokens | Less capable for non-code tasks |
| Excellent cross-file context awareness | Large download for top tier variant |
| Strong on competitive coding benchmarks | Can be slower than smaller models |
| MoE version rivals GPT-4 on code tasks | Niche focus — not a general-purpose model |

> **Verdict:** Top coding model available locally

---

### 13. CodeLlama (7B / 13B / 34B)
**Category:** Coding Specialist | **Params:** 7B / 13B / 34B | **Size:** 3.8 GB / 7.4 GB / 19 GB | **RAM:** 8 GB / 16 GB / 32 GB | **Context:** 16K tokens

**Best For:** Code generation, completion, debugging in 20+ languages, IDE integration, code chat

| ✅ Pros | ❌ Cons |
|---|---|
| Purpose-built for code by Meta | Smaller context window (16K) |
| Multiple size options | Superseded by DeepSeek Coder V2 on benchmarks |
| Well-tested and widely used | Less capable on latest language features |
| Great for IDE assistant integration | No vision or multimodal support |
| Good Python, JS, and C++ performance | Less active development now |

> **Verdict:** Reliable workhorse for everyday coding tasks

---

### 14. Mixtral 8x7B / 8x22B
**Category:** Mixture of Experts | **Params:** 46.7B / 141B total (12.9B / 39B active) | **Size:** 26 GB / 80 GB | **RAM:** 48 GB / 96 GB | **Context:** 32K tokens

**Best For:** Fast high-quality inference, coding, multilingual tasks, applications needing 70B quality at lower compute cost

| ✅ Pros | ❌ Cons |
|---|---|
| Only activates ~25% of parameters per token | Total model size still very large |
| Much faster than equivalent dense model | Needs high RAM even for 8x7B |
| Strong multilingual performance | Smaller context (32K) vs. newer models |
| Good coding quality | Complex architecture for fine-tuning |
| Efficient at scale | Licensing is more restrictive than Llama |

> **Verdict:** Best efficiency ratio for high-end hardware

---

### 15. LLaVA 1.6
**Category:** Multimodal / Vision | **Params:** 7B / 13B / 34B | **Size:** 4.7 GB / 8 GB / 20 GB | **RAM:** 8 GB / 16 GB / 32 GB | **Context:** 4K tokens

**Best For:** Image Q&A, scene description, visual document reading, basic OCR, multimodal chat

| ✅ Pros | ❌ Cons |
|---|---|
| Accessible entry into local vision models | Smaller context window (4K) |
| Multiple size options | Not as strong as Llama 3.2-Vision |
| Combines Vicuna + vision encoder | Image resolution limitations |
| Easy to deploy | Older architecture |
| Good for general image understanding | Being superseded by newer vision models |

> **Verdict:** Good starter vision model, now largely superseded by Llama 3.2-Vision

---

### 16. Command-R / Command-R+ (Cohere)
**Category:** Enterprise / RAG | **Params:** 35B / 104B | **Size:** 21 GB / 59 GB | **RAM:** 32 GB / 64 GB | **Context:** 128K tokens

**Best For:** Retrieval-Augmented Generation (RAG), enterprise chat, tool use, multi-step agentic tasks

| ✅ Pros | ❌ Cons |
|---|---|
| Designed specifically for RAG pipelines | Very large model sizes |
| Excellent tool use and function calling | Slower than smaller alternatives |
| Strong citation and grounding behavior | Less community support than Meta models |
| Commercial-grade quality | Overkill for simple chat use cases |
| Long context handling | Requires significant hardware investment |

> **Verdict:** Best for enterprise RAG and agentic workflows

---

### 17. Dolphin 2.9 (Uncensored)
**Category:** Uncensored / Creative | **Params:** 8B / 70B | **Size:** 4.9 GB / 40 GB | **RAM:** 8 GB / 64 GB | **Context:** 8K tokens

**Best For:** Fiction writing, creative storytelling, open-ended tasks, roleplay, research without filters

| ✅ Pros | ❌ Cons |
|---|---|
| No safety filters for creative freedom | No safety guardrails — use responsibly |
| Based on strong Llama 3 base model | Shorter context window (8K) |
| Excellent for fiction and narrative writing | Not suitable for production or public apps |
| Good for sensitive research topics | Can produce harmful content if misused |
| Active community and regular updates | Ethically complex deployment |

> **Verdict:** Best for unconstrained creative writing

---

### 18. Nomic Embed Text
**Category:** Embeddings | **Params:** 137M | **Size:** 0.3 GB | **RAM:** 2 GB RAM | **Context:** 8K tokens

**Best For:** Semantic search, RAG vector databases, document similarity, clustering, classification

| ✅ Pros | ❌ Cons |
|---|---|
| Tiny footprint (0.3 GB) | Text-only — no generation capability |
| High-performing embedding model | Not for chat or Q&A directly |
| Open weights | Requires a separate generation model for full RAG |
| Very fast generation | Limited to retrieval/similarity tasks |
| Works great with local vector DBs (Chroma, Qdrant, etc.) | Less useful as a standalone tool |

> **Verdict:** Essential companion for any local RAG pipeline

---

### 19. TinyLlama (1.1B)
**Category:** Ultra-Lightweight | **Params:** 1.1B | **Size:** 0.6 GB | **RAM:** 2 GB RAM | **Context:** 2K tokens

**Best For:** Testing, CI/CD pipelines, very low-power hardware, basic text classification, demos

| ✅ Pros | ❌ Cons |
|---|---|
| Loads in seconds | Very limited reasoning ability |
| Works on nearly any hardware | Tiny context window (2K) |
| Useful for automation scripts | Not suitable for real-world work tasks |
| Good for quick concept testing | Often gives shallow or incomplete answers |
| Smallest possible footprint | Easily outclassed by Phi-3 Mini for real use |

> **Verdict:** For testing and automation pipelines only

---

### 20. OpenAI GPT Open-Weights (o1 / o3-mini)
**Category:** Reasoning — OpenAI Open-Weight | **Params:** Varies | **Context:** 128K tokens

**Best For:** Complex problem solving, agentic tasks, advanced reasoning, developer workflows

| ✅ Pros | ❌ Cons |
|---|---|
| OpenAI research quality in open-weight release | Newer — less community documentation |
| Powerful reasoning and agentic capability | Hardware requirements still being mapped |
| Strong benchmark performance | Licensing terms may restrict some commercial use |
| Versatile for developer use cases | Less tested locally vs. established Meta models |
| Backed by OpenAI research pipeline | Unknown long-term open-weight commitment |

> **Verdict:** Watch this space — promising newcomer from OpenAI

---

## Understanding Quantization (How to Shrink Models)

When pulling a model in Ollama, you can specify a quantization level to trade a small amount of quality for dramatically less disk and RAM usage.

| Tag | Quality | Size Reduction | Best Used For |
|---|---|---|---|
| `Q8_0` | Near lossless | ~50% vs FP16 | Maximum quality, enough VRAM |
| `Q5_K_M` | Excellent ⭐ recommended | ~60% vs FP16 | Sweet spot — best quality/size tradeoff |
| `Q4_K_M` | Very good | ~70% vs FP16 | Most users — fast with minor quality loss |
| `Q4_0` | Good (older method) | ~70% vs FP16 | Legacy — use Q4_K_M instead |
| `Q2_K` | Acceptable | ~80% vs FP16 | Very limited hardware — noticeable quality drop |

**Pro Tip:** Start with `Q5_K_M` or `Q4_K_M` for the largest model your hardware can comfortably fit.

```bash
# Example: pull Llama 3.3 70B with Q4 quantization
ollama pull llama3.3:70b-instruct-q4_K_M
```

---

*Note: Model sizes shown are approximate for default quantization. Sizes and hardware requirements vary by quantization level. Hardware requirements are estimates for comfortable local inference — you may be able to run models with less RAM using CPU offloading at slower speeds. Data current as of early 2026.*
