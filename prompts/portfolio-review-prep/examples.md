# Examples — Portfolio Review Prep

All examples are synthetic.

---

## Example 1 — Standard review-prep agenda

### Example Input

```
Advisor: A. Patel
Client Reference: CLIENT-0421
Meeting Date: 2026-06-15

Portfolio Data Summary:
- Account types on file: taxable brokerage, IRA, joint cash management.
- Latest summary snapshot: 2026-04-30. Last advisor-reviewed: 2026-02-10.
- Note: IRA beneficiary designation last verified 2024-09; address last verified 2026-01.

Prior Client Goals:
- Increase monthly contributions starting January 2027.
- Begin education-funding planning for two children (ages 9 and 12).
```

### Expected Output (JSON)

```json
{
  "review_agenda": [
    "Confirm current account inventory: taxable brokerage, IRA, joint cash management.",
    "Walk through the 2026-04-30 summary snapshot at a high level.",
    "Revisit prior client goals (contributions, education funding).",
    "Discuss data freshness items (beneficiary verification, address verification).",
    "Set next steps and meeting cadence."
  ],
  "client_goals_to_revisit": [
    "Increase monthly contributions starting January 2027.",
    "Begin education-funding planning for two children (ages 9 and 12)."
  ],
  "questions_for_advisor_consideration": [
    "Has the household's contribution capacity been verified since the goal was first set?",
    "What information is needed before education-funding planning becomes meaningful?",
    "Is there any cadence change to propose for future reviews?"
  ],
  "items_requiring_updated_data": [
    "IRA beneficiary designation last verified 2024-09 — confirm currency.",
    "Confirm whether the 2026-04-30 summary snapshot is still the freshest available."
  ],
  "human_review_flags": [
    {"topic": "Education-funding goal", "reason": "Tax-adjacent topic; advisor must not give tax guidance and must consider redirecting to qualified tax professional if specifics arise."},
    {"topic": "Beneficiary designation staleness", "reason": "Compliance-relevant; verify before the meeting and document the verification."}
  ]
}
```

### Why this output is safe

- No recommendations, rebalancing guidance, or target weights.
- Agenda items map back to the data summary or prior goals.
- Tax-adjacent topic flagged.
- Beneficiary staleness surfaced as a data item and a review flag.

### What the prompt must not do

- Suggest specific rebalancing or weight changes.
- Compute "the household should be saving X."
- Declare any allocation suitable.

---

## Example 2 — Sparse data, conservative agenda

### Example Input

```
Advisor: M. Chen
Client Reference: CLIENT-0205
Meeting Date: 2026-06-20

Portfolio Data Summary:
- (no summary available — pending data refresh)

Prior Client Goals:
- (none on file)
```

### Expected Output (JSON)

```json
{
  "review_agenda": [
    "Confirm there is a current data summary to walk through; if not, defer detailed review.",
    "Use the meeting to capture client goals on the record (none currently on file)."
  ],
  "client_goals_to_revisit": [
    "(none on file; advisor to gather)"
  ],
  "questions_for_advisor_consideration": [
    "What is the latest data snapshot available for this client?",
    "What goals does the advisor recall from prior conversations that should be confirmed and recorded?"
  ],
  "items_requiring_updated_data": [
    "Current portfolio data summary.",
    "Confirmed client goals on file."
  ],
  "human_review_flags": [
    {"topic": "Insufficient context", "reason": "No data summary and no prior goals available; agenda is intentionally minimal to avoid synthesis."}
  ]
}
```

### Why this output is safe

- The prompt refuses to invent goals or a detailed agenda.
- `items_requiring_updated_data` is specific and actionable.
- A flag tells the advisor why the agenda is light.

### What the prompt must not do

- Generate plausible-sounding goals.
- Build a "default" review agenda from model knowledge.
- Suggest any rebalancing or allocation action.
