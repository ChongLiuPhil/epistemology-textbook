# Form Core — 教材形式与发布原则

**角色：** 保存长期形式决定，避免把某次工具默认值误认为作者永久偏好。

## 成果类型

- 类型：中文哲学教材 / 学习—整合—梳理型持续修订项目。
- 当前主要公开成果：Cloudflare Workers 上持续发布的 HTML Web Edition。
- PDF / DOCX / EPUB：与 HTML 共用同一套 Quarto canonical source，按需生成，不作为日常编辑源。

## 规范编辑与来源

- 正式正文：`index.qmd` 与 `manuscript/*.qmd`。
- 正式书目：`references.bib`。
- 书籍共享结构：`_quarto.yml`；Web 与按需出版格式分别由 `_quarto-web.yml`、`_quarto-pdf.yml`、`_quarto-docx.yml`、`_quarto-epub.yml`、`_quarto-latex.yml` 承担 profile-specific 配置。
- `textbook/`：迁移前 LaTeX 历史快照，仅用于审计、比较和 provenance，不再编辑。
- `_book/`：生成结果，不是可编辑真值源。

## 语言

- 教材正文与内部治理：中文为主要规范语言。
- 公共 GitHub 入口：`README.zh-CN.md` 与 `README.md` 保持双语入口。
- 内部 HARC-lite 治理文档不要求逐份英文镜像。

## 出版模型

本项目采用 Personal Publishing Framework (PPF) 的 source / build / publish / release 分离语义，并保留早期参考项目带来的 Quarto 多格式形式启发：

- 一套 canonical QMD / bibliography 同时服务 HTML、PDF、DOCX、EPUB 与 LaTeX；
- HTML 是 `continuous` publication，经 canonical Web gate 后由 Cloudflare Workers Builds 持续发布；
- PDF / DOCX / EPUB / LaTeX 通过独立手动 workflow、按 profile、一次一种格式构建；
- 手动生成 artifact 不自动等于 `RELEASE-APPROVED`，也不自动创建 GitHub Release；
- 当前 canonical Web identity 是 `https://epistemology-textbook.philosophy-research.workers.dev/`；
- GitHub Pages legacy publication 已按 `RETIRE` policy 退出当前发布路径。

详细项目级映射见 `docs/publication-profile.zh-CN.md`。

## Web Edition 与排版规则

网页形式可以与参考项目保持接近的阅读逻辑，同时保留本项目已经形成的公开阅读与反馈机制：

- 左侧目录明确标为“本书目录”；
- 右侧页面目录明确标为“本章目录”；
- 窄屏设备在正文顶部提供可折叠的“本章目录”，其内容直接复用 Quarto 生成的 canonical TOC，不维护第二套目录；
- 中文正文采用适合长篇阅读的 serif 字体栈，导航与界面采用 sans-serif；
- 正文桌面阅读列保持约 820px 的适中宽度；
- 长公式、表格、图片和代码不得把阅读列撑破；
- 提供搜索、reader mode、前后页、返回顶部、引文/脚注预览、citation click detail、章末 bibliography backlink、查看源码与报告问题入口；
- 网页开放阅读不设置付费门槛；支持完全自愿。

本项目已采用 citation dialog / bibliography backlink，但只作为 Web 表现层增强；canonical citation 仍来自 QMD + `references.bib`，其他输出格式不依赖这层 JavaScript。

## 版本与反馈

- 网页持续修订；精确学术引用可以记录 Git commit。
- 内容问题与网页问题通过不同 GitHub Issue Form 分流。
- 多格式 artifact 都是 canonical source 的派生产物，不允许反向编辑形成第二套正文。

## 临时实现默认值

以下属于实现选择，不应自动被视为永久作者偏好：

- Quarto 当前 HTML theme：`cosmo`。
- 当前具体 CSS 数值、间距、断点与视觉微调。
- PDF / DOCX / EPUB 当前使用 Quarto 默认输出配置，后续可在不改变 canonical source 的前提下逐步建立出版级样式。

这些默认值可以在不改变核心 Form 原则的前提下迭代。
