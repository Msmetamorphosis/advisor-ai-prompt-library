"""
Generate a weekly usage report for the prompt library.

This is a working example of what an AI operations team would run against
the production log stream defined in docs/observability-and-monitoring.md.
For portfolio purposes, it consumes a JSONL file of synthetic prompt-call
events (one event per line, matching the log schema in the observability
doc) and produces a structured Markdown report.

In a real deployment, the input source would be a warehouse query against
the gateway log table. The aggregation logic and threshold checks below
are the production-ready part; only the source is swapped.

Usage:
    python scripts/generate_usage_report.py [path/to/events.jsonl]

If no path is provided, the script generates a small synthetic event set
in-memory so the report still runs and you can see the shape of the output.
"""
from __future__ import annotations
import json
import sys
import random
import statistics
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Thresholds from docs/observability-and-monitoring.md
THRESHOLDS = {
    "success_rate_min": 0.95,
    "correction_rate_max": 0.40,
    "edit_distance_max": 0.35,
    "cost_overrun_pct_max": 0.25,
    "output_overrun_pct_max": 0.50,
    "eval_drift_drop_max": 0.05,
    "schema_failure_rate_max": 0.02,
}

# Per-prompt declared budgets (would normally be loaded from each prompt.yaml)
PROMPT_BUDGETS = {
    "crm-note-assistant":      {"max_cost_per_call_usd": 0.005, "target_output_tokens": 300},
    "advisor-meeting-prep":    {"max_cost_per_call_usd": 0.015, "target_output_tokens": 600},
    "client-meeting-summary":  {"max_cost_per_call_usd": 0.020, "target_output_tokens": 750},
    "internal-policy-search":  {"max_cost_per_call_usd": 0.015, "target_output_tokens": 450},
    "client-follow-up-email":  {"max_cost_per_call_usd": 0.025, "target_output_tokens": 350},
    "portfolio-review-prep":   {"max_cost_per_call_usd": 0.060, "target_output_tokens": 1100},
}

def synthesize_events(n: int = 5000) -> list[dict]:
    """Synthetic event set for demonstration. Real input is a JSONL file or warehouse query."""
    rng = random.Random(42)
    prompts = list(PROMPT_BUDGETS.keys())
    weights = [4.0, 1.5, 1.5, 2.0, 1.0, 0.3]
    events = []
    now = datetime.now(timezone.utc)
    for _ in range(n):
        prompt = rng.choices(prompts, weights=weights, k=1)[0]
        budget = PROMPT_BUDGETS[prompt]
        target_out = budget["target_output_tokens"]
        max_cost = budget["max_cost_per_call_usd"]
        # Most calls are healthy; a small fraction drift
        is_anomaly = rng.random() < 0.04
        out_tokens = int(target_out * (rng.uniform(0.7, 1.1) if not is_anomaly else rng.uniform(1.6, 2.2)))
        cost_usd  = max_cost * (rng.uniform(0.6, 0.95) if not is_anomaly else rng.uniform(1.3, 1.8))
        edit_dist = rng.uniform(0.05, 0.25) if not is_anomaly else rng.uniform(0.35, 0.6)
        review = rng.choices(
            ["accepted", "edited", "rejected", "escalated"],
            weights=[60, 30, 5, 5], k=1,
        )[0]
        schema_pass = rng.random() > (0.001 if not is_anomaly else 0.05)
        events.append({
            "timestamp": (now - timedelta(seconds=rng.randint(0, 7*24*3600))).isoformat(),
            "prompt_id": prompt,
            "prompt_version": "1.0.0",
            "input_tokens": rng.randint(800, 7000),
            "output_tokens": out_tokens,
            "cost_usd": round(cost_usd, 5),
            "schema_validation": "pass" if schema_pass else "fail",
            "prohibited_phrase_scan": "pass",
            "human_review_status": review,
            "edit_distance": round(edit_dist, 3),
        })
    return events

def load_events(path: Path | None) -> list[dict]:
    if path is None:
        return synthesize_events()
    events = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events

