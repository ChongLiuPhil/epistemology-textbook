#!/usr/bin/env python3
"""Validate repository-backed HARC-lite collaboration state."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "HARC_MANIFEST.yaml"
PROJECT = ROOT / "project.yaml"

PATH_SECTIONS = {"bootstrap", "required_read_order", "state", "artifacts"}
GENERATED_ARTIFACT_KEYS = {"web_output"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def text(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        fail(f"missing repository file: {rel}")
    return path.read_text(encoding="utf-8")


def scalar(body: str, key: str) -> str:
    match = re.search(
        rf"(?m)^\s*{re.escape(key)}:\s*(?:\"([^\"]+)\"|'([^']+)'|([^#\n]+?))\s*$",
        body,
    )
    if not match:
        fail(f"missing scalar in repository metadata: {key}")
    return next(group.strip() for group in match.groups() if group is not None)


def manifest_declared_paths(body: str) -> list[tuple[str, str, str]]:
    """Return (section, key, path) for repository paths declared by the manifest."""
    declared: list[tuple[str, str, str]] = []
    current_section: str | None = None

    for line in body.splitlines():
        section_match = re.match(r"^  ([A-Za-z0-9_]+):\s*$", line)
        if section_match:
            current_section = section_match.group(1)
            continue

        if current_section not in PATH_SECTIONS:
            continue

        if current_section == "required_read_order":
            item_match = re.match(r'^\s{4}-\s*"([^"]+)"\s*$', line)
            if item_match:
                declared.append((current_section, "item", item_match.group(1)))
            continue

        scalar_match = re.match(
            r'^\s{4}([A-Za-z0-9_]+):\s*"([^"]+)"\s*$', line
        )
        if scalar_match:
            key, value = scalar_match.groups()
            declared.append((current_section, key, value))

    return declared


def require_marker(rel: str, marker: str) -> None:
    if marker not in text(rel):
        fail(f"{rel} is missing required marker: {marker}")


def check_manifest_paths(manifest: str) -> None:
    declared = manifest_declared_paths(manifest)
    if not declared:
        fail("manifest declares no repository paths")

    seen: set[tuple[str, str]] = set()
    for section, key, rel in declared:
        identity = (section, key if key != "item" else rel)
        if identity in seen:
            fail(f"duplicate manifest path declaration: {section}.{key} -> {rel}")
        seen.add(identity)

        if section == "artifacts" and key in GENERATED_ARTIFACT_KEYS:
            continue

        path = ROOT / rel
        if not path.exists():
            fail(f"manifest path does not exist: {section}.{key} -> {rel}")

    required_bootstrap = {
        "START_HERE.zh-CN.md",
        "ONBOARDING_CHECK.zh-CN.md",
        "AGENTS.md",
        "HARC_CONTEXT_INTERFACE.yaml",
    }
    declared_values = {rel for _, _, rel in declared}
    missing = sorted(required_bootstrap - declared_values)
    if missing:
        fail("manifest is missing bootstrap/control paths: " + ", ".join(missing))


def check_manifest_project_consistency(manifest: str) -> None:
    project = PROJECT.read_text(encoding="utf-8")

    manifest_profile = scalar(manifest, "profile")
    manifest_profile_version = scalar(manifest, "profile_version")
    manifest_protocol_version = scalar(manifest, "adopted_protocol_version")
    manifest_commit = scalar(manifest, "adopted_protocol_commit")

    if not re.fullmatch(r"[0-9a-f]{40}", manifest_commit):
        fail("manifest adopted_protocol_commit must be a 40-character Git SHA")

    comparisons = {
        "profile": (manifest_profile, scalar(project, "profile")),
        "profile_version": (manifest_profile_version, scalar(project, "profile_version")),
        "adopted_protocol_version": (
            manifest_protocol_version,
            scalar(project, "adopted_protocol_version"),
        ),
        "adopted_protocol_commit": (
            manifest_commit,
            scalar(project, "adopted_protocol_commit"),
        ),
    }
    for label, (manifest_value, project_value) in comparisons.items():
        if manifest_value != project_value:
            fail(
                f"manifest/project governance mismatch for {label}: "
                f"{manifest_value!r} != {project_value!r}"
            )


def check_context_interface(manifest: str) -> None:
    context = text("HARC_CONTEXT_INTERFACE.yaml")
    for marker in (
        'mode: "repository-backed"',
        'authoritative_store: "github"',
        'authoritative_session_copy: false',
        'read_latest_before_high_impact_action: true',
        'read_latest_before_write: true',
        'invalidate_touched_cache_after_write: true',
        'conflict_state: "REVISION-CONFLICT"',
        '"stop_write"',
        '"fresh_fetch_changed_state"',
        '"reconcile_or_rebase_current_change"',
        'activation_phrase: "BOOK REPOSITORY CONTEXT — ACTIVE"',
    ):
        if marker not in context:
            fail(f"context interface is missing invariant: {marker}")

    manifest_paths = {
        key: rel
        for section, key, rel in manifest_declared_paths(manifest)
        if section in {"bootstrap", "state"} and key != "item"
    }
    context_markers = {
        "start_here": 'start_here: "{}"',
        "onboarding_check": 'onboarding_check: "{}"',
        "agent_contract": 'agent_contract: "{}"',
        "working_memory_index": 'index: "{}"',
        "working_memory_current_focus": 'current_focus: "{}"',
        "working_memory_task_plan": 'task_plan: "{}"',
        "working_memory_work_log": 'work_log: "{}"',
    }
    for manifest_key, template in context_markers.items():
        if manifest_key not in manifest_paths:
            fail(f"manifest is missing role needed by context interface: {manifest_key}")
        marker = template.format(manifest_paths[manifest_key])
        if marker not in context:
            fail(
                f"context interface does not match manifest role "
                f"{manifest_key}: {manifest_paths[manifest_key]}"
            )


def check_operational_state() -> None:
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
            "RECENTLY RESOLVED / PROMOTED",
            "CLARIFICATION COMPLETION RULE",
            "SYNC DEFECTS",
        ),
        "docs/framework-status.zh-CN.md": (
            "CURRENT-PUBLISHED-BASELINE",
            "Release Approval",
        ),
        "docs/release-status.zh-CN.md": (
            "AUTHOR-PUBLISHED / CONTINUOUSLY-REVISED",
            "RELEASE-APPROVED",
            "责任主体",
        ),
    }
    for rel, markers in required_sections.items():
        body = text(rel)
        for marker in markers:
            if marker not in body:
                fail(f"{rel} is missing required state marker: {marker}")


def check_protocol_semantics() -> None:
    for marker in ("D001", "D004", "D005"):
        require_marker("core/DECISION_LOG.zh-CN.md", marker)

    for marker in (
        "作者 Chong Liu",
        "责任主体",
        "REVISION-CONFLICT",
        "RESOLVED / PROMOTED",
        "Release Approval",
    ):
        require_marker("AGENTS.md", marker)

    for marker in ("责任主体", "作者 Chong Liu", "学习—整合—梳理", "哲学研究不能被简单等同"):
        require_marker("core/CONTENT_CORE.zh-CN.md", marker)

    for marker in ("PDF / DOCX / EPUB", "GitHub Pages", "手动 workflow"):
        require_marker("core/FORM_CORE.zh-CN.md", marker)

    for marker in (
        "BOOK REPOSITORY CONTEXT — ACTIVE",
        "PASS / PARTIAL / FAIL",
        "Repository revision:",
        "Release status:",
    ):
        require_marker("ONBOARDING_CHECK.zh-CN.md", marker)


def check_existing_project_boundaries() -> None:
    require_marker("LICENSE-DECISION.md", "UNRESOLVED")
    require_marker("CITATION.cff", "cff-version: 1.2.0")
    require_marker("CITATION.cff", "repository-code:")
    require_marker(".github/PULL_REQUEST_TEMPLATE.md", "CONTENT")
    require_marker(".github/PULL_REQUEST_TEMPLATE.md", "AI-PROPOSED")

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


def main() -> None:
    if not MANIFEST.exists():
        fail("missing HARC_MANIFEST.yaml")
    if not PROJECT.exists():
        fail("missing project.yaml")

    manifest = MANIFEST.read_text(encoding="utf-8")
    if scalar(manifest, "profile") != "HARC-lite-book":
        fail("HARC manifest does not declare the HARC-lite-book profile")

    check_manifest_paths(manifest)
    check_manifest_project_consistency(manifest)
    check_context_interface(manifest)
    check_operational_state()
    check_protocol_semantics()
    check_existing_project_boundaries()

    print(
        "Repository governance check passed: manifest-declared paths resolve; "
        "project/manifest versions agree; onboarding, revision-conflict, human-responsibility, "
        "clarification-promotion, architecture/release gates, legacy boundaries, citation "
        "metadata, and unresolved rights state are explicit."
    )


if __name__ == "__main__":
    main()
