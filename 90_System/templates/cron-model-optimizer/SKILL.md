---
name: cron-model-optimizer
version: 1.0.0
description: "Optimize cron job model assignments to reduce cost without sacrificing quality. Use when: (1) reviewing cron jobs for cost optimization, (2) choosing which LLM model to assign to a new or existing cron job, (3) assessing task complexity to pick the right model tier. Triggers on phrases like \"optimize cron models\", \"reduce cron costs\", \"which model for this cron job\", \"cron cost analysis\", \"save money on cron\"."
metadata:
  category: general
---

# Cron Model Optimizer

Assess cron job complexity and assign the most cost-effective model.

## Recommended Models (Genspark LLM Proxy)

One best pick per price tier. Relative cost indexed to cheapest = 1x.

| Tier | Model ID | Ctx | Reasoning | Cost | Provider | When to use |
|------|----------|-----|-----------|------|----------|-------------|
| 🟢 Budget | `gpt-5.4-nano` | 400K | ✅ | **1x** | openai-compat | Cheapest with reasoning |
| 🟢 Budget | `gemini-3.1-flash-lite-preview` | 1M | ❌ | **1.2x** | gemini¹ | Cheapest 1M; simple summarize |
| 🟢 Budget | `minimax-m2p5` | 128K | ❌ | **1.5x** | openai-compat | Budget, text only |
| 🟡 Economy | `kimi-k2p5` | 128K | ❌ | **2x** | openai-compat | Budget alternative |
| 🟡 Economy | `gemini-3-flash-preview` | 1M | ✅ | **2x** | gemini¹ | Best value: reasoning + 1M |
| 🟡 Economy | `gpt-5.4-mini` | 400K | ✅ | **3x** | openai-compat | Strong reasoning, good tool calling |
| 🟠 Standard | `claude-sonnet-4-6` | 200K | ✅ | **10x** | openai-compat | Best general-purpose |
| 🟠 Standard | `claude-opus-4-6` | 200K | ✅ | **17x** | openai-compat | Top quality, 200K context |
| 🔴 Premium | `claude-sonnet-4-6-1m` | 1M | ✅ | **20x** | openai-compat | Sonnet quality + 1M context |
| 🔴 Premium | `claude-opus-4-6-1m` | 1M | ✅ | **33x** | openai-compat | Top quality + 1M context |

¹ Gemini models require separate `genspark-gemini-proxy` provider (different API protocol). All others share `genspark-llm-proxy`.

### Provider Config

**OpenAI-compatible** (Claude, GPT, Kimi, MiniMax) — all share one provider:
```jsonc
"genspark-llm-proxy": {
  "baseUrl": "https://www.genspark.ai/api/llm_proxy/v1",
  "api": "openai-completions",
  "models": [{ "id": "<model-id>", ... }]
}
```

**Gemini** — must use a separate provider (server routes and protocol differ):
```jsonc
"genspark-gemini-proxy": {
  "baseUrl": "https://www.genspark.ai/api/llm_proxy/gemini/v1beta",
  "api": "google-generative-ai",
  "models": [{ "id": "<model-id>", ... }]
}
```

Same `apiKey` (gsk token) works for both.

## Task Complexity Assessment

Evaluate each cron job across 4 dimensions. Score each Low=1 / Medium=2 / High=3.

### Dimension 1: Tool Call Volume & Pattern

| Score | Description | Example |
|-------|-------------|---------|
| 1 | 1–5 fixed calls, no branching | Fetch 3 stock prices → compare thresholds |
| 2 | 5–15 fixed calls | 8 Twitter searches → summarize |
| 3 | 15+ calls, dynamic/conditional branching | Search → pick best → crawl those → analyze |

### Dimension 2: Reasoning Depth

| Score | Description | Example |
|-------|-------------|---------|
| 1 | Template match, threshold compare | VIX > 35 → alert |
| 2 | Summarization, trend identification | Synthesize 10 articles into 5-line brief |
| 3 | Multi-factor judgment, strategy decisions | Evaluate Greeks + war signals → trade decision |

