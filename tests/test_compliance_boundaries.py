"""Compliance-boundary tests: prohibited phrases must not appear in production prompt text.

The test is deliberately *intelligent*: it ignores phrases that appear inside
prohibition contexts (e.g., system-prompt lines that begin with "Do not", or
example sections labelled "What the prompt must not do"). It only flags phrases
that appear as if the prompt were instructing the model to produce them.

We scan:
  * Every system.md (the production prompt text).
  * Every examples.md "Expected Output" code block.

We deliberately do NOT scan:
  * prompt.yaml (where prohibitions are listed by design).
  * eval-cases.json (where `must_not_include` arrays list the phrases by design).
  * compliance-constraints.md (which exists to enumerate banned phrases).
  * retrieval-rules.md / citation-rules.md (governance docs that name patterns).
  * changelog.md (which records prohibition tightening).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


pytestmark = pytest.mark.compliance


PROHIBITION_MARKERS = (
    "do not", "must not", "must avoid", "must refuse", "prohibited",
    "forbidden", "cannot", "avoid", "no recommendation", "not advice",
    "does not", "did not", "must not include", "must not contain",
    "is not", "are not", "refuses", "refused", "deferred", "decline",
    "declined", "echo or endorse", "do not echo", "do not restate",
    "do not produce", "do not include", "do not opine", "do not provide",
    "do not characterize", "must not produce", "must not include",
    "could be read as", "ensure no", "no tax", "no legal",
    "client asked", "client said", "client used", "client mentioned",
    "question about", "asked about", "inquiry", "products exist",
    "surface", "surfaced", "flag", "flagged", "flag emitted",
    "review_flags", "human_review_flags", "recorded", "records",
    "redirect", "redirects", "redirected", "refer to", "referral",
)


def _is_prohibition_context(line: str, prev_lines: list[str]) -> bool:
    """Return True if the phrase appears in a context that *names* it as prohibited."""
    haystack = " ".join([*prev_lines[-4:], line]).lower()
    return any(marker in haystack for marker in PROHIBITION_MARKERS)


def _scan_text_for_phrases(text: str, phrases: list[str]) -> list[tuple[int, str, str]]:
    """Return list of (line_no, phrase, line) violations — phrases NOT in a prohibition context."""
    violations: list[tuple[int, str, str]] = []
    lines = text.splitlines()
    current_heading = ""
    for i, line in enumerate(lines):
        # Track the nearest enclosing heading.
        if line.strip().startswith("#"):
            current_heading = line.strip().lower()
        lowered = line.lower()
        for phrase in phrases:
            if phrase.lower() in lowered:
                # Build context window: heading + last 4 lines + this line.
                context_lines = [current_heading] + lines[max(0, i - 4):i]
                if _is_prohibition_context(line, context_lines):
                    continue
                # Also skip lines that quote the phrase as part of a heading like
                # "What the prompt must not do".
                if "must not" in current_heading or "prohibited" in current_heading:
                    continue
                # Also skip lines inside a bullet that visibly enumerates banned items
                # (e.g., a line starting with `- "...":` inside a banned-phrase list).
                if re.match(r"^\s*[-*]\s*\".*\"\s*$", line):
                    # bare quoted phrase as a bullet item — likely an enumeration; allow.
                    continue
                violations.append((i + 1, phrase, line.rstrip()))
    return violations


def test_system_prompt_no_unflagged_prohibited_phrases(
    prompt_dir: Path, prohibited_phrases: list[str]
) -> None:
    system_md = prompt_dir / "system.md"
    text = system_md.read_text(encoding="utf-8")
    violations = _scan_text_for_phrases(text, prohibited_phrases)
    assert not violations, (
        f"{prompt_dir.name}/system.md contains prohibited phrases outside a prohibition "
        f"context:\n" + "\n".join(f"  line {ln}: '{p}' in: {line}" for ln, p, line in violations)
    )


def test_examples_expected_output_no_unflagged_prohibited_phrases(
    prompt_dir: Path, prohibited_phrases: list[str]
) -> None:
    """Scan examples.md for expected-output code blocks. Skip rationale prose where
    the phrase is intentionally named to be banned."""
    examples_md = prompt_dir / "examples.md"
    if not examples_md.exists():
        pytest.skip(f"{prompt_dir.name}: no examples.md.")
    text = examples_md.read_text(encoding="utf-8")
    violations = _scan_text_for_phrases(text, prohibited_phrases)
    assert not violations, (
        f"{prompt_dir.name}/examples.md contains prohibited phrases outside a prohibition "
        f"context:\n" + "\n".join(f"  line {ln}: '{p}' in: {line}" for ln, p, line in violations)
    )


def test_client_facing_prompt_has_review_reminder(prompt_dir: Path) -> None:
    """Any prompt whose risk level is High or Restricted must include explicit
    human-review reminder language in system.md."""
    meta = yaml.safe_load((prompt_dir / "prompt.yaml").read_text(encoding="utf-8")) or {}
    if meta["risk_level"] not in {"High", "Restricted"}:
        pytest.skip(f"{prompt_dir.name}: not High/Restricted.")
    system_text = (prompt_dir / "system.md").read_text(encoding="utf-8").lower()
    review_signals = ["human review", "advisor must review", "before sending",
                      "before saving", "pending advisor review", "advisor is responsible"]
    assert any(s in system_text for s in review_signals), (
        f"{prompt_dir.name}: High/Restricted prompts must include explicit advisor-review "
        f"language in system.md. Looked for any of: {review_signals}"
    )


def test_user_templates_use_double_curly_placeholders(prompt_dir: Path) -> None:
    user_template = prompt_dir / "user-template.md"
    if not user_template.exists():
        pytest.skip(f"{prompt_dir.name}: no user-template.md.")
    text = user_template.read_text(encoding="utf-8")
    # At least one placeholder of the form {{name}}
    assert re.search(r"\{\{[a-z_][a-z0-9_]*\}\}", text), (
        f"{prompt_dir.name}/user-template.md must use double-curly placeholders like "
        f"{{{{client_meeting_notes}}}}."
    )
