#!/usr/bin/env python3
r"""Generate Quarto reading pages from the canonical LaTeX textbook sources.

The LaTeX manuscript remains the source of truth. This script expands the
existing ``\input``/``\include`` graph and translates the small set of
book-specific LaTeX conventions into Quarto Markdown.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXTBOOK = ROOT / "textbook"
OUT = ROOT / "website" / "generated"

PARTS = [
    (
        "第一部　知识、怀疑与理由",
        [
            ("01-knowledge", "chapters/revised/01-knowledge.tex"),
            ("02-skepticism-luck", "chapters/revised/02-skepticism-luck.tex"),
            ("03-justification-context", "chapters/revised/03-justification-context.tex"),
        ],
    ),
    (
        "第二部　认识来源、社会系统与理性模型",
        [
            ("04-sources", "chapters/revised/04-sources.tex"),
            ("05-social-knowledge", "chapters/revised/05-social-knowledge.tex"),
            ("06-formal", "chapters/revised/06-formal.tex"),
        ],
    ),
    (
        "第三部　认识价值、技术环境与比较方法",
        [
            ("07-value", "chapters/revised/07-value.tex"),
            ("08-digital-ai", "chapters/revised/08-digital-ai.tex"),
            ("09-comparative", "chapters/revised/09-comparative.tex"),
        ],
    ),
]

BACKMATTER = [
    ("study-guide", "backmatter/study-guide.tex"),
    ("research-studio", "backmatter/research-studio.tex"),
    ("exercise-hints", "backmatter/exercise-hints.tex"),
    ("glossary", "backmatter/glossary.tex"),
]

CALL_OUTS = {
    "openingcase": ("tip", "开篇案例"),
    "argumentbox": ("note", "论证重构"),
    "comparison": ("important", "比较视角"),
    "checkpoint": ("note", "自测小结"),
    "exercises": ("warning", "章末练习"),
    "readingmap": ("tip", "分层阅读地图"),
}

INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        cut = None
        for i, ch in enumerate(line):
            if ch != "%":
                continue
            backslashes = 0
            j = i - 1
            while j >= 0 and line[j] == "\\":
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                cut = i
                break
        if cut is not None:
            line = line[:cut]
        lines.append(line.rstrip())
    return "\n".join(lines)


def resolve_tex(current: Path, target: str) -> Path:
    raw = Path(target)
    candidates = []
    if raw.suffix:
        candidates.extend([TEXTBOOK / raw, current.parent / raw])
    else:
        candidates.extend(
            [
                TEXTBOOK / f"{target}.tex",
                current.parent / f"{target}.tex",
                TEXTBOOK / target,
                current.parent / target,
            ]
        )
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(f"Cannot resolve LaTeX include {target!r} from {current}")


def expand_tex(path: Path, stack: tuple[Path, ...] = ()) -> str:
    path = path.resolve()
    if path in stack:
        chain = " -> ".join(str(p.relative_to(ROOT)) for p in (*stack, path))
        raise RuntimeError(f"Circular LaTeX include: {chain}")
    text = strip_comments(path.read_text(encoding="utf-8"))

    def replace(match: re.Match[str]) -> str:
        child = resolve_tex(path, match.group(1))
        return "\n" + expand_tex(child, (*stack, path)) + "\n"

    previous = None
    while previous != text:
        previous = text
        text = INPUT_RE.sub(replace, text)
    return text


def parse_balanced(
    text: str, start: int, open_char: str = "{", close_char: str = "}"
) -> tuple[str, int] | None:
    if start >= len(text) or text[start] != open_char:
        return None
    depth = 0
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
    return None


def replace_command(text: str, name: str, nargs: int, render) -> str:
    needle = "\\" + name
    pos = 0
    while True:
        idx = text.find(needle, pos)
        if idx < 0:
            break
        after = idx + len(needle)
        if after < len(text) and text[after].isalpha():
            pos = after
            continue
        cursor = after
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        args: list[str] = []
        ok = True
        for _ in range(nargs):
            if cursor >= len(text) or text[cursor] != "{":
                ok = False
                break
            parsed = parse_balanced(text, cursor)
            if parsed is None:
                ok = False
                break
            arg, cursor = parsed
            args.append(arg)
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
        if not ok:
            pos = after
            continue
        replacement = render(*args)
        text = text[:idx] + replacement + text[cursor:]
        pos = idx + len(replacement)
    return text


def convert_citations(text: str) -> str:
    def keys(raw: str) -> str:
        return "; ".join("@" + key.strip() for key in raw.split(",") if key.strip())

    def paren(match: re.Match[str]) -> str:
        note = match.group(1)
        body = keys(match.group(2))
        if note:
            body += ", " + note.strip()
        return f"[{body}]"

    def narrative(match: re.Match[str]) -> str:
        note = match.group(1)
        raw_keys = [k.strip() for k in match.group(2).split(",") if k.strip()]
        if len(raw_keys) == 1:
            return "@" + raw_keys[0] + (f" [{note.strip()}]" if note else "")
        body = "; ".join("@" + k for k in raw_keys)
        return f"[{body}]" + (f" ({note.strip()})" if note else "")

    text = re.sub(
        r"\\(?:parencite|autocite|citep)(?:\[([^\]]+)\])?\{([^}]+)\}", paren, text
    )
    text = re.sub(
        r"\\(?:textcite|citet)(?:\[([^\]]+)\])?\{([^}]+)\}", narrative, text
    )
    text = re.sub(r"\\cite(?:\[([^\]]+)\])?\{([^}]+)\}", paren, text)
    return text


def inline_markup(text: str) -> str:
    text = replace_command(
        text,
        "term",
        2,
        lambda zh, en: f"**{inline_markup(zh)}**（*{inline_markup(en)}*）",
    )
    text = replace_command(
        text,
        "readingstrand",
        3,
        lambda title, desc, refs: (
            f"\n\n**{inline_markup(title)}：** {inline_markup(desc)} "
            f"\\parencite{{{refs}}}\n\n"
        ),
    )
    text = replace_command(
        text,
        "chaptergoals",
        1,
        lambda body: (
            "\n\n::: {.callout-note title=\"学习目标\"}\n"
            + inline_markup(body)
            + "\n:::\n\n"
        ),
    )
    text = replace_command(
        text,
        "minitopic",
        1,
        lambda title: f"\n\n### {inline_markup(title)}\n\n",
    )
    text = replace_command(
        text,
        "keyreading",
        1,
        lambda body: f"\n\n**核心阅读：** {inline_markup(body)}\n\n",
    )
    text = replace_command(
        text,
        "furtherreading",
        1,
        lambda body: f"\n\n**延伸阅读：** {inline_markup(body)}\n\n",
    )

    text = replace_command(text, "textbf", 1, lambda body: f"**{inline_markup(body)}**")
    text = replace_command(text, "textit", 1, lambda body: f"*{inline_markup(body)}*")
    text = replace_command(text, "emph", 1, lambda body: f"*{inline_markup(body)}*")
    text = replace_command(text, "texttt", 1, lambda body: f"`{body}`")
    text = replace_command(text, "enquote", 1, lambda body: f"“{inline_markup(body)}”")
    text = replace_command(text, "mbox", 1, lambda body: inline_markup(body))
    text = replace_command(text, "footnote", 1, lambda body: f"^[{inline_markup(body)}]")
    text = replace_command(
        text, "href", 2, lambda url, label: f"[{inline_markup(label)}]({url})"
    )
    text = replace_command(text, "url", 1, lambda url: f"<{url}>")
    text = replace_command(text, "label", 1, lambda _body: "")
    text = replace_command(text, "index", 1, lambda _body: "")
    text = replace_command(text, "addcontentsline", 3, lambda *_args: "")
    text = replace_command(text, "setcounter", 2, lambda *_args: "")
    text = replace_command(text, "vspace", 1, lambda *_args: "")
    text = replace_command(text, "hspace", 1, lambda *_args: "")

    text = convert_citations(text)

    text = re.sub(
        r"\\(?:noindent|ignorespaces|smallskip|medskip|bigskip|clearpage|newpage|phantomsection|centering|raggedright)\b",
        "",
        text,
    )
    text = re.sub(r"\\thispagestyle\{[^}]*\}", "", text)
    text = text.replace(r"\%", "%").replace(r"\&", "&").replace(r"\_", "_")
    text = text.replace(r"\#", "#").replace(r"\$", "$")
    text = text.replace(r"\ldots", "…").replace(r"\dots", "…")
    text = text.replace(r"\LaTeX", "LaTeX").replace(r"\XeLaTeX", "XeLaTeX")
    text = text.replace("~", " ")
    return text


def convert_tables(text: str) -> str:
    patterns = [
        re.compile(
            r"\\begin\{tabularx\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}(.*?)\\end\{tabularx\}",
            re.S,
        ),
        re.compile(
            r"\\begin\{longtable\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}(.*?)\\end\{longtable\}",
            re.S,
        ),
        re.compile(
            r"\\begin\{tabular\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}(.*?)\\end\{tabular\}",
            re.S,
        ),
    ]

    def clean_cell(cell: str) -> str:
        cell = re.sub(
            r"\\multicolumn\{\d+\}\{[^}]*\}\{(.*)\}\s*$", r"\1", cell.strip(), flags=re.S
        )
        cell = re.sub(
            r"\\(?:toprule|midrule|bottomrule|hline|endhead|endfirsthead|endfoot|endlastfoot)\b",
            "",
            cell,
        )
        cell = inline_markup(cell)
        cell = re.sub(r"\s+", " ", cell).strip()
        cell = cell.replace("|", r"\|")
        return cell

    def replace(match: re.Match[str]) -> str:
        body = match.group(1)
        body = re.sub(
            r"\\(?:toprule|midrule|bottomrule|hline|endhead|endfirsthead|endfoot|endlastfoot)\b",
            "",
            body,
        )
        raw_rows = re.split(r"\\\\(?:\[[^\]]*\])?", body)
        rows: list[list[str]] = []
        for raw in raw_rows:
            raw = raw.strip()
            if not raw:
                continue
            cells = [clean_cell(c) for c in re.split(r"(?<!\\)&", raw)]
            if any(cells):
                rows.append(cells)
        if not rows:
            return ""
        width = max(len(row) for row in rows)
        normalized = [row + [""] * (width - len(row)) for row in rows]
        header = normalized[0]
        lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join("---" for _ in range(width)) + " |",
        ]
        for row in normalized[1:]:
            lines.append("| " + " | ".join(row) + " |")
        return "\n\n" + "\n".join(lines) + "\n\n"

    for pattern in patterns:
        previous = None
        while previous != text:
            previous = text
            text = pattern.sub(replace, text)
    return text


def convert_environments(text: str) -> str:
    text = convert_tables(text)

    for env, (kind, title) in CALL_OUTS.items():
        if env == "argumentbox":
            text = re.sub(
                r"\\begin\{argumentbox\}(?:\[([^\]]*)\])?",
                lambda m: (
                    f'\n\n::: {{.callout-{kind} title="{title}'
                    + (f" {m.group(1).strip()}" if m.group(1) else "")
                    + '"}\n'
                ),
                text,
            )
        else:
            text = text.replace(
                f"\\begin{{{env}}}",
                f'\n\n::: {{.callout-{kind} title="{title}"}}\n',
            )
        text = text.replace(f"\\end{{{env}}}", "\n:::\n\n")

    def tcolor_open(match: re.Match[str]) -> str:
        options = match.group(1)
        title_match = re.search(r"title=\{([^{}]+)\}", options)
        title = title_match.group(1) if title_match else "补充说明"
        return f'\n\n::: {{.callout-note title="{title}"}}\n'

    text = re.sub(r"\\begin\{tcolorbox\}\[([^\]]*)\]", tcolor_open, text)
    text = text.replace(r"\end{tcolorbox}", "\n:::\n\n")

    text = re.sub(r"\\begin\{enumerate\}(?:\[[^\]]*\])?", "\n", text)
    text = text.replace(r"\end{enumerate}", "\n")
    text = re.sub(r"\\begin\{itemize\}(?:\[[^\]]*\])?", "\n", text)
    text = text.replace(r"\end{itemize}", "\n")
    text = text.replace(r"\begin{description}", "\n").replace(r"\end{description}", "\n")
    text = re.sub(r"(?m)^\s*\\item\[([^\]]+)\]\s*", r"\n- **\1：** ", text)
    text = re.sub(r"(?m)^\s*\\item\s*", "\n1. ", text)

    text = text.replace(r"\[", "\n\n$$\n").replace(r"\]", "\n$$\n\n")
    text = re.sub(r"\\begin\{equation\*?\}", "\n\n$$\n", text)
    text = re.sub(r"\\end\{equation\*?\}", "\n$$\n\n", text)
    text = re.sub(r"\\begin\{displaymath\}", "\n\n$$\n", text)
    text = re.sub(r"\\end\{displaymath\}", "\n$$\n\n", text)
    text = re.sub(
        r"\\begin\{align\*?\}", lambda _m: "\n\n$$\n\\begin{aligned}\n", text
    )
    text = re.sub(
        r"\\end\{align\*?\}", lambda _m: "\n\\end{aligned}\n$$\n\n", text
    )

    for env in ["center", "flushleft", "flushright", "samepage"]:
        text = text.replace(f"\\begin{{{env}}}", "\n").replace(f"\\end{{{env}}}", "\n")

    return text


def convert_headings(text: str) -> str:
    def heading(level: int):
        marks = "#" * level

        def render(match: re.Match[str]) -> str:
            star = match.group(1)
            title = inline_markup(match.group(2))
            suffix = " {.unnumbered}" if star else ""
            return f"{marks} {title}{suffix}\n"

        return render

    text = re.sub(r"\\chapter(\*)?\{([^{}]+)\}", heading(1), text)
    text = re.sub(r"\\section(\*)?\{([^{}]+)\}", heading(2), text)
    text = re.sub(r"\\subsection(\*)?\{([^{}]+)\}", heading(3), text)
    text = re.sub(r"\\subsubsection(\*)?\{([^{}]+)\}", heading(4), text)
    return text


def cleanup(text: str) -> str:
    text = inline_markup(text)
    text = re.sub(r"\\\\(?:\[[^\]]*\])?", "  \n", text)
    text = re.sub(
        r"\\(?:frontmatter|mainmatter|backmatter|maketitle|tableofcontents|printindex)\b",
        "",
        text,
    )
    text = re.sub(r"\\printbibliography(?:\[[^\]]*\])?", "", text)
    text = re.sub(
        r"\\(?:small|footnotesize|normalsize|large|Large|LARGE|huge|Huge)\b", "", text
    )
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def latex_to_qmd(text: str) -> str:
    text = convert_environments(text)
    text = convert_headings(text)
    text = cleanup(text)
    return text


def page_header(source: str, numbered: bool = True) -> str:
    return (
        "---\n"
        f"number-sections: {'true' if numbered else 'false'}\n"
        f"source-file: {source}\n"
        "---\n\n"
        '<div class="source-note">本页由 LaTeX 主稿自动生成；请勿直接编辑生成文件。</div>\n\n'
    )


def write_page(slug: str, source: str, numbered: bool = True) -> Path:
    source_path = TEXTBOOK / source
    expanded = expand_tex(source_path)
    qmd = latex_to_qmd(expanded)
    target = OUT / f"{slug}.qmd"
    target.write_text(page_header(f"textbook/{source}", numbered=numbered) + qmd, encoding="utf-8")
    return target


def ensure_first_heading(path: Path) -> None:
    body = path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^#\s+\S", body):
        raise RuntimeError(f"Generated page has no level-1 heading: {path.relative_to(ROOT)}")


def validate_generated(paths: list[Path]) -> None:
    for path in paths:
        ensure_first_heading(path)
        body = path.read_text(encoding="utf-8")
        if r"\input{" in body or r"\include{" in body:
            raise RuntimeError(f"Unexpanded include remains in {path.relative_to(ROOT)}")
        leftovers = [
            r"\chaptergoals",
            r"\minitopic",
            r"\readingstrand",
            r"\begin{openingcase}",
            r"\begin{argumentbox}",
            r"\begin{comparison}",
            r"\begin{checkpoint}",
            r"\begin{exercises}",
            r"\begin{readingmap}",
            r"\begin{tcolorbox}",
            r"\begin{tabular",
            r"\begin{longtable",
            r"\item",
        ]
        found = [token for token in leftovers if token in body]
        if found:
            raise RuntimeError(
                f"Unsupported LaTeX remains in {path.relative_to(ROOT)}: {', '.join(found)}"
            )
        if "::: {.callout-" in body and body.count("::: {.callout-") > body.count("\n:::\n"):
            raise RuntimeError(f"Unclosed callout in {path.relative_to(ROOT)}")


def build() -> list[Path]:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    generated: list[Path] = []
    generated.append(write_page("00-preface", "frontmatter.tex", numbered=False))
    for _part, chapters in PARTS:
        for slug, source in chapters:
            generated.append(write_page(slug, source))
    for slug, source in BACKMATTER:
        generated.append(write_page(slug, source, numbered=False))

    references = OUT / "references.qmd"
    references.write_text(
        "---\nnumber-sections: false\nsource-file: textbook/references.bib\n---\n\n"
        "# 参考文献 {.unnumbered}\n\n"
        "以下条目由全书引文自动汇总。\n\n"
        "::: {#refs}\n:::\n",
        encoding="utf-8",
    )
    generated.append(references)
    validate_generated(generated)
    return generated


def check_sources() -> None:
    required = [TEXTBOOK / "frontmatter.tex", TEXTBOOK / "references.bib"]
    for _part, chapters in PARTS:
        required.extend(TEXTBOOK / source for _slug, source in chapters)
    required.extend(TEXTBOOK / source for _slug, source in BACKMATTER)
    missing = [p for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing web source(s): "
            + ", ".join(str(p.relative_to(ROOT)) for p in missing)
        )

    pages = build()
    print(f"Generated {len(pages)} Quarto pages under {OUT.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="generate and validate pages; retained for CI/readability",
    )
    parser.parse_args()
    check_sources()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