### Dimension 3: Output Complexity

| Score | Description | Example |
|-------|-------------|---------|
| 1 | Fixed format, short | "VIX 22.5 \| SPY $540" |
| 2 | Structured report, templated | 15-line formatted briefing |
| 3 | Dynamic format + API writes | Generate HTML → upload Google Doc → push Telegram |

### Dimension 4: External API Sensitivity

| Score | Description | Example |
|-------|-------------|---------|
| 1 | Read-only, tolerates errors | gsk search, gsk stock |
| 2 | Write APIs, fixed patterns | gws docs create (same command each time) |
| 3 | Write APIs, dynamic params / code execution | Python trading code, browser automation |

### Score → Model Tier

| Total | Complexity | Recommended |
|-------|-----------|-------------|
| 4–5 | 🟢 Simple | `gemini-3.1-flash-lite-preview` (1x) |
| 6–7 | 🟡 Moderate | `gpt-5.4-mini` (3x) |
| 8–9 | 🟠 Complex | `claude-sonnet-4-6` (10x) |
| 10–12 | 🔴 Critical | `claude-opus-4-6-1m` (33x) |

### Common Patterns

**Pattern A — Data Fetch → Threshold → Alert** (score ~4, 🟢)
Stock monitor, uptime check. All fixed calls, number comparison, template output.
→ `gemini-3.1-flash-lite-preview`

**Pattern B — Multi-Source Scrape → Summarize** (score ~6, 🟡)
Twitter scan, news digest. Many fixed calls, synthesis needed, brief output.
→ `gpt-5.4-mini`

**Pattern C — Research → Report → Publish** (score ~9, 🟠)
Daily briefing, morning report. Dynamic crawling, analysis, Google Doc write.
→ `claude-sonnet-4-6`

**Pattern D — Analyze → Decide → Execute** (score ~11, 🔴)
Trading bot, auto-responder. Dynamic tools, multi-factor decisions, code execution.
→ `claude-opus-4-6-1m`

**Pattern E — Read → Structured Doc → Upload** (score ~8, 🟠)
Teams daily report. Medium tools, thematic grouping, HTML + Google Doc.
→ `claude-sonnet-4-6`

## Workflow

### 1. List current cron jobs
```
cron(action=list)
```
For each `isolated` / `agentTurn` job, note: current model, frequency, payload prompt.

### 2. Score each job
Apply the 4-dimension framework above. Read the payload prompt carefully — the complexity is in the prompt, not the job name.

### 3. Check provider config
```
gateway(action=config.get, path=models.providers)
```
If a needed model or provider is missing, add via `config.patch`. Remember: Gemini needs its own provider.

### 4. Update jobs
```
cron(action=update, jobId=<id>, patch={
  "payload": { ...full_existing_payload, "model": "<provider>/<model-id>" }
})
```
Include the **full payload** in the patch (kind, message, timeoutSeconds, model) — not just the model field.

### 5. Verify
Optionally trigger one job to test: `cron(action=run, jobId=<id>)`. Monitor next few runs for errors. If a downgraded model fails (missed tool calls, bad output), upgrade one tier.

## Optimization Priority

High-frequency jobs save the most. Prioritize by runs/day:

| Frequency | Runs/day | Optimize first? |
|-----------|----------|----------------|
| 15 min | 96 | 🔴 Yes — biggest savings |
| 30 min | 48 | 🔴 Yes |
| 1 hour | 24 | 🟡 Medium |
| 4 hours | 6 | 🟢 Low priority |
| 1/day | 1 | 🟢 Lowest — quality matters more |

## Rules

- **Never downgrade** jobs that execute trades or write to financial accounts
- `sessionTarget: "main"` + `payload.kind: "systemEvent"` uses the main session model — cannot override per-job
- Always preserve the full payload message when updating
- Test one run after changing before leaving unmonitored
- If a job needs browser automation or image understanding, avoid `gemini-3.1-flash-lite-preview` (weaker at visual tasks)

