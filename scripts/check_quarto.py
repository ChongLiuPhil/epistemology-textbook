#!/usr/bin/env python3
"""Lightweight consistency checks for the canonical Quarto manuscript."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "_quarto.yml"
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
    for entry in ("_book/", ".quarto/"):
        if entry not in ignored:
            fail(f"build output is not ignored by .gitignore: {entry}")


def check_quarto_config(config: str) -> None:
    if not re.search(r"(?m)^project:\s*\n(?:.*\n)*?\s{2}type:\s*book\s*$", config):
        fail("_quarto.yml is not configured as a Quarto book")

    if not re.search(r"(?m)^format:\s*$", config):
        fail("_quarto.yml has no format section")

    for output_format in ("html", "pdf", "docx", "epub"):
        if not re.search(rf"(?m)^\s{{2}}{output_format}:\s*$", config):
            fail(f"Quarto publication format is not configured: {output_format}")

    if re.search(r"(?mi)^\s*downloads:\s*", config):
        fail("automatic download links are not enabled during continuous Web Edition development")

    required_markers = {
        "root bibliography": "bibliography: references.bib",
        "Chinese language": "lang: zh-CN",
        "book author": 'author: "Chong Liu"',
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
    for label, marker in required_markers.items():
        if marker not in config:
            fail(f"{label} is missing from _quarto.yml")

    canonical_paths = ["index.qmd"] + [f"manuscript/{name}" for name in EXPECTED]
    for rel_path in canonical_paths:
        if rel_path not in config:
            fail(f"_quarto.yml does not include canonical source: {rel_path}")


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
        r"(?i)(quarto\s+(?:render|publish)[^\n]*(?:epub|pdf|docx)|"
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
    for target in ("epub", "pdf", "docx"):
        if re.search(rf"(?m)^{target}\s*:", makefile):
            fail(f"daily release target remains in Makefile: {target}")

    if (ROOT / "epub.css").exists():
        fail("obsolete epub.css remains in the active project root")


def check_pages_deployment() -> None:
    workflow = PAGES_WORKFLOW.read_text(encoding="utf-8")
    required_markers = {
        "HTML-only daily render": "quarto render --to html",
        "official Pages configuration": "actions/configure-pages@",
        "Pages artifact upload": "actions/upload-pages-artifact@",
        "Pages deployment": "actions/deploy-pages@",
        "rendered _book deployment source": "path: _book",
        "rendered HTML integrity check": "python3 scripts/check_rendered_html.py",
        "GitHub Pages environment": "name: github-pages",
        "main-only deployment guard": "github.ref == 'refs/heads/main'",
    }
    for label, marker in required_markers.items():
        if marker not in workflow:
            fail(f"{label} is missing from {PAGES_WORKFLOW.relative_to(ROOT)}")

    for output_format in ("pdf", "docx", "epub"):
        if re.search(rf"(?i)quarto\s+render[^\n]*--to\s+{output_format}\b", workflow):
            fail(f"daily Pages workflow unexpectedly renders {output_format}")


def check_publication_workflow() -> None:
    workflow = PUBLICATION_WORKFLOW.read_text(encoding="utf-8")
    required_markers = {
        "manual trigger": "workflow_dispatch:",
        "PDF render": "quarto render --to pdf",
        "DOCX render": "quarto render --to docx",
        "EPUB render": "quarto render --to epub",
        "publication artifact upload": "actions/upload-artifact@",
        "artifact directory": "build-artifacts",
    }
    for label, marker in required_markers.items():
        if marker not in workflow:
            fail(f"{label} is missing from {PUBLICATION_WORKFLOW.relative_to(ROOT)}")

    forbidden_markers = (
        "actions/deploy-pages@",
        "actions/create-release@",
        "softprops/action-gh-release",
        "gh release create",
    )
    for marker in forbidden_markers:
        if marker in workflow:
            fail(
                "manual publication-format build must not publish a release automatically: "
                f"{marker}"
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
    check_active_build_files()
    check_pages_deployment()
    check_publication_workflow()
    check_reader_support()
    files = check_sources()
    cited_count, bib_count = check_citations(files)

    print(
        "Quarto source check passed: "
        f"{len(files)} canonical QMD files, {cited_count} cited keys, "
        f"{bib_count} bibliography entries; HTML/PDF/DOCX/EPUB share one Quarto source, "
        "daily CI deploys only integrity-checked HTML to GitHub Pages, publication formats "
        "are build-only manual artifacts, and reader navigation/feedback remain configured."
    )


if __name__ == "__main__":
    main()
