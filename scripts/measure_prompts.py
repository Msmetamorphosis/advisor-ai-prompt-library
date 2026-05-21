"""
Measure real token counts for every prompt in advisor-ai-prompt-library.

Methodology:
- system.md = system prompt (sent every call)
- user-template.md = the template; we estimate INPUT VARIABLES separately based on
  realistic financial-services context sizes per prompt type
- examples.md = NOT sent at runtime (it's documentation), so excluded from per-call cost
- Output size is estimated per prompt based on schema / type of response

Tokenizer: tiktoken cl100k_base (a reasonable proxy across GPT/Claude;
Claude's tokenizer is ~10-15% different but cl100k is the closest available
public approximation. We document this caveat in the cost model.)
"""
import os, json, tiktoken
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
enc = tiktoken.get_encoding("cl100k_base")

def tok(s: str) -> int:
    return len(enc.encode(s))

# Per-prompt realistic runtime context (input variables filled into the template)
# Sized from observed financial-services workloads.
RUNTIME_CONTEXT = {
    "advisor-meeting-prep": {
        # Last 6 months of CRM notes + IPS excerpt + recent portfolio snapshot
        "input_variables_tokens": 2500,
        # Output: 1-page meeting brief
        "expected_output_tokens": 600,
        "type": "tier-2-standard",
    },
    "client-meeting-summary": {
        # Transcript of 45-60 min meeting (long input)
        "input_variables_tokens": 6000,
        # Structured JSON summary
        "expected_output_tokens": 800,
        "type": "tier-2-standard",
    },
    "crm-note-assistant": {
        # Short advisor dictation/notes
        "input_variables_tokens": 400,
        # Structured JSON fields
        "expected_output_tokens": 300,
        "type": "tier-1-light",
    },
    "client-follow-up-email": {
        # Meeting summary + client preferences + recent activity
        "input_variables_tokens": 1500,
        # Short professional email draft
        "expected_output_tokens": 350,
        "type": "tier-3-reasoning",
    },
    "internal-policy-search": {
        # User query + retrieved policy passages (top-k = 5, ~500 tok each)
        "input_variables_tokens": 3000,
        # Answer with citations
        "expected_output_tokens": 500,
        "type": "tier-2-standard",
    },
    "portfolio-review-prep": {
        # Holdings table + IPS + recent transactions + market context
        "input_variables_tokens": 4500,
        # Multi-section talking points + flags
        "expected_output_tokens": 1200,
        "type": "tier-3-reasoning",
    },
}

results = []
prompts_dir = REPO / "prompts"
for pdir in sorted(prompts_dir.iterdir()):
    if not pdir.is_dir():
        continue
    name = pdir.name
    sys_path = pdir / "system.md"
    usr_path = pdir / "user-template.md"
    sys_tokens = tok(sys_path.read_text()) if sys_path.exists() else 0
    template_tokens = tok(usr_path.read_text()) if usr_path.exists() else 0
    rc = RUNTIME_CONTEXT.get(name, {})
    input_vars = rc.get("input_variables_tokens", 0)
    out_tokens = rc.get("expected_output_tokens", 0)
    # Per-call input = system + template scaffolding + filled variables
    per_call_input = sys_tokens + template_tokens + input_vars
    results.append({
        "prompt": name,
        "recommended_tier": rc.get("type"),
        "system_md_tokens": sys_tokens,
        "user_template_tokens": template_tokens,
        "runtime_input_variables_tokens": input_vars,
        "per_call_input_tokens": per_call_input,
        "per_call_output_tokens": out_tokens,
    })

print(json.dumps(results, indent=2))
(REPO / "prompt_token_measurements.json").write_text(json.dumps(results, indent=2))
