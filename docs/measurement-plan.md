# Measurement Plan

The library is a program, not a side project. Programs are judged by outcomes. This document defines the metrics used to evaluate whether the library is delivering value, where it is failing, and where the next investment should go.

Metrics are tracked **per prompt** and **across the library** at agreed cadences. Each metric has a definition, a target, and a measurement method. Where measurement requires telemetry not present in this mock repo, the method is documented as the deployment-time requirement.

---

## Outcome Metrics

These are the metrics the business cares about.

### 1. Time Saved

**Definition:** Minutes the advisor would have spent on the task without the library, minus minutes spent including review.
**Target:** ≥30% reduction per task; ≥3 minutes absolute saving for prompts used multiple times daily.
**Method:** Sampled time-and-motion studies during pilot. Self-reported time logs during production with periodic validation.

### 2. Adoption Rate

**Definition:** Percentage of advisors in the target population who used the prompt in the last 30 days.
**Target:** ≥40% within 3 months of release; ≥60% within 6 months.
**Method:** Invocation telemetry at the gateway. Lack of adoption is treated as a signal the workflow placement is wrong, not that advisors are at fault.

### 3. Prompt Reuse Rate

**Definition:** Average number of invocations per active advisor per week.
**Target:** Workflow-specific; baseline established during pilot.
**Method:** Gateway telemetry.

### 4. Reduction in Duplicate Prompt Requests

**Definition:** Volume of intake issues that ask for an existing prompt.
**Target:** Decline over time as the library and discovery improve.
**Method:** Intake-issue triage tag counts.

---

## Quality Metrics

These are the metrics the AI Enablement team uses to keep the library healthy.

### 5. Advisor Edit Distance

**Definition:** Levenshtein (or comparable) distance between draft and final, normalized by draft length.
**Target:** ≤20% on average for client-facing prompts; ≤10% for internal-only prompts.
**Method:** Capture draft + final in the advisor tool; compute distance asynchronously. Anonymized.

### 6. Schema Compliance

**Definition:** Percentage of structured-output invocations whose result validates against the declared `output-schema.json`.
**Target:** ≥99%.
**Method:** Validator pipeline at the gateway.

### 7. Hallucination Rate

**Definition:** Eval-case-level rate of any output scoring <4 on Hallucination Resistance.
**Target:** 0% on the regression suite at every release.
**Method:** Re-run of the eval suite at every release and on every underlying-model upgrade. Sampled in production.

### 8. Review Flag Accuracy

**Definition:** When the prompt emits a `human_review_flag`, how often does the advisor confirm it represented a real review-worthy topic?
**Target:** ≥80% confirmation; ≤10% false positives.
**Method:** One-click confirm/dismiss in the advisor tool. Calibrated quarterly.

### 9. Escalation Rate

**Definition:** Percentage of invocations where the prompt refused / escalated rather than answering.
**Target:** Workflow-specific. For `internal-policy-search`, escalation on insufficient sources is **desired** — a 0% escalation rate is a red flag, not a success.
**Method:** Output-parsing at the gateway.

### 10. User Satisfaction

**Definition:** Periodic survey: "Would you keep using this prompt if I removed it tomorrow?"
**Target:** ≥80% yes.
**Method:** Quarterly survey, sample size sized for confidence per prompt.

---

## Counter-Metrics (Watch These Too)

Single-direction optimization is dangerous. We pair each outcome metric with a counter-metric.

| Outcome metric | Counter-metric | Why |
|---|---|---|
| Time saved | Advisor edit distance | "Saved time" by skipping review is not value. |
| Adoption rate | Bug-report volume | High adoption with high error is a problem. |
| Schema compliance | Refusal rate | 100% schema compliance because the prompt always returns "I cannot help" isn't success. |
| Hallucination rate | Refusal helpfulness | A prompt that never hallucinates because it always refuses is worse than the previous workflow. |

---

## Reporting Cadence

| Audience | Cadence | Format |
|---|---|---|
| AI Enablement Lead | Weekly | Library-level summary; per-prompt drilldowns |
| Compliance Liaison | Monthly | High / Restricted prompts; flag accuracy; escalation patterns |
| Business Unit Sponsor | Quarterly | Outcome metrics; ROI; new-prompt pipeline |
| VP Technology / Executive | Quarterly | One-page summary; investment asks; risk picture |

---

## The Honest Conversation

A measurement plan is only useful if you're willing to publish bad numbers. The team commits to:

- Publishing every quarter's metrics — including misses — to the same audience.
- Treating a missed metric as a signal to fix the prompt or fix the placement, not a signal to remove the metric.
- Sunsetting prompts that consistently underperform rather than defending them.

If the library can't justify itself with numbers, it doesn't justify itself.
