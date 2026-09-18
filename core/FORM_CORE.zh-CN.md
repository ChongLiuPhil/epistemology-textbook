# Form Core — 教材形式与发布原则

**角色：** 保存长期形式决定，避免把某次工具默认值误认为作者永久偏好。

## 成果类型

- 类型：中文哲学学习教材 / 持续修订 Web Edition / 可按需生成电子出版格式。
- 当前主要公开成果：GitHub Pages 上的 HTML 阅读版。
- PDF、DOCX、EPUB 作为同一 canonical source 的按需出版构建，不形成第二套正文。

## 规范编辑与来源

- 正式正文：`index.qmd` 与 `manuscript/*.qmd`。
- 正式书目：`references.bib`。
- 书籍结构与格式配置：`_quarto.yml`。
- 正式网页阅读增强：`assets/includes/` 与 `book.css`，不得把正文内容复制进这些文件。
- `textbook/`：迁移前 LaTeX 历史快照，仅用于审计、比较和 provenance，不再编辑。
- `_book/`：生成结果，不是可编辑真值源。

## 语言

- 教材正文与内部治理：中文为主要规范语言。
- 公共 GitHub 入口：`README.zh-CN.md` 与 `README.md` 保持双语入口。
- 内部 HARC-lite 治理文档不要求逐份英文镜像。

## 出版 profile

本项目的电子出版、网页阅读和排版方向参考：

`ChongLiuPhil/What-Remains-Human-Epistemic-Agency-and-Human-Value-in-the-Age-of-AI`

当前参考 revision：

`040511a8c09866eeed6479b933e25bf51705ab32`

采用的是形式原则而不是仓库复制：

- 一套 Quarto canonical manuscript 同源生成 HTML / PDF / DOCX / EPUB；
- 日常公开交付仍优先 HTML；
- 其他电子出版格式由独立、按需 workflow 构建；
- 网页正文保持适合长篇阅读的窄栏、高行距和克制视觉层；
- 移动端提供可折叠“本章目录”；
- 引文在网页中既可快速查看，又可以定位本章参考文献并返回引用位置；
- 章末注释、参考文献与翻页导航形成清楚的阅读层次；
- 生成格式永远不成为第二套编辑源。

不采用参考项目的私有 Cloudflare 发布、密码预览、项目专属双语治理或作者思想库结构；本项目继续使用公开 GitHub Pages、开放阅读与 GitHub Issues。

详细映射见 `docs/publication-profile.zh-CN.md`。

## 当前 Web Edition 规则

- 左侧目录明确标为“本书目录”。
- 右侧页面目录明确标为“本章目录”。
- 窄屏设备增加正文内可折叠“本章目录”，来源仍是 Quarto 生成的同一 TOC。
- 提供搜索、reader mode、前后页、返回顶部、查看源码与报告问题入口。
- 引文与脚注支持悬浮查看；引文点击可在当前位置查看详情并返回引用位置。
- 章内参考文献使用明确标题“本章参考文献”。
- 网页开放阅读不设置付费门槛；支持完全自愿。
- 日常 CI 只构建和发布 HTML。
- PDF / DOCX / EPUB 由独立手动 publication-format workflow 从同一 canonical QMD 构建；手动 artifact build 不等于正式 Release Approval。

## 版本与反馈

- 网页持续修订；精确学术引用可以记录 Git commit。
- 内容问题与网页问题通过不同 GitHub Issue Form 分流。
- 正式多格式 release 仍受 `docs/release-status.zh-CN.md` 的作者审核和许可/权利 gate 约束。

## 临时实现默认值

以下属于实现选择，不应自动被视为永久作者偏好：

- Quarto 当前 HTML theme：`cosmo`。
- 当前具体 CSS 数值、间距、断点与视觉微调。
- 当前 PDF/DOCX/EPUB 的 Quarto 默认排版参数，除非作者以后单独确定出版规范。

这些默认值可以在不改变核心 Form 原则的前提下迭代。
