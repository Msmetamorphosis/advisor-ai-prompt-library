#!/usr/bin/env python3
"""Validate the advisor-ai-prompt-library.

Scans every prompt module in prompts/ and validates:

  1. Required files are present (prompt.yaml, system.md, examples.md,
     eval-cases.json, changelog.md).
  2. prompt.yaml parses, has all required fields, valid risk_level and status,
     semver version, ISO date in last_reviewed, and Medium/High/Restricted
     prompts declare human_review_required: true with substantive compliance_notes.
  3. eval-cases.json parses, contains >= 5 cases, has the required per-case keys,
     and prompt_id matches prompt.yaml.
  4. output-schema.json (where referenced) parses and validates as JSON Schema
     Draft 2020-12 and declares `required` + `additionalProperties: false`.
  5. user-template.md (when present) uses {{double_curly}} placeholders.
  6. compliance-constraints.md is present for any prompt that drafts client-
     facing communication (heuristic: name contains "Client" and "Email").
  7. prompt_id values are unique across the library and match folder names.

Prints a human-readable report and exits non-zero on any failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, SchemaError


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = REPO_ROOT / "prompts"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"

REQUIRED_FILES = {"prompt.yaml", "system.md", "examples.md", "eval-cases.json", "changelog.md"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MIN_EVAL_CASES = 5

EVAL_CASE_REQUIRED_KEYS = {"id", "description", "input", "expected_behavior"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.ok: list[str] = []

    def err(self, scope: str, msg: str) -> None:
        self.errors.append(f"[ERROR] {scope}: {msg}")

    def warn(self, scope: str, msg: str) -> None:
        self.warnings.append(f"[WARN]  {scope}: {msg}")

    def good(self, scope: str, msg: str) -> None:
        self.ok.append(f"[OK]    {scope}: {msg}")

    def render(self) -> str:
        sections: list[str] = []
        sections.append("=" * 72)
        sections.append("Prompt Library Validation Report")
        sections.append("=" * 72)
        sections.append("")
        sections.append(f"  OK:       {len(self.ok)}")
        sections.append(f"  WARN:     {len(self.warnings)}")
        sections.append(f"  ERRORS:   {len(self.errors)}")
        sections.append("")
        if self.errors:
            sections.append("Errors:")
            sections.extend(f"  {e}" for e in self.errors)
            sections.append("")
        if self.warnings:
            sections.append("Warnings:")
            sections.extend(f"  {w}" for w in self.warnings)
            sections.append("")
        sections.append("Passing checks:")
        sections.extend(f"  {o}" for o in self.ok)
        return "\n".join(sections)


def _load_required_metadata() -> dict[str, Any]:
    return json.loads((FIXTURES_DIR / "required_metadata_fields.json").read_text(encoding="utf-8"))


def _validate_required_files(prompt_dir: Path, report: Report) -> None:
    scope = f"prompts/{prompt_dir.name}"
    missing = [f for f in REQUIRED_FILES if not (prompt_dir / f).exists()]
    if missing:
        report.err(scope, f"missing required files: {missing}")
    else:
        report.good(scope, "required files present")


def _validate_prompt_yaml(prompt_dir: Path, required: dict[str, Any], report: Report) -> dict[str, Any] | None:
    scope = f"prompts/{prompt_dir.name}/prompt.yaml"
    meta_path = prompt_dir / "prompt.yaml"
    if not meta_path.exists():
        return None
    try:
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        report.err(scope, f"YAML parse error: {e}")
        return None
    if not isinstance(meta, dict):
        report.err(scope, "did not parse to a dict.")
        return None

    missing = [f for f in required["fields"] if f not in meta]
    if missing:
        report.err(scope, f"missing required fields: {missing}")

    if meta.get("risk_level") not in required["valid_risk_levels"]:
        report.err(scope, f"invalid risk_level={meta.get('risk_level')!r}")

    if meta.get("status") not in required["valid_status_values"]:
        report.err(scope, f"invalid status={meta.get('status')!r}")

    if not SEMVER_RE.match(str(meta.get("version", ""))):
        report.err(scope, f"version={meta.get('version')!r} is not semantic.")

    if not ISO_DATE_RE.match(str(meta.get("last_reviewed", ""))):
        report.err(scope, f"last_reviewed={meta.get('last_reviewed')!r} is not YYYY-MM-DD.")

    if meta.get("risk_level") in {"Medium", "High", "Restricted"}:
        if meta.get("human_review_required") is not True:
            report.err(scope, "risk_level requires human_review_required: true.")

    if meta.get("risk_level") in {"High", "Restricted"}:
        notes = (meta.get("compliance_notes") or "").strip()
        if len(notes) < 30:
            report.err(scope, f"High/Restricted requires substantive compliance_notes (>=30 chars); got {len(notes)}.")

    if meta.get("prompt_id") != prompt_dir.name:
        report.err(scope, f"prompt_id={meta.get('prompt_id')!r} does not match folder name.")

    prohibitions = meta.get("prohibited_use_cases") or []
    if not isinstance(prohibitions, list) or not prohibitions:
        report.err(scope, "prohibited_use_cases must be a non-empty list.")

    approvers = meta.get("approved_by") or []
    if not isinstance(approvers, list) or not approvers:
        report.err(scope, "approved_by must be a non-empty list.")

    if not [e for e in report.errors if scope in e]:
        report.good(scope, f"metadata OK (v{meta.get('version')}, {meta.get('risk_level')}).")
    return meta


def _validate_eval_cases(prompt_dir: Path, meta: dict[str, Any] | None, report: Report) -> None:
    scope = f"prompts/{prompt_dir.name}/eval-cases.json"
    eval_path = prompt_dir / "eval-cases.json"
    if not eval_path.exists():
        return
    try:
        data = json.loads(eval_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report.err(scope, f"invalid JSON: {e}")
        return
    cases = data.get("cases") or []
    if len(cases) < MIN_EVAL_CASES:
        report.err(scope, f"requires >= {MIN_EVAL_CASES} cases, has {len(cases)}.")
    seen_ids: set[str] = set()
    for i, case in enumerate(cases):
        missing = EVAL_CASE_REQUIRED_KEYS - set(case.keys())
        if missing:
            report.err(scope, f"case #{i} ({case.get('id', '<no-id>')}) missing keys: {missing}")
        cid = case.get("id")
        if cid in seen_ids:
            report.err(scope, f"duplicate case id: {cid}")
        seen_ids.add(cid)
    if meta and data.get("prompt_id") != meta.get("prompt_id"):
        report.err(scope, f"prompt_id={data.get('prompt_id')!r} != prompt.yaml prompt_id={meta.get('prompt_id')!r}")
    if not [e for e in report.errors if scope in e]:
        report.good(scope, f"{len(cases)} cases, all keys present.")


def _validate_output_schema(prompt_dir: Path, meta: dict[str, Any] | None, report: Report) -> None:
    if not meta:
        return
    schema_name = meta.get("output_schema")
    if not schema_name:
        return
    scope = f"prompts/{prompt_dir.name}/{schema_name}"
    schema_path = prompt_dir / schema_name
    if not schema_path.exists():
        report.err(scope, "referenced but file missing.")
        return
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report.err(scope, f"invalid JSON: {e}")
        return
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as e:
        report.err(scope, f"invalid JSON Schema: {e.message}")
        return
    if "required" not in schema:
        report.err(scope, "missing top-level 'required'.")
    if schema.get("additionalProperties") is not False:
        report.err(scope, "additionalProperties must be false for strictness.")
    if not [e for e in report.errors if scope in e]:
        report.good(scope, "JSON Schema valid and strict.")


def _validate_user_template(prompt_dir: Path, report: Report) -> None:
    user_template = prompt_dir / "user-template.md"
    if not user_template.exists():
        return
    scope = f"prompts/{prompt_dir.name}/user-template.md"
    text = user_template.read_text(encoding="utf-8")
    if not re.search(r"\{\{[a-z_][a-z0-9_]*\}\}", text):
        report.err(scope, "must use {{placeholder}} variables.")
    else:
        report.good(scope, "uses {{placeholder}} variables.")


def _validate_compliance_constraints(prompt_dir: Path, meta: dict[str, Any] | None, report: Report) -> None:
    if not meta:
        return
    name_lower = meta.get("name", "").lower()
    if "client" in name_lower and "email" in name_lower:
        scope = f"prompts/{prompt_dir.name}/compliance-constraints.md"
        if not (prompt_dir / "compliance-constraints.md").exists():
            report.err(scope, "client-facing email prompt requires compliance-constraints.md.")
        else:
            report.good(scope, "compliance-constraints.md present.")


def main() -> int:
    report = Report()
    required = _load_required_metadata()

    if not PROMPTS_DIR.exists():
        report.err("prompts/", "directory missing.")
        print(report.render())
        return 1

    prompt_dirs = sorted([p for p in PROMPTS_DIR.iterdir() if p.is_dir()])
    if not prompt_dirs:
        report.err("prompts/", "no prompt modules found.")
        print(report.render())
        return 1

    seen_ids: dict[str, str] = {}
    for prompt_dir in prompt_dirs:
        _validate_required_files(prompt_dir, report)
        meta = _validate_prompt_yaml(prompt_dir, required, report)
        if meta and "prompt_id" in meta:
            pid = meta["prompt_id"]
            if pid in seen_ids:
                report.err(
                    f"library",
                    f"duplicate prompt_id={pid} in {prompt_dir.name} and {seen_ids[pid]}",
                )
            else:
                seen_ids[pid] = prompt_dir.name
        _validate_eval_cases(prompt_dir, meta, report)
        _validate_output_schema(prompt_dir, meta, report)
        _validate_user_template(prompt_dir, report)
        _validate_compliance_constraints(prompt_dir, meta, report)

    print(report.render())
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
