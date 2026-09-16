#!/usr/bin/env python3
"""One-time repair for bare Pandoc citations touching CJK text.

Pandoc treats adjacent CJK letters as part of a bare citation key, so a source
fragment such as ``@goldman1976进入`` can render as a link to the nonexistent
key ``goldman1976进入``.  This script inserts visible word-boundary spaces only
around known bibliography keys when they directly touch CJK characters.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "references.bib"
CJK = r"\u3400-\u9fff"


def bibliography_keys() -> list[str]:
    text = BIB.read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", text))
    if not keys:
        raise SystemExit("No bibliography keys found")
    return sorted(keys, key=len, reverse=True)


def repair(text: str, keys: list[str]) -> tuple[str, int]:
    alternatives = "|".join(re.escape(key) for key in keys)
    # The ASCII-key boundary prevents a shorter bibliography key from matching
    # inside a longer citation token.
    left = re.compile(
        rf"(?<=[{CJK}])@({alternatives})(?![A-Za-z0-9_:.+-])"
    )
    right = re.compile(
        rf"@({alternatives})(?=[{CJK}])"
    )

    text, left_count = left.subn(r" @\1", text)
    text, right_count = right.subn(r"@\1 ", text)
    return text, left_count + right_count


def main() -> None:
    keys = bibliography_keys()
    files = [ROOT / "index.qmd", *sorted((ROOT / "manuscript").glob("*.qmd"))]
    total = 0

    for path in files:
        original = path.read_text(encoding="utf-8")
        updated, count = repair(original, keys)
        if count:
            path.write_text(updated, encoding="utf-8")
            total += count
            print(f"{path.relative_to(ROOT)}: repaired {count} citation boundary/boundaries")

    if total == 0:
        raise SystemExit("No citation boundaries required repair")

    print(f"Repaired {total} citation boundaries in canonical QMD sources")


if __name__ == "__main__":
    main()
