"""Shared pytest fixtures for the advisor-ai-prompt-library test suite."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = REPO_ROOT / "prompts"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

# Files every prompt module must ship.
BASE_REQUIRED_FILES = {
    "prompt.yaml",
    "system.md",
    "examples.md",
    "eval-cases.json",
    "changelog.md",
}


def _prompt_dirs() -> list[Path]:
    if not PROMPTS_DIR.exists():
        return []
    return sorted([p for p in PROMPTS_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")])


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def prompt_dirs() -> list[Path]:
    return _prompt_dirs()


@pytest.fixture(scope="session")
def prohibited_phrases() -> list[str]:
    data = json.loads((FIXTURES_DIR / "prohibited_phrases.json").read_text(encoding="utf-8"))
    return data["phrases"]


@pytest.fixture(scope="session")
def required_metadata() -> dict[str, Any]:
    return json.loads((FIXTURES_DIR / "required_metadata_fields.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def loaded_prompts(prompt_dirs: list[Path]) -> list[dict[str, Any]]:
    """Load all prompt.yaml files once; surface parse errors clearly."""
    out: list[dict[str, Any]] = []
    for d in prompt_dirs:
        meta_path = d / "prompt.yaml"
        if not meta_path.exists():
            out.append({"_path": d, "_meta_path": meta_path, "_error": "prompt.yaml missing"})
            continue
        try:
            data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:  # pragma: no cover — surfaced via tests
            data = {"_yaml_error": str(e)}
        out.append({"_path": d, "_meta_path": meta_path, **data})
    return out


def pytest_generate_tests(metafunc):
    """Parametrize tests that take a `prompt_dir` argument with each prompt module."""
    if "prompt_dir" in metafunc.fixturenames:
        dirs = _prompt_dirs()
        metafunc.parametrize(
            "prompt_dir",
            dirs,
            ids=[d.name for d in dirs],
        )
