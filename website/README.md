# 电子阅读版发布说明

本项目的网页与 EPUB 均直接由根目录 Quarto 项目生成。

## 正文来源

- `index.qmd`
- `manuscript/*.qmd`
- `references.bib`

这些文件是正式电子书的 source of truth。`website/` 不保存第二套正文，也不存在需要人工同步的网页稿。

## 本地构建

```sh
make check
make html
make epub
# 或一次生成全部格式
make all
```

构建产物统一写入 `_book/`。

## 发布

`.github/workflows/publish-book.yml` 在 pull request 中验证 HTML 与 EPUB；合并到 `main` 后，把验证通过的 `_book/` 发布到 `gh-pages`，同时上传 EPUB artifact。

正式阅读地址：

`https://chongliuphil.github.io/epistemology-textbook/`
