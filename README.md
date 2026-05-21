# advisor-ai-prompt-library

A working example of what governed, production-oriented AI prompt infrastructure could look like inside a regulated financial services organization.

Built as an independent portfolio and research project by Crystal Tubbs.

---

# What You Are Looking At

This repository is a fully functional reference implementation exploring how AI prompt libraries could be operationalized safely inside regulated enterprise environments, particularly wealth management and financial services organizations.

The project was built around a simple observation:

Most enterprise AI usage today still operates through ad hoc prompting. Employees open ChatGPT, Copilot, or Claude, improvise instructions, and hope the outputs are useful, compliant, and accurate enough to trust. That workflow may be acceptable for low-risk experimentation, but it becomes increasingly problematic in regulated environments where consistency, auditability, and governance matter.

This repository explores what happens when prompts are instead treated as governed operational assets.

Every file in this repository exists to model what a production-oriented prompt governance system could look like:
- structured prompt modules
- governance documentation
- approval workflows
- semantic versioning
- regression testing
- evaluation infrastructure
- risk classification
- human review enforcement
- operational validation

The goal is not to present AI as autonomous decision making. The goal is to demonstrate how AI augmentation could be made safer, more reliable, and more operationally usable when surrounded by the right architectural controls.

---

# The Problem This Repository Explores

Financial advisors spend a substantial portion of their day on operational and documentation-heavy workflows that are necessary, but not directly client-facing:
- meeting preparation
- CRM note creation
- policy lookups
- follow-up communication
- portfolio review preparation
- internal information retrieval

Large language models can dramatically reduce the time required for these workflows. However, in regulated environments, ungoverned prompting introduces meaningful operational risk.

A single employee improvising prompts in a chat interface may unintentionally:
- generate recommendation-like language
- surface hallucinated policy answers
- omit required disclosures
- expose sensitive client information
- create inconsistent documentation quality
- bypass review expectations
- produce outputs with no audit trail or reproducibility

The central premise behind this repository is that enterprise AI reliability does not emerge from prompting alone. Reliability emerges from the surrounding governance, validation, testing, and operational structure.

This project explores what that structure could look like.

---

# Why Governed Prompt Libraries Matter

One of the biggest misconceptions in enterprise AI today is the idea that prompt engineering is simply about writing better instructions.

In practice, enterprise prompt engineering becomes a systems design problem.

Once AI systems begin interacting with regulated workflows, the organization must answer questions like:
- Who approves prompts before production use?
- How are prompt changes documented?
- How are outputs validated?
- How often are prompts reviewed?
- What happens when policies change?
- Which prompts require human review?
- How are hallucinations mitigated?
- How is prohibited language detected?
- How are prompts versioned across teams?
- How are outputs evaluated over time?

This repository was built to explore those questions through a working implementation rather than abstract discussion.

The broader philosophy behind the project is that prompt libraries in regulated industries should be treated similarly to production software systems:
- versioned
- reviewed
- tested
- monitored
- governed
- auditable

Prompt engineering at enterprise scale becomes less about clever prompting and more about operational reliability.

---

# What This Repository Includes

The repository models a hypothetical advisor workflow environment and includes six prompt modules representing common operational moments within a wealth management organization.

These modules cover:
- advisor meeting preparation
- client meeting summaries
- CRM note drafting
- advisor follow-up communication
- internal policy retrieval
- portfolio review preparation

Each module contains:
- a system prompt
- user prompt templates
- output schemas
- worked examples
- evaluation cases
- governance metadata
- compliance constraints
- semantic version tracking
- changelog documentation

The prompts are intentionally structured as governed operational artifacts rather than isolated instructions.

---

# Governance Built Into the System

A major focus of the project is demonstrating governance as a system-level requirement rather than an informal policy layer.

Every prompt in the repository is assigned a risk classification:
- Low
- Medium
- High
- Restricted

