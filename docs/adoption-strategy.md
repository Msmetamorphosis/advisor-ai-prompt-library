# Adoption Strategy

The hard part of enterprise AI is not the model. It is **getting people who already have a job to use the model instead of doing the job the way they always did.** This document describes how a version-controlled prompt library accelerates advisor adoption — and where it can fail.

---

## The Adoption Problem

Without a prompt library, advisors who try AI typically:

1. **Improvise.** Each advisor writes their own prompt in a chat window. Output quality varies by their prompting skill, not the model's capability.
2. **Lose trust on first error.** When an unsupervised output crosses a compliance line — a guarantee, a recommendation, a hallucinated policy — the advisor concludes "AI isn't ready" and stops using it.
3. **Hit a ceiling.** Even successful improvisers don't share their prompts. The firm's AI value is bottlenecked by individual prompting skill.
4. **Get blocked by Compliance.** Compliance has no scalable way to review every advisor's prompt-by-prompt usage, so the safest answer is "don't."

The library re-frames the problem: **the prompt is the contract, not the chat.** Advisors don't author the contract — they consume it.

---

## What the Library Changes

| Without library | With library |
|---|---|
| Each advisor invents their own prompt. | Advisors pick from a vetted catalog. |
| Output structure varies. | Output structure is a JSON contract. |
| Compliance reviews ad hoc, slowly. | Compliance reviews **once**, per release. |
| Errors recur silently. | Errors become eval cases; regression is detected. |
| Adoption is per-advisor heroics. | Adoption is a workflow rollout. |

---

## The Adoption Loop

```
   ┌──────────────────┐
   │ 1. Find a high-  │
   │    volume advisor│
   │    workflow      │
   └─────────┬────────┘
             ▼
   ┌──────────────────┐
   │ 2. Author a      │
   │    prompt and    │
   │    eval set      │
   └─────────┬────────┘
             ▼
   ┌──────────────────┐
   │ 3. Pilot with    │
   │    10-20 advisors│
   └─────────┬────────┘
             ▼
   ┌──────────────────┐
   │ 4. Measure       │
   │    (time, edit   │
   │    distance,     │
   │    escalation)   │
   └─────────┬────────┘
             ▼
   ┌──────────────────┐
   │ 5. Release with  │
   │    enablement +  │
   │    release note  │
   └─────────┬────────┘
             ▼
   ┌──────────────────┐
   │ 6. Monitor; feed │
   │    failures back │
   │    into eval set │
   └──────────────────┘
```

The loop is intentional: every prompt the library ships **earned its place** by measurably saving an advisor time on a real workflow, and every change forward is grounded in observed failure modes.

---

## What Advisors Care About

In ranked order, based on field interviews in similar firms:

1. **"Will this get me in trouble?"** Compliance safety is table stakes — without it, none of the other points matter.
2. **"Does it sound like me?"** Output that sounds robotic gets rewritten and the time savings evaporate.
3. **"Can I trust the facts?"** A single hallucinated client name destroys months of credibility.
4. **"Is it faster than what I do today?"** Real time savings, measured in minutes per task.
5. **"Will I remember to use it next week?"** Workflow placement matters more than capability.

The library's design addresses each point directly:
- Risk taxonomy + compliance review address (1).
- The system prompt's tone guidance + advisor review address (2).
- Grounding and refusal address (3).
- Eval cases include the failure modes that destroy trust early.

---

## Reducing Prompting Variance

The library reduces variance in three ways:

1. **One canonical system prompt per workflow.** Every advisor sees the same instructions, the same boundaries, the same output structure.
2. **One canonical placeholder schema.** The user template defines what the advisor must supply — no more "I forgot to include the meeting date."
3. **One canonical output schema (where applicable).** Downstream consumers (CRM, email tools) get the same shape every time.

This is the difference between **"AI in the firm"** and **"AI as part of the firm's operating model."**

---

## Trust as a Build Order

Trust is built in this order — and breaking the order kills adoption:

1. **First, the prompt refuses well.** Advisors notice when AI declines and explains why. That builds confidence faster than success.
2. **Second, the prompt is grounded.** When advisors see the source citation, they trust the answer.
3. **Third, the prompt is consistent.** When two advisors get comparable output for comparable input, they start sharing tips.
4. **Fourth, the prompt is fast.** Speed gains compound, but only after refusal, grounding, and consistency.

A prompt library that ships speed before refusal will lose the advisor population on the first error.

---

## Failure Modes the Library Must Avoid

- **The "everything bagel" prompt.** A prompt that tries to do meeting prep, summary, and follow-up at once is unreviewable and unreliable. Keep prompts narrow.
- **The "free-text returns" prompt.** Without an output schema or structured fields, you can't measure quality and you can't write regression tests.
- **The "no owner" prompt.** A prompt without a named owner becomes a liability the moment the underlying model changes.
- **The "advisor signs off, always" assumption.** Some advisors will paste the draft and send. Compliance-sensitive prompts must be designed so that even an unattended paste produces output the firm can defend.
- **The "we'll eval later" promise.** A prompt without eval cases is a prompt without a regression net. Models change; without regression, drift is invisible.

---

## How AI Enablement Earns Its Seat

This library is not just an asset — it's a **commitment to a measurable program**. The metrics in [`measurement-plan.md`](./measurement-plan.md) tell us whether the program is working. The lifecycle in [`prompt-lifecycle.md`](./prompt-lifecycle.md) tells us how to keep working it.

The interview talking point that lands: *"We don't ask advisors to trust AI. We give them prompts they can rely on, and we measure whether they actually rely on them."*
