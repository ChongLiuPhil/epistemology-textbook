#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return yaml.safe_load((ROOT/name).read_text(encoding="utf-8"))

def fail(msg):
    print("ERROR:",msg,file=sys.stderr)
    raise SystemExit(1)

project=load("project.yaml")
website=load("website.yaml")
publishing=load("publishing.yaml")
stack=load("project-stack.yaml")
lock=load("project-stack.lock.yaml")

pid=stack["project"]["id"]
for label,value in (
    ("project.yaml",project.get("id")),
    ("website.yaml",website.get("project_id")),
    ("publishing.yaml",publishing.get("project",{}).get("id")),
):
    if value != pid:
        fail(f"{label} project id {value!r} != stack id {pid!r}")

ppf_commit=stack["components"]["publishing"]["adopted_commit"]
if project.get("publishing",{}).get("adopted_framework_commit") != ppf_commit:
    fail("project.yaml PPF adopted commit differs from project-stack")
if publishing.get("framework",{}).get("adopted_commit") != ppf_commit:
    fail("publishing.yaml PPF adopted commit differs from project-stack")

native=stack["components"]["governance"]["project_native"]
gov=project.get("governance",{})
if gov.get("profile") != native.get("profile"):
    fail("project-native governance profile differs from stack functional mapping")
if gov.get("adopted_protocol_commit") != native.get("adopted_commit"):
    fail("project-native governance commit differs from stack functional mapping")

resolved=lock.get("resolved",{})
expected={
    "ahicp": stack["components"]["governance"]["adopted_commit"],
    "ppf": ppf_commit,
    "vault_interface": stack["components"]["portfolio_interface"]["adopted_commit"],
    "starter": stack["starter"]["adopted_commit"],
}
for key,value in expected.items():
    if resolved.get(key) != value:
        fail(f"project-stack.lock drift for {key}")

web=publishing["deployment"]["web"]
canonical=(web.get("canonical_identity") or {}).get("url") or web.get("current_production_url")
links=website.get("links") or []
if not canonical:
    fail("publishing.yaml has no canonical Web identity")
norm=lambda s: s.rstrip("/")
if norm(canonical) not in {norm(x if isinstance(x,str) else x.get("href","")) for x in links}:
    fail("website.yaml does not expose the publishing canonical Web URL")

if web.get("legacy_url_policy") == "retire":
    retired="https://chongliuphil.github.io/epistemology-textbook"
    for item in links:
        href=item if isinstance(item,str) else item.get("href","")
        if norm(href)==retired:
            fail("website.yaml still exposes retired GitHub Pages URL")

status_text=" ".join((website.get("status") or {}).values())
if "staged Phase 2" in status_text or "尚未切换生产" in status_text:
    fail("website.yaml contains stale pre-cutover Cloudflare status")

print("Project stack consistency passed: IDs, PPF revision, legacy governance mapping, lock, canonical URL, and retired-provider boundary agree.")