That classification determines:
- review cadence
- approval requirements
- oversight expectations
- release constraints
- human-in-the-loop requirements

Rather than relying on employees to remember governance procedures manually, the repository attempts to operationalize those requirements directly into the validation and testing process.

The included validation suite enforces rules such as:
- required metadata presence
- schema integrity
- evaluation case coverage
- prohibited phrase detection
- prompt uniqueness
- semantic version formatting
- human review enforcement for higher-risk workflows

In this model, prompts that fail governance validation simply do not ship.

---

# Human-in-the-Loop by Design

This repository intentionally focuses less on autonomous AI agents and more on controlled augmentation workflows.

The system is designed around the assumption that AI should support human expertise, not replace it.

Client-facing workflows therefore incorporate:
- advisor review expectations
- structured escalation pathways
- review flags
- bounded outputs
- compliance-aware constraints

The underlying philosophy is simple:

> AI drafts. Humans decide.

Human oversight is treated as an architectural requirement rather than a behavioral assumption.

---

# Reliability Through Architecture, Not Prompting Alone

A major motivation behind this project was exploring how architectural reliability layers can stabilize AI behavior more effectively than prompt wording alone.

The repository incorporates concepts such as:
- regression evaluation
- structured validation
- constrained outputs
- governance enforcement
- review workflows
- audit-oriented change tracking

The broader idea is that enterprise AI reliability emerges from the surrounding operational architecture rather than from any single prompt.

This becomes especially important in regulated environments where consistency and trust matter more than novelty.

---

# Model Tiering and Cost Discipline

One of the most underappreciated operational risks in enterprise AI today is not safety or hallucination. It is cost drift.

Most organizations deploying AI workflows allow employees and engineering teams to default to the most capable, and therefore most expensive, available model regardless of whether the underlying task requires it. A short CRM note extraction gets routed to the same flagship reasoning model used for complex multi-step analysis. The model behaves correctly. The cost structure quietly does not.

This repository explores model tiering as an additional governance layer in the prompt library itself, rather than as an afterthought handled at the API gateway.

The library defines four tiers, each with its own approved-model list, cost ceiling per call, and escalation rules:

- **tier-1-light:** classification, extraction, short rewrites, routing decisions
- **tier-2-standard:** summarization, structured output, single-turn Q&A, retrieval synthesis
- **tier-3-reasoning:** multi-step reasoning, client-facing drafts, policy interpretation
- **tier-4-frontier:** explicitly reserved for novel compliance reasoning and evaluator-of-evaluators use; requires named approval

Every prompt module in the library declares its tier and provides a written rationale for why it sits there. Promotion to a higher tier requires evidence that the lower tier failed an eval case. Demotion to a lower tier requires only that evals pass at the cheaper tier. The asymmetry is intentional. Expensive is hard. Cheap is easy.

## The Real Cost Picture

The `docs/cost-model.md` file contains a fully reproducible cost model built from the actual measured token counts of the six prompts in this library and verified public list pricing from Anthropic, OpenAI, and Google as of May 2026. All numbers can be regenerated by running the scripts in `scripts/`.

At a realistic enterprise wirehouse scale — approximately 9,000 advisors, 220 trading days per year, six prompts in production at the call frequencies documented in the cost model — the picture looks like this:

| Strategy | Annual cost | Delta vs recommended |
|---|---:|---:|
| Recommended tiering (cheaper models for lighter tasks) | $138,293 | baseline |
| Default everything to Claude Sonnet 4.6 | $325,795 | +$187,502 (+136%) |
| Default everything to Claude Opus 4.7 | $542,992 | +$404,699 (+293%) |

Correct tiering reduces annual cost by **57.6%** versus a Sonnet-default approach and by **74.5%** versus an Opus-default approach, on the same workload, with no expected quality loss because the cheaper tier is only assigned where eval cases pass at the cheaper tier first.

## The Scaling Picture

