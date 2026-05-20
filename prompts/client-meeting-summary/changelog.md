# Changelog — client-meeting-summary

## v1.0.0 — 2026-05-15

- Initial approved release.
- Risk classified as High (output may inform client-facing follow-up).
- Compliance review completed by Compliance Liaison.
- Strict JSON output schema established (`output-schema.json`).
- `human_review_flags` required as a structured array with `topic` and `reason`.
- Six eval cases covering standard, performance/guarantee language, sparse notes, multi-owner action items, suitability bait, and NPI restraint.
- Approvers: prompt owner, AI Enablement Lead, Compliance Liaison.

## v0.9.0 — 2026-05-08 (pilot)

- Pilot release. Moved from free-text output to a strict JSON schema after a pilot reviewer noted inconsistent action-item structure.
- Added "Draft — pending advisor review" closing line in `crm_ready_note`.

## v0.5.0 — 2026-04-25 (draft)

- Initial draft. CRM note output was free-form.