def aggregate(events: list[dict]) -> dict:
    by_prompt = defaultdict(list)
    for ev in events:
        by_prompt[ev["prompt_id"]].append(ev)

    rollup = {}
    for prompt_id, evs in by_prompt.items():
        budget = PROMPT_BUDGETS.get(prompt_id, {})
        target_out = budget.get("target_output_tokens", 0)
        max_cost   = budget.get("max_cost_per_call_usd", 0)

        n = len(evs)
        out_tokens = [e["output_tokens"] for e in evs]
        costs      = [e["cost_usd"] for e in evs]
        edits      = [e.get("edit_distance", 0.0) for e in evs]

        schema_fail = sum(1 for e in evs if e.get("schema_validation") == "fail") / n
        correction  = sum(1 for e in evs if e["human_review_status"] in ("edited", "rejected")) / n
        rejection   = sum(1 for e in evs if e["human_review_status"] == "rejected") / n
        escalation  = sum(1 for e in evs if e["human_review_status"] == "escalated") / n
        success     = 1 - schema_fail

        p50_out = statistics.median(out_tokens)
        p95_out = statistics.quantiles(out_tokens, n=20)[-1] if n >= 20 else max(out_tokens)
        mean_cost = statistics.mean(costs)
        mean_edit = statistics.mean(edits)

        flags = []
        if success < THRESHOLDS["success_rate_min"]:
            flags.append(f"success rate {success:.1%} below {THRESHOLDS['success_rate_min']:.0%} threshold")
        if correction > THRESHOLDS["correction_rate_max"]:
            flags.append(f"correction rate {correction:.1%} above {THRESHOLDS['correction_rate_max']:.0%} threshold")
        if mean_edit > THRESHOLDS["edit_distance_max"]:
            flags.append(f"mean edit distance {mean_edit:.2f} above {THRESHOLDS['edit_distance_max']:.2f} threshold")
        if max_cost and (mean_cost - max_cost) / max_cost > THRESHOLDS["cost_overrun_pct_max"]:
            flags.append(f"mean cost ${mean_cost:.4f} exceeds budget ${max_cost:.4f} by >{THRESHOLDS['cost_overrun_pct_max']:.0%}")
        if target_out and (p50_out - target_out) / target_out > THRESHOLDS["output_overrun_pct_max"]:
            flags.append(f"p50 output {int(p50_out)} exceeds target {target_out} by >{THRESHOLDS['output_overrun_pct_max']:.0%}")
        if schema_fail > THRESHOLDS["schema_failure_rate_max"]:
            flags.append(f"schema failure rate {schema_fail:.1%} above {THRESHOLDS['schema_failure_rate_max']:.0%} threshold")

        rollup[prompt_id] = {
            "calls": n,
            "success_rate": success,
            "correction_rate": correction,
            "rejection_rate": rejection,
            "escalation_rate": escalation,
            "mean_edit_distance": mean_edit,
            "p50_output_tokens": int(p50_out),
            "p95_output_tokens": int(p95_out),
            "target_output_tokens": target_out,
            "mean_cost_usd": mean_cost,
            "max_cost_per_call_usd": max_cost,
            "weekly_cost_usd": sum(costs),
            "flags": flags,
        }
    return rollup

def render_markdown(rollup: dict) -> str:
    total_calls = sum(r["calls"] for r in rollup.values())
    total_cost  = sum(r["weekly_cost_usd"] for r in rollup.values())
    flagged     = sum(1 for r in rollup.values() if r["flags"])

    lines = []
    lines.append(f"# Weekly Usage Report")
    lines.append(f"_Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}_")
    lines.append("")
    lines.append(f"- Total calls this week: **{total_calls:,}**")
    lines.append(f"- Total cost this week: **${total_cost:,.2f}**")
    lines.append(f"- Prompts with active flags: **{flagged} of {len(rollup)}**")
    lines.append("")
    lines.append("## Per-prompt summary")
    lines.append("")
    lines.append("| Prompt | Calls | Success | Correction | p50 / target out | Mean cost / budget | Status |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for prompt_id in sorted(rollup):
        r = rollup[prompt_id]
        status = "OK" if not r["flags"] else f"FLAG ({len(r['flags'])})"
        lines.append(
            f"| {prompt_id} | {r['calls']:,} | {r['success_rate']:.1%} | "
            f"{r['correction_rate']:.1%} | {r['p50_output_tokens']} / {r['target_output_tokens']} | "
            f"${r['mean_cost_usd']:.4f} / ${r['max_cost_per_call_usd']:.4f} | {status} |"
        )
    lines.append("")
    lines.append("## Flagged prompts — required review")
    lines.append("")
    any_flag = False
    for prompt_id in sorted(rollup):
        r = rollup[prompt_id]
        if not r["flags"]:
            continue
        any_flag = True
        lines.append(f"### {prompt_id}")
        for f in r["flags"]:
            lines.append(f"- {f}")
        lines.append("")
    if not any_flag:
        lines.append("_No prompts crossed action thresholds this week._")
        lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("Thresholds are defined in `docs/observability-and-monitoring.md`. A prompt that crosses any threshold for two consecutive weekly reviews automatically opens a governance review per `GOVERNANCE.md`.")
    return "\n".join(lines)

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    events = load_events(path)
    rollup = aggregate(events)
    report = render_markdown(rollup)
    out_path = REPO / "weekly_usage_report.md"
    out_path.write_text(report)
    print(report)
    print()
    print(f"--- Report written to {out_path.relative_to(REPO)} ---")

if __name__ == "__main__":
    main()
