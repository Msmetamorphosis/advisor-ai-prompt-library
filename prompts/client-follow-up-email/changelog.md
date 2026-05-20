# Changelog — client-follow-up-email

## v1.0.0 — 2026-05-15

- Initial approved release.
- Risk classified as High.
- Compliance review completed by Compliance Liaison.
- `compliance-constraints.md` introduced; required closer made non-paraphrasable.
- Refusal path added when meeting summary contains content that cannot be safely drafted.
- Six eval cases covering standard, sensitive-topic redirect, NPI restraint, required-closer immutability, unsafe-input refusal, and marketing-language resistance.
- Approvers: prompt owner, AI Enablement Lead, Compliance Liaison.

## v0.9.0 — 2026-05-08 (pilot)

- Pilot release. After pilot, refusal path was added because the draft sometimes attempted to draft an email even when the meeting summary contained recommendation language.
- Tightened against echoing client-uttered "guaranteed" or "outperform" language.
- Required closer locked to verbatim form to prevent paraphrasing drift.

## v0.5.0 — 2026-04-29 (draft)

- Initial draft. Required-closer wording was paraphrasable; this was the first issue compliance flagged.
