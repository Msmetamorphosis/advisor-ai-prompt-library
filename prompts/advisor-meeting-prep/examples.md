# Examples — Advisor Meeting Prep

All examples are **synthetic**. No real clients, advisors, accounts, or firms.

---

## Example 1 — Standard pre-meeting brief

### Example Input

```
Advisor: A. Patel
Client Reference: CLIENT-0421
Meeting Date: 2026-05-22

CRM Notes:
- 2026-03-14: Client mentioned interest in increasing monthly contributions next year. Asked about education funding for two children, ages 9 and 12.
- 2026-04-02: Sent confirmation of last quarter statement. Client acknowledged receipt.
- 2026-04-30: Client asked whether college planning conversations would be appropriate for the May meeting.

Approved Context:
- Last review meeting: 2026-02-10. Discussed long-term goals and household budgeting cadence.
```

### Expected Output

```
known_facts:
- Client expressed interest in increasing monthly contributions next year (note 2026-03-14).
- Two children, ages 9 and 12 (note 2026-03-14).
- Last review meeting was 2026-02-10 (approved context).
- Last quarterly statement acknowledged on 2026-04-02.

client_stated_goals:
- Increase monthly contributions next year.
- Explore education funding for two children.

prior_action_items:
- Confirmation of quarterly statement (status: done, 2026-04-02).

open_questions:
- What is the client's current monthly contribution baseline?
- What account types are available or in use for education funding?
- What is the planned timeline for the contribution increase?

suggested_conversation_topics:
- Confirm the goals captured above are still current.
- Discuss what information the advisor needs to assess education-funding options at a future meeting.
- Confirm cadence and format for future reviews.

missing_information:
- Current contribution baseline.
- Current account inventory relevant to education funding.

human_review_flags:
- Topic "education funding" may touch tax-advantaged accounts and tax-adjacent guidance; advisor should ensure no tax advice is given.
```

### Why this output is safe

- Every "known fact" is grounded in a specific note.
- Goals are restated in the client's own framing.
- No recommendation, no suitability statement, no projection.
- The tax-adjacent topic is surfaced as a `human_review_flag`, not stripped.

### What the prompt must not do

- Recommend a specific account type (e.g., "open a 529").
- State that any product is suitable.
- Generate language the advisor could paste into a client email.
- Invent the client's name, account numbers, or balances.

---

## Example 2 — Insufficient context (refusal-style output)

### Example Input

```
Advisor: A. Patel
Client Reference: CLIENT-0911
Meeting Date: 2026-05-25

CRM Notes:
(empty)

Approved Context:
(none provided)
```

### Expected Output

```
known_facts:
- (none — no approved context provided)

client_stated_goals:
- (none recorded)

prior_action_items:
- (none recorded)

open_questions:
- (none can be inferred without source notes)

suggested_conversation_topics:
- (deferred until source notes are available)

missing_information:
- Approved CRM notes for CLIENT-0911.
- Date and outcome of the most recent meeting.
- Any standing action items or open questions on file.

human_review_flags:
- Insufficient source context. Brief was not generated to avoid fabrication.
```

### Why this output is safe

- The prompt refuses to synthesize a brief from model knowledge.
- `missing_information` is specific and actionable.
- The advisor receives a clear signal that they must source the notes themselves.

### What the prompt must not do

- Generate plausible-sounding goals or action items from thin air.
- Provide a "generic" brief that doesn't tie to this client.
- Apologize at length — the refusal is structured, not narrative.
