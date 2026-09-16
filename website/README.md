# 在线阅读版

本目录用于《我们如何知道？——问题驱动的认识论》的网页阅读层。

## 原则

- `textbook/` 中的 LaTeX 主稿仍是正文的唯一 source of truth。
- `website/generated/` 由 `scripts/build_web.py` 自动生成，不应手工编辑。
- `_quarto.yml` 负责书籍目录、章节导航、引用与脚注展示。
- `book.css` 只负责网页阅读排版，不改变教材内容。

## 本地构建

安装 Quarto 后，在仓库根目录运行：

```bash
make web
```

这会先从 LaTeX 生成 Quarto 页面，再把 HTML 书籍渲染到 `_book/`。

只检查 LaTeX → Quarto 转换层：

```bash
make web-source
```

## 发布

`.github/workflows/publish-book.yml` 会在相关文件变化时构建在线版；合并到 `main` 后，验证通过的 `_book/` 发布到 `gh-pages`。

预期 GitHub Pages 地址：

`https://chongliuphil.github.io/epistemology-textbook/`

网页发布与项目的其他元数据相互独立；正文修订仍应首先修改 `textbook/` 中的源文件。
