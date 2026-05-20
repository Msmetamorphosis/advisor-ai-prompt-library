# Changelog — portfolio-review-prep

## v1.0.0 — 2026-05-15

- Initial approved release.
- Risk classified as High.
- Compliance review completed by Compliance Liaison.
- Strict JSON output schema established; `human_review_flags` is a typed array.
- Prohibitions against rebalancing guidance, target weights, projections, and suitability statements enforced in `system.md` and tested.
- Six eval cases covering standard agenda, sparse-input conservatism, no-rebalancing restraint, stale-data flag, no-projection restraint, and suitability restraint.
- Approvers: prompt owner, AI Enablement Lead, Compliance Liaison.

## v0.9.0 — 2026-05-08 (pilot)

- Pilot release. Tightened against rebalancing language after a pilot output proposed "shifting" allocation.
- Added stale-data flag after a pilot output worked off a 6-month-old snapshot without surfacing the staleness.

## v0.5.0 — 2026-04-25 (draft)

- Initial draft. Output occasionally suggested "target weight" language; removed in v0.9.0.
