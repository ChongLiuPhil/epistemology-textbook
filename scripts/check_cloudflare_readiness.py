#!/usr/bin/env python3
"""Validate repository-side Cloudflare Phase 2 readiness without deploying."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRANGLER = ROOT / "wrangler.jsonc"
PUBLISHING = ROOT / "publishing.yaml"
READINESS = ROOT / "docs" / "cloudflare-readiness.yaml"
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
    if not WRANGLER.exists():
        fail("missing wrangler.jsonc")

    body = WRANGLER.read_text(encoding="utf-8")
    try:
        data = json.loads(body)
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
        fail("Phase 2 readiness expects a static-assets-only Worker; unexpected main script")

    if "binding" in assets:
        fail("static-assets-only readiness config should not declare an assets binding")


def check_contract() -> None:
    for marker in (
        "current_provider: github-pages",
        "target_provider: cloudflare-workers",
        "output_directory: _book",
        "migration_status: staged",
    ):
        require(PUBLISHING, marker)

    for marker in (
        "status: ready-for-account-side-staging",
        "active_cloudflare_deploy_workflow: false",
        "cloudflare_account: unverified",
        "worker_target: unverified",
        "github_secret_CLOUDFLARE_ACCOUNT_ID: unverified",
        "github_secret_CLOUDFLARE_API_TOKEN: unverified",
        "target_canonical_url: unresolved",
        "preview_deployment: not-run",
        "production_deployment: not-run",
        "status: blocked",
    ):
        require(READINESS, marker)


def check_no_premature_cloudflare_deploy() -> None:
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
                    "Cloudflare deployment became active before readiness gates were resolved: "
                    f"{path.relative_to(ROOT)} contains {marker}"
                )


def main() -> None:
    check_wrangler()
    check_contract()
    check_no_premature_cloudflare_deploy()

    print(
        "Cloudflare readiness check passed: static-assets Wrangler configuration is "
        "consistent with _book; GitHub Pages remains current production; account-side "
        "Cloudflare prerequisites remain explicitly unverified; no active Cloudflare "
        "deployment workflow can cut over production prematurely."
    )


if __name__ == "__main__":
    main()
