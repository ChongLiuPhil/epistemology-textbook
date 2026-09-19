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
READINESS_DOC = ROOT / "docs" / "cloudflare-readiness.zh-CN.md"
ADOPTION_DOC = ROOT / "docs" / "ppf-adoption.md"
PHASE1_AUDIT = ROOT / "docs" / "ppf-pilot-audit.zh-CN.md"
STAGING_RUNBOOK = ROOT / "docs" / "cloudflare-staging-runbook.zh-CN.md"
CURRENT_FOCUS = ROOT / "docs" / "working-memory" / "current-focus.zh-CN.md"
TASK_PLAN = ROOT / "docs" / "working-memory" / "task-plan.zh-CN.md"
INSTALLER = ROOT / "scripts" / "ensure_quarto.sh"
BUILD_WRAPPER = ROOT / "scripts" / "cloudflare_build.sh"
EXTERNAL_CI_CONTRACT = ROOT / "cloudflare-external-ci.yaml"
EXTERNAL_CI_WORKFLOW = ROOT / ".github" / "workflows" / "cloudflare-external-ci.yml"
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
        'workers_dev_url: "https://epistemology-textbook.philosophy-research.workers.dev"',
        'cloudflare_build_id: "d6bc8b62-78ba-4a9e-98ea-7a049a539858"',
        'cloudflare_build_id: "a12446a5-e341-48e4-8c22-1a184b1102c8"',
        'version_id: "3f8a15d6-9994-4e90-839c-2144c8dc54b7"',
        "target_canonical_url: unresolved",
        "status: blocked",
    ):
        require(READINESS, marker)

    readiness_body = READINESS.read_text(encoding="utf-8")

    credential_match = re.search(
        r"^\s*build_token:\s*(\S+)\s*$",
        readiness_body,
        re.MULTILINE,
    )
    if not credential_match:
        fail("docs/cloudflare-readiness.yaml is missing account-side build credential state")
    if credential_match.group(1) not in {
        "cloudflare-managed-present-security-review-pending",
        "cloudflare-managed-default-reviewed-broad-scope",
        "hardened-least-privilege",
    }:
        fail(f"unexpected readiness build credential state: {credential_match.group(1)}")

    publishing_body = PUBLISHING.read_text(encoding="utf-8")
    publishing_credential_match = re.search(
        r"^\s*build_token:\s*(\S+)\s*$",
        publishing_body,
        re.MULTILINE,
    )
    if not publishing_credential_match:
        fail("publishing.yaml is missing build credential readiness state")
    if publishing_credential_match.group(1) not in {
        "present-security-review-pending",
        "reviewed-broad-scope-hardening-pending",
        "hardened-least-privilege",
    }:
        fail(
            "unexpected publishing.yaml build credential state: "
            f"{publishing_credential_match.group(1)}"
        )

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
        'workers_dev_url: "https://epistemology-textbook.philosophy-research.workers.dev"',
        "cloudflare_main_build: passed",
        "preview_deployment: passed",
        "production_cutover: blocked",
    ):
        require(PUBLISHING, marker)


def check_hardened_external_ci_candidate() -> None:
    contract_markers = (
        "profile: hardened-external-ci",
        "status: candidate-validate-only",
        "token_type: account-owned-api-token",
        "resource: epistemology-textbook",
        "role: editor",
        "token_secret: CLOUDFLARE_API_TOKEN",
        "account_id_variable: CLOUDFLARE_ACCOUNT_ID",
        "automatic_production_deploy: false",
        "automatic_preview_deploy: false",
        "production_requires_main: true",
        "disable_workers_builds_before_external_ci_becomes_authoritative: required",
    )
    for marker in contract_markers:
        require(EXTERNAL_CI_CONTRACT, marker)

    workflow = EXTERNAL_CI_WORKFLOW.read_text(encoding="utf-8")
    required_workflow_markers = (
        "pull_request:",
        "workflow_dispatch:",
        "default: validate",
        "make cloudflare-build",
        "github.event_name == 'workflow_dispatch' && inputs.mode != 'validate'",
        "github.event_name == 'workflow_dispatch' && inputs.mode == 'preview'",
        "github.event_name == 'workflow_dispatch' && inputs.mode == 'production'",
        'test "$GITHUB_REF" = "refs/heads/main"',
        "secrets.CLOUDFLARE_API_TOKEN",
        "vars.CLOUDFLARE_ACCOUNT_ID",
        "wrangler versions upload --preview-alias",
        "npm run cloudflare:deploy",
    )
    for marker in required_workflow_markers:
        if marker not in workflow:
            fail(f"hardened external-CI candidate is missing safety marker: {marker}")

    for forbidden_trigger in ("  push:", "  schedule:"):
        if forbidden_trigger in workflow:
            fail(
                "hardened external-CI candidate must remain manual for deployment; "
                f"unexpected trigger {forbidden_trigger.strip()}"
            )


