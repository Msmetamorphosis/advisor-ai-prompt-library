# Retrieval Rules — Internal Policy Search

This document defines what counts as an approved source for `internal-policy-search` and how retrieval interacts with the prompt.

---

## Approved Sources

In this mock library, "approved internal sources" refers to (illustratively):

- The firm's published internal operations knowledge base.
- The firm's published Written Supervisory Procedures (WSP) excerpts where indexed for operational reference.
- Approved Standard Operating Procedure (SOP) documents.
- Published policy memoranda from the relevant business unit.

In a real deployment, these would be vector-indexed and retrieved at query time. The prompt expects retrieval to have already happened — `retrieved_sources` is passed as input.

---

## Retrieval Contract

The caller must supply `retrieved_sources` as a list of objects:

```
[
  {
    "title": "<source title>",
    "section": "<section or page reference>",
    "effective_date": "<YYYY-MM-DD or null>",
    "excerpt": "<verbatim passage relevant to the question>"
  },
  ...
]
```

The prompt:

- **Must not** treat absence of `retrieved_sources` as permission to answer from general knowledge.
- **Must** prefer the source with the most recent `effective_date` when multiple sources address the same question.
- **Must** disclose effective dates in the citation when present.

---

## Out-of-Scope Sources

The prompt must ignore and not answer based on:

- Publicly available web content (even if retrieved by mistake).
- Vendor marketing material.
- Documents marked draft, archived, retired, or superseded.
- Documents whose `effective_date` is in the future without an explicit "effective-immediately" annotation.

If only out-of-scope sources are present, the prompt must treat `retrieved_sources` as effectively empty and follow the refusal path.

---

## Source Freshness

The prompt must flag in `missing_information` any case where:

- The newest source is older than 365 days for an operational policy.
- The retrieved source set spans contradictory positions (the prompt cannot resolve a contradiction in firm policy on its own).
- A source is dated but does not carry an `effective_date` field — the prompt should surface this as a quality issue.
