# Observability and Monitoring

The most expensive blind spot in enterprise AI programs today is not the model bill. It is the absence of operational visibility into what the prompt library is actually doing in production. Without observability, "the prompt is working" is a vibe, not a fact. This document defines the observability model this library is designed to support.

The repository itself does not include a running observability stack. That belongs in a platform layer alongside the model gateway, the logging pipeline, and the analytics warehouse. What the repository does include is the **architecture philosophy, the metrics that matter, the governance logic that ties them to action, and the log schema downstream systems should emit.**

---

## Philosophy

Observability for a prompt library is not the same as observability for an application backend. The system under observation is the **interaction between a prompt, a model, an input, and a human reviewer**. The right metrics measure that interaction, not just CPU and latency.

Four principles shape the model:

1. **Every prompt call is a logged event.** No silent calls, no untracked retries, no "I tested it once and it worked."
2. **Quality is measured continuously, not just at release.** Eval cases run on every prompt change, but they also sample production traffic to detect drift the eval suite did not anticipate.
3. **Human corrections are the most valuable signal in the system.** When an advisor edits, rejects, or escalates a prompt output, that is gold-standard feedback about what the prompt actually got wrong.
4. **Cost is a first-class operational metric.** Tier usage, output length, and per-prompt unit economics are observed alongside quality, because cost drift is a real failure mode.

---

## The metrics that matter

The metrics below are organized into four categories. Each is something a real AI operations team should be looking at weekly, with thresholds that trigger review.

### Quality and reliability

| Metric | Definition | Healthy band | Action threshold |
|---|---|---|---|
| Prompt success rate | % of calls where the output passed automated validation (schema, required fields, prohibited-phrase scan) | ≥ 98% | < 95% triggers prompt review |
| Human correction frequency | % of outputs that the advisor materially edited before use | ≤ 25% | > 40% triggers prompt review |
| Average edit distance | Levenshtein distance between model output and final advisor-edited version, normalized by output length | ≤ 0.20 | > 0.35 triggers prompt review |
| Escalation frequency | % of calls that the advisor flagged for compliance or supervisor review | Baseline-dependent | Statistically significant week-over-week increase triggers review |
| Hallucination incident rate | Confirmed hallucinations per 10,000 calls, identified via citation-check or human flag | Target near zero | Any confirmed incident triggers root-cause review |
| Refusal correctness | % of refusals that were genuinely appropriate (vs over-refusal of legitimate requests) | ≥ 90% | < 80% triggers system prompt review |

### Cost and efficiency

| Metric | Definition | Healthy band | Action threshold |
|---|---|---|---|
| Cost per call vs declared `max_cost_per_call_usd` | Actual vs budgeted | Within 10% | > 25% over triggers review |
| Output token p50 vs `target_output_tokens` | Median actual output length vs declared target | Within 25% | > 50% over triggers length-discipline review |
| Output token p95 | 95th percentile output length | < `max_output_tokens` | At ceiling consistently means the ceiling is too low or the prompt is under-specified |
| Model tier usage distribution | Share of calls per tier across the library | Stable | Drift toward higher tiers triggers tier-rationale review |
| Cache hit rate (where applicable) | % of input prompt tokens served from cache | ≥ 60% on system prompts | < 30% means prompt is changing too often or caching is misconfigured |

### Adoption and user experience

| Metric | Definition | Healthy band | Action threshold |
|---|---|---|---|
| Active prompt usage per advisor per week | Calls per advisor per active prompt | Prompt-dependent | Sharp drop suggests prompt is failing users; sharp rise on tier-3 suggests routing leak |
| Time-to-completion delta | Time to complete the underlying workflow with vs without the prompt | Net positive | Net negative means the prompt is creating work, not saving it |
| User satisfaction score | Periodic 1-5 advisor rating per prompt | ≥ 4.0 | < 3.5 triggers prompt review |
| Adoption breadth | % of eligible advisors who used the prompt in the last 30 days | Prompt-dependent | Decline > 20% MoM triggers review |

### Governance and drift

