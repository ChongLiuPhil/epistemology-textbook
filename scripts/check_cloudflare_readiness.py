#!/usr/bin/env python3
"""Validate the repository-side Cloudflare Workers Builds contract without deploying."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRANGLER = ROOT / "wrangler.jsonc"
PACKAGE = ROOT / "package.json"
NODE_VERSION = ROOT / ".nvmrc"
BUILD_CONTRACT = ROOT / "cloudflare-builds.yaml"
PUBLISHING = ROOT / "publishing.yaml"
READINESS = ROOT / "docs" / "cloudflare-readiness.yaml"
INSTALLER = ROOT / "scripts" / "ensure_quarto.sh"
BUILD_WRAPPER = ROOT / "scripts" / "cloudflare_build.sh"
WORKFLOWS = ROOT / ".github" / "workflows"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(path: Path, marker: str) -> None:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    if marker not in path.read_text(encoding="utf-8"):
        fail(f"{path.relative_to(ROOT)} is missing required marker: {marker}")


def check_wrangler() -> None:
    try:
        data = json.loads(WRANGLER.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("missing wrangler.jsonc")
    except json.JSONDecodeError as exc:
        fail(f"wrangler.jsonc must remain JSON-compatible in this project: {exc}")

    if data.get("name") != "epistemology-textbook":
        fail("wrangler Worker name does not match project id")

    compatibility_date = data.get("compatibility_date")
    if not isinstance(compatibility_date, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", compatibility_date
    ):
        fail("wrangler compatibility_date is missing or invalid")

    assets = data.get("assets")
    if not isinstance(assets, dict) or assets.get("directory") != "./_book":
        fail("wrangler assets.directory must point to ./_book")

    if "main" in data:
        fail("reference Worker must remain static-assets-only; unexpected main script")


def check_toolchain() -> None:
    try:
        package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("missing package.json")
    except json.JSONDecodeError as exc:
        fail(f"invalid package.json: {exc}")

    wrangler = package.get("devDependencies", {}).get("wrangler")
    if wrangler != "4.135.0":
        fail(f"Wrangler must be pinned exactly to 4.135.0, found {wrangler!r}")

    scripts = package.get("scripts", {})
    if scripts.get("cloudflare:deploy") != "wrangler deploy":
        fail("package.json cloudflare:deploy must be 'wrangler deploy'")
    if scripts.get("cloudflare:preview") != "wrangler versions upload":
        fail("package.json cloudflare:preview must be 'wrangler versions upload'")

    if NODE_VERSION.read_text(encoding="utf-8").strip() != "24":
        fail(".nvmrc must pin Node major 24")

    for marker in (
        'VERSION=',
        '1.10.18',
        'sha256sum --check --status',
        'linux-amd64.tar.gz',
        'linux-arm64.tar.gz',
    ):
        require(INSTALLER, marker)

    for marker in (
        'bash scripts/ensure_quarto.sh',
        'make web-publish-check',
    ):
        require(BUILD_WRAPPER, marker)


def check_workers_builds_contract() -> None:
    markers = (
        "mode: workers-builds-git",
        "repository: ChongLiuPhil/epistemology-textbook",
        "production_branch: main",
        "non_production_branch_builds: true",
        'build: "bash scripts/cloudflare_build.sh"',
        'deploy: "npm run cloudflare:deploy"',
        'preview_deploy: "npm run cloudflare:preview"',
        'node: "24"',
        'wrangler: "4.135.0"',
        'quarto: "1.10.18"',
        "name: epistemology-textbook",
        "static_assets_directory: ./_book",
        "credentials_in_repository: prohibited",
        "github_app_repository_scope: selected-repositories-only",
    )
    for marker in markers:
        require(BUILD_CONTRACT, marker)


def check_publication_contract() -> None:
    for marker in (
        "current_provider: github-pages",
        "target_provider: cloudflare-workers",
        "integration_mode: workers-builds-git",
        "build_contract: cloudflare-builds.yaml",
        'canonical_publish_gate: "make web-publish-check"',
        "output_directory: _book",
        "migration_status: staged",
    ):
        require(PUBLISHING, marker)

    for marker in (
        "preferred_mode: workers-builds-git",
        'canonical_publish_gate: "make web-publish-check"',
        "active_github_actions_cloudflare_deploy: false",
        "cloudflare_oauth_mcp: unavailable-in-current-session",
        "github_app: verified-via-github-checks",
        "repository_connection: verified",
        "worker_target: verified",
        "production_trigger: verified-main-build-passed",
        "preview_trigger: verified-preview-build-passed",
        "build_token: cloudflare-managed-present-security-review-pending",
        'workers_dev_url: "https://epistemology-textbook.philosophy-research.workers.dev"',
        'cloudflare_build_id: "d6bc8b62-78ba-4a9e-98ea-7a049a539858"',
        'cloudflare_build_id: "a12446a5-e341-48e4-8c22-1a184b1102c8"',
        'version_id: "3f8a15d6-9994-4e90-839c-2144c8dc54b7"',
        "target_canonical_url: unresolved",
        "status: blocked",
    ):
        require(READINESS, marker)

    readiness_body = READINESS.read_text(encoding="utf-8")

    http_match = re.search(r"^\s*workers_dev_http:\s*(\S+)\s*$", readiness_body, re.MULTILINE)
    if not http_match:
        fail("docs/cloudflare-readiness.yaml is missing workers_dev_http state")
    if http_match.group(1) not in {
        "not-run",
        "external-tool-unverified",
        "passed-via-github-actions",
    }:
        fail(f"unexpected workers_dev_http state: {http_match.group(1)}")

    production_http_match = re.search(
        r"^\s*production_http_verification:\s*(\S+)\s*$",
        readiness_body,
        re.MULTILINE,
    )
    if not production_http_match:
        fail("docs/cloudflare-readiness.yaml is missing production_http_verification state")
    if production_http_match.group(1) not in {
        "not-run",
        "passed-on-workers-dev-staging",
    }:
        fail(
            "unexpected production_http_verification state: "
            f"{production_http_match.group(1)}"
        )

    if http_match.group(1) == "passed-via-github-actions":
        for marker in (
            "runtime_http_verification:",
            "workflow_run: 35431565729",
            "pages_checked: 5",
            "local_assets_checked: 30",
        ):
            require(READINESS, marker)
        if "workers-dev-http-content-verification" in readiness_body:
            fail("HTTP verification blocker must be removed after runtime verification passes")

    for marker in (
        "account_access: connected",
        "github_app: verified",
        "repository_connection: verified",
        "worker_target: verified",
        "workers_builds_triggers: verified",
        "build_token: present-security-review-pending",
        'workers_dev_url: "https://epistemology-textbook.philosophy-research.workers.dev"',
        "cloudflare_main_build: passed",
        "preview_deployment: passed",
        "production_cutover: blocked",
    ):
        require(PUBLISHING, marker)


def check_no_premature_github_actions_deploy() -> None:
    forbidden = (
        "cloudflare/wrangler-action",
        "wrangler deploy",
        "CLOUDFLARE_API_TOKEN",
        "CLOUDFLARE_ACCOUNT_ID",
    )

    for path in sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml")):
        body = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in body:
                fail(
                    "GitHub Actions Cloudflare deployment became active before the "
                    f"Workers Builds path was validated: {path.relative_to(ROOT)} contains {marker}"
                )


def main() -> None:
    check_wrangler()
    check_toolchain()
    check_workers_builds_contract()
    check_publication_contract()
    check_no_premature_github_actions_deploy()

    print(
        "Cloudflare Workers Builds contract check passed: the canonical Web publication "
        "gate, pinned toolchain, Wrangler static-assets config, Git integration commands, "
        "and verified Workers Builds connection state are mutually consistent; "
        "GitHub Pages remains current production, Cloudflare staging builds have passed, "
        "and no GitHub Actions Cloudflare cutover is active."
    )


if __name__ == "__main__":
    main()
