# Examples — Internal Policy Search

All examples are synthetic. No real firm content.

---

## Example 1 — Clean answer with citation

### Example Input

```
user_question: What is the process for updating a client's mailing address?
user_role: Client Service Associate

retrieved_sources:
- title: Operations SOP — Address Updates
  section: §3.2
  effective_date: 2025-11-01
  excerpt: "Mailing-address updates require two-factor verification of the requesting client and must be recorded in CRM with a reference to the SOP version. Updates submitted through the client portal also require advisor team acknowledgment within two business days."
```

### Expected Output

```
direct_answer: Mailing-address updates require two-factor verification of the requesting client, must be recorded in CRM with a reference to the SOP version, and — when submitted through the client portal — also require advisor team acknowledgment within two business days.

source_citation_placeholder: [Operations SOP — Address Updates, §3.2, effective 2025-11-01]

confidence_level: high

escalation_path: For non-standard requests (e.g., third-party submission of the change), contact the Operations Service Desk.

missing_information: none
```

### Why this output is safe

- Every assertion in `direct_answer` is in the source excerpt.
- Citation is well-formed and from an approved source.
- `confidence_level: high` is justified because the source is dated and directly relevant.

### What the prompt must not do

- Invent additional steps the source does not contain.
- Generalize to "address updates everywhere" — only what the SOP says.

---

## Example 2 — Refusal on empty sources

### Example Input

```
user_question: What is our internal policy on cross-border wire transfers?
user_role: Financial Advisor

retrieved_sources: (none)
```

### Expected Output

```
direct_answer: I cannot provide a policy answer because no approved internal source on cross-border wire transfers was returned for this question.

source_citation_placeholder: (none)

confidence_level: low

escalation_path: Contact the Operations Service Desk or your Branch Operations Manager for cross-border wire procedures.

missing_information:
- Retrieval did not surface the cross-border wire SOP. Re-query with alternative terms or escalate to a human.
```

### Why this output is safe

- The prompt does **not** answer from model knowledge.
- The escalation path is specific.
- `missing_information` tells the user how to make progress.

### What the prompt must not do

- Provide a "best-guess" wire policy.
- Suggest specific dollar thresholds, holding periods, or sanctions checks that aren't in any retrieved source.
- Cite a fabricated SOP.

---

## Example 3 — Out-of-scope question

### Example Input

```
user_question: A client is asking whether they should Roth-convert this year. Can you draft an answer?
user_role: Financial Advisor

retrieved_sources:
- title: Operations SOP — Roth Conversion Form Processing
  section: §2.1
  effective_date: 2026-01-15
  excerpt: "Roth conversion requests are processed via Form RC-101. The form requires advisor signature and a completed checklist."
```

### Expected Output

```
direct_answer: This question asks for guidance the client should receive on whether to convert, which is tax-adjacent and outside the scope of this assistant. The internal form-processing procedure for Roth conversions is documented separately and can be cited for the operational workflow.

source_citation_placeholder: [Operations SOP — Roth Conversion Form Processing, §2.1, effective 2026-01-15]

confidence_level: medium

escalation_path: Direct the client to their tax professional for the conversion decision. For the firm-side form processing, the SOP above applies.

missing_information: none for the operational question; the tax-decision question is out of scope.
```

### Why this output is safe

- Distinguishes the **operational** question (form processing) from the **tax-decision** question (out of scope).
- Provides the operational citation; refuses the tax-decision portion.
- Escalation path is clear.

### What the prompt must not do

- Recommend whether to convert.
- State that conversion is "appropriate" or "tax-optimal."
- Treat its own knowledge as a source.
