# Model and Prompt Governance Lifecycle

This document describes the lifecycle of a prompt in this library from initial proposal through eventual sunset. The structure parallels the model governance lifecycle frameworks that mature financial-services firms operate for traditional model risk (SR 11-7 in the United States banking context, and the analogous frameworks used by broker-dealers, insurers, and asset managers). Prompt governance is a recent enough discipline that the regulatory frameworks have not fully caught up, but the operational shape is the same: every prompt is an asset under management, and every asset under management has a documented lifecycle.

The lifecycle defined here is the one this library is built to support. It is not a claim that any specific firm operates exactly this way today. It is a working sketch of the stages a serious AI Enablement function should expect a prompt to move through.

---

## Stage 1: Proposal

A new prompt enters the library through a proposal. The proposal is a structured document — implemented in this repository as a GitHub issue using the `prompt_change_request.md` template — that captures:

- The user problem the prompt is intended to solve
- The advisor workflow it sits inside
- The expected risk classification and supervisory review class
- The expected model tier and a preliminary cost estimate
- The intended success metrics
- The compliance review touchpoints the proposer believes apply

Proposals are reviewed by the AI Enablement function for fit with the library's scope, redundancy with existing prompts, and feasibility. Rejected proposals are documented with a written rationale, because rejection rationale is one of the most useful artifacts a maturing AI program can accumulate over time.

---

## Stage 2: Authoring and internal evaluation

Approved proposals move to authoring. The author drafts the prompt module — `prompt.yaml`, `system.md`, `user-template.md`, `examples.md`, and an initial `eval-cases.json` containing at least six cases that exercise the standard path, the refusal path, sensitivity-bait, NPI restraint, numeric restraint, and at least one edge case the author specifically expects to break the prompt.

The author runs the local validation suite (`scripts/validate_prompt_library.py` and `pytest`) and is responsible for confirming that the prompt passes governance validation before it leaves their hands. Prompts that cannot pass the local validator do not move forward.

The author also runs the prompt against the eval suite on a **lower tier than the one they intend to declare**, and documents the result in `tier_rationale`. If the lower tier passes, the prompt is downgraded. If the lower tier fails, the rationale records which eval case failed and why. This is the mechanism that prevents tier inflation over time.

---

## Stage 3: Legal and compliance review

Prompts that are client-facing, that touch regulated communication categories, or that fall into the High or Restricted risk classifications go through compliance review before pilot. Internal-only and Low-risk prompts may bypass this stage, by policy, but the policy itself is reviewed by compliance.

Compliance review evaluates:

- Whether the prompt's domain falls inside categories that require principal review under broker-dealer supervisory rules
- Whether the prompt's outputs could constitute investment recommendations, projections, or testimonials under the marketing rule
- Whether the prompt's inputs could include NPI and, if so, whether the firm's NPI handling controls apply
- Whether the prompt's retention class is correct
- Whether the prohibited-language constraints are sufficient for the prompt's domain

Compliance review produces a written approval, conditional approval (with specific changes required), or rejection. The approval is preserved as part of the prompt's metadata and is referenced in the changelog.

Legal review is invoked separately when a prompt touches new product categories, new client surfaces, new jurisdictions, or any area where the firm's existing legal posture does not already cover the use case.

---

## Stage 4: Pilot approval

Approved prompts move to a controlled pilot. A pilot has explicit constraints:

- A bounded population (typically a single branch, a single advisor team, or a volunteer cohort of 20-50 advisors)
- A defined duration (typically four to twelve weeks)
- Explicit success criteria tied to the metrics defined in `docs/measurement-plan.md`
- A defined rollback procedure and a named owner who can execute it

The AI Risk Committee — or its functional equivalent at the firm — approves the pilot scope, the success criteria, and the rollback procedure before the pilot begins. The pilot is not a soft launch. It is an instrumented experiment whose outcome is reviewed against pre-declared criteria.

During the pilot, the observability stack defined in `docs/observability-and-monitoring.md` runs at full fidelity, including the eval-drift sampling that compares production calls to the prompt's eval suite. The pilot owner reviews the weekly usage report and is responsible for surfacing any threshold breaches to the committee.

---

## Stage 5: Monitored rollout

Pilots that meet their success criteria move to monitored rollout. Rollout is staged, not flipped:

