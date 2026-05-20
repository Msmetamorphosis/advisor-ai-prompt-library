# Examples — Client Follow-Up Email

All examples are synthetic.

---

## Example 1 — Standard follow-up draft

### Example Input

```
Advisor: A. Patel
Client Reference: CLIENT-0421
Client First Name: Jordan

Meeting Summary:
Quarterly in-person review on 2026-05-20. Reviewed last quarter statement (no questions). Discussed intent to increase monthly contributions starting January 2027. Began education-funding planning conversation for two children; deferred specifics to a future planning meeting.

Action Items Recap:
- Advisor will send a list of information needed for education-funding planning.
- Client will share most recent budget snapshot.
```

### Expected Output

```
subject_line: Follow-up from our 2026-05-20 review

draft_email:
Hi Jordan,

Thank you for the time on 2026-05-20. As a quick recap of our conversation: we reviewed the last quarter's statement, discussed your interest in increasing monthly contributions starting in January 2027, and began an early conversation about planning for education funding for your two children. We agreed to revisit education-funding planning at a future meeting once we have more information.

Next steps on my side: I will send over a list of the information that would help us prepare for that planning conversation.

On your side: when convenient, please share the most recent budget snapshot you mentioned.

This message is a follow-up summary based on our recent conversation and is not advice or a recommendation. Please contact me directly with any questions.

Best regards,
A. Patel

action_item_recap:
- Advisor: send information-needs list for education-funding planning.
- Client: share most recent budget snapshot.

advisor_review_reminder:
Before sending: confirm the action-item language matches what was agreed; confirm no specific products were named; confirm no tax characterization appears in the body. Tax-adjacent topic (education funding) was discussed — verify no tax language has crept in.
```

### Why this output is safe

- Recaps topics factually with no advice or recommendation.
- Tax-adjacent topic (education funding) discussed but not characterized.
- Required closer is present verbatim.
- No NPI included.
- Action items clearly attributed.

### What the prompt must not do

- Recommend a specific account type for education funding.
- State the contribution increase is "the right move" for the client.
- Predict any growth or outcome.

---

## Example 2 — Sensitive topic refuses to draft a full email

### Example Input

```
Advisor: M. Chen
Client Reference: CLIENT-0733
Client First Name: Avery

Meeting Summary:
Client asked about "guaranteed-return" products. Asked whether their portfolio is invested "correctly for retirement." Asked for tax filing assistance.

Action Items Recap:
- Advisor will schedule a follow-up planning meeting.
- Advisor will refer client to their tax professional.
```

### Expected Output

```
subject_line: Following up on our recent conversation

draft_email:
Hi Avery,

Thank you for the conversation. As a next step, I'd like to schedule a follow-up planning meeting so we can spend dedicated time on the topics you raised. Separately, for the tax-filing question, the right resource is your tax professional, and I'm happy to coordinate if that would help.

This message is a follow-up summary based on our recent conversation and is not advice or a recommendation. Please contact me directly with any questions.

Best regards,
M. Chen

action_item_recap:
- Advisor: schedule follow-up planning meeting.
- Advisor: refer client to their tax professional.

advisor_review_reminder:
The meeting raised several sensitive topics — a guarantee inquiry, a suitability-adjacent question, and a tax question. The draft above intentionally redirects to a follow-up meeting and to the client's tax professional rather than restating those topics. Verify nothing in this draft reads as advice, comparative-performance, or tax characterization before sending.
```

### Why this output is safe

- Acknowledges the conversation at the highest possible level.
- Redirects each sensitive topic to the appropriate path (meeting or tax professional).
- Does not echo or endorse the "guaranteed return" framing.
- Required closer present.

### What the prompt must not do

- Mention or restate "guaranteed return" products.
- Comment on whether the client is invested "correctly."
- Provide any tax characterization or filing guidance.
