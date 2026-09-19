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
SECURITY_AUDIT = ROOT / "docs" / "cloudflare-build-token-security.zh-CN.md"
DECISION_LOG = ROOT / "core" / "DECISION_LOG.zh-CN.md"
CURRENT_FOCUS = ROOT / "docs" / "working-memory" / "current-focus.zh-CN.md"
TASK_PLAN = ROOT / "docs" / "working-memory" / "task-plan.zh-CN.md"
QUARTO_WEB = ROOT / "_quarto-web.yml"
INSTALLER = ROOT / "scripts" / "ensure_quarto.sh"
BUILD_WRAPPER = ROOT / "scripts" / "cloudflare_build.sh"
EXTERNAL_CI_CONTRACT = ROOT / "cloudflare-external-ci.yaml"
EXTERNAL_CI_WORKFLOW = ROOT / ".github" / "workflows" / "cloudflare-external-ci.yml"
HTML_WORKFLOW = ROOT / ".github" / "workflows" / "html-ci.yml"
RUNTIME_WORKFLOW = ROOT / ".github" / "workflows" / "cloudflare-runtime-http.yml"
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
        "selected_production_profile: workers-builds-native",
        "human_risk_acceptance: accepted-broad-managed-user-token-scope",
        "least_privilege: false",
    )
    for marker in markers:
        require(BUILD_CONTRACT, marker)


def check_publication_contract() -> None:
    for marker in (
        "current_provider: cloudflare-workers",
        "target_provider: null",
        "integration_mode: workers-builds-git",
        "build_contract: cloudflare-builds.yaml",
        'canonical_publish_gate: "make web-publish-check"',
        "output_directory: _book",
        "migration_status: canonical-active-verified",
        "integration_state: PRODUCTION_ACTIVE",
        "cutover_state: ACTIVE",
        "legacy_url_policy: retire",
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
        'target_canonical_url: "https://epistemology-textbook.philosophy-research.workers.dev/"',
        "custom_domain: not-applicable-workers-dev-canonical",
        "selected_production_profile: workers-builds-native",
        "human_risk_acceptance: accepted-broad-managed-user-token-scope",
        "status: complete",
        "post_cutover_verification:",
        'git_commit: "63510364ed40a97faf190c484dd80afc91971ecb"',
        "github_actions_runtime_run: 35453967021",
        "github_actions_runtime_check_id: 105925881599",
        "cloudflare_provider_check_id: 105926103705",
        'cloudflare_build_id: "42aa93fe-d9b6-49e4-80be-a849951a6b9d"',
        "legacy_retirement:",
        "policy: retire",
        "status: complete-human-confirmed",
        "unpublish:",
        "status: human-confirmed",
        "confirmed_at: 2026-09-20",
        "actor: repository-owner",
        "independent_http_verification:",
        "status: unavailable-current-session",
        "blockers: []",
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
        "cloudflare-managed-default-reviewed-broad-scope-profile-a-accepted",
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
        "reviewed-broad-scope-profile-a-accepted",
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
        "pending-post-cutover",
        "passed-post-cutover",
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
        "production_cutover: verified-active",
        "production_security_profile: workers-builds-native",
        'current_production_url: "https://epistemology-textbook.philosophy-research.workers.dev/"',
        "target_production_url: null",
        "canonical_url: active-workers-dev",
        "custom_domain: not-applicable",
        "github_pages_retirement: complete-human-confirmed",
    ):
        require(PUBLISHING, marker)


