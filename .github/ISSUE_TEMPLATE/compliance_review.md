---
name: Compliance Review
about: Request compliance review of a prompt or pending release.
title: "[COMPLIANCE] <prompt id> v<x.y.z>"
labels: compliance-review
assignees: ''
---

## Prompt(s) Under Review

- Prompt ID: `<id>`
- Version: `<vX.Y.Z>`
- Risk level: <Low / Medium / High / Restricted>
- Prompt Owner: `@<name>`

## Trigger for This Review

- [ ] Initial release
- [ ] Scheduled re-review (per `GOVERNANCE.md` §3)
- [ ] Model version change
- [ ] Regulatory advisory (cite below)
- [ ] Incident / near-miss (cite incident ID)
- [ ] Scope or risk-level change

## Materials Provided

- [ ] `prompt.yaml`
- [ ] `system.md`
- [ ] `user-template.md`
- [ ] `examples.md`
- [ ] `eval-cases.json` and recent eval results
- [ ] `compliance-constraints.md` (if client-facing)
- [ ] Output samples (sanitized)

## Reviewer Focus Areas

Please assess against [`RISK-TAXONOMY.md`](../../RISK-TAXONOMY.md) and [`EVALUATION-RUBRIC.md`](../../EVALUATION-RUBRIC.md), with particular attention to:

1. Boundary fidelity — what the prompt refuses to do.
2. Refusal quality — clarity, escalation path.
3. Disclosure adequacy — presence and prominence of required language.
4. Supervisory traceability — can a supervisor reconstruct what was sent?
5. Eval coverage — do test cases include the failure modes you care about?

## Reviewer Decision

- [ ] Approved as drafted
- [ ] Approved with required changes (list below)
- [ ] Rejected — re-draft required

### Required changes

<!-- numbered list of specific changes -->

## Sign-off

- Reviewer: `@<name>`
- Date: `YYYY-MM-DD`
- Next mandatory review: `YYYY-MM-DD`