def check_no_premature_github_actions_deploy() -> None:
    forbidden = (
        "cloudflare/wrangler-action",
        "wrangler deploy",
        "CLOUDFLARE_API_TOKEN",
        "CLOUDFLARE_ACCOUNT_ID",
    )

    for path in sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml")):
        if path == EXTERNAL_CI_WORKFLOW:
            continue
        body = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in body:
                fail(
                    "Cloudflare deployment credential/command appeared outside the "
                    f"explicit hardened candidate workflow: {path.relative_to(ROOT)} contains {marker}"
                )


def check_human_readable_state_reconciliation() -> None:
    machine = READINESS.read_text(encoding="utf-8")

    if "status: connected-runtime-verified" in machine:
        human = READINESS_DOC.read_text(encoding="utf-8")
        required_human_markers = (
            "ACCOUNT-CONNECTED / MAIN+PREVIEW+RUNTIME-VERIFIED / CUTOVER-BLOCKED",
            "Current canonical production: GitHub Pages.",
            "candidate / validate-only PASS",
            "不是 production-tested",
            "Cloudflare canonical production cutover: NOT DONE / BLOCKED.",
        )
        for marker in required_human_markers:
            if marker not in human:
                fail(
                    "human-readable Cloudflare readiness drifted from "
                    f"connected-runtime-verified machine state: missing {marker!r}"
                )
        for stale in (
            "ACCOUNT-SIDE-UNVERIFIED",
            "Account-side readiness: UNVERIFIED",
        ):
            if stale in human:
                fail(
                    "human-readable Cloudflare readiness contains stale account-side state: "
                    f"{stale}"
                )

    adoption = ADOPTION_DOC.read_text(encoding="utf-8")
    for marker in (
        "Adopted framework commit: `9326920e1920d18f0a71eac26d4068da9d6bdffe`",
        "NOT ADOPTED",
        "does **not** silently follow PPF `main`",
        "candidate / validate-only PASS",
    ):
        if marker not in adoption:
            fail(f"PPF adoption record is missing reconciliation marker: {marker}")

    phase1 = PHASE1_AUDIT.read_text(encoding="utf-8")
    if "Historical Phase 1 audit." not in phase1:
        fail("PPF Phase 1 audit must be explicitly marked as historical")

    runbook = STAGING_RUNBOOK.read_text(encoding="utf-8")
    for marker in (
        "candidate / validate-only PASS",
        "不是 production-tested",
        "Profile C — Future Native Granular",
    ):
        if marker not in runbook:
            fail(f"Cloudflare staging runbook is missing security-profile marker: {marker}")

    current_focus = CURRENT_FOCUS.read_text(encoding="utf-8")
    if "Profile B 已经推进到当前无新 credential 条件下的可验证极限" not in current_focus:
        fail("Current Focus does not reflect completed Profile B candidate validation")

    task_plan = TASK_PLAN.read_text(encoding="utf-8")
    if "until first real Cloudflare staging is verified" in task_plan:
        fail("Task Plan still claims first Cloudflare staging is unverified")
    if "Cloudflare staging is verified." not in task_plan:
        fail("Task Plan must record that Cloudflare staging is verified")


def main() -> None:
    check_wrangler()
    check_toolchain()
    check_workers_builds_contract()
    check_publication_contract()
    check_hardened_external_ci_candidate()
    check_no_premature_github_actions_deploy()
    check_human_readable_state_reconciliation()

    print(
        "Cloudflare Workers Builds contract check passed: the canonical Web publication "
        "gate, pinned toolchain, Wrangler static-assets config, Git integration commands, "
        "and verified Workers Builds connection state are mutually consistent; "
        "the hardened external-CI candidate is constrained to validate/manual modes; "
        "GitHub Pages remains current production and no automatic GitHub Actions "
        "Cloudflare cutover is active."
    )


if __name__ == "__main__":
    main()
