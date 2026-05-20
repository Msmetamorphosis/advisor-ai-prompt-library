# Advisor Workflow Map

This document maps the prompts in the library to the points in the advisor's day where they are most useful. The goal is to make the library navigable not by capability but by *moment*.

---

## A Typical Advisor Day, with the Library

```
   08:00  ┌─ Inbox / planning
          │
   09:00  ├─ Prep for 10:00 client meeting          ◀── advisor-meeting-prep
          │   (CRM context → structured brief)
          │
   10:00  ├─ Client meeting (in-person / video)
          │
   11:00  ├─ Post-meeting CRM documentation         ◀── client-meeting-summary
          │   (advisor notes → summary + CRM note)  ◀── crm-note-assistant
          │
   12:00  ├─ Lunch / market check
          │
   13:00  ├─ Operations question                    ◀── internal-policy-search
          │   (procedure / form lookup)
          │
   14:00  ├─ Draft follow-up to morning client      ◀── client-follow-up-email
          │   (advisor reviews & sends)
          │
   15:00  ├─ Prep for tomorrow's portfolio review   ◀── portfolio-review-prep
          │   (data summary → review agenda)
          │
   16:00  ├─ Calls / informal CRM updates           ◀── crm-note-assistant
          │
   17:00  └─ Wrap up
```

The library does not try to be present at every moment. It targets six recurring moments where the time cost is high and the variance is large.

---

## Workflow Bands

### Before a Meeting

- **`advisor-meeting-prep`** (Medium risk)
  Builds a brief from approved CRM notes and approved context. Output is internal-only.
  *Outcome:* the advisor walks into the meeting with a single page of known facts, open questions, and topics — and explicit "missing information" callouts if context is thin.

### During the Meeting

The library deliberately does **not** ship a real-time-transcript prompt. Real-time transcription introduces:
- A second model in the loop (speech-to-text).
- Recording-consent and supervisory recording requirements.
- A failure mode where misheard content becomes part of the record.

Real-time use is intentionally out of scope at v1.0.0. It is on the [`prompt-lifecycle.md`](./prompt-lifecycle.md) backlog under a separate intake.

### After the Meeting

- **`client-meeting-summary`** (High risk)
  The advisor's own meeting notes become a structured summary with a CRM-ready note draft.
- **`crm-note-assistant`** (Medium risk)
  Quick, tight CRM entries for non-meeting events (calls, voicemails, emails, address changes).

### CRM Documentation Generally

- **`crm-note-assistant`** (Medium risk)
  Any moment the advisor would otherwise type a CRM note manually. Source-grounded; no characterization; ends in "Draft — pending advisor review."

### Operational / Policy Lookup

- **`internal-policy-search`** (Medium risk)
  Any moment the advisor or CSA needs to know "what's our procedure for X." Strictly source-grounded with citations; refuses when sources are absent.

### Client Communication

- **`client-follow-up-email`** (High risk)
  Drafts a follow-up after a meeting. Advisor reviews and edits before sending. Required closer is non-paraphrasable. Refuses if the meeting summary contains content that cannot be safely communicated.

### Portfolio Review Prep

- **`portfolio-review-prep`** (High risk)
  Internal agenda from approved data summary and prior goals. No recommendations. No target weights. No projections.

---

## Workflow Coverage Matrix

| Workflow moment | Prompt | Risk | Output is for | Client-visible? |
|---|---|---|---|---|
| Before meeting | `advisor-meeting-prep` | Medium | Advisor | No |
| Post-meeting summary | `client-meeting-summary` | High | Advisor (may inform CRM) | No directly; basis for follow-up |
| CRM note | `crm-note-assistant` | Medium | Advisor → CRM | No |
| Follow-up email | `client-follow-up-email` | High | Client (after advisor review) | Yes |
| Policy lookup | `internal-policy-search` | Medium | Internal user | No |
| Portfolio review prep | `portfolio-review-prep` | High | Advisor | No |

---

## What Is Not in This Library (and Why)

- **Onboarding-document generation** — touches forms and required disclosures; needs its own program.
- **Performance-attribution narratives** — too easy to drift into projection/comparison; deferred.
- **Trade rationale drafting** — out of scope for advisor productivity; belongs to a separately governed product surface.
- **Client-direct chat / "ask the advisor's AI"** — out of scope at v1.0.0. The library never produces output the client sees without advisor edit.

These omissions are deliberate. The library's value comes from being narrow and trustworthy, not broad and aspirational.
