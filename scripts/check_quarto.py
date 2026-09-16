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


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not CONFIG.exists():
        fail("missing _quarto.yml")
    if not BIB.exists():
        fail("missing references.bib")

    config = CONFIG.read_text(encoding="utf-8")
    forbidden = ["scripts/build_web.py", "website/generated/", "textbook/references.bib"]
    for marker in forbidden:
        if marker in config:
            fail(f"legacy build dependency remains in _quarto.yml: {marker}")
    if "epub:" not in config:
        fail("EPUB output is not configured")

    files = [ROOT / "index.qmd"] + [MANUSCRIPT / name for name in EXPECTED]
    for path in files:
        if not path.exists():
            fail(f"missing canonical Quarto source: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if "source-file:" in text or "本页由 LaTeX 主稿自动生成" in text:
            fail(f"legacy generated-source marker remains in {path.relative_to(ROOT)}")

    for name in EXPECTED:
        if f"manuscript/{name}" not in config:
            fail(f"_quarto.yml does not include manuscript/{name}")

    bib_text = BIB.read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib_text))
    if not bib_keys:
        fail("no bibliography entries found")

    cited: set[str] = set()
    citation_pattern = re.compile(r"(?<![\w@])@([A-Za-z][A-Za-z0-9_:.+-]*)")
    for path in files:
        cited.update(citation_pattern.findall(path.read_text(encoding="utf-8")))

    missing = sorted(cited - bib_keys)
    if missing:
        fail("citation keys missing from references.bib: " + ", ".join(missing))

    print(
        "Quarto source check passed: "
        f"{len(files)} source files, {len(cited)} cited keys, {len(bib_keys)} bibliography entries."
    )


if __name__ == "__main__":
    main()
