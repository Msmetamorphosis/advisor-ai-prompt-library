# Example Release Note — Library v1.0.0

**Date:** 2026-05-20
**Audience:** Advisors, CSAs, Operations
**Maintainer:** AI Enablement — Advisor Productivity

This document is a realistic example of the release note that would accompany the v1.0.0 cut of the library. It uses the format from [`templates/release-note-template.md`](../templates/release-note-template.md) and is preserved here for reference.

---

## What's New

The first production release of the advisor AI prompt library — six prompts covering pre-meeting prep, meeting summary, CRM note documentation, client follow-up email drafts, internal policy search, and portfolio review prep. Every prompt has passed compliance review for its risk level and ships with an eval-case regression suite.

## Affected Prompts

| Prompt | Prior Version | New Version | Change Type |
|---|---|---|---|
| `advisor-meeting-prep` | n/a | `v1.0.0` | Initial release |
| `client-meeting-summary` | n/a | `v1.0.0` | Initial release |
| `crm-note-assistant` | n/a | `v1.0.0` | Initial release |
| `client-follow-up-email` | n/a | `v1.0.0` | Initial release |
| `internal-policy-search` | n/a | `v1.0.0` | Initial release |
| `portfolio-review-prep` | n/a | `v1.0.0` | Initial release |

## What Changed (for advisors)

- Six new prompts are available in the advisor tool, organized by workflow moment.
- Each prompt explicitly tells you (in the system prompt and in the on-screen helper) what it will and will not do.
- Outputs that are intended to reach a client are clearly labeled "Draft — pending advisor review."
- Tax-, legal-, suitability-, and performance-related topics are surfaced as `human_review_flags` rather than answered.
- The internal policy search refuses to answer if it can't cite an approved source.

## What Did Not Change

- Your existing workflows in CRM, email, and portfolio tools are unchanged. The library produces drafts; you decide what to save and send.
- No prompt sends anything on your behalf.

## What Advisors Need to Do

- [ ] Skim the new prompt catalog page in the advisor tool.
- [ ] Try one prompt against a real workflow this week and report back via the in-tool feedback link.
- [ ] Acknowledge the v1.0.0 release in the enablement portal (one click).
- [ ] Attend one of the optional 20-minute walkthrough sessions (calendar link in the portal).

## Known Limitations

- No real-time transcription or in-meeting prompt at v1.0.0. The library targets before-, after-, and between-meeting moments.
- `internal-policy-search` quality depends on the retrieval corpus. If you find a policy that should be retrievable but isn't, please flag it via the in-tool feedback link.
- `client-follow-up-email` will refuse to draft if your meeting summary contains content that cannot be safely communicated. That refusal is intentional — please reach out to your supervisor or compliance liaison rather than rewording the summary to "get around" it.

## How to Report Issues

- For incorrect or unsafe output: use the bug-report path in the advisor tool, which files an issue using the [Bug Report template](../.github/ISSUE_TEMPLATE/bug_report.md).
- For new prompts you'd like to see: file a [Prompt Change Request](../.github/ISSUE_TEMPLATE/prompt_change_request.md).

## Rollback Information

If v1.0.0 causes a defect:

- Last known-good tag: n/a (this is the initial release; rollback is to pre-library workflow).
- Rollback contact: AI Enablement — Advisor Productivity.
- Expected rollback SLA: 4 business hours for `client-follow-up-email` (client-facing). 1 business day for other prompts.

---

## Behind-the-Scenes Detail

For the audience that wants it (typically pilot participants and supervisors), here's the high-level decision rationale for v1.0.0:

1. **Why these six prompts first.** They cover the highest-volume non-client-facing-time tasks identified in the workflow analysis. They are bounded enough to ship safely.
2. **Why we deferred real-time transcription.** Because consent, supervisory recording, and second-model error layering are non-trivial. We will return to it once v1.0.0 metrics are stable.
3. **Why we shipped four Medium-risk prompts and three High-risk prompts at once.** The High-risk prompts share boundary patterns (refuse, redirect, no advice, required closer), so reviewing them in a single batch was more efficient than staggering and rebuilding context across separate reviews.
4. **Why every prompt has a refusal path.** Because the way advisors lose trust in AI is the first time they get an answer that should have been a refusal. We chose to over-invest in refusal quality at v1.0.0.

If you have questions about any of these decisions, file an issue or reach out directly.
