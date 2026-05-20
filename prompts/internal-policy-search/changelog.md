# Changelog — internal-policy-search

## v1.0.0 — 2026-05-15

- Initial approved release.
- Risk classified as Medium.
- `retrieval-rules.md` and `citation-rules.md` introduced to formalize what the prompt is allowed to use as a source and how citations must be constructed.
- Refusal path required when `retrieved_sources` is empty or out-of-scope only.
- Out-of-scope handling (tax / legal / investment) explicitly defined.
- Six eval cases covering clean answer, empty-source refusal, out-of-scope tax question, stale-source freshness flag, contradictory sources, and NPI restraint.
- Approvers: prompt owner, AI Enablement Lead.

## v0.9.0 — 2026-05-08 (pilot)

- Pilot release. Added stale-source freshness flag after a pilot answer relied on a 2-year-old SOP that had been superseded.
- Strengthened NPI restraint after one pilot answer echoed a partial account number.

## v0.5.0 — 2026-04-20 (draft)

- Initial draft. Original draft permitted answering from general knowledge when retrieval was thin — that path was eliminated in v0.9.0.
