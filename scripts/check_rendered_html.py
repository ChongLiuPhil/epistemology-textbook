#!/usr/bin/env python3
"""Validate the fully rendered Quarto HTML site.

The source checks catch project-level mistakes before rendering.  This script
checks the reader-facing output itself: every local link/resource must resolve,
HTML fragments must point to a real anchor, no duplicate IDs may exist, and no
rendered reader link may still point to a canonical .qmd source file.
"""

from __future__ import annotations

import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "_book").resolve()
SITE_URL = "https://chongliuphil.github.io/epistemology-textbook/"
SITE_PARTS = urlsplit(SITE_URL)
SITE_PATH = SITE_PARTS.path.rstrip("/")
SITE_PREFIX = SITE_PATH + "/"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[tuple[str, str, str]] = []

    def _record(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        identifier = values.get("id")
        if identifier:
            self.ids.append(identifier)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((tag, attribute, value))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._record(tag, attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._record(tag, attrs)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def within_book(path: Path) -> bool:
    try:
        path.relative_to(BOOK)
    except ValueError:
        return False
    return True


def resolve_local(current: Path, raw_url: str) -> tuple[Path, str] | None:
    if raw_url.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None

    parsed = urlsplit(raw_url)

    if parsed.scheme in {"http", "https"}:
        if (parsed.scheme, parsed.netloc) != (SITE_PARTS.scheme, SITE_PARTS.netloc):
            return None
        path = unquote(parsed.path)
        if path == SITE_PATH:
            relative = ""
        elif path.startswith(SITE_PREFIX):
            relative = path[len(SITE_PREFIX) :]
        else:
            return None
        target = (BOOK / relative).resolve()
    elif parsed.scheme or parsed.netloc:
        return None
    else:
        path = unquote(parsed.path)
        if path == SITE_PATH:
            target = BOOK
        elif path.startswith(SITE_PREFIX):
            target = (BOOK / path[len(SITE_PREFIX) :]).resolve()
        elif path.startswith("/"):
            # A root-relative URL outside this GitHub Pages project is not a
            # file owned by the book and cannot be checked locally.
            return None
        elif path:
            target = (current.parent / path).resolve()
        else:
            target = current.resolve()

    if target.is_dir():
        target = (target / "index.html").resolve()

    return target, parsed.fragment


def main() -> None:
    if not BOOK.is_dir():
        fail("_book/ does not exist; render HTML before running this check")

    html_files = sorted(path.resolve() for path in BOOK.rglob("*.html"))
    if not html_files:
        fail("no rendered HTML files found under _book/")

    parsed_pages = {path: parse_page(path) for path in html_files}
    anchors = {path: set(page.ids) for path, page in parsed_pages.items()}
    errors: list[str] = []
    checked_references = 0

    for page_path, page in parsed_pages.items():
        page_name = page_path.relative_to(BOOK)

        for identifier, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f"{page_name}: duplicate HTML id #{identifier}")

        for tag, attribute, raw_url in page.references:
            resolved = resolve_local(page_path, raw_url)
            if resolved is None:
                continue

            target, fragment = resolved
            checked_references += 1

            if not within_book(target):
                errors.append(f"{page_name}: {attribute} escapes _book/: {raw_url}")
                continue

            if target.suffix.lower() == ".qmd":
                errors.append(
                    f"{page_name}: rendered reader link still points to QMD source: {raw_url}"
                )
                continue

            if not target.exists():
                errors.append(
                    f"{page_name}: missing local target for {tag}[{attribute}]: "
                    f"{raw_url} -> {target.relative_to(BOOK)}"
                )
                continue

            if fragment and target.suffix.lower() == ".html":
                target_anchors = anchors.get(target)
                if target_anchors is None:
                    target_anchors = set(parse_page(target).ids)
                if fragment not in target_anchors:
                    errors.append(
                        f"{page_name}: missing HTML fragment #{fragment} in "
                        f"{target.relative_to(BOOK)} (from {raw_url})"
                    )

    if errors:
        print("Rendered HTML integrity check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "Rendered HTML integrity check passed: "
        f"{len(html_files)} HTML pages, {checked_references} local references checked."
    )


if __name__ == "__main__":
    main()
