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

At a realistic enterprise wirehouse scale, approximately 9,000 advisors, 220 trading days per year, six prompts in production at the call frequencies documented in the cost model, the picture looks like this:

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

A model gateway can enforce which models a prompt is allowed to call. It cannot decide which tier a prompt belongs in. That decision is upstream; it lives with the prompt author, who has to justify the tier choice against eval results.

By encoding the tier decision into the prompt metadata, the library produces three useful artifacts at validation time:

1. A machine-readable registry that any gateway, app, or finance forecast can read.
2. An audit trail of why each prompt sits at the tier it sits at, with reference to which lower-tier eval failed.
3. A natural review cadence — when cheaper models improve, every tier-3 prompt is a candidate for re-evaluation at tier-2.

Full methodology, pricing sources, and reproducibility instructions live in `docs/cost-model.md`. The three scripts that produce the numbers:`scripts/measure_prompts.py`, `scripts/cost_model.py`, and `scripts/cost_model_extrapolation.py` can be re-run with different volume assumptions or updated pricing in minutes.

The broader point is that **model selection is a governance decision, not an engineering preference.** Treating it as the latter is how organizations end up paying for Opus capability on Haiku-class work.

---

# Output Length Discipline

If model tiering is the largest available cost lever in a prompt library, output length discipline is the second largest, and the two compound.

On every major vendor's current pricing card, output tokens cost approximately five times what input tokens cost. Anthropic prices Haiku 4.5 at $1 input / $5 output, Sonnet 4.6 at $3 / $15, and Opus 4.7 at $5 / $25. OpenAI prices GPT-5.4 at $2.50 / $15. Google prices Gemini 2.5 Flash at $0.30 / $2.50. The 5x ratio is structural.

The operational implication is that the output portion of any prompt's bill is the dominant cost driver, and verbosity in the model response is therefore the single most expensive form of waste in a prompt library. A model asked to summarize a meeting without a length cap routinely produces 2x to 3x more text than the user actually needed, on the most expensive token type.

This library treats output length as a governed concern at three levels:

1. **In the prompt metadata.** Every `prompt.yaml` declares `max_output_tokens` (the hard ceiling enforced at the API layer) and `target_output_tokens` (the expected typical length used by evals).
2. **In the prompt itself.** Every `system.md` includes an explicit Output Length section near the end, restating the ceiling and forbidding common forms of verbosity (preambles like "Here is the summary you requested," postambles like "Let me know if you'd like more detail," unbounded sectioning, narrating the response before generating it).
3. **In the validation suite.** Length fields are required metadata, and `target_output_tokens` must be at most eighty percent of `max_output_tokens` to leave room for legitimate variance without inviting drift.

Holding tiering constant and only varying output discipline, the cost impact on this six-prompt library at the same enterprise scale is:

| Strategy | Annual cost |
|---|---:|
| Correct tiering + disciplined output (length caps enforced) | $138,293 |
| Correct tiering + unconstrained output (no length cap) | $217,147 |

Output length discipline alone is a **$78,854 per year reduction (approximately 36%)** on top of correct tiering, on this small library. It compounds with tiering rather than competing with it. The combined effect of correct tiering and disciplined output, versus the common enterprise default of "use the best model and let it produce what it produces," is roughly a five-to-ten-fold reduction in annual cost on the same workload.

The discipline also has to be taught, not just enforced. End users issuing ad-hoc instructions to library prompts are the primary source of unconstrained output. The `docs/output-length-discipline.md` doc lays out the teaching framework for both prompt authors and end users, including the most common verbosity mistakes (no length instruction at all, vague "be concise" language without numeric targets, length instructions buried where the model will forget them, allowing preamble and postamble, open-ended structural prompts). The underlying rule of thumb is that **if the expected output length cannot be described in one sentence, the prompt is under-specified.**

Full mechanics, pricing math, and the per-prompt verbosity multipliers used in the cost projection are in `docs/output-length-discipline.md`. The cost numbers above can be regenerated by running `scripts/cost_model_output_discipline.py`.

---

# Observability and Monitoring

The most expensive blind spot in enterprise AI programs today is not the model bill. It is the absence of operational visibility into what the prompt library is actually doing in production. Without observability, "the prompt is working" is a hope, not a fact.

