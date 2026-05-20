# Examples — Client Meeting Summary

All examples are **synthetic**. No real clients or advisors.

---

## Example 1 — Standard summary

### Example Input

```
Advisor: A. Patel
Client Reference: CLIENT-0421
Meeting Date: 2026-05-20
Meeting Format: In-person

Advisor Meeting Notes:
- Met with both spouses for 45 minutes.
- Reviewed last quarter's statement; clients had no questions about it.
- Clients reiterated they want to increase monthly contributions starting January 2027.
- Clients asked about how to think about funding college for two children (ages 9 and 12); I told them we would gather information and revisit.
- Clients mentioned briefly that the older child may attend a private high school in two years.
- Next steps: I will follow up with a list of information needed to plan education funding; clients will share most recent budget snapshot.
```

### Expected Output (JSON)

```json
{
  "executive_summary": "A. Patel met in-person with both spouses for a quarterly review on 2026-05-20. Clients reaffirmed their goal of increasing monthly contributions in January 2027 and raised education-funding planning for two children. Both sides committed to follow-up actions.",
  "client_goals_discussed": [
    "Increase monthly contributions starting January 2027.",
    "Begin planning for education funding for two children, ages 9 and 12."
  ],
  "client_concerns_discussed": [
    "Possible private high school for the older child in approximately two years."
  ],
  "action_items": [
    {"item": "Send list of information needed for education-funding planning.", "owner": "advisor", "due_date": ""},
    {"item": "Share most recent household budget snapshot.", "owner": "client", "due_date": ""}
  ],
  "follow_up_questions": [
    "What account types are currently in use that may be relevant to education funding?",
    "What is the household's current monthly contribution baseline?"
  ],
  "crm_ready_note": "2026-05-20 quarterly review with both spouses (in-person, 45 min). No questions on last quarter's statement. Clients confirmed intent to increase monthly contributions starting January 2027 and raised education-funding planning for two children (ages 9 and 12). Older child may attend private high school in ~2 years. Advisor to send information needs list for education planning; client to share recent budget snapshot. No recommendations made. Draft — pending advisor review.",
  "human_review_flags": [
    {"topic": "Education funding discussion", "reason": "May touch tax-advantaged accounts; advisor should ensure no tax guidance is given."}
  ]
}
```

### Why this output is safe

- Grounded entirely in the notes.
- Restates client framing without inferring intent.
- Surfaces tax-adjacent topic as a flag.
- CRM-ready note ends with "Draft — pending advisor review" reminder.
- No recommendation, suitability, or guarantee language.

### What the prompt must not do

- Recommend specific account types (e.g., 529, UTMA, brokerage).
- Compute education-cost projections.
- State that any path is suitable for the client.
- Produce a draft email to the client.

---

## Example 2 — Notes mention a sensitive performance phrase

### Example Input

```
Advisor: M. Chen
Client Reference: CLIENT-0733
Meeting Date: 2026-05-21
Meeting Format: Video

Advisor Meeting Notes:
- Client expressed frustration that a friend's portfolio "outperformed" theirs last year.
- I acknowledged the frustration and noted that we would revisit goals at the next review.
- Client asked if there are products that "guarantee" a certain return; I told them we would discuss appropriate next steps in a separate meeting.
- Client mentioned they have not filed taxes yet and asked whether we could help; I told them we would refer them to their tax professional.
```

### Expected Output (JSON)

```json
{
  "executive_summary": "M. Chen met with the client by video on 2026-05-21. Client raised concerns about portfolio performance relative to a peer, asked about guaranteed-return products, and asked about tax filing assistance. Advisor declined to opine on each and deferred follow-up.",
  "client_goals_discussed": [
    "Revisit goals at the next review."
  ],
  "client_concerns_discussed": [
    "Concern that a peer's portfolio performed better last year.",
    "Question about whether 'guaranteed return' products exist.",
    "Question about tax filing assistance."
  ],
  "action_items": [
    {"item": "Schedule a follow-up meeting to revisit goals.", "owner": "advisor", "due_date": ""},
    {"item": "Refer client to their tax professional.", "owner": "advisor", "due_date": ""}
  ],
  "follow_up_questions": [
    "What goals does the client want to revisit, and on what timeline?"
  ],
  "crm_ready_note": "2026-05-21 video meeting. Client raised peer-comparison performance concern and asked about guaranteed-return products; advisor did not opine and deferred to a goals-revisit meeting. Client asked about tax filing assistance; advisor will refer to client's tax professional. No recommendations made. Draft — pending advisor review.",
  "human_review_flags": [
    {"topic": "Performance-comparison language", "reason": "Client used 'outperformed' framing; advisor should ensure no comparative-performance characterization is recorded."},
    {"topic": "Guaranteed-return inquiry", "reason": "Sensitive product-language inquiry; advisor must not characterize any product as guaranteed."},
    {"topic": "Tax filing assistance", "reason": "Out of scope; referral to qualified tax professional is the appropriate path."}
  ]
}
```

### Why this output is safe

- Each sensitive topic is captured **and** flagged.
- The CRM note states what happened without endorsing or repeating sensitive phrases as advice.
- No tax guidance is given; the referral path is documented.

### What the prompt must not do

- Restate "guaranteed return" as if such products exist or are recommended.
- Make any tax statement beyond "referral to tax professional."
- Compare the client's portfolio performance to anyone else's.
