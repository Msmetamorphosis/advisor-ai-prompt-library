# advisor-ai-prompt-library

> A working example of what a governed, production-grade AI prompt library looks like for regulated financial services firms — built by Metamorphic Curations to show you exactly what we would deliver.

---

## What You Are Looking At

This repository is a **fully functional reference implementation** of an enterprise AI prompt library for a wealth management firm. Every file in it is something your team would actually use: working governance docs, tested prompts, a CI-enforced test suite, operational scripts, and the documentation advisors and compliance reviewers would receive on day one.

We built this so you can see the work, not just hear about it. Fork it, run the tests, read the system prompts, trace a prompt from intake through compliance review to production release. This is the standard we hold ourselves to on every engagement.

---

## The Business Problem We Are Solving For You

Financial advisors spend a disproportionate share of their day on tasks that are not face-to-face client time: meeting preparation, CRM documentation, follow-up emails, portfolio review prep, and policy lookups. General-purpose AI tools (ChatGPT, Copilot, Claude) can compress these tasks, but in a regulated environment, ungoverned prompting introduces real risks:

- **Inconsistent output quality** across advisors using ad-hoc prompts.
- **Compliance exposure** from drafts that read as recommendations, guarantees, or unauthorized advice.
- **Hallucinated policy answers** that contradict the firm's actual procedures.
- **PII leakage** into prompts that were never reviewed.
- **No audit trail** for what was generated, who reviewed it, or whether it was sent.

A prompt library — versioned like code, tested like code, and reviewed like code — is the reliability layer between the advisor, the model, the firm's data, and the regulator. This is what we build.

---

## What You Get When You Engage Us

We deliver a governed prompt library scoped to your advisor workflows. Here is what that includes.

### Six Prompt Modules, Each Covering a Moment in the Advisor's Day

| Workflow moment | Prompt | What it does |
|---|---|---|
| Before a client meeting | `advisor-meeting-prep` | Surfaces known facts, prior action items, and open questions from your CRM |
| During or after the meeting | `client-meeting-summary` | Produces a structured summary plus a CRM-ready note for advisor review |
| CRM documentation | `crm-note-assistant` | Tight, source-grounded CRM entries with source evidence built in |
| Follow-up communication | `client-follow-up-email` | Drafts an advisor-reviewed email with required compliance closer intact |
| Operational questions | `internal-policy-search` | Cites your internal policy or escalates — never invents |
| Portfolio review prep | `portfolio-review-prep` | Builds a meeting agenda from approved data summaries |

Every prompt ships with a system prompt, a user template with placeholder variables, output schema, worked examples, six or more regression test cases, per-prompt changelog, and compliance constraints documentation for client-facing prompts.

### Governance Built In, Not Bolted On

Every prompt is risk-classified (Low, Medium, High, or Restricted) using the decision tree in `RISK-TAXONOMY.md`. Risk classification drives who approves the prompt, how often it is reviewed, and whether human-in-the-loop is required. The rules are enforced by the test suite, not just documented.

```
Low       Peer review, 12-month cadence
Medium    AI Enablement Lead sign-off, 6-month cadence
High      Compliance Liaison sign-off, quarterly cadence
Restricted All of the above + Business Unit Sponsor, 30-day cadence
```

### A Test Suite That Enforces What Compliance Requires

Run `pytest` and the suite verifies:

- Every prompt folder contains the required files.
- Every `prompt.yaml` declares required metadata fields with valid values.
- Every `eval-cases.json` and `output-schema.json` is valid and well-formed.
- Every prompt has at least five eval cases including refusal cases.
- `human_review_required: true` is set for every Medium, High, and Restricted prompt.
- Prohibited phrases (guaranteed return, tax advice, you should invest, and others) do not appear in production system prompts or example outputs.
- Semantic versioning is well-formed.
- Prompt IDs are unique across the library.

CI failure means the prompt does not ship. No exceptions.

### Semantic Versioning at the Prompt Level

Every prompt is versioned independently.

- **Major (X.0.0):** schema change, scope change, or new approver required.
- **Minor (1.X.0):** new behavior or field, backward compatible.
- **Patch (1.0.X):** wording, typo, or compliance language tightening with no behavior change.

Every change requires an entry in the prompt's `changelog.md` and in the top-level `CHANGELOG.md`. The Git history is the audit log.

### Human-in-the-Loop Enforced by the System

The library does not rely on advisors remembering to review. The advisor-review reminder is in the system prompt of every client-facing prompt. The test suite verifies it is there. The output schema labels every draft as "Draft — pending advisor review." Compliance-sensitive topics surface as structured `human_review_flags`, not buried prose.

AI drafts. Advisors decide. That sentence is not a philosophy statement. It is enforced in code.

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

---

## How to Run the Tests Yourself

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

---

## How We Measure Whether It Is Working

Adoption is not a success metric. Time saved, edit distance, escalation rate, and hallucination rate are. `docs/measurement-plan.md` defines each metric, its target, and how it is measured. We do not ask you to trust that the library is delivering value. We define what delivering value looks like before we ship, and we report against it every quarter.

---

## What an Engagement Looks Like

1. **Workflow analysis.** We map your highest-volume non-client-facing-time tasks and identify which ones have the right input/output structure for prompt-assisted workflows.
2. **Prompt design and governance setup.** We author the system prompts, user templates, eval cases, and governance documentation for each approved workflow.
3. **Compliance review.** We run the library through your compliance liaison using the materials in this repo as the review package.
4. **Pilot.** We deploy to a closed group of advisors, measure, and tighten.
5. **Production release.** We hand off a tagged release with a full test suite, changelog, and advisor-facing release note.
6. **Ongoing ownership.** We can own the library on your behalf or transfer it to your internal team. Either way, you get the same versioning, test, and review infrastructure so the work continues safely after we leave.

---

## What This Is Not

- This library does not send anything to clients on behalf of advisors.
- It does not make investment recommendations, suitability determinations, or tax statements.
- It does not bypass your supervisory procedures — it is designed to document, support, and survive them.
- It is not a chatbot. It is a governed set of workflow tools that happen to be powered by a language model.

---

## Why Governed Prompt Libraries Matter at Enterprise Scale

Prompt engineering at enterprise scale is not writing clever instructions. It is the reliability layer between:

1. **Human users** — advisors, CSAs, operations staff.
2. **Enterprise data** — CRM, policy documents, approved research.
3. **Model behavior** — drift, hallucination, sycophancy, format breakage.
4. **Compliance constraints** — FINRA, SEC, internal supervisory policy.
5. **Workflow adoption** — does the advisor actually use it tomorrow?
6. **Measurable outcomes** — time saved, edit distance, escalation rate.

A governed prompt library makes AI augmentation safer and more adoptable than each advisor improvising in a chat box. This repository is the proof of concept. An engagement with us is the production version, scoped to your workflows, your data, and your compliance requirements.

---

## About This Repository

**What this is:** A fully functional reference implementation and demonstration of enterprise AI prompt governance for wealth management, built by Metamorphic Curations.

**What this is not:** A production deployment. Any firm wishing to adapt these patterns for live advisor use must perform their own compliance, supervisory, information security, model risk management, and privacy review.

All examples are synthetic. No proprietary client data is included.

---

## Ready to Build This for Your Firm?

This repository is the starting point. An engagement produces a version scoped to your specific advisor workflows, integrated with your CRM and retrieval systems, reviewed by your compliance team, and handed off with the governance infrastructure to run it safely.

**Contact:** Crystal Tubbs, Metamorphic Curations LLC
