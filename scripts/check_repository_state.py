#!/usr/bin/env python3
"""Validate repository-backed collaboration state and reject known stale truths."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "START_HERE.zh-CN.md",
    "AGENTS.md",
    "HARC_MANIFEST.yaml",
    "HARC_CONTEXT_INTERFACE.yaml",
    "core/CONTENT_CORE.zh-CN.md",
    "core/FORM_CORE.zh-CN.md",
    "core/DECISION_LOG.zh-CN.md",
    "docs/working-memory.zh-CN.md",
    "docs/working-memory/current-focus.zh-CN.md",
    "docs/working-memory/task-plan.zh-CN.md",
    "docs/working-memory/work-log.zh-CN.md",
    "docs/book-architecture.zh-CN.md",
    "docs/framework-status.zh-CN.md",
    "LICENSE-DECISION.md",
    "CITATION.cff",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

def text(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        fail(f"missing collaboration/governance file: {rel}")
    return path.read_text(encoding="utf-8")

def require_marker(rel: str, marker: str) -> None:
    if marker not in text(rel):
        fail(f"{rel} is missing required marker: {marker}")

def main() -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            fail(f"missing collaboration/governance file: {rel}")

    manifest = text("HARC_MANIFEST.yaml")
    if 'profile: "HARC-lite-book"' not in manifest:
        fail("HARC manifest does not declare the HARC-lite-book profile")
    match = re.search(r'adopted_protocol_commit:\s*"([0-9a-f]{40})"', manifest)
    if not match:
        fail("HARC manifest must pin a 40-character adopted protocol commit")

    context = text("HARC_CONTEXT_INTERFACE.yaml")
    for marker in (
        'mode: "repository-backed"',
        'authoritative_store: "github"',
        'read_latest_before_write: true',
        'authoritative_session_copy: false',
    ):
        if marker not in context:
            fail(f"context interface is missing invariant: {marker}")

    required_sections = {
        "docs/working-memory/current-focus.zh-CN.md": (
            "CURRENT_STAGE",
            "CURRENT_OBJECTIVE",
            "PRIMARY_BLOCKER",
            "IMMEDIATE_NEXT_ACTION",
        ),
        "docs/working-memory/task-plan.zh-CN.md": (
            "ACTIVE TASKS",
            "NEXT ACTIONS",
            "PENDING HUMAN DECISIONS / CLARIFICATIONS",
            "SYNC DEFECTS",
        ),
        "core/DECISION_LOG.zh-CN.md": ("D001", "D002", "D003"),
        "docs/framework-status.zh-CN.md": ("CURRENT-PUBLISHED-BASELINE",),
    }
    for rel, markers in required_sections.items():
        body = text(rel)
        for marker in markers:
            if marker not in body:
                fail(f"{rel} is missing required state marker: {marker}")

    require_marker("LICENSE-DECISION.md", "UNRESOLVED")
    require_marker("CITATION.cff", "cff-version: 1.2.0")
    require_marker("CITATION.cff", "repository-code:")
    require_marker(".github/PULL_REQUEST_TEMPLATE.md", "CONTENT")
    require_marker(".github/PULL_REQUEST_TEMPLATE.md", "AI-PROPOSED")

    # This old file encoded a retired EPUB/gh-pages workflow and must not return.
    if (ROOT / "website" / "README.md").exists():
        fail("stale website/README.md returned; website has no separate active publishing source")

    reference = text("reference/README.md")
    for marker in ("不参与当前构建", "权利状态"):
        if marker not in reference:
            fail(f"reference/README.md must state external-material boundary: {marker}")
    if "textbook/Makefile" in reference:
        fail("reference/README.md still points to the legacy LaTeX build as current")

    legacy = text("textbook/README.md")[:1600]
    for marker in ("LEGACY", "不再是当前构建说明"):
        if marker not in legacy:
            fail(f"textbook/README.md lacks a clear legacy banner: {marker}")

    project = text("project.yaml")
    for marker in ("harc-lite-book", "e741c43c5cd158c43910e3832c7d757226717a97"):
        if marker not in project:
            fail(f"project.yaml is missing governance metadata: {marker}")

    print(
        "Repository governance check passed: HARC-lite control files, pinned protocol "
        "revision, Working Memory schema, citation metadata, PR routing, legacy boundaries, "
        "and unresolved license/third-party rights state are explicit."
    )

if __name__ == "__main__":
    main()
