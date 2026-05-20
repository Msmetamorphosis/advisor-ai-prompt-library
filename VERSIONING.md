# Versioning Policy

We treat prompts as code and version them with **semantic versioning** at three layers:

1. **Per-prompt version** — declared in each `prompt.yaml` (`version:`) and tracked in `prompts/<name>/changelog.md`.
2. **Library version** — the Git tag on the repository, tracked in `CHANGELOG.md`.
3. **Registry snapshot** — `prompt-registry.json` regenerated on every release.

A change to one prompt only bumps that prompt's version; the library version is bumped on release cuts.

---

## Semantic Versioning Rules

Format: **`MAJOR.MINOR.PATCH`** (e.g., `1.3.2`).

### MAJOR (`X.0.0`) — breaking change

Bump MAJOR when **any of the following** change in a way that breaks downstream consumers:

- The output schema (`output-schema.json`) changes shape or removes a field.
- The required input fields change (new required `{{placeholder}}` added, or one removed).
- The prompt's scope changes (e.g., expands from "meeting prep" to "meeting prep + portfolio review").
- The risk level increases (Low → Medium or higher).
- A new required approver is introduced.
- The prompt's `prompt_id` changes (rare; only on full rewrites).

A MAJOR change resets compliance review and requires a full approval cycle for the new risk level.

### MINOR (`1.X.0`) — additive, backward compatible

Bump MINOR when:

- A new optional output field is added.
- A new optional input placeholder is added with a sensible default.
- Scope is **narrowed** (e.g., now refuses an additional unsafe case).
- New eval cases are added.
- New human-review flags are introduced (always additive).
- Performance or grounding is improved without changing the contract.

MINOR changes require peer + AI Enablement Lead review. Compliance review is required if the prompt is High / Restricted.

### PATCH (`1.0.X`) — no behavior change

Bump PATCH for:

- Wording refinements that do not change behavior.
- Typo fixes.
- Compliance language tightening (e.g., strengthening a disclosure reminder) that does not alter scope.
- Internal comments, ordering, or formatting in the system prompt.
- Test-suite-only updates.

PATCH releases still require peer review and a passing eval suite, but skip the full compliance gate unless the language change touches regulated disclosures.

---

## Hotfix Policy

A **hotfix** is a patch released outside the normal cadence to address:

- A defect causing demonstrable client-facing risk.
- A compliance finding requiring immediate language correction.
- A model-update regression breaking the eval suite in production.

Hotfix procedure:

1. Branch from the tag of the current production version (not from `main`).
2. Apply the minimal fix.
3. Open a PR labeled `hotfix` — bypasses the standard 24-hour review window but **does not bypass** the eval suite or required approvers.
4. Tag as `vMAJOR.MINOR.PATCH+1` (e.g., `v1.3.4 → v1.3.5`).
5. Forward-port the fix to `main` immediately.

Hotfixes are reported in the next supervisory review packet.

---

## Rollback Strategy

Every released prompt version is a Git tag and is preserved indefinitely. To roll back:

1. Identify the last-known-good tag (e.g., `v1.3.4`).
2. Open a `rollback` PR that restores the prior prompt files and bumps the patch version (`v1.3.5` containing the v1.3.4 content + a changelog note).
3. Regenerate `prompt-registry.json`.
4. Re-run the full pytest suite.
5. Communicate to advisors via release-note channel.

Rollbacks are **always patch bumps forward**, never version-number reversals. Audit history must read monotonically.

---

## Branching Model

```
main                  ← always releasable, all tests passing
├── release/v1.4.0    ← release-candidate branch, frozen for compliance review
├── feature/<prompt>-<change>   ← per-change feature branches
├── hotfix/<prompt>-<issue>     ← urgent fixes branched from prod tag
└── rollback/<prompt>-vX.Y.Z    ← rollback branches
```

Branch rules:

- `main` is protected. Direct commits are disabled.
- All changes arrive via PR with the [`pull_request_template.md`](./.github/pull_request_template.md).
- CI must pass before merge: `pytest` + `validate_prompt_library.py` + registry generation.
- Release branches are cut weekly; emergencies use the hotfix path.

---

## Example Version History

This is what a healthy per-prompt `changelog.md` looks like:

```
v1.0.0 — Initial approved release. (2026-02-01)
        Compliance: J. Reed. AI Enablement: S. Iyer.
v1.1.0 — Added human-review flags for tax/legal mentions. (2026-02-22)
        New optional output field: review_flags[].
v1.1.1 — Compliance language patch: tightened disclosure reminder. (2026-03-15)
v1.2.0 — Added "missing_information" output field. (2026-04-04)
v2.0.0 — Changed output schema: review_flags[] is now required and typed. (2026-05-10)
        Breaking change; downstream CRM connector updated in v2.1.
v2.0.1 — Hotfix: refused to draft when client_identifier is empty. (2026-05-12)
```

A reviewer reading this changelog can answer in 30 seconds: what changed, when, who signed off, and what broke that we fixed.
