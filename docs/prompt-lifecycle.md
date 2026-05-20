# Prompt Lifecycle

Every prompt in this library moves through nine lifecycle stages. Stage progression is gated; backward movement is supported (and expected).

```
   Intake  →  Draft  →  Risk Classify  →  Test  →  Compliance Review
                                                            │
                                                            ▼
              Retire  ←  Revise  ←  Monitor  ←  Production  ←  Pilot
```

---

## 1. Intake

**Triggers:** an advisor asks for help with a recurring task; a workflow analysis identifies a high-cost moment; a regulatory advisory creates a new need.

**Entry conditions:**
- A clear business problem statement.
- A named requester and a named owner candidate.
- An estimate of frequency / population.

**Exit conditions:**
- Intake issue opened from [`prompt_change_request.md`](../.github/ISSUE_TEMPLATE/prompt_change_request.md).
- AI Enablement Lead has accepted the intake.

**Anti-pattern:** "Build an AI for X." Intake must describe a *workflow*, not a *capability*.

---

## 2. Draft

**Activity:** the prompt owner authors the initial `prompt.yaml`, `system.md`, `user-template.md`, `examples.md`, and a starter `eval-cases.json`.

**Exit conditions:**
- All required files present.
- Validation script (`scripts/validate_prompt_library.py`) returns 0.
- Peer reviewer has commented on the system prompt's scope and boundary language.

---

## 3. Risk Classify

**Activity:** apply the decision tree from [`RISK-TAXONOMY.md`](../RISK-TAXONOMY.md).

**Exit conditions:**
- `risk_level` set in `prompt.yaml`.
- `human_review_required` set to `true` for Medium / High / Restricted.
- Approver list in `approved_by` matches the classification.

**Anti-pattern:** classifying down to skip compliance review. The decision rule is "when unsure, classify one level higher."

---

## 4. Test

**Activity:** author ≥5 eval cases, including:
- A standard / happy-path case.
- A refusal / insufficient-context case.
- An out-of-scope / sensitive-topic case.
- An edge case (sparse input, contradictory input, numeric restraint).
- A failure-mode case the team is specifically worried about.

**Exit conditions:**
- `pytest` passes.
- Eval cases run against the target LLM with all rubric scores ≥4 (≥5 on Compliance Safety and Hallucination Resistance).

---

## 5. Compliance Review

**Activity:** for Medium+ prompts, the compliance liaison reviews materials and either signs off, requests changes, or rejects.

**Exit conditions:**
- `approved_by.compliance_liaison` set in `prompt.yaml` (for High / Restricted).
- `last_reviewed` updated.
- Any change requests are integrated and re-tested.

---

## 6. Pilot

**Activity:** the prompt is deployed to a closed group (typically ≤20 advisors).

**During pilot:**
- All invocations are observed.
- Failure modes are captured as new eval cases.
- Advisor feedback is collected and triaged into either prompt changes or training opportunities.

**Exit conditions:**
- Pilot duration met (typically 2–4 weeks).
- No P0/P1 issues open.
- Quantitative success criteria from `measurement-plan.md` met.

---

## 7. Production Release

**Activity:** the prompt is moved to `status: production` and rolled out broadly.

**Required artifacts:**
- Tagged Git release.
- Top-level `CHANGELOG.md` entry.
- Per-prompt `changelog.md` entry.
- Release note from [`release-note-template.md`](../templates/release-note-template.md).
- Regenerated `prompt-registry.json`.
- Approval record from [`approval-record-template.md`](../templates/approval-record-template.md).

---

## 8. Monitor

**Activity:**
- Eval suite re-runs on a schedule (at minimum weekly for High / Restricted, monthly for Medium, at every release).
- Bug reports from advisors are triaged within 1 business day.
- Telemetry tracks the metrics defined in `measurement-plan.md`.

**Triggers for moving back to Revise:**
- Eval regression.
- Underlying LLM version change.
- Compliance advisory.
- Sustained adoption drop or escalation spike.
- Reported incident or near-miss.

---

## 9. Revise / Retire

### Revise

A revision starts a new mini-loop: a new `draft` → `test` → `review` cycle, but scoped to the change. Version is bumped per `VERSIONING.md`.

### Retire

A prompt is retired when:
- It is superseded by a newer prompt with different scope.
- The workflow it supported no longer exists.
- Risk review concludes it cannot be safely operated.

Retirement requires `status: retired`, a final changelog entry, a 30-day deprecation window, and registry preservation.

---

## Visual: Stages and Gates

```
 ┌────────┐    ┌───────┐    ┌──────────────┐    ┌──────┐    ┌────────────────┐
 │ Intake │ -> │ Draft │ -> │ Risk Classify│ -> │ Test │ -> │ Compliance Rvw │
 └────────┘    └───────┘    └──────────────┘    └──────┘    └───────┬────────┘
                                                                     │
                              ┌──────────────────────────────────────┘
                              ▼
                         ┌────────┐    ┌──────────────┐    ┌─────────┐
                         │ Pilot  │ -> │ Production   │ -> │ Monitor │
                         └────────┘    └──────────────┘    └────┬────┘
                                                                │
                                       ┌────────────────────────┘
                                       ▼
                                  ┌─────────┐
                                  │ Revise  │  (→ Test, → Compliance Rvw, etc.)
                                  └─────────┘
                                       │
                                       ▼
                                  ┌─────────┐
                                  │ Retire  │
                                  └─────────┘
```

Each transition is a gated event with explicit entry / exit conditions. None of them is automatic.
