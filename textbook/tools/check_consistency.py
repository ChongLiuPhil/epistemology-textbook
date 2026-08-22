#!/usr/bin/env python3
"""《我们如何知道？》源稿一致性校验。

不依赖 LaTeX 构建，直接检查源码树：

1. 章文件 \\input 图谱完整（所有被引用的 .tex 都存在）。
2. 章末练习与 backmatter/exercise-hints.tex 的提示逐章配对。
3. 正文引用键与 references.bib 双向对账：
   - 引用了但 bib 中不存在的键（会导致编译失败）；
   - bib 中存在但从未被引用的闲置条目。
4. 统计指标快照（大节数、术语表条目、索引标记），便于对照 README 记录。

用法：在 textbook/ 目录下运行 `python3 tools/check_consistency.py .`
全部通过时退出码为 0，否则为 1。
"""

import pathlib
import re
import sys

INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
EXERCISES_RE = re.compile(r"\\begin\{exercises\}(.*?)\\end\{exercises\}", re.S)
ITEM_RE = re.compile(r"^\s*\\item\b", re.M)
SECTION_STAR_RE = re.compile(r"\\section\*\{第(.+?)章\}")
INDEX_MARK = re.compile(r"\\(?:term|index)\{")


def strip_comments(text: str) -> str:
    """去掉 % 注释（忽略转义的 \\%）。"""
    return re.sub(r"(?<!\\)%.*", "", text)


def collect_cite_keys(text: str) -> set:
    """扫描所有 *cite* 命令，正确处理可选参数与多键多花括号（\\cites）。

    另识别 style.tex 自定义宏 \\readingstrand{层}{说明}{键列表}——
    分层阅读地图中的文献键经该宏的第三个花括号组传入 \\parencite。
    """
    keys = set()
    for m in re.finditer(r"\\[A-Za-z]+cite[A-Za-z]*\*?", text):
        rest = text[m.end():]
        pos = 0
        while pos < len(rest):
            ch = rest[pos]
            if ch == "[":
                end = rest.find("]", pos)
            elif ch == "(":
                end = rest.find(")", pos)
            elif ch == "{":
                end = rest.find("}", pos)
                if end != -1:
                    for key in rest[pos + 1:end].split(","):
                        key = key.strip()
                        if re.fullmatch(r"[A-Za-z0-9:_./+-]+", key):
                            keys.add(key)
            else:
                break
            if ch not in "[({":
                break
            if end == -1:
                break
            pos = end + 1
    for m in re.finditer(
            r"\\readingstrand\{[^}]*\}\{[^}]*\}\{([^}]*)\}", text):
        for key in m.group(1).split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


def read(p: pathlib.Path) -> str:
    return strip_comments(p.read_text(encoding="utf-8"))


def main(root: pathlib.Path) -> int:
    problems = []

    chapters_dir = root / "chapters" / "revised"
    chapter_files = sorted(chapters_dir.glob("*.tex"))

    # ---- 1. include 图谱 -------------------------------------------------
    known_inputs = set()
    for cf in chapter_files:
        for target in INPUT_RE.findall(read(cf)):
            path = (root / target).with_suffix(".tex")
            known_inputs.add(path)
            if not path.exists():
                problems.append(f"[include] {cf.name} 引用了不存在的 {target}")

    # ---- 2. 练习与提示配对 ----------------------------------------------
    ex_counts = {}
    for cf in chapter_files:
        text = read(cf)
        n = sum(len(ITEM_RE.findall(m)) for m in EXERCISES_RE.findall(text))
        ex_counts[cf] = n

    hints_file = root / "backmatter" / "exercise-hints.tex"
    hint_text = read(hints_file)
    parts = SECTION_STAR_RE.split(hint_text)
    # parts 形如 [前言, '一', 内容, '二', 内容, ...]
    hint_counts = {}
    for i in range(1, len(parts), 2):
        label, body = parts[i], parts[i + 1]
        hint_counts[label.strip()] = len(ITEM_RE.findall(body))

    cn_num = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
              "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    rev_num = {v: k for k, v in cn_num.items()}
    total_ex = total_hint = 0
    for idx, cf in enumerate(chapter_files, start=1):
        n_ex = ex_counts.get(cf, 0)
        total_ex += n_ex
        label = rev_num.get(idx, str(idx))
        n_hint = hint_counts.get(label, 0)
        total_hint += n_hint
        if n_ex != n_hint:
            problems.append(
                f"[配对] 第{idx}章（{cf.name}）：练习 {n_ex} 条 vs 提示 {n_hint} 条"
            )
    print(f"练习合计 {total_ex} 条，提示合计 {total_hint} 条")

    # ---- 3. 文献双向对账 --------------------------------------------------
    bib_keys = set()
    bib = (root / "references.bib").read_text(encoding="utf-8")
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", bib):
        if m.group(1).lower() not in {"comment", "preamble", "string"}:
            bib_keys.add(m.group(2))

    cited = set()
    tex_files = [p for p in root.rglob("*.tex")]
    for tf in tex_files:
        cited |= collect_cite_keys(read(tf))

    missing = sorted(cited - bib_keys)
    unused = sorted(bib_keys - cited)
    for k in missing:
        problems.append(f"[文献] 正文引用了 bib 中不存在的键：{k}")
    for k in unused:
        problems.append(f"[文献] bib 中存在但从未被引用的条目：{k}")
    print(f"文献条目 {len(bib_keys)} 条；正文引用键 {len(cited)} 个")

    # ---- 4. 统计快照 -------------------------------------------------------
    n_sections = 0
    for tf in tex_files:
        n_sections += len(re.findall(r"^\\section\{", read(tf), re.M))
    glossary = (root / "backmatter" / "glossary.tex").read_text(encoding="utf-8")
    print(f"\\section 大节合计 {n_sections} 个；"
          f"索引标记 {sum(len(INDEX_MARK.findall(read(t))) for t in tex_files)} 处")

    # ---- 结果 --------------------------------------------------------------
    if problems:
        print("\n发现以下问题：")
        for p in problems:
            print("  - " + p)
        return 1
    print("\n全部校验通过。")
    return 0


if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
    sys.exit(main(root.resolve()))
