# Compliance Constraints — Client Follow-Up Email

This document is enforced both by the system prompt and (where applicable) by the test suite. It is the canonical reference for what this prompt **must not say** and what it **must always say**.

---

## Prohibited Language

The following phrases (or substantively equivalent variants) must not appear in `draft_email` or `subject_line`:

| Category | Examples |
|---|---|
| Performance promises | "guaranteed return", "risk free", "will outperform", "will grow to", "you can expect to earn" |
| Suitability statements | "this is suitable for you", "appropriate for your situation", "the right investment for you" |
| Recommendations | "you should invest", "I recommend buying", "we recommend selling", "approved recommendation" |
| Tax language | "tax advice", "tax-free guarantee", "you won't owe tax on", "this is tax-optimal for you" |
| Legal language | "legal advice", "this is legally binding", "you should sue", "we'll represent you" |
| Marketing language | "industry-leading", "best in class", "limited-time opportunity", "act now" |

Some of these phrases also appear in the library-wide `tests/fixtures/prohibited_phrases.json` and are enforced by `tests/test_compliance_boundaries.py` against production prompt text and example outputs.

---

## Required Language

The following closer must appear verbatim near the end of `draft_email`:

> "This message is a follow-up summary based on our recent conversation and is not advice or a recommendation. Please contact me directly with any questions."

This closer is part of the firm's communications policy as represented in this mock library. It is not optional and cannot be paraphrased by the prompt.

---

## Required Behavior on Sensitive Topics

| If the meeting touched … | The draft must … |
|---|---|
| A tax question | Acknowledge the topic at most generically and direct the client to their tax professional. Do not provide tax characterization. |
| A legal question | Direct the client to their attorney. Do not characterize legal outcomes. |
| A suitability or "am I invested correctly" question | Reference the scheduled or recommended follow-up planning meeting. Do not state any suitability conclusion. |
| A guarantee or peer-performance comparison | Acknowledge the topic was discussed at most generically. Do not restate or endorse any guarantee or comparison. |
| NPI (account #, SSN, DOB, balances) | Do not include NPI in the draft. Use the client's first name in the greeting only. |

The `advisor_review_reminder` must explicitly note any of the above that was triggered.

---

## Forbidden Output Patterns

- The draft must not include exclamation marks of urgency (e.g., "Don't miss out!").
- The draft must not use second-person imperatives that direct action on a financial product ("buy", "sell", "open", "close" applied to a security or account).
- The draft must not include `{{`-style placeholders in the final output; all required placeholders must be resolved or the prompt must refuse to draft.

---

## Reviewer Checklist

When the advisor reviews the draft, they should confirm:

- [ ] No prohibited language is present.
- [ ] The required closer is present and intact.
- [ ] No NPI is present.
- [ ] The action-item recap matches the underlying meeting record.
- [ ] If a sensitive topic was discussed, the redirect to a qualified professional or the next meeting is present.
- [ ] The draft is consistent with firm communications policy.
