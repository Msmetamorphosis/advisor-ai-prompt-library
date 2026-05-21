"""
What if the library grows to 50 prompts at the same usage profile?
This isn't fantasy — RBC, Morgan Stanley, JPM have all disclosed
prompt libraries in the 40-100 prompt range publicly.

We assume the SAME tier distribution holds:
  - 1 of 6 prompts is tier-1 (17%) -> 8 of 50 prompts tier-1
  - 3 of 6 prompts is tier-2 (50%) -> 25 of 50 prompts tier-2
  - 2 of 6 prompts is tier-3 (33%) -> 17 of 50 prompts tier-3

And the SAME per-prompt cost-per-call averages hold.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
data = json.loads((REPO / "cost_model_results.json").read_text())
rows = data["rows"]

# Average cost per call by tier (recommended vs sonnet-default vs opus-default)
by_tier = {}
for r in rows:
    t = r["tier"]
    by_tier.setdefault(t, []).append(r)

# Average calls per year per prompt by tier (just for projection)
tier_avg = {}
for t, rs in by_tier.items():
    tier_avg[t] = {
        "n_prompts": len(rs),
        "avg_annual_calls_per_prompt": sum(x["annual_calls"] for x in rs) / len(rs),
        "avg_cost_per_call_rec":    sum(x["cost_per_call_rec"]    for x in rs) / len(rs),
        "avg_cost_per_call_sonnet": sum(x["cost_per_call_sonnet"] for x in rs) / len(rs),
        "avg_cost_per_call_opus":   sum(x["cost_per_call_opus"]   for x in rs) / len(rs),
    }

# 50-prompt library projection
TARGET_LIB_SIZE = 50
tier_share = {
    "tier-1-light":     8,    # 16% — light extraction/classification
    "tier-2-standard": 25,    # 50% — summarization, retrieval, structured output
    "tier-3-reasoning":17,    # 34% — reasoning/client-facing
}
assert sum(tier_share.values()) == TARGET_LIB_SIZE

totals = {"rec": 0, "sonnet": 0, "opus": 0, "calls": 0}
for tier, n in tier_share.items():
    avg = tier_avg[tier]
    calls = n * avg["avg_annual_calls_per_prompt"]
    totals["calls"] += calls
    totals["rec"]    += calls * avg["avg_cost_per_call_rec"]
    totals["sonnet"] += calls * avg["avg_cost_per_call_sonnet"]
    totals["opus"]   += calls * avg["avg_cost_per_call_opus"]

print("=" * 70)
print("50-prompt library projection (same usage profile, 9,000 advisors)")
print("=" * 70)
print(f"Total annual calls:  {int(totals['calls']):>14,}")
print(f"Recommended tiering: ${totals['rec']:>14,.0f}/yr")
print(f"All on Sonnet 4.6:   ${totals['sonnet']:>14,.0f}/yr")
print(f"All on Opus 4.7:     ${totals['opus']:>14,.0f}/yr")
print()
print(f"Savings vs Sonnet-default: ${totals['sonnet']-totals['rec']:>12,.0f}/yr  ({(1-totals['rec']/totals['sonnet'])*100:.1f}%)")
print(f"Savings vs Opus-default:   ${totals['opus']-totals['rec']:>12,.0f}/yr  ({(1-totals['rec']/totals['opus'])*100:.1f}%)")
