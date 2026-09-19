# Publication Profile — 电子出版与网页形式映射

**状态：** ACTIVE FORM PROFILE  
**参考项目：** `ChongLiuPhil/What-Remains-Human-Epistemic-Agency-and-Human-Value-in-the-Age-of-AI`  
**历史参考 revision：** `040511a8c09866eeed6479b933e25bf51705ab32`

本文件说明本项目的电子出版、网页阅读与多格式构建约定。参考项目提供形式启发，但本项目的当前发布真值由 PPF contract、Quarto profiles 与本文件共同约束，不机械同步另一个仓库的基础设施。

## 1. 单一正文真源

`index.qmd`、`manuscript/*.qmd` 与 `references.bib` 是唯一正式内容来源。

- Web HTML 输出到 `_book/`；
- PDF / DOCX / EPUB / LaTeX 输出到 `_publication/<format>/`；
- 生成结果不得反向成为第二套正文；
- `textbook/` 继续只是历史 LaTeX 快照。

## 2. Continuous Web + on-demand formats

当前 PPF publication model：

- HTML：`continuous`，经 `make web-publish-check` 验证后由 Cloudflare Workers Builds 持续发布；
- PDF / DOCX / EPUB / LaTeX：`on-demand`，通过 `Build Publication Format` workflow 每次明确构建一种格式；
- BUILD 不自动等于 RELEASE；
- artifact 构建成功不自动创建 GitHub Release，也不改变正式 Release Approval。

当前 canonical Web identity：

`https://epistemology-textbook.philosophy-research.workers.dev/`

GitHub Pages legacy policy 已完成 `RETIRE`；它不再是当前发布路径。

## 3. 长篇网页阅读

网页形式优先支持连续阅读，而不是应用式界面：

- 正文宽度保持克制，中文正文使用较舒展行距；
- 桌面端左侧为“本书目录”、右侧为“本章目录”；
- 移动端复用 Quarto 生成的同一 TOC，生成正文内可折叠“本章目录”，不维护第二份人工目录；
- 长公式、表格、代码和图片不能撑破阅读栏；
- focus-visible、reduced-motion 与窄屏布局属于基本可访问性要求；
- reader mode、搜索、前后章导航、返回顶部、查看源码和报告问题入口继续保留。

## 4. 引文与章末参考文献

Web profile 采用：

- Quarto 原生 citation hover；
- citation click 打开当前文献详情；
- “查看本章参考文献”定位到对应 bibliography entry；
- 章末 bibliography 为正文引用位置生成返回导航；
- 章内 bibliography 标题统一为“本章参考文献”。

这些增强只属于 HTML 表现层，不修改 canonical citation source，也不改变 PDF / DOCX / EPUB / LaTeX 的正文语义。

## 5. Publication visibility 与访问策略

当前项目状态：

- source visibility：`public`；
- Web publication authorization：`authorized`；
- Web publication visibility：`public`；
- access mode：`none`。

PPF 已允许未来项目或未来状态采用 private source / restricted publication / authenticated access，但本教材不为了测试基础设施而人为开启访问控制。

## 6. 开放阅读、许可与第三方权利

- 网页完整阅读不设置付费门槛；
- 内容反馈和网页反馈继续使用 GitHub Issue Forms；
- 项目正式开放许可仍受 `CLR-001` 约束；
- 外部参考 PDF 的再分发仍受 `CLR-002` 约束；
- on-demand publication artifact 不包含未获再分发授权的外部 PDF。

## 7. 临时实现默认值

以下是可替换实现，不自动构成永久作者偏好：

- Quarto HTML theme：`cosmo`；
- 当前 CSS 数值、断点、间距和 dialog 视觉；
- 当前 PDF / DOCX / EPUB / LaTeX 的 profile 参数；
- Cloudflare Workers 作为当前 delivery provider。

Canonical source、publication semantics 与人类 Release Approval 边界应比具体 provider 和样式实现更持久。
