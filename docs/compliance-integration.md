# Compliance Integration

This document defines how the prompt library integrates with the compliance and supervisory functions that any AI deployment in wealth management or broker-dealer environments must operate inside. It is not legal advice, and it is not a substitute for an actual compliance review. It is a working sketch of the operational hooks the library exposes so that compliance and supervision can do their jobs without becoming a bottleneck.

Three areas of integration are addressed: **prohibited language detection**, **supervisory review queues**, and **regulatory retention awareness**.

---

## Why this belongs in the library

Compliance integration is often treated as a downstream concern, layered on top of an AI deployment after the fact. That approach reliably produces two failure modes:

1. The compliance team is asked to approve outputs they cannot reproduce, because the prompts, models, and inputs that produced them are not preserved in a reviewable form.
2. The engineering team has to retrofit governance into a system that was never designed to support it, usually after a finding.

Building compliance hooks into the prompt library itself means the artifacts compliance needs to do their job — the prompt, the version, the model, the inputs, the output, the human review status, the flags — are emitted by design, not reverse-engineered.

---

## Prohibited language detection

The library enforces prohibited-language constraints at three layers, each catching a different failure mode:

**Layer 1: Prompt-time prevention.** Every `system.md` includes explicit instructions about prohibited language for the prompt's domain. For client-facing prompts, this includes prohibited recommendation language (`"you should buy"`, `"I recommend"`, `"this is a good investment"`), prohibited guarantee language (`"guaranteed return"`, `"risk-free"`, `"no downside"`), and prohibited performance language (`"will outperform"`, `"will beat the market"`). For all prompts, prohibited NPI exposure language is included. This is the cheapest layer — preventing the language from being generated in the first place.

**Layer 2: Pre-release validation.** The test suite includes a context-aware prohibited-phrase scanner that runs against every prompt's `system.md`, `user-template.md`, and `examples.md`. The scanner is intentionally smart enough to distinguish actual prohibited language from documentation that names a phrase in order to ban it — the test file `tests/test_compliance_boundaries.py` implements the prohibition-marker logic. No prompt ships with prohibited language inside it.

**Layer 3: Production-time scanning.** Every output emitted by a library prompt should pass through the same scanner before it is presented to the advisor. The scanner result is captured in the log event as `prohibited_phrase_scan: pass | fail`. Failures route the output to a supervisory review queue rather than being silently suppressed, because suppressing the output without review hides the signal that something in the prompt is broken.

The list of prohibited phrases is centralized in `tests/fixtures/prohibited_phrases.json` so that adding a new phrase updates all three layers at once. New phrase additions are subject to the same change-control process as prompt changes — proposed via PR, reviewed by compliance, version-bumped in the prompt library changelog.

---

## Supervisory review queues

Wealth management firms operate under broker-dealer supervisory frameworks that require designated principals to review certain categories of client communications. The library exposes review status as a structured concern so that the supervisory function can ingest it cleanly.

Each prompt's `prompt.yaml` declares a `supervisory_review_class` field that maps to one of four review treatments:

| Class | Meaning | Typical examples in this library |
|---|---|---|
| `pre-use` | The output must be reviewed by a principal before the advisor uses it | None of the current six prompts |
| `post-use-sampled` | A statistical sample of outputs is reviewed after use | `client-follow-up-email` (sample rate set by compliance) |
| `post-use-flagged` | All outputs flagged by automated scanners or by the advisor are reviewed; the rest are retained but not actively reviewed | `client-meeting-summary`, `portfolio-review-prep` |
| `internal-only` | No client-facing surface; no supervisory review required, but standard retention applies | `crm-note-assistant`, `advisor-meeting-prep`, `internal-policy-search` |

The mapping between prompt and review class is **not a decision made by the library**. It is a decision made by the firm's compliance function. The library exposes the field so that the decision is auditable and version-controlled alongside the prompt.

The log event schema in `docs/observability-and-monitoring.md` already includes `supervisor_review_required` and `human_review_status`. The supervisory review queue is a downstream consumer of those events, filtering to the events that match its review class and routing them to the appropriate principal.

---

## Regulatory retention awareness

The major retention regimes that touch wealth management AI deployments are SEC Rule 17a-4 (broker-dealer recordkeeping), FINRA Rule 4511 (general books and records), and the various state-level analogues. Two principles drive how the library handles retention:

1. **Every artifact involved in an advisor-facing or client-facing output is retained.** This includes the input variables, the rendered prompt, the model and version, the output, the human review status, and any edits the advisor made before use. Storing the output without the prompt and inputs is not sufficient for reproducibility, and reproducibility is what reviewers will ask for.
2. **Retention classification lives in the prompt metadata.** Every `prompt.yaml` declares a `retention_class` field with three possible values: `client_communication` (default retention period, typically six years from the date of the communication for broker-dealer records), `internal_record` (firm-specified retention, often three to seven years), or `transient_assist` (short-retention scratch outputs that never become books and records).

The `retention_class` is also emitted in every log event so that the downstream retention system can route the event to the correct storage tier. Records that fall under `client_communication` require write-once-read-many (WORM) storage to satisfy 17a-4(f). The library does not implement WORM storage — it tags the events so the platform that does implement WORM can pick them up correctly.

A practical implication of retention awareness is that **prompt versions cannot be deleted from history once they have been used in production.** The `CHANGELOG.md` and the per-prompt `changelog.md` files preserve the full lineage of every change for the lifetime of the library. A prompt may be sunset, but its history remains queryable, because an output produced by version 1.2.0 must be reproducible from the exact version that produced it.

---

## What this is not

This document is not a regulatory compliance certification. It does not establish that the library, as currently configured, satisfies the specific obligations of any particular firm under SEC, FINRA, state, or international law. Real compliance integration requires sign-off from the firm's actual compliance function, working from the specific regulatory inventory that applies to that firm.

What this document does is establish that **the library is designed to be compliance-ready**, in the sense that the artifacts a compliance function needs — auditable prompt versions, structured review status, traceable retention metadata, automated prohibited-language detection — are produced as a matter of architecture rather than retrofitted under deadline.

That is the difference between an AI program that can be reviewed and an AI program that can be reviewed at scale.
