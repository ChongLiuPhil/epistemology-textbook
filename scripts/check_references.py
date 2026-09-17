#!/usr/bin/env python3
"""Validate bibliography metadata and citation coverage without network access."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references.bib"
SOURCE_PATHS = [ROOT / "index.qmd", *sorted((ROOT / "manuscript").glob("*.qmd"))]

ENTRY_START_RE = re.compile(r"@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
CITATION_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9_][A-Za-z0-9_:.+\-/]*)(?![\w])")
CROSSREF_PREFIXES = ("fig-", "tbl-", "eq-", "sec-", "lst-")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)


def fail(message: str) -> None:
    print(f"[references] ERROR: {message}", file=sys.stderr)


def split_entries(text: str) -> list[tuple[str, str, str]]:
    """Return (entry_type, key, entry_body) for brace-delimited BibTeX entries."""
    entries: list[tuple[str, str, str]] = []
    pos = 0
    while True:
        match = ENTRY_START_RE.search(text, pos)
        if not match:
            break
        entry_type, key = match.group(1).lower(), match.group(2)
        open_brace = text.find("{", match.start())
        depth = 0
        quoted = False
        escaped = False
        end = None
        for index in range(open_brace, len(text)):
            char = text[index]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                quoted = not quoted
                continue
            if quoted:
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            raise ValueError(f"unclosed BibTeX entry: {key}")
        entries.append((entry_type, key, text[match.end() : end - 1]))
        pos = end
    return entries


def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    pos = 0
    length = len(body)
    while pos < length:
        while pos < length and (body[pos].isspace() or body[pos] == ","):
            pos += 1
        name_match = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", body[pos:])
        if not name_match:
            next_comma = body.find(",", pos)
            if next_comma == -1:
                break
            pos = next_comma + 1
            continue
        name = name_match.group(1).lower()
        pos += name_match.end()
        if pos >= length:
            fields[name] = ""
            break

        if body[pos] == "{":
            depth = 1
            start = pos + 1
            pos += 1
            escaped = False
            while pos < length and depth:
                char = body[pos]
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                pos += 1
            value = body[start : pos - 1] if depth == 0 else body[start:]
        elif body[pos] == '"':
            start = pos + 1
            pos += 1
            escaped = False
            while pos < length:
                char = body[pos]
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    break
                pos += 1
            value = body[start:pos]
            pos += 1
        else:
            start = pos
            while pos < length and body[pos] != ",":
                pos += 1
            value = body[start:pos].strip()
        fields[name] = value.strip()
    return fields


def normalize_doi(value: str) -> str:
    doi = value.strip()
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    return doi.strip().lower()


def collect_citations() -> set[str]:
    citations: set[str] = set()
    for path in SOURCE_PATHS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for key in CITATION_RE.findall(text):
            if not key.startswith(CROSSREF_PREFIXES):
                citations.add(key)
    return citations


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    text = BIB_PATH.read_text(encoding="utf-8")
    try:
        entries = split_entries(text)
    except ValueError as exc:
        fail(str(exc))
        return 1

    if not entries:
        fail("references.bib contains no BibTeX entries")
        return 1

    by_key: dict[str, tuple[str, dict[str, str]]] = {}
    duplicate_keys: set[str] = set()
    doi_to_keys: defaultdict[str, list[str]] = defaultdict(list)
    url_to_keys: defaultdict[str, list[str]] = defaultdict(list)
    doi_count = 0
    url_count = 0

    for entry_type, key, body in entries:
        fields = parse_fields(body)
        if key in by_key:
            duplicate_keys.add(key)
        by_key[key] = (entry_type, fields)

        if not fields.get("title"):
            errors.append(f"{key}: missing title")
        if not (fields.get("year") or fields.get("date")):
            warnings.append(f"{key}: missing year/date")

        raw_doi = fields.get("doi")
        if raw_doi:
            doi_count += 1
            normalized = normalize_doi(raw_doi)
            if any(ch.isspace() for ch in normalized) or not DOI_RE.fullmatch(normalized):
                errors.append(f"{key}: malformed DOI {raw_doi!r}")
            else:
                doi_to_keys[normalized].append(key)

        raw_url = fields.get("url")
        if raw_url:
            url_count += 1
            if any(ch.isspace() for ch in raw_url):
                errors.append(f"{key}: URL contains whitespace: {raw_url!r}")
            else:
                parsed = urlsplit(raw_url)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    errors.append(f"{key}: malformed URL {raw_url!r}")
                else:
                    url_to_keys[raw_url].append(key)

    for key in sorted(duplicate_keys):
        errors.append(f"duplicate bibliography key: {key}")
    for doi, keys in sorted(doi_to_keys.items()):
        if len(keys) > 1:
            errors.append(f"duplicate DOI {doi}: {', '.join(sorted(keys))}")
    for url, keys in sorted(url_to_keys.items()):
        if len(keys) > 1:
            warnings.append(f"shared URL across entries {', '.join(sorted(keys))}: {url}")

    citations = collect_citations()
    bib_keys = set(by_key)
    missing = sorted(citations - bib_keys)
    uncited = sorted(bib_keys - citations)
    if missing:
        errors.append("citation keys missing from references.bib: " + ", ".join(missing))

    if uncited:
        warnings.append(
            f"{len(uncited)} bibliography entries are currently uncited (kept as audit information): "
            + ", ".join(uncited)
        )

    for warning in warnings:
        print(f"[references] WARNING: {warning}")
    for error in errors:
        fail(error)

    print(
        "[references] "
        f"entries={len(entries)} cited_keys={len(citations)} uncited={len(uncited)} "
        f"doi_fields={doi_count} url_fields={url_count}"
    )
    if errors:
        print(f"[references] FAILED with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("[references] bibliography metadata checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
