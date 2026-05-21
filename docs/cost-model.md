# Cost Model

This document shows the real cost impact of model tiering across the six prompts in this library. Numbers use **actual measured token counts** of the prompts in this repo and **verified public list pricing** as of May 2026. The methodology is reproducible from `scripts/cost_model.py`.

This is a mock portfolio repository. Volume assumptions are illustrative and sized to enterprise wirehouse / IBD scale (approximately 9,000 advisors, comparable to Raymond James Financial's reported headcount of 8,943 at FY2025 year-end). Per-prompt frequency estimates are based on reasonable advisor workflow assumptions, not actual firm telemetry.

---

## Pricing inputs (verified May 2026)

| Model | Input $/MTok | Output $/MTok | Source |
|---|---:|---:|---|
| Claude Haiku 4.5 | $1.00 | $5.00 | [anthropic.com](https://www.anthropic.com/news/claude-haiku-4-5) |
| Claude Sonnet 4.6 | $3.00 | $15.00 | [anthropic.com](https://www.anthropic.com/pricing) |
| Claude Opus 4.7 | $5.00 | $25.00 | [anthropic.com](https://www.anthropic.com/pricing) |
| GPT-5.4-nano | $0.20 | $1.25 | [openai.com/api/pricing](https://openai.com/api/pricing/) |
| GPT-5.4-mini | $0.75 | $4.50 | [openai.com/api/pricing](https://openai.com/api/pricing/) |
| GPT-5.4 | $2.50 | $15.00 | [openai.com/api/pricing](https://openai.com/api/pricing/) |
| Gemini 2.5 Flash | $0.30 | $2.50 | [ai.google.dev](https://ai.google.dev/gemini-api/docs/pricing) |

All rates are per million tokens (MTok), standard tier, no caching discount applied. Caching and batch discounts (typically 50–90% off cached input) would reduce all numbers proportionally but do not change the relative tiering math.

---

## Methodology

**Per-call input tokens** = `system.md tokens + user-template.md tokens + runtime input variables tokens`

System prompts and user templates are measured directly from the repo using the `cl100k_base` tokenizer (close approximation across vendors; Claude tokenizer differs by 10–15% in practice). Runtime input variable sizes (transcript, CRM notes, holdings tables, etc.) are estimated per prompt based on realistic FA workflows. Output token sizes are estimated based on each prompt's expected response shape (short JSON vs full email vs multi-section brief).

**Volume assumption:** 9,000 advisors × 220 trading days × prompt-specific calls-per-advisor-per-day.

---

## Per-prompt measurements

| Prompt | Tier | Input tokens | Output tokens | Calls/yr | $/call (recommended) |
|---|---|---:|---:|---:|---:|
| crm-note-assistant | tier-1-light | 892 | 300 | 7,920,000 | $0.0024 |
| advisor-meeting-prep | tier-2-standard | 3,280 | 600 | 2,970,000 | $0.0063 |
| client-meeting-summary | tier-2-standard | 6,726 | 800 | 2,970,000 | $0.0107 |
| internal-policy-search | tier-2-standard | 3,636 | 500 | 3,960,000 | $0.0061 |
| client-follow-up-email | tier-3-reasoning | 2,386 | 350 | 1,980,000 | $0.0124 |
| portfolio-review-prep | tier-3-reasoning | 5,209 | 1,200 | 594,000 | $0.0336 |

Total: **20.4M calls/year** across these six prompts at the assumed scale.

---

## Annual cost comparison

| Prompt | Recommended tier | All on Sonnet 4.6 | All on Opus 4.7 |
|---|---:|---:|---:|
| crm-note-assistant (Haiku) | $18,945 | $56,834 | $94,723 |
| advisor-meeting-prep (Haiku) | $18,652 | $55,955 | $93,258 |
| client-meeting-summary (Haiku) | $31,856 | $95,569 | $159,281 |
| internal-policy-search (Haiku) | $24,299 | $72,896 | $121,493 |
| client-follow-up-email (Sonnet) | $24,568 | $24,568 | $40,946 |
| portfolio-review-prep (Sonnet) | $19,974 | $19,974 | $33,291 |
| **TOTAL** | **$138,293** | **$325,795** | **$542,992** |

**Savings vs Sonnet-as-default:** $187,502/yr (57.6% reduction)
**Savings vs Opus-as-default:** $404,699/yr (74.5% reduction)

---

## Projection: 50-prompt library

Six prompts is a starting point. Enterprise prompt libraries typically grow to 40–100 production prompts over 12–18 months. Holding the same tier distribution (8 tier-1, 25 tier-2, 17 tier-3) and the same per-prompt usage averages:

| Scenario | Annual cost |
|---|---:|
| Recommended tiering | **$1,291,562** |
| All on Sonnet 4.6 | $2,867,486 |
| All on Opus 4.7 | $4,779,144 |

At a 50-prompt library, correct tiering saves **$1.58M/yr vs Sonnet-default** or **$3.49M/yr vs Opus-default**.

---

## What this is and is not

**This is:** A reproducible cost model using real measured prompts and current public pricing. The numbers move with prompt design, model pricing, and volume — all of which are explicit inputs.

**This is not:** A claim about any specific firm's actual usage, an Anthropic-vs-OpenAI procurement recommendation, or an estimate of total firm AI spend. Embedding costs, fine-tuning, evaluation infrastructure, vector stores, gateway overhead, and observability are out of scope here.

**Caveats worth naming in any executive presentation:**
1. Token counts are tokenizer-approximate; actual billed tokens may differ ±10–15% per vendor.
2. Caching can reduce repeat-system-prompt cost by ~90% — material for chatty workflows but doesn't change tier choice.
3. Real workloads include retries, failed evals, and tool-call rounds — typical multiplier 1.2–1.5x.
4. Higher tiers have higher first-call latency, which has its own UX and productivity cost not modeled here.

The point of the model isn't the absolute dollar amount. It's that **correct tiering is a 50–75% cost reduction with no quality loss on prompts where the cheaper tier passes evals.** That's the lever.
