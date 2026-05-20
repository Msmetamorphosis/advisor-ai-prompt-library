"""Schema-file tests: any output-schema.json must be valid JSON Schema."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator, SchemaError


pytestmark = pytest.mark.schema


def test_output_schema_is_valid_json_schema(prompt_dir: Path) -> None:
    meta = yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8")) or {}
    schema_name = meta.get("output_schema")
    if not schema_name:
        pytest.skip(f"{prompt_dir.name}: no output_schema declared.")

    schema_path = prompt_dir / schema_name
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        pytest.fail(f"{prompt_dir.name}: {schema_name} is not valid JSON: {e}")

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as e:
        pytest.fail(f"{prompt_dir.name}: {schema_name} is not a valid JSON Schema: {e.message}")


def test_output_schema_declares_required(prompt_dir: Path) -> None:
    """Output schemas should be strict: declare `required` and `additionalProperties: false`."""
    meta = yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8")) or {}
    schema_name = meta.get("output_schema")
    if not schema_name:
        pytest.skip(f"{prompt_dir.name}: no output_schema declared.")

    schema = json.loads((prompt_dir / schema_name).read_text(encoding="utf-8"))
    assert "required" in schema, f"{prompt_dir.name}: {schema_name} must declare `required`."
    assert schema.get("additionalProperties") is False, (
        f"{prompt_dir.name}: {schema_name} must set additionalProperties=false for strictness."
    )
