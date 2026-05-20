---
name: Bug Report
about: Report incorrect, unsafe, or broken prompt output.
title: "[BUG] <prompt id>: <short description>"
labels: bug
assignees: ''
---

## Severity

- [ ] **P0** — Output reached or could reach a client; compliance-sensitive.
- [ ] **P1** — Eval case failing; production impact within hours.
- [ ] **P2** — Quality regression; no immediate compliance risk.
- [ ] **P3** — Cosmetic / minor wording.

## Affected Prompt

- Prompt ID: `<id>`
- Version: `<vX.Y.Z>`
- Risk level: `<Low/Medium/High/Restricted>`

## What Happened

<!-- Describe the observed behavior. Include sanitized input and output. -->

## What Was Expected

<!-- Describe the expected behavior with reference to the prompt's `system.md` and `examples.md`. -->

## Reproduction

1. Input (sanitized — no PII / NPI):

```
<input>
```

2. Resulting output:

```
<output>
```

3. Environment:
   - LLM provider / model:
   - Library version:
   - Where the prompt was invoked (advisor tool / CRM plugin / etc.):

## Impact

- [ ] Output was sent to a client.
- [ ] Output was used in CRM but never sent.
- [ ] Output was caught in advisor review.
- [ ] Output was caught in automated check.

## Suggested Disposition

- [ ] Hotfix (patch bump)
- [ ] Schedule fix in next sprint
- [ ] Roll back to last known good version
- [ ] Pause prompt pending investigation

## Compliance Notification

- [ ] Compliance has been notified (required for P0).
- [ ] Supervisor has been notified (required for P0 if output was sent to a client).
- [ ] N/A
