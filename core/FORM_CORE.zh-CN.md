# Form Core — 教材形式与发布原则

**角色：** 保存长期形式决定，避免把某次工具默认值误认为作者永久偏好。

## 成果类型

- 类型：中文哲学教材 / 持续修订 Web Edition。
- 当前主要公开成果：GitHub Pages 上的 HTML 阅读版。

## 规范编辑与来源

- 正式正文：`index.qmd` 与 `manuscript/*.qmd`。
- 正式书目：`references.bib`。
- 书籍结构与 HTML 配置：`_quarto.yml`。
- `textbook/`：迁移前 LaTeX 历史快照，仅用于审计、比较和 provenance，不再编辑。
- `_book/`：生成结果，不是可编辑真值源。

## 语言

- 教材正文与内部治理：中文为主要规范语言。
- 公共 GitHub 入口：`README.zh-CN.md` 与 `README.md` 保持双语入口。
- 内部 HARC-lite 治理文档不要求逐份英文镜像。

## 当前 Web Edition 规则

- 左侧目录明确标为“本书目录”。
- 右侧页面目录明确标为“本章目录”。
- 提供搜索、reader mode、前后页、返回顶部、引文/脚注预览、查看源码与报告问题入口。
- 网页开放阅读不设置付费门槛；支持完全自愿。
- 当前日常 CI 只构建 HTML。
- EPUB / PDF / DOCX 延后到独立 release workflow，并继续从同一 canonical QMD 生成。

## 版本与反馈

- 网页持续修订；精确学术引用可以记录 Git commit。
- 内容问题与网页问题通过不同 GitHub Issue Form 分流。

## 临时实现默认值

以下属于实现选择，不应自动被视为永久作者偏好：

- Quarto 当前 HTML theme：`cosmo`。
- 当前具体 CSS 数值、间距、断点与视觉微调。

这些默认值可以在不改变核心 Form 原则的前提下迭代。
