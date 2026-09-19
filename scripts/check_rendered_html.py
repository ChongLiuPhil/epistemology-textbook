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
SITE_URL = "https://epistemology-textbook.philosophy-research.workers.dev/"
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
        if SITE_PATH:
            if path == SITE_PATH:
                relative = ""
            elif path.startswith(SITE_PREFIX):
                relative = path[len(SITE_PREFIX) :]
            else:
                return None
        else:
            # The canonical workers.dev site is hosted at the domain root, so
            # every same-origin absolute path belongs to this rendered book.
            relative = path.lstrip("/")

        target = (BOOK / relative).resolve()
    elif parsed.scheme or parsed.netloc:
        return None
    else:
        path = unquote(parsed.path)

        # Fragment-only references such as "#section" always refer to the
        # current page. This check must happen before canonical-root mapping:
        # for a root-hosted site SITE_PATH is "", which otherwise makes an
        # empty path look like the site root/index page.
        if not path:
            target = current.resolve()
        elif SITE_PATH:
            if path == SITE_PATH:
                target = BOOK
            elif path.startswith(SITE_PREFIX):
                target = (BOOK / path[len(SITE_PREFIX) :]).resolve()
            elif path.startswith("/"):
                # A root-relative URL outside a subpath-hosted site is not a
                # file owned by this book.
                return None
            else:
                target = (current.parent / path).resolve()
        elif path.startswith("/"):
            # At a domain-root canonical site, root-relative URLs are book
            # paths and can be validated against the rendered artifact.
            target = (BOOK / path.lstrip("/")).resolve()
        else:
            target = (current.parent / path).resolve()

    if target.is_dir():
        target = (target / "index.html").resolve()

    return target, parsed.fragment


def main() -> None:
    if not BOOK.is_dir():
        fail("_book/ does not exist; render HTML before running this check")

    required_files = [
        "index.html",
        "manuscript/00-open-access-and-support.html",
        "manuscript/01-knowledge.html",
        "manuscript/05-social-knowledge.html",
        "manuscript/09-comparative.html",
        "manuscript/study-guide.html",
        "manuscript/research-studio.html",
        "manuscript/glossary.html",
        "manuscript/references.html",
    ]
    for relative in required_files:
        if not (BOOK / relative).is_file():
            fail(f"missing required rendered Web artifact: {relative}")

    required_text = {
        "index.html": ("本书目录", "当前阅读版本"),
        "manuscript/01-knowledge.html": (
            "本章目录",
            "github.com/ChongLiuPhil/epistemology-textbook",
        ),
        "manuscript/00-open-access-and-support.html": ("版本、引用与来源",),
    }
    for relative, markers in required_text.items():
        body = (BOOK / relative).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in body:
                fail(f"{relative} is missing required rendered marker: {marker}")

    legacy_url = "https://chongliuphil.github.io/epistemology-textbook/"
    for html_path in BOOK.rglob("*.html"):
        body = html_path.read_text(encoding="utf-8")
        if legacy_url in body:
            fail(
                f"{html_path.relative_to(BOOK)} still contains retired GitHub Pages canonical URL"
            )

    unexpected_extensions = {".epub", ".pdf", ".docx", ".tex"}
    unexpected = [
        path.relative_to(BOOK)
        for path in BOOK.rglob("*")
        if path.is_file() and path.suffix.lower() in unexpected_extensions
    ]
    if unexpected:
        fail(
            "unexpected publication-format artifact(s) in _book/: "
            + ", ".join(str(path) for path in unexpected)
        )

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
