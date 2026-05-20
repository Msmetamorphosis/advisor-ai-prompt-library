# Prompt Risk Taxonomy

Every prompt in this library is classified into one of four risk levels. The classification drives **review depth, review cadence, approver list, and whether human-in-the-loop is required**.

Risk is assigned at intake, validated at compliance review, and revisited at every scheduled re-review. The classification lives in `prompt.yaml` as `risk_level:`.

---

## Risk Levels at a Glance

| Level | Human Review Required | Cadence | Approvers | Examples |
|---|---|---|---|---|
| **Low** | Recommended | 12 mo | Owner + peer | Internal note formatting, agenda drafts |
| **Medium** | **Required** | 6 mo | Owner + AI Enablement Lead | Meeting prep, internal policy lookup, CRM notes |
| **High** | **Required** | 3 mo | Owner + Lead + Compliance | Client-facing drafts, portfolio review prep |
| **Restricted** | **Required + supervisory** | 30 days / model-change | Owner + Lead + Compliance + BU Sponsor | Anything touching suitability, advice, NPI |

---

## Low Risk

**Definition:** The prompt operates on non-sensitive input, produces output that is purely internal and operational, and has no client-visible or regulator-relevant content.

**Characteristics:**
- No PII or NPI.
- Output is consumed by the advisor or their team for internal use.
- Failure mode is "minor inefficiency," not "compliance event."

**Examples:**
- Reformatting meeting agendas.
- Suggesting talking-point bullet structure from advisor's own notes.
- Generating internal-only checklist templates.

**Review:** Peer review by another team member; passing eval suite; standard PR.

---

## Medium Risk

**Definition:** The prompt operates on internal source material (CRM notes, advisor input, approved knowledge base) and produces output that may be referenced operationally but is not directly sent to clients.

**Characteristics:**
- May reference client context but is not delivered to the client.
- Could mislead an advisor if hallucinated.
- Human review is mandatory before any downstream use.

**Examples:**
- `advisor-meeting-prep` — a brief built from CRM context.
- `crm-note-assistant` — CRM entries the advisor will save.
- `internal-policy-search` — operational answers an advisor relies on internally.

**Review:** AI Enablement Lead sign-off; full eval suite; semi-annual re-review.

---

## High Risk

**Definition:** The prompt produces output that **may be visible to a client** or that **summarizes content with supervisory implications**.

**Characteristics:**
- Output may be sent to clients after advisor review.
- Errors create direct compliance exposure (mis-statement, missing disclosure, implied advice).
- Boundary fidelity is critical — the prompt must refuse out-of-scope requests.

**Examples that fit High risk:**

1. **Investment recommendation boundaries** — prompts that summarize a meeting where investment topics arose; must not restate them as recommendations.
2. **Tax or legal language** — prompts that may surface tax-adjacent discussion; must redirect to qualified professionals.
3. **Suitability-related content** — prompts that touch goals, risk tolerance, or product fit; must not infer suitability.
4. **Client-specific financial advice** — prompts that compose anything resembling instruction to act on the client's portfolio.
5. **Client-facing communication** — emails, letters, summaries that the client will read.
6. **Use of non-public personal information (NPI)** — prompts that operate on identifying client data must be treated as High at minimum.

**Examples in this library:**
- `client-meeting-summary`
- `client-follow-up-email`
- `portfolio-review-prep`

**Review:** Compliance liaison sign-off; quarterly re-review; advisor-review reminder enforced in `system.md`.

---

## Restricted

**Definition:** The prompt operates in a domain the firm has determined cannot be safely delegated to AI without supervisory controls beyond what this library normally enforces.

**Characteristics:**
- Requires explicit supervisory approval before each deployment.
- May require a logged, reviewable session and human approval per use, not just per release.
- Often paired with separate Model Risk Management (MRM) documentation.

**Examples (illustrative — none ship as Restricted in this portfolio repo by default):**
- Generating any artifact that could read as a formal recommendation letter.
- Composing content for a regulated disclosure document.
- Operating on bulk NPI exports.
- Producing content for plan-document or ERISA-adjacent communications.

**Review:** Owner + AI Enablement Lead + Compliance + Business Unit Sponsor; review every 30 days or any time the underlying LLM version changes; live monitoring of every invocation.

---

## Risk Classification Decision Tree

```
Does the output reach a client (directly or via the advisor)?
├── Yes → at minimum HIGH
│        └── Does it touch suitability, advice, tax, legal, NPI, or formal disclosures?
│             ├── Yes → RESTRICTED
│             └── No  → HIGH
│
└── No  → Is the output a basis for operational or supervisory decisions?
         ├── Yes → MEDIUM
         └── No  → LOW
```

When unsure, classify **one level higher** and let compliance review confirm or downgrade. There is no penalty for caution; there is significant penalty for under-classification.

---

## Re-Classification Triggers

A prompt's risk level may need to be reassessed if:

- Its scope changes (new output field, new use case).
- The underlying LLM is replaced with a model of different behavior characteristics.
- A regulatory advisory introduces a new sensitivity (e.g., new client communication rule).
- An incident or near-miss is reported on the prompt.
- An advisor adoption pattern emerges that was not anticipated at design time (e.g., advisors are pasting client emails into a prompt that was scoped for internal notes).

Re-classification is a MAJOR version bump and triggers the full approval workflow.
