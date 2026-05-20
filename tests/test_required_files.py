"""Structural tests: every prompt folder must contain the required files."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from conftest import BASE_REQUIRED_FILES


pytestmark = pytest.mark.structure


def test_prompts_directory_exists(repo_root: Path) -> None:
    assert (repo_root / "prompts").is_dir(), "prompts/ directory must exist."


def test_at_least_one_prompt_exists(prompt_dirs):
    assert len(prompt_dirs) >= 1, "Library must contain at least one prompt module."


def test_required_files_present(prompt_dir: Path) -> None:
    """Every prompt module ships the base set of required files."""
    missing = [f for f in BASE_REQUIRED_FILES if not (prompt_dir / f).exists()]
    assert not missing, f"{prompt_dir.name} is missing required files: {missing}"


def test_user_template_present_when_required(prompt_dir: Path) -> None:
    """All prompts in this library use a user template except internal-policy-search,
    which receives its inputs as structured retrieval. If a prompt declares
    `required_inputs` it must ship a user-template.md."""
    meta = yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8")) or {}
    if meta.get("required_inputs"):
        # internal-policy-search consumes structured retrieval directly; still ships
        # a user-template-equivalent set of inputs but documents them in system.md
        # and examples.md, so we only require user-template.md when the prompt
        # folder is one of the advisor-workflow prompts.
        user_template = prompt_dir / "user-template.md"
        if prompt_dir.name != "internal-policy-search":
            assert user_template.exists(), (
                f"{prompt_dir.name} declares required_inputs but is missing user-template.md"
            )


def test_output_schema_when_referenced(prompt_dir: Path) -> None:
    """If prompt.yaml references an output schema, the file must exist."""
    meta = yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8")) or {}
    schema_name = meta.get("output_schema")
    if schema_name:
        schema_path = prompt_dir / schema_name
        assert schema_path.exists(), (
            f"{prompt_dir.name} references output_schema={schema_name} but file is missing."
        )


def test_compliance_constraints_for_client_facing(prompt_dir: Path) -> None:
    """Any prompt that produces client-facing drafts must ship a compliance-constraints.md."""
    meta = yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8")) or {}
    name_lower = meta.get("name", "").lower()
    # In this library, only client-follow-up-email produces client-facing drafts.
    if "client" in name_lower and "email" in name_lower:
        assert (prompt_dir / "compliance-constraints.md").exists(), (
            f"{prompt_dir.name} produces client-facing drafts but is missing compliance-constraints.md"
        )
