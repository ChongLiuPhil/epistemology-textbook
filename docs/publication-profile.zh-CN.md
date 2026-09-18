# Publication Profile — 电子出版与网页形式映射

**状态：** ACTIVE FORM PROFILE  
**参考项目：** `ChongLiuPhil/What-Remains-Human-Epistemic-Agency-and-Human-Value-in-the-Age-of-AI`  
**参考 revision：** `040511a8c09866eeed6479b933e25bf51705ab32`

本文件说明“形式接近参考项目”具体意味着什么，避免以后把两个项目的全部基础设施机械同步。

## 1. 共同形式原则

### 单一正文真源

`index.qmd`、`manuscript/*.qmd` 与 `references.bib` 是本教材唯一正式内容来源。

HTML、PDF、DOCX、EPUB 都从同一套来源重新生成；生成结果不直接回写成第二套正文。

### HTML-first，其他格式按需构建

- GitHub Pages HTML：持续公开、进入 `main` 后自动发布；
- PDF / DOCX / EPUB：通过独立 workflow 按需构建，服务电子出版测试、审阅和未来 release；
- 日常内容 PR 不因为存在多格式能力而强制构建所有格式。

### 长篇网页阅读

网页形式优先考虑连续阅读，而不是应用式界面：

- 正文宽度保持克制；
- 中文正文使用较舒展行距；
- 桌面端左“本书目录”、右“本章目录”；
- 移动端把同一章目录复制为正文内可折叠导航，不维护第二份人工目录；
- 长公式、表格、代码和图片不能撑破阅读栏；
- focus-visible、reduced-motion 与移动端布局继续作为基本可访问性要求。

### 引文与章末层次

- Quarto 原生 citation hover 保留；
- citation click 可以显示本条文献详情；
- 章末参考文献提供返回正文引用位置的导航；
- 章内参考文献标题统一为“本章参考文献”；
- 网页增强只存在于 HTML 表现层，不改变 canonical QMD。

## 2. 本项目保留的差异

与参考项目不同，本项目：

- 是公开教材，不使用 Cloudflare 密码保护；
- 继续自动部署到 GitHub Pages；
- 保留开放阅读与自愿支持页面；
- 保留 reader mode、GitHub source/issue actions 和结构化 Issue Forms；
- 不采用参考项目的 BOOK_THESES、AUTHORIAL_ALIGNMENT_POLICY、source-map 或私有研究工作区作为必备结构；
- 不要求完整中英双语书稿；
- 当前正式许可仍未决定。

## 3. 多格式构建与 Release 的区别

`Build Publication Formats Manually` 生成的 PDF / DOCX / EPUB 是**构建 artifact**，用于检查和准备，不自动表示：

- 已形成正式出版版本；
- 已解决许可；
- 已完成作者 Final/Release Review；
- 已允许把第三方参考资料一起分发。

正式 release 仍以 `docs/release-status.zh-CN.md` 为准。

## 4. 未来排版升级

如果以后确定正式出版社、纸张尺寸、引文体例或 PDF 视觉规范，应在本 profile 上增加项目特定约束，而不是修改 canonical manuscript 来适配单一渠道。
