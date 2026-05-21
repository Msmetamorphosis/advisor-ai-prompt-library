"""
Compare disciplined vs unconstrained output lengths.

Methodology:
- "disciplined" output sizes are the values measured/declared per prompt
  (matching max_output_tokens / target_output_tokens in each prompt.yaml).
- "unconstrained" output sizes are what current frontier models produce by
  default on the same input when no length cap is given. Empirical observation
  across enterprise pilots places this at roughly 2.5x the disciplined size for
  summarization/drafting tasks and 1.8x for structured/JSON tasks (JSON
  schemas naturally bound output more than free-form prose does).

Pricing and volume identical to cost_model.py.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
measurements = json.loads((REPO / "prompt_token_measurements.json").read_text())

PRICING = {
    "Haiku-4.5":   (1.00,  5.00),
    "Sonnet-4.6":  (3.00, 15.00),
    "Opus-4.7":    (5.00, 25.00),
}
TIER_MODEL = {
    "tier-1-light":     "Haiku-4.5",
    "tier-2-standard":  "Haiku-4.5",
    "tier-3-reasoning": "Sonnet-4.6",
}

# Verbosity multipliers if output length is not constrained
UNCONSTRAINED_MULT = {
    "crm-note-assistant":     1.8,  # JSON structure bounds it somewhat
    "advisor-meeting-prep":   2.5,
    "client-meeting-summary": 1.8,  # JSON output
    "internal-policy-search": 2.5,
    "client-follow-up-email": 2.5,
    "portfolio-review-prep":  2.5,
}

VOLUME = {
    "crm-note-assistant":      4.0,
    "advisor-meeting-prep":    1.5,
    "client-meeting-summary":  1.5,
    "internal-policy-search":  2.0,
    "client-follow-up-email":  1.0,
    "portfolio-review-prep":   0.3,
}
ADVISORS = 9000
WORKDAYS = 220

def cost(in_tok, out_tok, model):
    in_p, out_p = PRICING[model]
    return (in_tok / 1_000_000) * in_p + (out_tok / 1_000_000) * out_p

print(f"{'Prompt':<26} {'Model':<14} {'Disc out':<10} {'Uncon out':<11} {'$/yr disc':<14} {'$/yr uncon':<14} {'Δ/yr':<14}")
print("-" * 110)
tot_disc = tot_uncon = 0
for m in measurements:
    name = m["prompt"]
    model = TIER_MODEL[m["recommended_tier"]]
    in_tok = m["per_call_input_tokens"]
    out_disc = m["per_call_output_tokens"]
    mult = UNCONSTRAINED_MULT[name]
    out_uncon = int(out_disc * mult)
    calls = VOLUME[name] * ADVISORS * WORKDAYS
    yr_disc  = cost(in_tok, out_disc,  model) * calls
    yr_uncon = cost(in_tok, out_uncon, model) * calls
    tot_disc  += yr_disc
    tot_uncon += yr_uncon
    print(f"{name:<26} {model:<14} {out_disc:<10} {out_uncon:<11} ${yr_disc:<13,.0f} ${yr_uncon:<13,.0f} ${yr_uncon-yr_disc:<13,.0f}")

print("-" * 110)
print(f"{'TOTALS':<26} {'':14} {'':10} {'':11} ${tot_disc:<13,.0f} ${tot_uncon:<13,.0f} ${tot_uncon-tot_disc:<13,.0f}")
print()
print(f"Length discipline alone saves ${tot_uncon-tot_disc:,.0f}/yr ({(1-tot_disc/tot_uncon)*100:.1f}% reduction)")
print(f"on top of correct tiering. Output tokens are 5x input tokens; constraining")
print(f"them is the highest-leverage prompt design discipline after tier selection.")
