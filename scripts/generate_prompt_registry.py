#!/usr/bin/env python3
"""Generate prompt-registry.json at the repo root.

Reads every prompts/<id>/prompt.yaml and emits a JSON registry summarizing the
library — useful for advisor-tool catalogs, supervisory dashboards, and audit
reviewers who want to see the library at a glance.

The registry shape:

  {
    "generated_at": "<ISO 8601 UTC>",
    "library_version": "<from CHANGELOG if extractable, else 'unreleased'>",
    "prompts": [
      {
        "prompt_id": "...",
        "name": "...",
        "version": "...",
        "risk_level": "...",
        "status": "...",
        "owner": "...",
        "human_review_required": true,
        "last_reviewed": "YYYY-MM-DD",
        "path": "prompts/..."
      },
      ...
    ]
  }
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = REPO_ROOT / "prompts"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
REGISTRY_PATH = REPO_ROOT / "prompt-registry.json"


def _library_version() -> str:
    if not CHANGELOG.exists():
        return "unreleased"
    text = CHANGELOG.read_text(encoding="utf-8")
    match = re.search(r"##\s*\[(\d+\.\d+\.\d+)\]", text)
    return match.group(1) if match else "unreleased"


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    if not PROMPTS_DIR.exists():
        print("[error] prompts/ directory not found.", file=sys.stderr)
        return 1

    entries: list[dict[str, object]] = []
    for prompt_dir in sorted(p for p in PROMPTS_DIR.iterdir() if p.is_dir()):
        meta_path = prompt_dir / "prompt.yaml"
        if not meta_path.exists():
            print(f"[warn] {prompt_dir.name} has no prompt.yaml; skipping.", file=sys.stderr)
            continue
        try:
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            print(f"[error] {prompt_dir.name}: YAML parse error: {e}", file=sys.stderr)
            return 1
        last_reviewed = meta.get("last_reviewed")
        if last_reviewed is not None and not isinstance(last_reviewed, str):
            last_reviewed = last_reviewed.isoformat()
        entries.append({
            "prompt_id": meta.get("prompt_id"),
            "name": meta.get("name"),
            "version": meta.get("version"),
            "risk_level": meta.get("risk_level"),
            "status": meta.get("status"),
            "owner": meta.get("owner"),
            "human_review_required": meta.get("human_review_required"),
            "last_reviewed": last_reviewed,
            "path": f"prompts/{prompt_dir.name}",
        })

    registry = {
        "generated_at": _iso_now(),
        "library_version": _library_version(),
        "prompts": entries,
    }
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {REGISTRY_PATH.relative_to(REPO_ROOT)} with {len(entries)} prompts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
