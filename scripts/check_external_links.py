#!/usr/bin/env python3
"""Audit external links in rendered HTML.

The default mode is informational. ``--strict`` exits non-zero only for links
that return a definite 404 or 410; authentication failures, rate limits,
server errors, TLS failures, and timeouts are reported as warnings because
those states are commonly transient or bot-specific.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html.parser
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "_book"
USER_AGENT = "epistemology-textbook-link-audit/1.0 (+https://chongliuphil.github.io/epistemology-textbook/)"
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data"}
DEFINITE_BROKEN = {404, 410}


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name not in {"href", "src"} or not value:
                continue
            value = value.strip()
            parsed = urllib.parse.urlsplit(value)
            if parsed.scheme in {"http", "https"}:
                # Fragments do not affect remote resource reachability.
                clean = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
                self.urls.add(clean)


@dataclass(frozen=True)
class Result:
    url: str
    status: str
    detail: str


def collect_urls(book_dir: Path) -> list[str]:
    urls: set[str] = set()
    for path in sorted(book_dir.rglob("*.html")):
        parser = LinkParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        urls.update(parser.urls)
    return sorted(urls)


def check_url(url: str, timeout: float) -> Result:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
            "Range": "bytes=0-0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if 200 <= status < 400:
                return Result(url, "ok", str(status))
            return Result(url, "warning", f"HTTP {status}")
    except urllib.error.HTTPError as exc:
        if exc.code in DEFINITE_BROKEN:
            return Result(url, "broken", f"HTTP {exc.code}")
        return Result(url, "warning", f"HTTP {exc.code}")
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        return Result(url, "warning", f"network error: {reason}")
    except Exception as exc:  # Keep the audit resilient to unusual TLS/redirect behavior.
        return Result(url, "warning", f"{type(exc).__name__}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-dir", type=Path, default=DEFAULT_BOOK)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    if not args.book_dir.exists():
        print(f"[external-links] ERROR: rendered book not found: {args.book_dir}", file=sys.stderr)
        return 2

    urls = collect_urls(args.book_dir)
    print(f"[external-links] checking {len(urls)} unique external URL(s)")
    if not urls:
        print("[external-links] no external links found")
        return 0

    results: list[Result] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(check_url, url, args.timeout): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: item.url)
    broken = [item for item in results if item.status == "broken"]
    warnings = [item for item in results if item.status == "warning"]
    ok = len(results) - len(broken) - len(warnings)

    for item in broken:
        print(f"[external-links] BROKEN {item.detail}: {item.url}")
    for item in warnings:
        print(f"[external-links] WARNING {item.detail}: {item.url}")

    print(
        f"[external-links] total={len(results)} ok={ok} "
        f"broken={len(broken)} warnings={len(warnings)}"
    )
    if args.strict and broken:
        print("[external-links] FAILED: definite broken links found", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
