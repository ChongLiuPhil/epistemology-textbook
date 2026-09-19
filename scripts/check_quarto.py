#!/usr/bin/env python3
"""Lightweight consistency checks for the canonical Quarto manuscript."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "_quarto.yml"
WEB_CONFIG = ROOT / "_quarto-web.yml"
PROFILE_CONFIGS = {
    "pdf": ROOT / "_quarto-pdf.yml",
    "docx": ROOT / "_quarto-docx.yml",
    "epub": ROOT / "_quarto-epub.yml",
    "latex": ROOT / "_quarto-latex.yml",
}
PUBLISHING = ROOT / "publishing.yaml"
WRANGLER = ROOT / "wrangler.jsonc"
BIB = ROOT / "references.bib"
MANUSCRIPT = ROOT / "manuscript"
MAKEFILE = ROOT / "Makefile"
GITIGNORE = ROOT / ".gitignore"
WORKFLOWS = ROOT / ".github" / "workflows"
PAGES_WORKFLOW = WORKFLOWS / "html-ci.yml"
PUBLICATION_WORKFLOW = WORKFLOWS / "build-publication-formats.yml"
RENDERED_CHECK = ROOT / "scripts" / "check_rendered_html.py"
MOBILE_READING_INCLUDE = ROOT / "assets" / "includes" / "reading-navigation.html"
OPEN_READING = MANUSCRIPT / "00-open-access-and-support.qmd"
ISSUE_TEMPLATES = ROOT / ".github" / "ISSUE_TEMPLATE"

EXPECTED = [
    "00-open-access-and-support.qmd",
    "00-preface.qmd",
    "01-knowledge.qmd",
    "02-skepticism-luck.qmd",
    "03-justification-context.qmd",
    "04-sources.qmd",
    "05-social-knowledge.qmd",
    "06-formal.qmd",
    "07-value.qmd",
    "08-digital-ai.qmd",
    "09-comparative.qmd",
    "study-guide.qmd",
    "research-studio.qmd",
    "exercise-hints.qmd",
    "glossary.qmd",
    "references.qmd",
]

REQUIRED_PROJECT_FILES = [
    ROOT / "index.qmd",
    CONFIG,
    WEB_CONFIG,
    *PROFILE_CONFIGS.values(),
    PUBLISHING,
    WRANGLER,
    BIB,
    MAKEFILE,
    ROOT / "book.css",
    ROOT / "project.yaml",
    ROOT / "website.yaml",
    GITIGNORE,
    PAGES_WORKFLOW,
    PUBLICATION_WORKFLOW,
    RENDERED_CHECK,
    MOBILE_READING_INCLUDE,
    ISSUE_TEMPLATES / "content-feedback.yml",
    ISSUE_TEMPLATES / "website-bug.yml",
    ISSUE_TEMPLATES / "config.yml",
]

GENERATED_MARKERS = (
    "source-file:",
    "本页由 LaTeX 主稿自动生成",
    "AUTO-GENERATED FROM LATEX",
)

CROSSREF_PREFIXES = ("fig-", "tbl-", "eq-", "sec-", "lst-")
CJK = r"\u3400-\u9fff"
OPEN_READING_URL = (
    "https://chongliuphil.github.io/epistemology-textbook/"
    "manuscript/00-open-access-and-support.html"
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_project_structure() -> None:
    for path in REQUIRED_PROJECT_FILES:
        if not path.exists():
            fail(f"missing required project file: {path.relative_to(ROOT)}")

    if not MANUSCRIPT.is_dir():
        fail("missing manuscript/ directory")
    if not WORKFLOWS.is_dir():
        fail("missing .github/workflows/ directory")

    ignored = GITIGNORE.read_text(encoding="utf-8")
    for entry in ("_book/", "_publication/", ".quarto/"):
        if entry not in ignored:
            fail(f"build output is not ignored by .gitignore: {entry}")


def check_quarto_config(config: str) -> None:
    if not re.search(r"(?m)^project:\s*\n(?:.*\n)*?\s{2}type:\s*book\s*$", config):
        fail("_quarto.yml is not configured as a Quarto book")

    if not re.search(r"(?ms)^profile:\s*\n\s{2}default:\s*web\s*$", config):
        fail("_quarto.yml does not declare web as the default profile")

    required_base_markers = {
        "root bibliography": "bibliography: references.bib",
        "Chinese language": "lang: zh-CN",
        "book author": 'author: "Chong Liu"',
        "book output name": 'output-file: "how-do-we-know"',
    }
    for label, marker in required_base_markers.items():
        if marker not in config:
            fail(f"{label} is missing from _quarto.yml")

    canonical_paths = ["index.qmd"] + [f"manuscript/{name}" for name in EXPECTED]
    for rel_path in canonical_paths:
        if rel_path not in config:
            fail(f"_quarto.yml does not include canonical source: {rel_path}")

    web = WEB_CONFIG.read_text(encoding="utf-8")
    required_web_markers = {
        "Web output directory": "output-dir: _book",
        "HTML format": "  html:",
        "public site URL": 'site-url: "https://chongliuphil.github.io/epistemology-textbook/"',
        "source repository": 'repo-url: "https://github.com/ChongLiuPhil/epistemology-textbook"',
        "reader feedback/source actions": "repo-actions: [issue, source]",
        "reader mode": "reader-mode: true",
        "back-to-top navigation": "back-to-top-navigation: true",
        "book sidebar label": 'header: "**本书目录**"',
        "chapter TOC label": 'toc-title: "本章目录"',
        "mobile chapter TOC include": "assets/includes/reading-navigation.html",
        "page footer": "page-footer:",
        "stable open-reading URL": OPEN_READING_URL,
    }
    for label, marker in required_web_markers.items():
        if marker not in web:
            fail(f"{label} is missing from _quarto-web.yml")

    expected_profiles = {
        "pdf": ("_publication/pdf", "  pdf:"),
        "docx": ("_publication/docx", "  docx:"),
        "epub": ("_publication/epub", "  epub:"),
        "latex": ("_publication/latex", "  latex:"),
    }
    for profile, (output_dir, format_marker) in expected_profiles.items():
        body = PROFILE_CONFIGS[profile].read_text(encoding="utf-8")
        if f"output-dir: {output_dir}" not in body:
            fail(f"{profile} profile has wrong output directory")
        if format_marker not in body:
            fail(f"{profile} profile does not configure its expected format")

    combined = config + "\n" + web
    if re.search(r"(?mi)^\s*downloads:\s*", combined):
        fail("automatic download links are not enabled during continuous Web Edition development")


def check_ppf_contract() -> None:
    publishing = PUBLISHING.read_text(encoding="utf-8")
    required = {
        "PPF schema": "schema: ppf/v0.1",
        "PPF source": "ChongLiuPhil/Personal-Publishing-Framework",
        "continuous Web mode": "mode: continuous",
        "on-demand mode": "mode: on-demand",
        "current Pages provider": "current_provider: github-pages",
        "target Cloudflare provider": "target_provider: cloudflare-workers",
        "staged migration": "migration_status: staged",
        "explicit release": "require_explicit_release: true",
    }
    for label, marker in required.items():
        if marker not in publishing:
            fail(f"{label} is missing from publishing.yaml")

    for profile in ("epub", "pdf", "docx", "latex"):
        pattern = rf"(?ms)^  {profile}:.*?mode:\s*on-demand"
        if not re.search(pattern, publishing):
            fail(f"publishing.yaml does not declare {profile} as on-demand")

    wrangler = WRANGLER.read_text(encoding="utf-8")
    for marker in ('"name": "epistemology-textbook"', '"directory": "./_book"'):
        if marker not in wrangler:
            fail(f"wrangler.jsonc is missing staged Cloudflare setting: {marker}")


def check_active_build_files() -> None:
    active_build_files = [
        CONFIG,
        MAKEFILE,
        PAGES_WORKFLOW,
        *[
            path
            for path in sorted(WORKFLOWS.glob("*.yml"))
            if path not in {PAGES_WORKFLOW, PUBLICATION_WORKFLOW}
        ],
        *[
            path
            for path in sorted(WORKFLOWS.glob("*.yaml"))
            if path not in {PAGES_WORKFLOW, PUBLICATION_WORKFLOW}
        ],
    ]
    legacy_patterns = {
        "old QMD generator": r"scripts/build_web\.py|website/generated/",
        "legacy LaTeX toolchain": r"(?i)latexmk|xelatex|pdflatex|textbook/[^\s]+\.tex",
    }
    forbidden_release_pattern = re.compile(
        r"(?i)(quarto\s+(?:render|publish)[^\n]*(?:epub|pdf|docx|latex)|"
        r"make\s+(?:epub|pdf|docx)|quarto-actions/publish)"
    )
    legacy_pages_pattern = re.compile(
        r"(?i)(git\s+(?:branch|push)[^\n]*gh-pages|refs/heads/gh-pages)"
    )

    for path in active_build_files:
        body = path.read_text(encoding="utf-8")
        for label, pattern in legacy_patterns.items():
            if re.search(pattern, body):
                fail(f"{label} dependency remains in {path.relative_to(ROOT)}")
        if forbidden_release_pattern.search(body):
            fail(
                "release-format command is allowed only in the manual publication workflow: "
                f"{path.relative_to(ROOT)}"
            )
        if legacy_pages_pattern.search(body):
            fail(f"legacy gh-pages branch deployment remains in {path.relative_to(ROOT)}")

    makefile = MAKEFILE.read_text(encoding="utf-8")
    for target in ("epub", "pdf", "docx", "latex"):
        if re.search(rf"(?m)^{target}\s*:", makefile):
            fail(f"daily release target remains in Makefile: {target}")

    if (ROOT / "epub.css").exists():
        fail("obsolete epub.css remains in the active project root")


def check_pages_deployment() -> None:
    workflow = PAGES_WORKFLOW.read_text(encoding="utf-8")
    required_markers = {
        "canonical Web publication gate": "make web-publish-check",
        "official Pages configuration": "actions/configure-pages@",
        "Pages artifact upload": "actions/upload-pages-artifact@",
        "Pages deployment": "actions/deploy-pages@",
        "rendered _book deployment source": "path: _book",
        "GitHub Pages environment": "name: github-pages",
        "main-only deployment guard": "github.ref == 'refs/heads/main'",
    }
    for label, marker in required_markers.items():
        if marker not in workflow:
            fail(f"{label} is missing from {PAGES_WORKFLOW.relative_to(ROOT)}")

    makefile = MAKEFILE.read_text(encoding="utf-8")
    gate_markers = {
        "web-publish-check target": "web-publish-check:",
        "Web-profile render inside canonical gate": "$(QUARTO) render --profile web",
        "rendered HTML validation inside canonical gate": "python3 scripts/check_rendered_html.py",
    }
    for label, marker in gate_markers.items():
        if marker not in makefile:
            fail(f"{label} is missing from Makefile")

    for output_format in ("pdf", "docx", "epub"):
        if re.search(rf"(?i)quarto\s+render[^\n]*--to\s+{output_format}\b", workflow):
            fail(f"daily Pages workflow unexpectedly renders {output_format}")


def check_publication_workflow() -> None:
    workflow = PUBLICATION_WORKFLOW.read_text(encoding="utf-8")
    required_markers = {
        "manual trigger": "workflow_dispatch:",
        "format input": "format:",
        "EPUB option": "- epub",
        "PDF option": "- pdf",
        "DOCX option": "- docx",
        "LaTeX option": "- latex",
        "profile render": 'quarto render --profile "${{ inputs.format }}"',
        "PPF publication directory": '_publication/${{ inputs.format }}/',
        "publication artifact upload": "actions/upload-artifact@",
    }
    for label, marker in required_markers.items():
        if marker not in workflow:
            fail(f"{label} is missing from {PUBLICATION_WORKFLOW.relative_to(ROOT)}")

    forbidden_markers = (
        "actions/deploy-pages@",
        "actions/create-release@",
        "softprops/action-gh-release",
        "gh release create",
        "quarto render --to pdf",
        "quarto render --to docx",
        "quarto render --to epub",
    )
    for marker in forbidden_markers:
        if marker in workflow:
            fail(
                "manual publication-format build must remain profile-based and must not "
                f"publish a release automatically: {marker}"
            )


def check_reader_support() -> None:
    text = OPEN_READING.read_text(encoding="utf-8")
    required_markers = (
        "阅读权不以付费为前提",
        "GitHub Issues",
        "版本、引用与来源",
        "当前开发范围",
    )
    for marker in required_markers:
        if marker not in text:
            fail(f"open-reading guidance is missing required section or principle: {marker}")

    mobile = MOBILE_READING_INCLUDE.read_text(encoding="utf-8")
    for marker in ("mobile-chapter-toc", "本章目录", "#quarto-margin-sidebar #TOC"):
        if marker not in mobile:
            fail(f"mobile chapter TOC include is missing expected behavior: {marker}")

    for name in ("content-feedback.yml", "website-bug.yml"):
        template = (ISSUE_TEMPLATES / name).read_text(encoding="utf-8")
        for marker in ("页面链接", "问题说明"):
            if marker not in template:
                fail(f"issue template {name} is missing reader-facing field: {marker}")


def check_sources() -> list[Path]:
    files = [ROOT / "index.qmd"] + [MANUSCRIPT / name for name in EXPECTED]
    for path in files:
        if not path.exists():
            fail(f"missing canonical Quarto source: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for marker in GENERATED_MARKERS:
            if marker in text:
                fail(f"legacy generated-source marker remains in {path.relative_to(ROOT)}: {marker}")

        if re.search(r"(?m)^\s*\$\s*$", text):
            fail(
                "standalone single-dollar math delimiter is not cross-format safe in "
                f"{path.relative_to(ROOT)}"
            )

        lines = text.splitlines()
        display_delimiters = [
            index for index, line in enumerate(lines) if line.strip() == "$"
        ]
        if len(display_delimiters) % 2:
            fail(f"unpaired display-math delimiter in {path.relative_to(ROOT)}")

        for opening, closing in zip(display_delimiters[0::2], display_delimiters[1::2]):
            if closing <= opening + 1:
                fail(f"empty display-math block in {path.relative_to(ROOT)}")
            if not lines[opening + 1].strip() or not lines[closing - 1].strip():
                fail(
                    "display math delimiter must directly touch its math content in "
                    f"{path.relative_to(ROOT)}"
                )
    return files


def check_citations(files: list[Path]) -> tuple[int, int]:
    bib_text = BIB.read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib_text))
    if not bib_keys:
        fail("no bibliography entries found")

    key_alternatives = "|".join(
        re.escape(key) for key in sorted(bib_keys, key=len, reverse=True)
    )
    malformed_boundary = re.compile(
        rf"(?<=[{CJK}])@(?:{key_alternatives})(?![A-Za-z0-9_:.+-])"
        rf"|@(?:{key_alternatives})(?=[{CJK}])"
    )

    cited: set[str] = set()
    citation_pattern = re.compile(
        r"(?<![A-Za-z0-9_@])@([A-Za-z][A-Za-z0-9_:.+-]*)"
    )

    for path in files:
        text = path.read_text(encoding="utf-8")
        boundary_match = malformed_boundary.search(text)
        if boundary_match:
            fail(
                "bare citation touches Chinese text and may be parsed as a longer key in "
                f"{path.relative_to(ROOT)}: {boundary_match.group(0)}"
            )

        for key in citation_pattern.findall(text):
            if not key.startswith(CROSSREF_PREFIXES):
                cited.add(key)

    missing = sorted(cited - bib_keys)
    if missing:
        fail("citation keys missing from references.bib: " + ", ".join(missing))

    return len(cited), len(bib_keys)


def main() -> None:
    require_project_structure()
    config = CONFIG.read_text(encoding="utf-8")
    check_quarto_config(config)
    check_ppf_contract()
    check_active_build_files()
    check_pages_deployment()
    check_publication_workflow()
    check_reader_support()
    files = check_sources()
    cited_count, bib_count = check_citations(files)

    print(
        "Quarto source check passed: "
        f"{len(files)} canonical QMD files, {cited_count} cited keys, "
        f"{bib_count} bibliography entries; PPF profiles share one canonical Quarto source, "
        "daily CI deploys only integrity-checked Web HTML to GitHub Pages during Phase 1, "
        "EPUB/PDF/DOCX/LaTeX remain explicit on-demand build artifacts, and "
        "reader navigation/feedback remain configured."
    )


if __name__ == "__main__":
    main()
