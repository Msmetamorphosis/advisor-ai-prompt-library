---
name: Prompt Change Request
about: Request a new prompt or a change to an existing prompt.
title: "[PROMPT] <short description>"
labels: prompt-change-request
assignees: ''
---

## Type of Change

- [ ] New prompt
- [ ] Modify existing prompt (behavior change)
- [ ] Modify existing prompt (wording / patch only)
- [ ] Retire prompt

## Affected Prompt

- Prompt ID: `<id or "new">`
- Current version: `<vX.Y.Z>`
- Proposed new version: `<vX.Y.Z>`
- Proposed risk level: Low / Medium / High / Restricted

## Business Justification

<!-- What advisor workflow does this serve? What is the cost of not doing it? -->

## Requested Behavior

<!-- Describe what the prompt should produce, what it should refuse, and any required output fields. -->

## Inputs

<!-- What approved inputs does the prompt require? Reference any retrieval sources. -->

## Compliance Considerations

- [ ] Could output reach a client?
- [ ] Could output touch suitability, advice, tax, legal, or NPI?
- [ ] Does this require new disclosure language?
- [ ] Does this change require Compliance Liaison review?

## Success Criteria

<!-- How will we know this is working? Reference rubric dimensions and target scores. -->

## Acceptance Checklist

- [ ] `prompt.yaml` drafted with all required metadata.
- [ ] `system.md` drafted with role, scope, allowed/prohibited behavior, human-review reminder.
- [ ] `user-template.md` drafted with `{{placeholders}}`.
- [ ] `examples.md` includes safe and unsafe-but-refused examples.
- [ ] `eval-cases.json` includes ≥5 cases including edge / refusal cases.
- [ ] `changelog.md` entry drafted.
- [ ] Risk classification confirmed.
