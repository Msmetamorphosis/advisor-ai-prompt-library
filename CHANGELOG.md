# Changelog

Built by: Metamorphic Curations LLC — portfolio demonstration, May 2026

All notable changes to the `advisor-ai-prompt-library` are documented here. This file aggregates library-level releases; per-prompt detail lives in each prompt's `changelog.md`.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-05-20

### Added

- Initial approved release of the advisor-ai-prompt-library.
- Six prompt modules, all peer-reviewed, compliance-screened, and eval-passing:
  - `advisor-meeting-prep` v1.0.0 (Medium risk)
  - `client-meeting-summary` v1.0.0 (High risk)
  - `crm-note-assistant` v1.0.0 (Medium risk)
  - `client-follow-up-email` v1.0.0 (High risk)
  - `internal-policy-search` v1.0.0 (Medium risk)
  - `portfolio-review-prep` v1.0.0 (High risk)
- Governance framework: `GOVERNANCE.md`, `VERSIONING.md`, `RISK-TAXONOMY.md`, `EVALUATION-RUBRIC.md`.
- Pytest suite covering required-files, metadata, schema validity, eval-case minimums, prohibited-phrase enforcement, human-review enforcement for Medium/High/Restricted, semantic-version validity, ID uniqueness.
- Validation script (`scripts/validate_prompt_library.py`) and registry generator (`scripts/generate_prompt_registry.py`).
- GitHub PR template and three issue templates (prompt change request, compliance review, bug report).
- Documentation: adoption strategy, advisor workflow map, human-review model, prompt lifecycle, measurement plan.

### Governance

- Approval workflow established per `GOVERNANCE.md` §2.
- Review cadences set per `GOVERNANCE.md` §3 and tracked via `last_reviewed` in each `prompt.yaml`.
- Compliance liaison sign-off recorded for all High-risk prompts.

### Notes

- This is a demonstration portfolio repository. See [`DISCLAIMER.md`](./DISCLAIMER.md).
- No proprietary firm data is included; all examples are synthetic.

---

## [0.9.0] — 2026-05-10 (Pilot)

### Added

- Pilot of all six prompts with a closed group of 12 internal reviewers (mock).
- Initial eval-case authoring (≥5 cases per prompt).
- Draft governance documents circulated for review.

### Changed

- `client-follow-up-email` system prompt tightened to refuse explicit performance language ("will outperform", "guaranteed").
- `internal-policy-search` requires source citation placeholder; refuses if no source is provided.

### Known Issues at Pilot

- `portfolio-review-prep` eval cases needed expansion before GA — completed in v1.0.0.
- Registry generator added late in pilot; not present in 0.9.0.

---

## Upcoming

Planned items not yet shipped (tracked as issues):

- `client-onboarding-checklist` prompt (Medium risk).
- Multilingual disclosure handling for `client-follow-up-email` (MAJOR bump candidate).
- Programmatic eval grader integration.
- Per-prompt usage telemetry dashboard.