This repository defines the observability contract the library is designed to support: a canonical log event schema for every prompt call, a set of quality, cost, adoption, and drift metrics with explicit healthy bands and action thresholds, three operational dashboards (library health, cost and tier distribution, quality and drift), and the governance triggers that fire when metrics cross threshold. The metrics span prompt success rate, human correction frequency, average edit distance, escalation frequency, hallucination incident tracking, model tier usage distribution, cost drift detection, prompt degradation over time, user satisfaction scoring, and time-to-completion.

A working example of how this would surface operationally is included as `scripts/generate_usage_report.py`, which consumes the canonical event schema and produces a weekly Markdown report with per-prompt status, flagged prompts requiring review, and the threshold breaches that triggered the flags.

Full mechanics, the log schema, the metric thresholds, and the governance triggers are in `docs/observability-and-monitoring.md`.

---

# Compliance Integration

Prohibited language detection, supervisory review queues, and regulatory retention awareness are built into the library as first-class concerns rather than retrofitted downstream.

Prohibited language is enforced at three layers: at prompt time inside each `system.md`, at pre-release time via a context-aware scanner in the test suite, and at production time as a log event field that routes failures to supervisory review rather than silently suppressing them. The phrase list is centralized in `tests/fixtures/prohibited_phrases.json` so a single update propagates to all three layers.

Supervisory review is structured into four classes (`pre-use`, `post-use-sampled`, `post-use-flagged`, `internal-only`) declared per prompt in `prompt.yaml`. The classification is owned by the firm's compliance function; the library exposes it as a versioned, auditable field.

Retention is governed by a `retention_class` field on every prompt that maps to the appropriate broker-dealer recordkeeping treatment under SEC Rule 17a-4 and FINRA Rule 4511. Every artifact involved in producing an advisor-facing or client-facing output (input variables, rendered prompt, model and version, output, human review status, advisor edits) is retained, because storing the output alone is not sufficient for reproducibility, and reproducibility is what reviewers will ask for.

Full mechanics are in `docs/compliance-integration.md`.

---

# Model and Prompt Governance Lifecycle

Every prompt in this library is treated as an asset under management with a documented lifecycle. The lifecycle has eight stages: proposal, authoring and internal evaluation, legal and compliance review, pilot approval, monitored rollout, periodic revalidation, policy-triggered review, and sunset and deprecation.

The stages encode the failure modes the library is designed to prevent. Lower-tier eval gating prevents tier inflation. Compliance review on the right prompts prevents regulated communications from being drafted by AI without sign-off. Monitored rollout prevents a prompt that worked for fifty pilot advisors from silently failing when it reaches five thousand. Periodic revalidation prevents prompts approved against last year's policy from continuing to run against this year's policy. Policy-triggered review prevents regulatory changes from catching the AI program flat-footed. The sunset process prevents the library from accumulating inactive prompts indefinitely.

Review cadence is set by risk class: Restricted quarterly, High every six months, Medium and Low annually. Sunset is a documented action with a written rationale and a deprecation notice, not silent removal, because outputs produced during a prompt's operational life remain books and records and must be reproducible from their source version indefinitely.

Full lifecycle definition is in `docs/model-governance-lifecycle.md`.

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
│   ├── adoption-strategy.md
│   ├── advisor-workflow-map.md
│   ├── compliance-integration.md
│   ├── cost-model.md
│   ├── example-release-v1.0.0.md
│   ├── human-review-model.md
│   ├── measurement-plan.md
│   ├── model-governance-lifecycle.md
│   ├── observability-and-monitoring.md
│   ├── output-length-discipline.md
│   └── prompt-lifecycle.md
└── scripts/
    ├── validate_prompt_library.py
    ├── generate_prompt_registry.py
    ├── generate_usage_report.py
    ├── measure_prompts.py
    ├── cost_model.py
    ├── cost_model_extrapolation.py
    └── cost_model_output_discipline.py
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

# Final Perspective

The central idea behind this repository is that enterprise AI systems become significantly more useful when organizations treat prompting as governed operational infrastructure rather than as an informal user behavior.

As organizations continue integrating systems like Microsoft Copilot, ChatGPT, and Claude into daily workflows, the challenge increasingly becomes less about accessing model capability and more about operationalizing that capability safely, consistently, and transparently.

This repository was built as a practical exploration of how that operationalization process could look inside regulated industries. Thank you for reading, make it a great day!
