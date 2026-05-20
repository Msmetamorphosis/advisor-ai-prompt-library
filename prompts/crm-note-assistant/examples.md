# Examples — CRM Note Assistant

All examples are synthetic.

---

## Example 1 — Tight note from a phone-call recap

### Example Input

```
Advisor: A. Patel
Client Reference: CLIENT-0421
Note Topic: Phone check-in 2026-05-19

Source Material:
- 10-minute phone check-in.
- Client confirmed contact info on file.
- Client mentioned upcoming travel through July; prefers email over phone in that window.
- Client asked to revisit education-funding topic at the next in-person meeting.
```

### Expected Output (JSON)

```json
{
  "crm_note": "2026-05-19 phone check-in (10 min). Client confirmed contact info on file, will be traveling through July and prefers email contact in that window, and requested that education-funding planning be revisited at the next in-person meeting. Draft — pending advisor review.",
  "source_evidence": [
    {"claim": "10-minute phone check-in", "source_excerpt": "10-minute phone check-in."},
    {"claim": "Confirmed contact info", "source_excerpt": "Client confirmed contact info on file."},
    {"claim": "Traveling through July; prefers email", "source_excerpt": "upcoming travel through July; prefers email over phone in that window."},
    {"claim": "Revisit education-funding at next in-person meeting", "source_excerpt": "asked to revisit education-funding topic at the next in-person meeting."}
  ],
  "review_flags": [
    {"topic": "Education-funding topic", "reason": "Tax-adjacent topic; advisor must ensure no tax guidance is given at follow-up."}
  ],
  "missing_information": [
    "Specific date for the next in-person meeting."
  ]
}
```

### Why this output is safe

- Every sentence in the CRM note ties to a source-evidence pair.
- The advisor isn't characterized (no "the client is anxious").
- Tax-adjacent topic is flagged for the next meeting.

### What the prompt must not do

- Speculate about the client's preferences beyond what was said.
- Recommend a specific education-funding vehicle.
- Echo account numbers if present.

---

## Example 2 — Source material too thin

### Example Input

```
Advisor: S. Iyer
Client Reference: CLIENT-0205
Note Topic: Voicemail received

Source Material:
- Voicemail from client. Could not make out details.
```

### Expected Output (JSON)

```json
{
  "crm_note": "2026 voicemail received from client; specifics could not be discerned from the source material. Advisor to follow up to confirm purpose. Draft — pending advisor review.",
  "source_evidence": [
    {"claim": "Voicemail received from client", "source_excerpt": "Voicemail from client. Could not make out details."}
  ],
  "review_flags": [],
  "missing_information": [
    "Purpose of the voicemail.",
    "Date of receipt.",
    "Whether a callback was attempted."
  ]
}
```

### Why this output is safe

- The note does not invent a topic.
- `missing_information` is specific and actionable.
- The advisor is steered to follow up rather than fabricate a record.

### What the prompt must not do

- Invent a topic the voicemail was about.
- Characterize the client's tone (no "sounded upset").
- Insert any advice or recommendation.
