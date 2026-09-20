#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT/name).read_text(encoding="utf-8")

def scalars(text):
    out = {}
    parents = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        key, value = raw.strip().split(":", 1)
        while parents and parents[-1][0] >= indent:
            parents.pop()
        if value.strip() == "":
            parents.append((indent, key))
            continue
        path = ".".join([p[1] for p in parents] + [key])
        value = value.strip().strip('"').strip("'")
        if value == "null":
            value = None
        elif value == "true":
            value = True
        elif value == "false":
            value = False
        out[path] = value
    return out


def fail(msg):
    print("ERROR:", msg, file=sys.stderr)
    raise SystemExit(1)

project_text=read("project.yaml")
website_text=read("website.yaml")
publishing_text=read("publishing.yaml")
stack_text=read("project-stack.yaml")
lock_text=read("project-stack.lock.yaml")

project=scalars(project_text)
website=scalars(website_text)
publishing=scalars(publishing_text)
stack=scalars(stack_text)
lock=scalars(lock_text)

pid=stack.get("project.id")
for label,value in (
    ("project.yaml",project.get("id")),
    ("website.yaml",website.get("project_id")),
    ("publishing.yaml",publishing.get("project.id")),
):
    if value != pid:
        fail(f"{label} project id {value!r} != stack id {pid!r}")

ppf_template_commit=stack.get("components.publishing.template_source_commit")
ppf_project_commit=stack.get("components.publishing.project_adopted_commit")
if project.get("publishing.adopted_framework_commit") != ppf_project_commit:
    fail("project.yaml PPF adopted commit differs from project-stack")
if publishing.get("framework.adopted_commit") != ppf_project_commit:
    fail("publishing.yaml PPF adopted commit differs from project-stack")

if project.get("governance.profile") != stack.get("components.governance.project_native.profile"):
    fail("project-native governance profile differs from stack functional mapping")
if project.get("governance.adopted_protocol_commit") != stack.get("components.governance.project_native.adopted_commit"):
    fail("project-native governance commit differs from stack functional mapping")

for key, expected in (
    ("resolved.ahicp",stack.get("components.governance.adopted_commit")),
    ("resolved.ppf",ppf_template_commit),
    ("resolved.vault_interface",stack.get("components.portfolio_interface.adopted_commit")),
    ("resolved.starter",stack.get("starter.adopted_commit")),
):
    if lock.get(key) != expected:
        fail(f"project-stack.lock drift for {key}")

canonical=publishing.get("deployment.web.canonical_identity.url") or publishing.get("deployment.web.current_production_url")
if not canonical:
    fail("publishing.yaml has no canonical Web identity")
links=re.findall(r"(?m)^\s*-\s+(https?://\S+)\s*$",website_text)
norm=lambda s: s.rstrip("/")
if norm(canonical) not in {norm(x) for x in links}:
    fail("website.yaml does not expose the publishing canonical Web URL")

if publishing.get("deployment.web.legacy_url_policy") == "retire":
    retired="https://chongliuphil.github.io/epistemology-textbook"
    if retired in {norm(x) for x in links}:
        fail("website.yaml still exposes retired GitHub Pages URL")

if "staged Phase 2" in website_text or "尚未切换生产" in website_text:
    fail("website.yaml contains stale pre-cutover Cloudflare status")

print("Project stack consistency passed: IDs, PPF revision, legacy governance mapping, lock, canonical URL, and retired-provider boundary agree.")
