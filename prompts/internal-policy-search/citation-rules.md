# Citation Rules — Internal Policy Search

Every answered question must include a `source_citation_placeholder` constructed from the retrieved sources.

---

## Citation Format

For each cited source, use:

```
[<title>, <section or page reference>, effective <YYYY-MM-DD or "undated">]
```

Examples:

- `[Operations SOP — Address Updates, §3.2, effective 2025-11-01]`
- `[WSP Excerpt — Client Communication Recordkeeping, p. 14, effective 2026-02-15]`
- `[Policy Memo — Beneficiary Designation Updates, §1, undated]`

If multiple sources support the answer, cite each:

- `[Source A …]; [Source B …]`

---

## Required Behavior

- The prompt must include at least one citation whenever `direct_answer` is anything other than a refusal.
- The prompt must not invent titles, sections, or dates. If the retrieved source does not provide a section reference, omit it (rather than fabricate one).
- The prompt must prefer the most recently effective source where multiple sources address the same point, and the citation must reflect that source.
- If a citation source is undated, the prompt must mark `confidence_level` as `medium` at most.

---

## Forbidden Citation Patterns

- Citing publicly available web pages, blogs, or external articles.
- Citing the underlying LLM as a source.
- Stating "according to general industry practice" — that is not a citation.
- Citing a source the model did not receive in `retrieved_sources`.

A response without a valid citation, when one is required, must be treated as a refusal: set `direct_answer` to the refusal text and `confidence_level` to `low`.
