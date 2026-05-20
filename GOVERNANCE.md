# Prompt Library Governance

This document defines the operating model for the advisor-ai-prompt-library. It is the operational counterpart to [`VERSIONING.md`](./VERSIONING.md) (how) and [`RISK-TAXONOMY.md`](./RISK-TAXONOMY.md) (what).

---

## 1. Prompt Ownership Model

Every prompt has exactly **one accountable owner** and **one named backup**. Ownership is declared in `prompt.yaml` and is non-anonymous.

| Role | Responsibility |
|---|---|
| **Prompt Owner** | Authors changes, runs eval suite, requests compliance review, signs off on releases. |
| **Backup Owner** | Steps in during PTO or role change. Same authority. |
| **Business Unit Sponsor** | Approves scope and funding for the prompt's existence. |
| **Compliance Liaison** | Reviews High / Restricted prompts and any client-facing output. |
| **AI Enablement Lead** | Owns the library overall — sets standards, breaks ties, approves the taxonomy. |

If the prompt owner leaves the firm or the role, the prompt is **paused in production** until a new owner is named. Unowned prompts do not run.

---

## 2. Approval Workflow

```
  ┌──────────┐    ┌───────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────┐
  │  Intake  │ -> │   Draft   │ -> │ Risk Classify│ -> │ Peer Review │ -> │   Test   │
  └──────────┘    └───────────┘    └──────────────┘    └─────────────┘    └────┬─────┘
                                                                                │
            ┌─────────────────────────────────────────────────────────────────┘
            ▼
   ┌──────────────────┐    ┌────────┐    ┌──────────────┐    ┌─────────┐
   │ Compliance Review│ -> │ Pilot  │ -> │ Prod Release │ -> │ Monitor │
   │ (if Med/High/    │    │ (≤ 20  │    │ (CHANGELOG + │    │ + eval  │
   │  Restricted)     │    │ users) │    │  Registry)   │    │   loop  │
   └──────────────────┘    └────────┘    └──────────────┘    └─────────┘
```

| Risk Level | Required Approvers |
|---|---|
| **Low** | Prompt Owner + 1 peer reviewer |
| **Medium** | Prompt Owner + AI Enablement Lead |
| **High** | Prompt Owner + AI Enablement Lead + Compliance Liaison |
| **Restricted** | All of the above + Business Unit Sponsor + supervisory documentation |

No prompt reaches production without:
- Passing the full `pytest` suite,
- A signed `approval-record.md`,
- A `changelog.md` entry,
- A top-level `CHANGELOG.md` entry.

---

## 3. Review Cadence

| Risk Level | Mandatory Re-Review |
|---|---|
| **Low** | Every 12 months |
| **Medium** | Every 6 months |
| **High** | Every 3 months |
| **Restricted** | Every 30 days, **or** any time the underlying model version changes |

`last_reviewed` in `prompt.yaml` is the source of truth. The validation script flags any prompt past its cadence.

Additionally, a re-review is triggered whenever:

- The underlying LLM or model version changes.
- A new regulatory advisory affects the prompt's scope.
- An eval case fails in CI.
- A supervisory escalation references the prompt.

---

## 4. Compliance Review Process

Compliance review is required for:

- Any prompt classified **High** or **Restricted**.
- Any prompt whose output may reach a client (email, letter, summary they will see).
- Any prompt that surfaces firm policy, tax positioning, suitability language, or fee/cost framing.
- Any prompt that handles PII or non-public personal information (NPI).

The compliance reviewer evaluates:

1. **Boundary fidelity** — does the system prompt prohibit the right things?
2. **Refusal quality** — does the prompt escalate when out of scope?
3. **Disclosure adequacy** — are required disclosures preserved in client-facing drafts?
4. **Supervisory traceability** — can a supervisor reconstruct what was sent and approved?
5. **Eval coverage** — do the test cases include the failure modes compliance cares about?

The reviewer's name and decision date are recorded in `prompt.yaml` under `approved_by` and `last_reviewed`.

---

## 5. Human-in-the-Loop Principles

These are not aspirational — they are **enforced by the test suite**:

1. **No client-facing output ships without advisor review.** The system prompt of every client-facing prompt contains an explicit advisor-review reminder. A pytest assertion verifies this.
2. **AI drafts, advisors decide.** The library generates drafts, recommendations of *what to discuss*, and structured notes. It does not generate advice.
3. **Refusal > fabrication.** Prompts must surface "missing information" or escalate, never invent.
4. **Flag, don't silence.** When a prompt detects a sensitive topic (tax, legal, suitability), it must add a `human_review_flag` to its output, not strip the topic.
5. **Compliance language is non-negotiable.** Disclosure boilerplate is treated as a required output field, not optional polish.

---

## 6. Audit Trail Expectations

The Git history *is* the audit log. To support that:

- Every change is a pull request — no direct commits to `main`.
- Every PR uses the [`pull_request_template.md`](./.github/pull_request_template.md) — business reason, prompt(s) changed, risk level, test results, compliance impact, rollback plan, approvers.
- Every release produces:
  - A tagged Git release (`v1.0.0`, `v1.1.0`, etc.).
  - An entry in `CHANGELOG.md`.
  - An entry in each affected prompt's `changelog.md`.
  - A regenerated `prompt-registry.json`.
- Every advisor-facing release is paired with a release note from [`templates/release-note-template.md`](./templates/release-note-template.md).
- `approval-record.md` per release captures who approved and when.

---

## 7. Escalation Paths

| Situation | Escalation |
|---|---|
| Eval case fails in CI | Prompt Owner is paged; production version remains pinned until fixed. |
| Compliance review identifies risk | Prompt is moved to `status: paused`. Re-release requires sign-off. |
| Advisor reports incorrect output in production | Bug report issue → Prompt Owner triages within 1 business day. |
| Hallucination or compliance-sensitive output reaches a client | Immediate supervisor notification → temporary library-wide pause of the prompt → root-cause review. |
| Model provider releases a major version | Library-wide regression run before any prompt is re-certified for the new model. |

---

## 8. Retirement and Rollback Process

### Retirement

A prompt is retired when:

- It is no longer aligned to a valid workflow.
- It has been superseded by a newer version with different scope.
- A risk review concludes it cannot be safely operated.

Retirement requires:

1. Setting `status: retired` in `prompt.yaml`.
2. A final `changelog.md` entry explaining the reason.
3. A 30-day deprecation window in advisor-facing tooling.
4. Archived registry entry preserved for audit history.

### Rollback

A rollback is initiated when a release introduces a defect that cannot be hot-patched within the SLA (4 business hours for client-facing prompts).

Rollback procedure:

1. Identify the last known-good version tag (e.g., `prompt/client-follow-up-email@v1.2.3`).
2. Open a PR that restores the prior `system.md`, `user-template.md`, and `prompt.yaml`.
3. Bump version with a `.x+1` patch and a changelog entry: "rollback from vX.Y.Z due to <reason>".
4. Re-run the eval suite.
5. Notify advisor users via release-note channel.

Rollbacks are **expected**, not embarrassing. A library that never rolls back is a library that isn't watching.
