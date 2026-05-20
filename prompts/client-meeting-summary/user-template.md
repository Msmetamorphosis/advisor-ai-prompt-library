# User Template — Client Meeting Summary

Summarize the advisor-attended client meeting using only the notes below.

---

**Advisor:** {{advisor_name}}
**Client Reference:** {{client_identifier}}
**Meeting Date:** {{meeting_date}}
**Meeting Format:** {{meeting_format}}

---

## Advisor Meeting Notes

{{advisor_meeting_notes}}

---

## Instructions

Produce the structured summary defined by the system prompt and `output-schema.json`. The `crm_ready_note` should be concise enough for advisor review in under 60 seconds. Surface any tax, legal, suitability, or NPI-related items as `human_review_flags`.

Do not produce any client-facing copy.
