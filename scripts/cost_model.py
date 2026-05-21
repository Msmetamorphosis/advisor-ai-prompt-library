"""
Build the actual cost model.

Pricing sources (all verified May 2026, USD per 1M tokens):
- Claude Haiku 4.5:   $1.00 input / $5.00 output    (anthropic.com, Oct 2025)
- Claude Sonnet 4.6:  $3.00 input / $15.00 output   (anthropic.com)
- Claude Opus 4.7:    $5.00 input / $25.00 output   (anthropic.com)
- GPT-5.4-nano:       $0.20 input / $1.25 output    (openai.com pricing page)
- GPT-5.4-mini:       $0.75 input / $4.50 output    (openai.com pricing page)
- GPT-5.4:            $2.50 input / $15.00 output   (openai.com pricing page)
- Gemini 2.5 Flash:   $0.30 input / $2.50 output    (ai.google.dev)

Volume assumption (configurable, but documented):
- 500 advisors
- Per-prompt frequency varies by use case (see VOLUME)
- 220 trading days/year
"""
import json
from pathlib import Path

PRICING = {
    # tier, label -> (input_$/Mtok, output_$/Mtok)
    "Haiku-4.5":    (1.00,  5.00),
    "Sonnet-4.6":   (3.00, 15.00),
    "Opus-4.7":     (5.00, 25.00),
    "GPT-5.4-nano": (0.20,  1.25),
    "GPT-5.4-mini": (0.75,  4.50),
    "GPT-5.4":      (2.50, 15.00),
    "Gemini-2.5-Flash": (0.30, 2.50),
}

# Realistic per-advisor frequency per workday (not every prompt fires every day)
VOLUME = {
    # prompt: calls per advisor per workday
    "crm-note-assistant":      4.0,  # heavy use, every client touchpoint
    "advisor-meeting-prep":    1.5,  # before client meetings
    "client-meeting-summary":  1.5,  # after client meetings
    "internal-policy-search":  2.0,  # ad-hoc policy lookups
    "client-follow-up-email":  1.0,  # post-meeting drafts
    "portfolio-review-prep":   0.3,  # quarterly-ish, averaged
}

ADVISORS = 9000   # ~Raymond James scale (8,943 as of FY2025)
WORKDAYS = 220

REPO = Path(__file__).resolve().parent.parent
measurements = json.loads((REPO / "prompt_token_measurements.json").read_text())

def cost_per_call(in_tok, out_tok, in_price, out_price):
    return (in_tok / 1_000_000) * in_price + (out_tok / 1_000_000) * out_price

# Recommended tier -> model mapping (the "right" choice)
TIER_MODEL = {
    "tier-1-light":     "Haiku-4.5",
    "tier-2-standard":  "Haiku-4.5",
    "tier-3-reasoning": "Sonnet-4.6",
}

# What "everything on Sonnet" looks like (the current default behavior)
DEFAULT_MODEL = "Sonnet-4.6"
# What "everything on Opus" looks like (worst case some teams do)
WORST_MODEL = "Opus-4.7"

rows = []
totals = {"recommended": 0, "all_sonnet": 0, "all_opus": 0, "calls": 0}

for m in measurements:
    name = m["prompt"]
    tier = m["recommended_tier"]
    in_tok = m["per_call_input_tokens"]
    out_tok = m["per_call_output_tokens"]
    calls_per_year = VOLUME[name] * ADVISORS * WORKDAYS

    # Cost per call by model
    rec_model = TIER_MODEL[tier]
    rec_in, rec_out = PRICING[rec_model]
    cost_rec = cost_per_call(in_tok, out_tok, rec_in, rec_out)

    son_in, son_out = PRICING[DEFAULT_MODEL]
    cost_son = cost_per_call(in_tok, out_tok, son_in, son_out)

    op_in, op_out = PRICING[WORST_MODEL]
    cost_op = cost_per_call(in_tok, out_tok, op_in, op_out)

    # Also OpenAI parallel (for comparison)
    if tier == "tier-1-light":
        oa_model = "GPT-5.4-nano"
    elif tier == "tier-2-standard":
        oa_model = "GPT-5.4-mini"
    else:
        oa_model = "GPT-5.4"
    oa_in, oa_out = PRICING[oa_model]
    cost_oa = cost_per_call(in_tok, out_tok, oa_in, oa_out)

    annual_rec = cost_rec * calls_per_year
    annual_son = cost_son * calls_per_year
    annual_op  = cost_op  * calls_per_year
    annual_oa  = cost_oa  * calls_per_year

    rows.append({
        "prompt": name,
        "tier": tier,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "calls_per_advisor_per_day": VOLUME[name],
        "annual_calls": int(calls_per_year),
        "rec_model": rec_model,
        "cost_per_call_rec": cost_rec,
        "cost_per_call_sonnet": cost_son,
        "cost_per_call_opus": cost_op,
        "annual_cost_recommended": annual_rec,
        "annual_cost_all_sonnet": annual_son,
        "annual_cost_all_opus": annual_op,
        "annual_cost_openai_recommended": annual_oa,
        "openai_rec_model": oa_model,
    })
    totals["recommended"] += annual_rec
    totals["all_sonnet"] += annual_son
    totals["all_opus"] += annual_op
    totals["calls"] += calls_per_year

# Print human-readable table
print(f"{'Prompt':<26} {'Tier':<18} {'In/Out tok':<14} {'Calls/yr':<12} {'Rec model':<14} {'$/call':<10} {'$/yr (rec)':<14} {'$/yr (Sonnet)':<14} {'$/yr (Opus)':<14}")
print("-" * 160)
for r in rows:
    print(f"{r['prompt']:<26} {r['tier']:<18} {r['input_tokens']}/{r['output_tokens']:<10} {r['annual_calls']:<12,} {r['rec_model']:<14} ${r['cost_per_call_rec']:<9.5f} ${r['annual_cost_recommended']:<13,.0f} ${r['annual_cost_all_sonnet']:<13,.0f} ${r['annual_cost_all_opus']:<13,.0f}")

print()
print(f"TOTAL annual calls across all 6 prompts: {int(totals['calls']):,}")
print(f"TOTAL annual cost — RECOMMENDED tiering (Anthropic):   ${totals['recommended']:>12,.0f}")
print(f"TOTAL annual cost — everything on Sonnet 4.6:          ${totals['all_sonnet']:>12,.0f}")
print(f"TOTAL annual cost — everything on Opus 4.7:            ${totals['all_opus']:>12,.0f}")
print()
print(f"Savings: Sonnet-default -> Recommended:  ${totals['all_sonnet'] - totals['recommended']:>12,.0f}/yr  ({(1-totals['recommended']/totals['all_sonnet'])*100:.1f}%)")
print(f"Savings: Opus-default   -> Recommended:  ${totals['all_opus']   - totals['recommended']:>12,.0f}/yr  ({(1-totals['recommended']/totals['all_opus'])*100:.1f}%)")

(REPO / "cost_model_results.json").write_text(json.dumps({"rows": rows, "totals": totals, "assumptions": {"advisors": ADVISORS, "workdays": WORKDAYS, "volume": VOLUME, "pricing": PRICING}}, indent=2))
