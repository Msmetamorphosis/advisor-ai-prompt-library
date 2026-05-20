# Human-in-the-Loop Review Model

This document defines how human review is operationalized in the library. It is not an aspiration — every claim here is enforced somewhere in the system prompt, the output schema, or the test suite.

---

## The Four Statements

1. **AI drafts. Advisors decide.** No prompt in this library produces a final artifact. Every output is a *draft* — labeled as such, structured as such, and accompanied by an explicit advisor-review reminder.

2. **Compliance-sensitive topics are flagged, not silenced.** When a prompt detects content touching tax, legal, suitability, performance language, or NPI, it surfaces the topic in a structured `human_review_flags` field. It does not strip the topic — that would hide the risk.

3. **No client-facing output ships without advisor approval.** The only prompt in v1.0.0 that produces client-facing content is `client-follow-up-email`, and it produces only drafts. Its system prompt, its `compliance-constraints.md`, and a pytest assertion all enforce the advisor-review reminder.

4. **Refusal is a feature, not a fallback.** Several prompts (`internal-policy-search`, `client-follow-up-email`, `advisor-meeting-prep`) are explicitly designed to refuse when their inputs are insufficient or unsafe. The refusal is structured: it tells the advisor *why* and *where to go next*.

---

## Review Touchpoints by Prompt

| Prompt | What the advisor reviews | What the advisor confirms |
|---|---|---|
| `advisor-meeting-prep` | Brief content | Facts are grounded; flagged topics will be handled appropriately. |
| `client-meeting-summary` | Summary + CRM note | Action items are accurate; no advice / suitability language present. |
| `crm-note-assistant` | CRM note draft | No subjective characterizations; no NPI echoed. |
| `client-follow-up-email` | Subject + draft email | No prohibited language; required closer intact; no NPI. |
| `internal-policy-search` | Direct answer + citation | Source is current; answer matches user's situation. |
| `portfolio-review-prep` | Agenda + flagged items | No recommendations or projections drifted in; data freshness verified. |

---

## What "Review" Means in Practice

Review is not "read it and click send." For client-facing prompts, review is:

1. **Compare against the source.** Does the draft reflect what actually happened?
2. **Scan for prohibited language.** Use the reviewer checklist in `compliance-constraints.md`.
3. **Edit for voice.** Make it sound like the advisor, not the model.
4. **Confirm or revise the action items.** The action-item recap is the most error-prone field; verify owner and timing.
5. **Confirm no NPI.** No account numbers, balances, or sensitive identifiers.
6. **Hit send only after the above.**

For internal-only prompts, review is lighter but not absent:

1. Skim for factual correctness against the source.
2. Confirm flagged topics are handled before the meeting.
3. Save the artifact (CRM note, brief, agenda) only after the skim.

---

## When Review Fails

Review is a human process and humans fail. The library hardens against three failure modes:

- **The "rubber stamp" advisor.** Even an unattended paste from `client-follow-up-email` produces output that doesn't include advice, guarantees, recommendations, projections, or NPI. The required closer survives.
- **The "skipped flag" advisor.** `human_review_flags` is a structured field — it is visible in any reasonable UI rendering, not buried in prose. The advisor would have to actively dismiss it.
- **The "ignored escalation" advisor.** When the prompt refuses, the refusal is structured and points to a specific human path. The advisor cannot accidentally interpret it as "the AI didn't have anything to say."

---

## Supervisory Review

Beyond the advisor's own review, supervisory review of advisor-AI output is supported by:

- **Stable output structure.** Schemas make supervisor sampling efficient.
- **Audit trail.** Git history of the library + per-invocation logs (in a real deployment) lets a supervisor reconstruct *what the AI produced* vs. *what the advisor sent*.
- **Eval coverage.** Supervisors can request the eval set for any prompt to understand what the library does and doesn't test for.

In a real deployment this is paired with the firm's WSP and supervisory tooling. In this mock library, the patterns are documented but not connected to a live system.

---

## The Bumper-Rail Principle

The library is designed as a set of bumper rails, not a gate. The advisor still drives. The library makes it harder to veer off the road, easier to see when they're drifting, and faster to recover when they do. That is what "AI augmentation, not replacement" actually means in a regulated environment.