| Metric | Definition | Healthy band | Action threshold |
|---|---|---|---|
| Evaluation drift | Change in eval-case pass rate on production-sampled inputs vs at-release baseline | Stable | Drop > 5 pts triggers re-evaluation; > 10 pts triggers rollback consideration |
| Days since last review | Time since last governance review per prompt | Within `review_cadence` declared in metadata | Any prompt past its declared cadence is non-compliant |
| Prohibited phrase emission rate | Rate at which the production-side scanner catches forbidden language in outputs | Near zero | Any emission triggers immediate prompt review |
| Schema validation failure rate | % of structured-output calls that produced invalid JSON | < 0.5% | > 2% triggers schema or prompt review |

---

## Log schema

Every prompt call should emit a single structured log event with at least the following fields. This is the canonical event shape downstream observability infrastructure should expect.

```json
{
  "event_id": "uuid",
  "timestamp": "ISO-8601",
  "prompt_id": "client-meeting-summary",
  "prompt_version": "1.0.0",
  "model": "claude-sonnet-4-6-20260301",
  "model_tier": "tier-2-standard",
  "advisor_id": "hashed_id",
  "branch_id": "hashed_id",
  "input_tokens": 6726,
  "output_tokens": 812,
  "latency_ms": 4280,
  "cost_usd": 0.0324,
  "schema_validation": "pass | fail | n/a",
  "prohibited_phrase_scan": "pass | fail",
  "compliance_flags": [],
  "human_review_status": "drafted | edited | accepted | rejected | escalated",
  "edit_distance": 0.12,
  "advisor_satisfaction_score": null,
  "supervisor_review_required": false,
  "retention_class": "client_communication | internal | transient",
  "eval_drift_sample": true
}
```

PII and client identifiers are hashed at the gateway before the event is emitted. `eval_drift_sample` is set on the random 1% of calls selected for drift monitoring, so the same record can be replayed against the prompt's eval suite to detect production-vs-eval skew.

---

## Example dashboards

Three dashboards cover most of the operational surface:

**1. Library Health (daily).** Per-prompt rows showing success rate, correction frequency, p50/p95 output tokens, cost per call vs budget, days since last review, and a red/yellow/green health flag computed from the action thresholds above.

**2. Cost and Tier Distribution (weekly).** Stacked bar by tier showing total calls and total cost. A second view shows per-prompt tier usage over time, flagging any prompt whose tier-3 share is growing (a sign the tier is leaking).

**3. Quality and Drift (weekly).** Eval pass rate on production-sampled inputs vs at-release baseline, per prompt, plotted as a time series. Sharp drops are the leading indicator of a prompt that needs re-evaluation, often before users notice.

---

## What triggers what

Observability without action is decoration. The library defines explicit governance triggers tied to the metrics above:

- **Prompt review** is automatically opened when any prompt crosses an action threshold for two consecutive weekly reviews.
- **Mandatory re-evaluation** is triggered by an evaluation-drift drop greater than 5 points, a confirmed hallucination incident, or a policy change that touches the prompt's domain.
- **Rollback consideration** is triggered by an eval-drift drop greater than 10 points, a prohibited-phrase emission, or a compliance escalation rate that doubles week-over-week.
- **Sunset review** is triggered by adoption breadth falling below 10% of eligible users for two consecutive quarters, suggesting the prompt is no longer earning its operational overhead.

These triggers exist so that "we will look at the data" becomes "the data tells us when to look."

---

## What this is and is not

This is the architecture and governance contract for observability. It is not a working pipeline. The pipeline lives in whatever telemetry, logging, and warehouse infrastructure the firm already runs — typically some combination of an API gateway, a structured log forwarder, a warehouse like Snowflake or BigQuery, and a BI layer like Tableau, Looker, or a custom dashboard.

The point of having the architecture defined inside the prompt library, rather than handled entirely downstream, is that **the prompt library is where the definitions live**. The metrics, thresholds, and triggers above are part of the governance contract of each prompt, not separate operational policy. That is what makes the library auditable as an operational asset rather than a folder of text files.
