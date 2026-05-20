"""Eval-case tests: every prompt has a well-formed regression test set."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml


pytestmark = pytest.mark.schema

MIN_EVAL_CASES = 5


def _load_eval(prompt_dir: Path) -> dict:
    return json.loads((prompt_dir / "eval-cases.json").read_text(encoding="utf-8"))


def test_eval_cases_is_valid_json(prompt_dir: Path) -> None:
    try:
        _load_eval(prompt_dir)
    except json.JSONDecodeError as e:
        pytest.fail(f"{prompt_dir.name}: eval-cases.json is not valid JSON: {e}")


def test_eval_cases_count(prompt_dir: Path) -> None:
    data = _load_eval(prompt_dir)
    cases = data.get("cases") or []
    assert len(cases) >= MIN_EVAL_CASES, (
        f"{prompt_dir.name}: requires at least {MIN_EVAL_CASES} eval cases, has {len(cases)}."
    )


def test_eval_case_structure(prompt_dir: Path) -> None:
    data = _load_eval(prompt_dir)
    required_keys = {"id", "description", "input", "expected_behavior"}
    for i, case in enumerate(data.get("cases", [])):
        missing = required_keys - set(case.keys())
        assert not missing, (
            f"{prompt_dir.name}: eval case #{i} ({case.get('id', '<no id>')}) "
            f"is missing required keys: {missing}"
        )


def test_eval_case_ids_unique(prompt_dir: Path) -> None:
    data = _load_eval(prompt_dir)
    ids = [c.get("id") for c in data.get("cases", [])]
    duplicates = {i for i in ids if ids.count(i) > 1}
    assert not duplicates, f"{prompt_dir.name}: duplicate eval case ids: {duplicates}"


def test_eval_prompt_id_matches(prompt_dir: Path) -> None:
    data = _load_eval(prompt_dir)
    meta = yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8"))
    assert data.get("prompt_id") == meta["prompt_id"], (
        f"{prompt_dir.name}: eval-cases.json prompt_id={data.get('prompt_id')} "
        f"does not match prompt.yaml prompt_id={meta['prompt_id']}"
    )
