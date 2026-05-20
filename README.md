# advisor-ai-prompt-library

> A version-controlled, governance-aware prompt library demonstrating how a mature AI Enablement team would design, test, and deploy reusable prompts for financial advisors, client service associates, and wealth management operations teams.

---

## ⚠️ Disclaimer

This repository is a **mock portfolio example** created for interview and demonstration purposes only. It is **not affiliated with, endorsed by, or representative of Raymond James Financial or any other firm**. All examples are synthetic. No proprietary data is included. See [`DISCLAIMER.md`](./DISCLAIMER.md) for the full notice.

---

## The Business Problem

Financial advisors spend a disproportionate share of their day on tasks that are not face-to-face client time: meeting preparation, CRM documentation, follow-up emails, portfolio review prep, and policy lookups. General-purpose AI tools (ChatGPT, Copilot, Claude) can compress these tasks — but in a regulated environment, ungoverned prompting introduces real risks:

- **Inconsistent output quality** across advisors using ad-hoc prompts.
- **Compliance exposure** from drafts that read as recommendations, guarantees, or unauthorized advice.
- **Hallucinated policy answers** that contradict the firm's actual procedures.
- **PII leakage** into prompts that were never reviewed.
- **No audit trail** for what was generated, who reviewed it, or whether it was sent.

A prompt library — versioned like code, tested like code, and reviewed like code — is the reliability layer between the advisor, the model, the firm's data, and the regulator.

---

## Why Advisor Prompt Libraries Matter

Prompt engineering at enterprise scale is not "writing clever instructions." It is the reliability layer between:

1. **Human users** — advisors, CSAs, operations staff.
2. **Enterprise data** — CRM, policy documents, approved research.
3. **Model behavior** — drift, hallucination, sycophancy, format breakage.
4. **Compliance constraints** — FINRA, SEC, internal supervisory policy.
5. **Workflow adoption** — does the advisor actually use it tomorrow?
6. **Measurable outcomes** — time saved, edit distance, escalation rate.

A governed prompt library makes AI **augmentation** safer and more adoptable than each advisor improvising in a chat box.

---

## Repository Structure

```
advisor-ai-prompt-library/
├── README.md                      ← you are here
├── DISCLAIMER.md                  ← mock-project disclosure
├── GOVERNANCE.md                  ← ownership, approval, review cadence
├── VERSIONING.md                  ← semantic versioning policy
├── RISK-TAXONOMY.md               ← Low / Medium / High / Restricted
├── EVALUATION-RUBRIC.md           ← 10-dimension scoring rubric
├── CHANGELOG.md                   ← release history
├── requirements.txt
├── pytest.ini
├── .gitignore
├── .github/
│   ├── pull_request_template.md
│   └── ISSUE_TEMPLATE/
│       ├── prompt_change_request.md
│       ├── compliance_review.md
│       └── bug_report.md
├── prompts/                       ← six advisor-workflow prompts
│   ├── advisor-meeting-prep/
│   ├── client-meeting-summary/
│   ├── crm-note-assistant/
│   ├── client-follow-up-email/
│   ├── internal-policy-search/
│   └── portfolio-review-prep/
├── templates/                     ← starter scaffolds for new prompts
├── tests/                         ← pytest validation + regression suite
├── docs/                          ← adoption, lifecycle, measurement
└── scripts/                       ← validation + registry generation
```

Every prompt module ships with:

| File | Purpose |
|---|---|
| `prompt.yaml` | Governance metadata (owner, risk, approvers, review date) |
| `system.md` | The system prompt — role, scope, allowed/prohibited behavior |
| `user-template.md` | The user prompt with `{{placeholder}}` variables |
| `output-schema.json` | (where applicable) JSON contract for structured output |
| `examples.md` | Sample input / expected output / safety rationale |
| `eval-cases.json` | ≥5 regression test cases |
| `changelog.md` | Per-prompt version history |
| `compliance-constraints.md` | (client-facing prompts) explicit do-not-say list |

---

## Prompt Governance Philosophy

1. **Prompts are code.** They are versioned, reviewed, tested, and released — not pasted into a chat window.
2. **Risk classification drives review depth.** Low risk = peer review. High / Restricted = compliance sign-off.
3. **Human-in-the-loop is non-negotiable for client-facing output.** No draft email leaves the firm without advisor review.
4. **Grounding beats fluency.** Prompts that depend on firm knowledge must cite or surface "missing information" rather than invent.
5. **Refusal is a feature.** A prompt that escalates "I cannot answer this without source X" is doing its job.
6. **Every prompt has an owner.** Ownership is named, reachable, and accountable.

