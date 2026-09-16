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

EXPECTED = [
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
]

GENERATED_MARKERS = (
    "source-file:",
    "本页由 LaTeX 主稿自动生成",
    "AUTO-GENERATED FROM LATEX",
)

CROSSREF_PREFIXES = ("fig-", "tbl-", "eq-", "sec-", "lst-")


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
    if not re.search(r"(?m)^format:\s*$", config) or not re.search(
        r"(?m)^\s{2}html:\s*$", config
    ):
        fail("HTML output is not configured in _quarto.yml")

    for output_format in ("epub", "pdf", "docx"):
        if re.search(rf"(?mi)^\s{{2}}{output_format}:\s*$", config):
            fail(f"release format is configured during Web Edition Development: {output_format}")

    if re.search(r"(?mi)^\s*downloads:\s*", config):
        fail("downloads configuration is not allowed during Web Edition Development")

    if "bibliography: references.bib" not in config:
        fail("_quarto.yml must use the root references.bib bibliography")
    if "lang: zh-CN" not in config:
        fail("_quarto.yml must keep the Chinese language setting (zh-CN)")

    canonical_paths = ["index.qmd"] + [f"manuscript/{name}" for name in EXPECTED]
    for rel_path in canonical_paths:
        if rel_path not in config:
            fail(f"_quarto.yml does not include canonical source: {rel_path}")


def check_active_build_files() -> None:
    build_files = [CONFIG, MAKEFILE, *sorted(WORKFLOWS.glob("*.yml")), *sorted(WORKFLOWS.glob("*.yaml"))]
    legacy_patterns = {
        "old QMD generator": r"scripts/build_web\.py|website/generated/",
        "legacy LaTeX toolchain": r"(?i)latexmk|xelatex|pdflatex|textbook/[^\s]+\.tex",
    }
    release_command_pattern = re.compile(
        r"(?i)(quarto\s+(?:render|publish)[^\n]*(?:epub|pdf|docx)|make\s+(?:epub|pdf|docx)|gh-pages|actions/deploy-pages|quarto-actions/publish)"
    )

    for path in build_files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in legacy_patterns.items():
            if re.search(pattern, text):
                fail(f"{label} dependency remains in {path.relative_to(ROOT)}")
        if release_command_pattern.search(text):
            fail(f"release/deployment command remains in active build file: {path.relative_to(ROOT)}")

    makefile = MAKEFILE.read_text(encoding="utf-8")
    for target in ("epub", "pdf", "docx"):
        if re.search(rf"(?m)^{target}\s*:", makefile):
            fail(f"daily release target remains in Makefile: {target}")

    if (ROOT / "epub.css").exists():
        fail("obsolete epub.css remains in the active project root")


def check_sources() -> list[Path]:
    files = [ROOT / "index.qmd"] + [MANUSCRIPT / name for name in EXPECTED]
    for path in files:
        if not path.exists():
            fail(f"missing canonical Quarto source: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for marker in GENERATED_MARKERS:
            if marker in text:
                fail(f"legacy generated-source marker remains in {path.relative_to(ROOT)}: {marker}")
    return files


def check_citations(files: list[Path]) -> tuple[int, int]:
    bib_text = BIB.read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib_text))
    if not bib_keys:
        fail("no bibliography entries found")

    cited: set[str] = set()
    citation_pattern = re.compile(r"(?<![\w@])@([A-Za-z][A-Za-z0-9_:.+-]*)")
    for path in files:
        for key in citation_pattern.findall(path.read_text(encoding="utf-8")):
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
    files = check_sources()
    cited_count, bib_count = check_citations(files)

    print(
        "Quarto source check passed: "
        f"{len(files)} canonical QMD files, {cited_count} cited keys, "
        f"{bib_count} bibliography entries; active output is HTML only."
    )


if __name__ == "__main__":
    main()