Enterprise prompt libraries rarely stay at six prompts. They typically grow to forty, sixty, or one hundred production prompts within twelve to eighteen months. Holding the same tier distribution observed in this library (roughly 16% tier-1, 50% tier-2, 34% tier-3) and the same per-prompt usage averages, a 50-prompt library at the same scale projects to:

| Strategy | Annual cost |
|---|---:|
| Recommended tiering | $1,291,562 |
| Default everything to Sonnet 4.6 | $2,867,486 |
| Default everything to Opus 4.7 | $4,779,144 |

The delta against a Sonnet-default approach is approximately **$1.58 million per year**. Against an Opus-default approach, approximately **$3.49 million per year**. That is the gap between disciplined routing and the path of least resistance.

## Why This Belongs in the Library, Not the Gateway

A model gateway can enforce which models a prompt is allowed to call. It cannot decide which tier a prompt belongs in. That decision is upstream — it lives with the prompt author, who has to justify the tier choice against eval results.

By encoding the tier decision into the prompt metadata, the library produces three useful artifacts at validation time:

1. A machine-readable registry that any gateway, app, or finance forecast can read.
2. An audit trail of why each prompt sits at the tier it sits at, with reference to which lower-tier eval failed.
3. A natural review cadence — when cheaper models improve, every tier-3 prompt is a candidate for re-evaluation at tier-2.

Full methodology, pricing sources, and reproducibility instructions live in `docs/cost-model.md`. The three scripts that produce the numbers — `scripts/measure_prompts.py`, `scripts/cost_model.py`, and `scripts/cost_model_extrapolation.py` — can be re-run with different volume assumptions or updated pricing in minutes.

The broader point is that **model selection is a governance decision, not an engineering preference.** Treating it as the latter is how organizations end up paying for Opus capability on Haiku-class work.

---

# Repository Structure

```text
advisor-ai-prompt-library/
├── README.md
├── DISCLAIMER.md
├── GOVERNANCE.md
├── VERSIONING.md
├── RISK-TAXONOMY.md
├── EVALUATION-RUBRIC.md
├── CHANGELOG.md
├── requirements.txt
├── pytest.ini
├── .github/
├── prompts/
│   ├── advisor-meeting-prep/
│   ├── client-meeting-summary/
│   ├── crm-note-assistant/
│   ├── client-follow-up-email/
│   ├── internal-policy-search/
│   └── portfolio-review-prep/
├── templates/
├── tests/
├── docs/
└── scripts/
```

---

# Running the Validation Suite

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the validation and regression suite:

```bash
pytest -v
```

Run the standalone validator:

```bash
python scripts/validate_prompt_library.py
```

Regenerate the prompt registry:

```bash
python scripts/generate_prompt_registry.py
```

---

# Measurement Philosophy

The repository intentionally treats adoption alone as an insufficient success metric.

The project instead models evaluation approaches focused on:
- time saved
- output consistency
- edit distance
- hallucination rate
- escalation frequency
- human correction frequency
- workflow completion efficiency

The broader objective is to explore whether governed AI augmentation systems can become operationally trustworthy enough for sustained enterprise adoption.

---

# What This Project Is Not

This repository is not:
- a production deployment
- an autonomous advisor system
- a suitability engine
- a financial recommendation engine
- a tax advisory system
- a client-facing chatbot

The implementation is intentionally constrained to workflow augmentation and governance exploration.

All examples and data included in the repository are synthetic.

---

# Final Perspective

The central idea behind this repository is that enterprise AI systems become significantly more useful when organizations stop treating prompting as an informal user behavior and begin treating it as governed operational infrastructure.

As organizations continue integrating systems like Microsoft Copilot, ChatGPT, and Claude into daily workflows, the challenge increasingly becomes less about accessing model capability and more about operationalizing that capability safely, consistently, and transparently.

This repository was built as a practical exploration of how that operationalization process could look inside regulated industries.