See [`GOVERNANCE.md`](./GOVERNANCE.md) for the full operating model.

---

## How to Run Tests

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full validation + regression suite
pytest -v

# 3. Run the standalone library validator
python scripts/validate_prompt_library.py

# 4. Regenerate the prompt registry
python scripts/generate_prompt_registry.py
```

The test suite enforces:

- Every prompt folder contains the required files.
- Every `prompt.yaml` declares the required metadata fields.
- Every `eval-cases.json` and `output-schema.json` is valid JSON.
- Every prompt has ≥5 eval cases and explicit prohibited use cases.
- `human_review_required: true` for every Medium / High / Restricted prompt.
- Prohibited phrases (e.g., "guaranteed return", "tax advice") do not appear in production system prompts or examples.
- Semantic versioning is well-formed.
- Prompt IDs are unique across the library.

CI failure = the prompt is not releasable.

---

## Example Use Cases

| Workflow moment | Prompt | What it does |
|---|---|---|
| Before a client meeting | `advisor-meeting-prep` | Surfaces known facts, prior action items, open questions |
| During / after the meeting | `client-meeting-summary` | Produces a structured summary + CRM-ready note |
| CRM documentation | `crm-note-assistant` | Tight, source-grounded CRM entries |
| Follow-up communication | `client-follow-up-email` | Drafts an advisor-reviewed email (no advice, no guarantees) |
| Operational questions | `internal-policy-search` | Cites the policy or escalates — never invents |
| Portfolio review prep | `portfolio-review-prep` | Builds an agenda from approved data summaries |

---

## Version Control Approach

We follow semantic versioning at the **prompt level**, not just the repo level:

- **Major (X.0.0):** breaking change — schema change, scope change, new approver required.
- **Minor (1.X.0):** new behavior, new field, expanded scope — backward compatible.
- **Patch (1.0.X):** wording, typo, compliance language tightening — behavior unchanged.

Every change requires a per-prompt `changelog.md` entry **and** a top-level `CHANGELOG.md` entry. See [`VERSIONING.md`](./VERSIONING.md).

---

## How This Supports Enterprise AI Adoption

- **Reduces prompting variance** — every advisor gets the same vetted scaffold instead of inventing prompts at the keyboard.
- **Compresses time-to-trust** — compliance reviews a prompt *once*, not every advisor's improvisation.
- **Creates an audit trail** — Git history *is* the prompt audit log.
- **Builds a measurement loop** — eval cases provide ground truth for regression and improvement.
- **Decouples humans from model drift** — when the underlying LLM updates, the prompt library re-runs its eval suite before re-certifying.
- **Makes adoption a workflow conversation, not a tooling conversation.** See [`docs/adoption-strategy.md`](./docs/adoption-strategy.md).

---

## Interview Talking Points

When walking a VP of Technology / AI Enablement through this repo:

1. **"Prompts are the API contract between humans and models."** Treat them with the same versioning, testing, and review rigor as production code.
2. **Risk taxonomy is the unlock for speed.** Low-risk prompts ship in days; restricted prompts get compliance and supervisory review. Both move faster than ungoverned chat.
3. **Eval cases are the regression net.** When the underlying model updates (Claude 3.7 → 4 → 4.5), we don't ask "did it break?" — we re-run the suite.
4. **Human-in-the-loop is a feature, not a limitation.** Every client-facing prompt explicitly tells the advisor to review before sending — that language is in the system prompt and verified by the test suite.
5. **Measurement isn't optional.** [`docs/measurement-plan.md`](./docs/measurement-plan.md) defines time saved, edit distance, escalation rate, hallucination rate, adoption rate. If you can't measure it, you can't justify it to the business.

---

## Project Maintainers

- **Owner (mock):** AI Enablement — Advisor Productivity
- **Compliance liaison (mock):** Supervisory Technology Risk
- **Repo author:** Crystal Molnar — portfolio example, May 2026

---

## License

This repository is provided as a **portfolio / interview artifact**. It is not licensed for production deployment without independent compliance and supervisory review by a qualified firm.
