"""Metadata tests: prompt.yaml conformance."""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


pytestmark = pytest.mark.metadata


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def _load_meta(prompt_dir: Path) -> dict:
    return yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8")) or {}


def test_prompt_yaml_parses(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    assert isinstance(meta, dict) and meta, f"{prompt_dir.name}: prompt.yaml did not parse to a dict."


def test_required_fields_present(prompt_dir: Path, required_metadata) -> None:
    meta = _load_meta(prompt_dir)
    missing = [f for f in required_metadata["fields"] if f not in meta]
    assert not missing, f"{prompt_dir.name}: missing required prompt.yaml fields: {missing}"


def test_risk_level_valid(prompt_dir: Path, required_metadata) -> None:
    meta = _load_meta(prompt_dir)
    assert meta["risk_level"] in required_metadata["valid_risk_levels"], (
        f"{prompt_dir.name}: invalid risk_level={meta['risk_level']}. "
        f"Must be one of {required_metadata['valid_risk_levels']}."
    )


def test_status_valid(prompt_dir: Path, required_metadata) -> None:
    meta = _load_meta(prompt_dir)
    assert meta["status"] in required_metadata["valid_status_values"], (
        f"{prompt_dir.name}: invalid status={meta['status']}. "
        f"Must be one of {required_metadata['valid_status_values']}."
    )


def test_version_is_semver(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    version = str(meta["version"])
    assert SEMVER_RE.match(version), (
        f"{prompt_dir.name}: version={version} is not semantic (MAJOR.MINOR.PATCH)."
    )


def test_human_review_required_for_med_high_restricted(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    if meta["risk_level"] in {"Medium", "High", "Restricted"}:
        assert meta.get("human_review_required") is True, (
            f"{prompt_dir.name}: risk_level={meta['risk_level']} requires human_review_required=true."
        )


def test_high_risk_has_compliance_notes(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    if meta["risk_level"] in {"High", "Restricted"}:
        notes = (meta.get("compliance_notes") or "").strip()
        assert len(notes) >= 30, (
            f"{prompt_dir.name}: risk_level={meta['risk_level']} requires substantive "
            f"compliance_notes (>=30 chars). Found: {len(notes)} chars."
        )


def test_prohibited_use_cases_listed(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    prohibitions = meta.get("prohibited_use_cases") or []
    assert isinstance(prohibitions, list) and len(prohibitions) >= 1, (
        f"{prompt_dir.name}: prohibited_use_cases must be a non-empty list."
    )


def test_approved_by_non_empty(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    approved_by = meta.get("approved_by") or []
    assert isinstance(approved_by, list) and len(approved_by) >= 1, (
        f"{prompt_dir.name}: approved_by must list at least one approver."
    )


def test_last_reviewed_is_iso_date(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    last_reviewed = str(meta.get("last_reviewed", ""))
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", last_reviewed), (
        f"{prompt_dir.name}: last_reviewed must be YYYY-MM-DD. Got: {last_reviewed!r}"
    )


def test_prompt_ids_unique(loaded_prompts) -> None:
    ids = [p["prompt_id"] for p in loaded_prompts if "prompt_id" in p]
    duplicates = {pid for pid in ids if ids.count(pid) > 1}
    assert not duplicates, f"Duplicate prompt_id values found: {duplicates}"


def test_prompt_id_matches_directory(prompt_dir: Path) -> None:
    meta = _load_meta(prompt_dir)
    assert meta["prompt_id"] == prompt_dir.name, (
        f"{prompt_dir.name}: prompt_id={meta['prompt_id']} does not match folder name."
    )
