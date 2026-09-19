#!/usr/bin/env python3
"""Read-only runtime verification for published Web artifacts."""

from __future__ import annotations

import argparse
import html.parser
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "epistemology-textbook-runtime-check/1.0 (+GitHub Actions)"
TIMEOUT = 25
RETRIES = 3

REQUIRED_PAGES = {
    "/": ("本书目录", "当前阅读版本"),
    "/manuscript/00-open-access-and-support.html": ("版本、引用与来源",),
    "/manuscript/01-knowledge.html": (
        "本章目录",
        "github.com/ChongLiuPhil/epistemology-textbook",
    ),
    "/manuscript/05-social-knowledge.html": (),
    "/manuscript/references.html": (),
}


class LocalAssetParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        for key in ("href", "src"):
            value = attr_map.get(key)
            if value:
                self.refs.add(value)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def fetch(url: str, *, max_bytes: int | None = None) -> tuple[int, bytes, str]:
    last_error: Exception | None = None
    for attempt in range(1, RETRIES + 1):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                },
            )
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                status = getattr(response, "status", 200)
                body = response.read(max_bytes) if max_bytes else response.read()
                return status, body, response.geturl()
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < RETRIES:
                time.sleep(attempt * 2)
    raise RuntimeError(f"failed after {RETRIES} attempts: {last_error}")


def verify_site(base_url: str, *, expect_root_marker: str | None = None) -> None:
    base = base_url.rstrip("/") + "/"
    print(f"Verifying {base}")

    fetched_html: dict[str, str] = {}

    for path, markers in REQUIRED_PAGES.items():
        url = urllib.parse.urljoin(base, path.lstrip("/"))
        try:
            status, body, final_url = fetch(url)
        except RuntimeError as exc:
            fail(f"{url}: {exc}")

        if status != 200:
            fail(f"{url}: expected HTTP 200, got {status}")

        text = body.decode("utf-8", errors="replace")
        fetched_html[path] = text

        if path == "/" and expect_root_marker and expect_root_marker not in text:
            fail(f"{url}: missing expected root marker {expect_root_marker!r}")

        for marker in markers:
            if marker not in text:
                fail(f"{url}: missing expected marker {marker!r}")

        print(f"PASS page {path} -> {status} ({final_url})")

    parser = LocalAssetParser()
    parser.feed(fetched_html["/"])
    parser.feed(fetched_html["/manuscript/01-knowledge.html"])

    asset_refs: list[str] = []
    for ref in sorted(parser.refs):
        parsed = urllib.parse.urlparse(ref)
        if parsed.scheme or parsed.netloc:
            continue
        clean = ref.split("#", 1)[0].split("?", 1)[0]
        if not clean:
            continue
        if (
            clean.endswith((".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".woff", ".woff2"))
            or "site_libs/" in clean
        ):
            asset_refs.append(ref)

    if not asset_refs:
        fail(f"{base}: no local CSS/JS/image/font assets discovered")

    for ref in asset_refs[:30]:
        url = urllib.parse.urljoin(base, ref)
        try:
            status, _, final_url = fetch(url, max_bytes=4096)
        except RuntimeError as exc:
            fail(f"asset {url}: {exc}")
        if status != 200:
            fail(f"asset {url}: expected HTTP 200, got {status}")
        print(f"PASS asset {ref} -> {status} ({final_url})")

    print(
        f"Runtime verification passed for {base}: "
        f"{len(REQUIRED_PAGES)} required pages and "
        f"{min(len(asset_refs), 30)} local assets checked."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expect-root-marker",
        default=None,
        help="Require this marker in the root HTML response.",
    )
    parser.add_argument("base_urls", nargs="+")
    args = parser.parse_args()

    for base_url in args.base_urls:
        verify_site(base_url, expect_root_marker=args.expect_root_marker)


if __name__ == "__main__":
    main()
