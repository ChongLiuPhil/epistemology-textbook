#!/usr/bin/env python3
"""Conservative source checks for display-math layout hazards."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "index.qmd", *sorted((ROOT / "manuscript").glob("*.qmd"))]
DISPLAY = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)
ENVIRONMENTS = ("aligned", "split", "cases", "array", "gathered", "alignedat")


def balanced_braces(value: str) -> bool:
    depth = 0
    escaped = False
    for char in value:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def width_hint(value: str) -> int:
    value = re.sub(r"%.*", "", value)
    value = re.sub(r"\\[A-Za-z]+", "x", value)
    value = re.sub(r"[{}_^&]", "", value)
    return len(re.sub(r"\s+", " ", value).strip())


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in FILES:
        body = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if body.count("$") % 2:
            errors.append(f"{rel}: unmatched $ display-math delimiter")

        source_lines = body.splitlines()
        in_display = False
        for line_number, line in enumerate(source_lines, start=1):
            if line.strip() != "$":
                continue
            if not in_display:
                in_display = True
                if line_number < len(source_lines) and source_lines[line_number].strip() == "":
                    errors.append(
                        f"{rel}:{line_number}: blank line immediately after opening $ delimiter"
                    )
            else:
                if line_number > 1 and source_lines[line_number - 2].strip() == "":
                    errors.append(
                        f"{rel}:{line_number}: blank line immediately before closing $ delimiter"
                    )
                in_display = False

        for env in ENVIRONMENTS:
            begins = len(re.findall(rf"\\begin\{{{env}\}}", body))
            ends = len(re.findall(rf"\\end\{{{env}\}}", body))
            if begins != ends:
                errors.append(f"{rel}: unbalanced math environment {env}: {begins} begin / {ends} end")

        for number, match in enumerate(DISPLAY.finditer(body), start=1):
            block = match.group(1)
            if not balanced_braces(block):
                errors.append(f"{rel}: display equation #{number} has unbalanced braces")
            hint = width_hint(block)
            multiline = "\\\\" in block or any(f"\\begin{{{env}}}" in block for env in ENVIRONMENTS)
            if hint > 96 and not multiline:
                warnings.append(f"{rel}: display equation #{number} may be too wide (hint {hint})")

    for warning in warnings:
        print("WARNING:", warning)
    for error in errors:
        print("ERROR:", error, file=sys.stderr)

    print(f"Math layout source check: {len(FILES)} QMD files, {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