def check_verified_main_build_checkpoint() -> None:
    markers = (
        "verified_main_build_checkpoint:",
        'git_commit: "71ad7c5cdfd9cb8cebdf9f4a3ac6a247959e0b15"',
        "github_check_id: 105904495866",
        'cloudflare_build_id: "93823dff-1206-4282-b037-24876840f0c6"',
        "status: passed",
    )
    for path in (READINESS, BUILD_CONTRACT):
        for marker in markers:
            require(path, marker)

    readiness_body = READINESS.read_text(encoding="utf-8")
    build_contract_body = BUILD_CONTRACT.read_text(encoding="utf-8")
    if "latest_main_cloudflare_build:" in readiness_body:
        fail("readiness evidence must use stable checkpoint semantics, not a moving latest build")
    if "latest_main_build:" in build_contract_body:
        fail("build contract evidence must use stable checkpoint semantics, not a moving latest build")


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

    if "status: connected-production-active" in machine:
        human = READINESS_DOC.read_text(encoding="utf-8")
        required_human_markers = (
            "CLOUDFLARE-CANONICAL-ACTIVE-VERIFIED / PAGES-RETIREMENT-HUMAN-CONFIRMED",
            "Current canonical identity: workers.dev.",
            "Cloudflare production delivery: ACTIVE / VERIFIED.",
            "GitHub Pages legacy policy: RETIRE / UNPUBLISH HUMAN-CONFIRMED.",
            "candidate / validate-only PASS",
            "不是 production-tested",
        )
        for marker in required_human_markers:
            if marker not in human:
                fail(
                    "human-readable Cloudflare readiness drifted from "
                    f"connected-production-active machine state: missing {marker!r}"
                )
        for stale in (
            "ACCOUNT-SIDE-UNVERIFIED",
            "Account-side readiness: UNVERIFIED",
            "Current canonical production: GitHub Pages.",
        ):
            if stale in human:
                fail(
                    "human-readable Cloudflare readiness contains stale state: "
                    f"{stale}"
                )

    require(PUBLISHING, "adopted_commit: 21a5360727167bad6f399477ded073431645fa1d")
    publishing = PUBLISHING.read_text(encoding="utf-8")
    for marker in (
        "source:\n  canonical: git\n  branch: main\n  visibility: public",
        "authorization_state: authorized",
        "visibility: public",
        "access:\n      mode: none",
        'provider_url: "https://epistemology-textbook.philosophy-research.workers.dev/"',
        "canonical_identity:\n      type: provider-native",
        'url: "https://epistemology-textbook.philosophy-research.workers.dev/"',
        "legacy_url_policy: retire",
    ):
        if marker not in publishing:
            fail(f"publishing.yaml is missing adopted PPF visibility/access marker: {marker}")

    adoption = ADOPTION_DOC.read_text(encoding="utf-8")
    for marker in (
        "21a5360727167bad6f399477ded073431645fa1d",
        "Previous adopted framework commit",
        "does **not** silently follow PPF `main`",
        "source visibility = public",
        "Web access mode = none",
        "current canonical identity = workers.dev",
        "legacy GitHub Pages policy = retire",
        "legacy unpublish = human-confirmed complete",
        "candidate / validate-only PASS",
    ):
        if marker not in adoption:
            fail(f"PPF adoption record is missing reconciliation marker: {marker}")

    phase1 = PHASE1_AUDIT.read_text(encoding="utf-8")
    if "Historical Phase 1 audit." not in phase1:
        fail("PPF Phase 1 audit must be explicitly marked as historical")

    runbook = STAGING_RUNBOOK.read_text(encoding="utf-8")
    for marker in (
        "selected-production-profile / operational-verified",
        "candidate / validate-only PASS",
        "不是 production-tested",
        "Profile C — Future Native Granular",
        "当前项目已选择 Profile A",
    ):
        if marker not in runbook:
            fail(f"Cloudflare staging runbook is missing security-profile marker: {marker}")

    security_audit = SECURITY_AUDIT.read_text(encoding="utf-8")
    for marker in (
        "PROFILE A SELECTED",
        "BROAD-SCOPE RISK ACCEPTED",
        "LEAST_PRIVILEGE_FALSE",
        "Profile B = not adopted",
    ):
        if marker not in security_audit:
            fail(f"Cloudflare security audit is missing Profile A decision marker: {marker}")
    if "HUMAN PROFILE DECISION PENDING" in security_audit:
        fail("Cloudflare security audit still claims the production profile decision is pending")

    decision_log = DECISION_LOG.read_text(encoding="utf-8")
    for marker in (
        "D007 — 选择 Cloudflare Production Security Profile A",
        "D009 — 显式采用 PPF publication visibility / access / canonical identity 语义",
        "D010 — GitHub Pages legacy policy = RETIRE",
        "21a5360727167bad6f399477ded073431645fa1d",
        "least_privilege: false",
        "不等于批准 canonical production cutover",
    ):
        if marker not in decision_log:
            fail(f"Decision Log is missing Profile A human decision marker: {marker}")

    current_focus = CURRENT_FOCUS.read_text(encoding="utf-8")
    for marker in (
        "Profile A — Workers Builds Native",
        "least_privilege: false",
        "workers.dev post-cutover provider build/runtime verification 已通过",
        "21a5360727167bad6f399477ded073431645fa1d",
        "Web publication: `authorized / public`",
        "Web access: `none`",
        "current canonical identity: workers.dev",
        "legacy GitHub Pages policy: `retire`",
        "`Unpublish site` human-confirmed complete on 2026-09-20",
        "Verified cutover revision：`63510364ed40a97faf190c484dd80afc91971ecb`",
        "Verified cutover runtime run：`35453967021`",
        "Verified cutover Cloudflare provider check：`105926103705`",
    ):
        if marker not in current_focus:
            fail(f"Current Focus is missing selected Profile A state: {marker}")
    for marker in (
        "Verified post-merge Cloudflare checkpoint check：`105904495866`",
        "93823dff-1206-4282-b037-24876840f0c6",
    ):
        if marker not in current_focus:
            fail(f"Current Focus is missing verified Cloudflare checkpoint marker: {marker}")

    task_plan = TASK_PLAN.read_text(encoding="utf-8")
    if "until first real Cloudflare staging is verified" in task_plan:
        fail("Task Plan still claims first Cloudflare staging is unverified")
    if "workers.dev canonical cutover is implemented" not in task_plan:
        fail("Task Plan must record that workers.dev canonical cutover is implemented")
    if "Checkpoint semantics intentionally replace a moving `latest_main_build` claim" not in task_plan:
        fail("Task Plan must explain stable provider-evidence checkpoint semantics")
    for marker in (
        "COMPLETED / PROFILE-A-SELECTED",
        "production security profile selected — Profile A",
        "broad-scope risk acceptance",
        "WM-T027",
        "WM-T028",
        "COMPLETED / HUMAN-CONFIRMED-UNPUBLISH",
        "GitHub Pages legacy policy — `RETIRE`",
        "Custom Domain — N/A for workers.dev canonical",
        "- [x] post-cutover production verification",
        "- [x] GitHub Pages current deployment unpublish — repository-owner human-confirmed",
    ):
        if marker not in task_plan:
            fail(f"Task Plan is missing Profile A completion marker: {marker}")

    readiness_body = READINESS.read_text(encoding="utf-8")
    if "human-security-profile-decision" in readiness_body:
        fail("security-profile blocker must be removed after human Profile A selection")
    if "target-canonical-url" in readiness_body:
        fail("target canonical URL blocker must be removed after workers.dev target selection")
    if "redirect-or-canonical-policy" in readiness_body:
        fail("legacy/canonical policy blocker must be removed after RETIRE selection")
    for marker in (
        "post_cutover_verification:",
        "status: passed",
        'git_commit: "63510364ed40a97faf190c484dd80afc91971ecb"',
        "github_actions_runtime_run: 35453967021",
        "github_actions_runtime_check_id: 105925881599",
        "cloudflare_provider_check_id: 105926103705",
        'cloudflare_build_id: "42aa93fe-d9b6-49e4-80be-a849951a6b9d"',
        'canonical_target: "https://epistemology-textbook.philosophy-research.workers.dev/"',
        'canonical_identity_current: "https://epistemology-textbook.philosophy-research.workers.dev/"',
        "canonical_target_selected: true",
        "custom_domain_required: false",
        "cutover:\n  status: complete",
        "legacy_retirement:",
        "policy: retire",
        "status: complete-human-confirmed",
        "unpublish:",
        "status: human-confirmed",
        "confirmed_at: 2026-09-20",
        "actor: repository-owner",
        "independent_http_verification:",
        "status: unavailable-current-session",
        "blockers: []",
    ):
        if marker not in readiness_body:
            fail(f"readiness state is missing completed legacy-retirement marker: {marker}")
    if "- post-cutover-runtime-verification" in readiness_body:
        fail("post-cutover runtime blocker must be removed after verified canonical activation")
    if "- github-pages-unpublish" in readiness_body:
        fail("GitHub Pages unpublish blocker must be removed after owner confirmation")

    quarto_web = QUARTO_WEB.read_text(encoding="utf-8")
    if 'site-url: "https://epistemology-textbook.philosophy-research.workers.dev/"' not in quarto_web:
        fail("Web site-url must point to the active workers.dev canonical identity")
    if "https://chongliuphil.github.io/epistemology-textbook/" in quarto_web:
        fail("retired GitHub Pages canonical URL must not remain in _quarto-web.yml")

    html_workflow = HTML_WORKFLOW.read_text(encoding="utf-8")
    for forbidden in (
        "actions/configure-pages",
        "actions/upload-pages-artifact",
        "actions/deploy-pages",
        "pages: write",
        "id-token: write",
        "deploy-pages:",
    ):
        if forbidden in html_workflow:
            fail(f"GitHub Pages deployment path must remain retired: found {forbidden}")

    runtime_workflow = RUNTIME_WORKFLOW.read_text(encoding="utf-8")
    for marker in (
        "push:",
        "branches: [main]",
        "Verify active workers.dev canonical runtime after main push",
        '--expect-root-marker "https://epistemology-textbook.philosophy-research.workers.dev/"',
    ):
        if marker not in runtime_workflow:
            fail(f"post-cutover runtime workflow is missing marker: {marker}")


def main() -> None:
    check_wrangler()
    check_toolchain()
    check_workers_builds_contract()
    check_publication_contract()
    check_verified_main_build_checkpoint()
    check_hardened_external_ci_candidate()
    check_no_premature_github_actions_deploy()
    check_human_readable_state_reconciliation()

    print(
        "Cloudflare Workers Builds contract check passed: the canonical Web publication "
        "gate, pinned toolchain, Wrangler static-assets config, Git integration commands, "
        "and verified Workers Builds connection state are mutually consistent; "
        "the hardened external-CI candidate is constrained to validate/manual modes; "
        "workers.dev is the verified canonical production target; GitHub Pages "
        "deployment is retired from normal CI and its unpublish is human-confirmed complete."
    )


if __name__ == "__main__":
    main()
