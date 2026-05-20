# Pull Request

## 1. Business Reason

<!-- Why does this change exist? What advisor problem does it solve? Reference the issue if applicable. -->

## 2. Prompt(s) Changed

| Prompt ID | Old Version | New Version | Change Type (Major / Minor / Patch / Hotfix) |
|---|---|---|---|
| `prompt-xxx` | `v1.2.0` | `v1.3.0` | Minor |

## 3. Risk Level

- [ ] Low
- [ ] Medium
- [ ] High
- [ ] Restricted

Has the risk level changed in this PR? If yes, justify: <!-- text -->

## 4. Test Results

- [ ] `pytest` passes locally.
- [ ] `python scripts/validate_prompt_library.py` returns 0.
- [ ] `python scripts/generate_prompt_registry.py` succeeds and the diff is committed.
- [ ] Eval suite for affected prompt(s) was re-run.
- [ ] No regression vs. the prior version on any rubric dimension.

Paste the eval summary:

```
Prompt: <id>
Cases run: <n>
Mean Compliance Safety: <score>
Min Compliance Safety: <score>
Mean Hallucination Resistance: <score>
Min Hallucination Resistance: <score>
Delta vs. previous version: <+/->
```

## 5. Compliance Impact

- [ ] No compliance impact (Low risk or PATCH wording).
- [ ] Compliance review requested (Medium / High / Restricted).
- [ ] Compliance reviewer: `@<name>` — date: `YYYY-MM-DD`.
- [ ] Disclosure / refusal language reviewed and unchanged, **or** changes are listed below.

Disclosure or refusal language changes:

<!-- diff or quoted text -->

## 6. Screenshots / Example Outputs

<!-- Paste before/after sample outputs from a representative eval case. -->

**Before:**

```
<output from previous version>
```

**After:**

```
<output from this version>
```

## 7. Rollback Plan

- [ ] Last known-good tag: `v<x.y.z>`
- [ ] Rollback PR template ready (link or stub).
- [ ] If client-facing prompt: advisor communication plan attached.

## 8. Approvers

Per [`GOVERNANCE.md`](../GOVERNANCE.md) §2:

- [ ] Prompt Owner: `@<name>`
- [ ] Peer Reviewer: `@<name>`
- [ ] AI Enablement Lead: `@<name>` (Medium+)
- [ ] Compliance Liaison: `@<name>` (High / Restricted)
- [ ] Business Unit Sponsor: `@<name>` (Restricted)

## 9. Checklist

- [ ] `changelog.md` updated for each affected prompt.
- [ ] Top-level `CHANGELOG.md` updated if this is a release cut.
- [ ] `last_reviewed` and `approved_by` updated in `prompt.yaml`.
- [ ] No prohibited phrases introduced in production prompt text.
- [ ] No PII, NPI, or client identifiers in test fixtures or examples.