- A first wave expands to roughly ten percent of the eligible population, typically a single business unit or region
- A second wave expands to thirty to fifty percent if the first wave's metrics hold
- A third wave reaches general availability if the second wave's metrics hold

Each wave has its own go/no-go review against the same observability metrics that governed the pilot. Rollback at any wave is a normal operational action, not a failure, and the criteria for rollback are documented in the prompt's release notes.

General availability is not the end of governance. It is the start of the steady-state lifecycle described next.

---

## Stage 6: Periodic revalidation

Every prompt in production carries a declared `review_cadence` in its `prompt.yaml` metadata. The cadence is set by risk classification:

| Risk class | Review cadence |
|---|---|
| Restricted | Quarterly |
| High | Every six months |
| Medium | Annually |
| Low | Annually |

The review evaluates the prompt against four questions:

1. Have the model, the policy, the workflow, or the regulatory environment changed in ways that affect this prompt since the last review?
2. Has the prompt drifted from its eval baseline in production, per the observability data?
3. Has the cost profile drifted from its declared budget?
4. Is there a cheaper model tier the prompt would now pass evals on, given improvements in lower-tier models since the last review?

A review can result in: continuation as-is, a version bump with documented changes, a tier downgrade if a cheaper model now passes, or a sunset decision. The fourth outcome — downgrading to a cheaper model — is the mechanism by which the library actively captures the benefit of improving model quality over time. Without it, every prompt's tier is a high-water mark that never falls.

---

## Stage 7: Policy-triggered review

In addition to periodic revalidation, prompts are reviewed when external triggers fire. The library defines four standard triggers:

- **A policy change** at the firm that touches the prompt's domain — for example, a change to the firm's marketing policy, a new product category, an update to the supervisory framework, or a change in NPI handling rules
- **A regulatory development** — new guidance from the SEC, FINRA, or a state regulator that touches the prompt's domain
- **A model deprecation** — the underlying model the prompt was approved against is being retired by the vendor or removed from the firm's approved-model list
- **A confirmed compliance incident** involving the prompt — a hallucination, a prohibited-language emission, or a supervisory escalation that resulted in a finding

Policy-triggered reviews are not part of the periodic cadence — they fire when the trigger fires. The library does not let a prompt continue running unchanged across a policy boundary it was not approved against.

---

## Stage 8: Sunset and deprecation

A prompt is sunset when it is no longer serving its purpose. The standard sunset triggers are:

- Adoption breadth falls below ten percent of eligible users for two consecutive quarters (the prompt is not earning its operational overhead)
- A successor prompt has shipped and reached general availability (the predecessor is now redundant)
- A regulatory or policy change makes the prompt's use case no longer permissible
- A model deprecation that the prompt cannot be revalidated against in time

Sunset is a documented action, not silent removal. The sunset process produces a written rationale, a deprecation notice to users with a transition path, and a version bump to a final terminal version. The prompt files remain in the repository — they are not deleted — because outputs produced by the prompt during its operational life remain books and records and must be reproducible from their source version indefinitely.

A sunsetted prompt is marked `status: sunset` in its `prompt.yaml`, its `review_cadence` is set to `none`, and it is excluded from the active prompt registry generated by `scripts/generate_prompt_registry.py`. The history remains queryable; the prompt is no longer callable.

---

## Why this matters

The lifecycle above is not bureaucracy for its own sake. Each stage exists because a real failure mode has occurred in real AI deployments without it:

- Without proposal review, prompt libraries accumulate redundant and contradictory prompts that compete for advisor attention.
- Without lower-tier eval gating, tier inflation goes one direction only and cost grows unchecked.
- Without compliance review on the right prompts, regulated communications get drafted by AI without anyone confirming they are permitted to be drafted by AI.
- Without monitored rollout, a prompt that works for fifty pilot advisors silently fails when it reaches five thousand.
- Without periodic revalidation, prompts approved against last year's policy keep running against this year's policy.
- Without policy-triggered review, regulatory changes catch the AI program flat-footed because no one mapped which prompts the change touches.
- Without a sunset process, the library accumulates inactive prompts indefinitely and the operational overhead of governing them grows without bound.

The lifecycle is what turns a prompt library from a folder of useful text into an asset class the firm can actually manage.
