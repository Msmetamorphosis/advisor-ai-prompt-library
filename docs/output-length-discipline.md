# Output Length Discipline

If model tiering is the largest available cost lever in a prompt library, **output length discipline is the second largest** — and the two compound. This document explains why, how this library enforces it, and how to teach it to prompt authors and end users.

---

## The 5x rule

On every major model vendor's current pricing card, **output tokens cost approximately 5x more than input tokens.**

| Model | Input $/MTok | Output $/MTok | Ratio |
|---|---:|---:|---:|
| Claude Haiku 4.5 | $1.00 | $5.00 | 5.0x |
| Claude Sonnet 4.6 | $3.00 | $15.00 | 5.0x |
| Claude Opus 4.7 | $5.00 | $25.00 | 5.0x |
| GPT-5.4 | $2.50 | $15.00 | 6.0x |
| GPT-5.4-mini | $0.75 | $4.50 | 6.0x |
| Gemini 2.5 Flash | $0.30 | $2.50 | 8.3x |

The implication is that an unconstrained 1,200-token meeting summary is not "a bit more expensive" than a tight 400-token one. The output portion of the bill is **3x higher**, on the side of the ledger that already dominates total cost for any prompt with even a modest response length.

Worked example using Sonnet 4.6 with a 3,000-token input:
- 400-token output: input cost $0.009 + output cost $0.006 = **$0.015/call**
- 1,200-token output: input cost $0.009 + output cost $0.018 = **$0.027/call**

The input cost is identical. The output cost — and total cost — nearly doubles, for output the user almost certainly did not want to read in full anyway.

At 9,000 advisors x 220 days x 1.5 calls/day, that's a **$35,640/year delta on a single prompt** caused entirely by failing to set a length ceiling.

---

## What this library does about it

Every `prompt.yaml` in this library declares three fields that, together, make output length a governed concern instead of a hopeful suggestion:

```yaml
max_output_tokens: 600
target_output_tokens: 450
response_length_guidance: >
  Single-page meeting brief. Bullet structure preferred over prose. Omit
  preamble like "Here is the brief you requested." Stop after the
  "Open questions" section.
```

- **`max_output_tokens`** is the hard ceiling. The gateway enforces it via the `max_tokens` API parameter. The model cannot exceed it.
- **`target_output_tokens`** is the expected typical length. Used by evals to flag prompts whose actual outputs consistently run hot.
- **`response_length_guidance`** is the natural-language instruction baked into `system.md` so the model itself understands what it is being asked to produce. The API ceiling is a backstop; the prompt-level guidance is the primary mechanism.

Every `system.md` ends with explicit length constraints, not just at the top of the prompt where they will be forgotten by the time the model is generating output.

The validation suite enforces:
1. Every prompt declares `max_output_tokens` and `target_output_tokens`.
2. `target_output_tokens` is at most 80% of `max_output_tokens` (the gap is the safety margin for legitimate variance).
3. The system prompt contains an explicit length instruction matching the metadata.
4. Eval cases include at least one case that tests **output verbosity** — an input that would tempt the model to over-produce.

---

## Teaching the discipline to prompt authors

The most common mistakes prompt authors make when designing output:

1. **No length instruction at all.** The model defaults to whatever the post-training distribution produces, which for current frontier models is "thorough" — often 2x to 4x what the user actually needs.
2. **Length instruction only in the user message.** By the time the model has read 2,000 tokens of input variables, the early "be concise" instruction is forgotten. **Length instructions belong in `system.md`, repeated near the response section.**
3. **Vague language** like "be concise" or "keep it short." Concise relative to what? Use numeric targets ("3-5 bullets", "under 200 words", "stop after the actionable items section").
4. **Allowing preamble and postamble.** "Here is the summary you requested:" and "Let me know if you'd like me to elaborate." each cost real money at scale. Forbid them explicitly.
5. **Open-ended structural prompts.** "Provide your analysis" invites essays. "Provide exactly three observations and two recommended actions" produces a bounded artifact.

The rule of thumb baked into this library: **if you can't describe the expected output length in one sentence, the prompt is under-specified.**

---

## Teaching the discipline to end users

End users — advisors, in this library's domain — also need to learn the lever, because they will be writing ad-hoc instructions inside the prompts the library provides. The training points worth communicating:

1. **You are paying for verbosity.** A model asked to "summarize this meeting" without a length cap produces, on average, 3x more output than is useful. That output costs 5x what the input costs.
2. **Length lives in the request.** "Summarize this meeting in 5 bullets" routinely produces a sharper artifact than "summarize this meeting" — and costs roughly a third as much.
3. **Stop sequences matter.** If you only need the first section, ask for only the first section. Do not generate the whole report and then read the first paragraph.
4. **Structured outputs are usually shorter.** JSON-with-required-fields produces tighter responses than free-form prose for the same information density.
5. **Re-asking is cheaper than over-producing.** It is almost always cheaper to ask a short follow-up than to ask for "thorough" output upfront, because the follow-up only generates the missing piece, not the whole thing again.

---

## The combined lever

Model tiering reduces cost by routing each task to the cheapest model that passes its evals. Output length discipline reduces cost by ensuring every model — at any tier — only generates the tokens that matter.

Together, on the six prompts in this library, the difference between "default to the best model, generate as much as it wants" and "tier correctly, constrain output" is roughly **5x to 10x** depending on prompt mix. That is the gap between an AI program that scales sustainably and one that quietly outgrows its budget every quarter.

Reproducible numbers are in `docs/cost-model.md`. The output-length comparison can be regenerated by running the cost scripts with the `disciplined` vs `unconstrained` output sizes documented in `scripts/cost_model.py`.
