# 编辑与贡献约定

本项目以 Quarto `.qmd` 作为唯一正式书稿格式。当前阶段是 **Web Edition Development**：一套 canonical QMD sources 经过检查后生成 HTML；进入 `main` 的修改还必须落实为 GitHub Pages 上实际可阅读的网页。

## 1. 编辑哪些文件

- 首页与教材入口：`index.qmd`
- 九章正文及前后置材料：`manuscript/*.qmd`
- 参考文献：`references.bib`
- 全书结构与 HTML 配置：`_quarto.yml`
- HTML 阅读样式：`book.css`

`textbook/` 是迁移前的历史 LaTeX 快照，不再是正文来源，也不应继续编辑或参与构建。

## 2. 内容编辑原则

### 保持问题驱动

每章围绕明确问题推进，而不是把人物、流派或术语简单并列。新增内容应说明它解决什么问题、反驳什么主张，或改变哪一步推理。

### 保持教学层次

基础说明负责建立问题与核心论证；扩展、研读、专题和深论内容负责增加争议、案例、技术细节和研究入口。避免让难度无提示地突然跃升。

### 观点与评价分开

介绍一个立场时先准确重构其理由，再进入批评、比较或作者判断。对有争议的哲学主张，不把单一解释写成无争议事实。

### 术语保持一致

修改核心术语时同步检查首次解释、`manuscript/glossary.qmd`、中英文名称以及其他章节中的用法。

## 3. Quarto 写作约定

优先使用标准 Markdown 与 Pandoc/Quarto 语法：

- 引文：`[@key]` 或带定位信息的 `[@key, 23]`
- 脚注：`[^note]`
- 行内公式：`$...$`
- 展示公式：`$$...$$`
- 教学提示、案例和论证框：Quarto callout fenced div

不要在正文或构建配置中重新引入 `.tex` 文件、`\\input` / `\\include`、XeLaTeX、latexmk 或依赖旧 LaTeX 主稿的生成步骤。数学表达式中的 TeX-style math notation 属于 Quarto/Pandoc 数学语法，可以继续使用。

## 4. 文献约定

所有正式引文键必须存在于根目录 `references.bib`。新增或修改文献条目时：

- 优先记录可核验的 DOI；`doi` 字段使用规范的 bare DOI（例如 `10.xxxx/...`），不要把 resolver URL 填进 DOI 字段。
- `url` 字段使用完整的 `http://` 或 `https://` 地址；DOI resolver 可以同时作为 URL 保留，但不能替代 `doi` 字段。
- 不要给多个不同条目复用同一 DOI。若确实是同一作品的不同版本，应先确认是否需要分别建条目以及应引用哪个版本。
- 新增条目原则上应在正文、阅读地图或研究材料中实际使用；暂未引用的条目可以保留，但 `make check` 会将它们列为审计信息。
- 对作者、标题、年份、卷期、页码、出版社或 DOI 的实质修订，应以出版社、DOI 注册元数据或其他权威书目信息为依据，不凭印象猜改。

提交前运行：

```sh
make check
```

该命令会检查 citation key、BibTeX 基本结构、重复/格式错误 DOI 与 URL 等确定性问题。外部链接是否仍可访问由独立的 `External Link Audit` 检查：相关内容进入 `main` 时自动运行，同时保留每周与手动触发。它与 Pages 发布门禁分离，因为 403、429、5xx、TLS 与超时可能只是第三方网站的临时或机器人访问限制。

## 5. 练习与后置材料

修改章末练习、提示或术语时，直接维护相应的 `manuscript/*.qmd`。若题目数量、顺序或术语定义发生变化，应同步检查练习提示和术语表是否仍对应。

## 6. 读者反馈与问题分流

公开网页中的“报告问题”是正式反馈入口。GitHub Issue chooser 提供两类结构化模板：

- **书稿纠错与内容建议**：概念、论证、事实、例子、翻译、术语、引文、参考文献、练习或教学结构问题；
- **网页显示与阅读问题**：目录、公式、表格、脚注、链接、移动端、浏览器兼容或可访问性问题。

处理反馈时优先确认公开网页是否仍能复现；内容问题要回到 canonical QMD 修改，网页问题优先检查 `_quarto.yml`、`book.css` 与 Quarto 输出。不要直接编辑 `_book/` 中的生成文件。

对于书稿反馈，尽量保留页面链接、章节/小节、问题说明、建议修改和参考来源；对于网页反馈，再补充设备与浏览器信息。修复后仍需走 Pull Request → HTML validation → `main` → Pages deployment 的完整流程。

## 7. 构建与检查

提交前至少运行：

```sh
make check
```

需要检查网页阅读效果时运行：

```sh
make preview
```

需要执行完整开发构建时运行：

```sh
make html
# 或 make all；当前阶段二者都只生成 HTML
```

当前日常流程不生成 EPUB、PDF 或 DOCX。这些发行格式将在网页版稳定后通过独立 release workflow 处理，并继续以同一套 canonical QMD sources 为来源。

## 8. Commit 与 Pull Request

建议一个提交只处理一类问题：

- `docs:` 项目文档与编辑说明
- `content:` 教材正文、案例与练习
- `refs:` 书目与引用
- `style:` HTML 阅读样式
- `ux:` 阅读、导航与反馈体验
- `chore:` Quarto 构建、检查和仓库维护

Pull Request 应说明改动内容、理由、是否改变章节结构或核心论证、文献变化，以及已运行的检查。涉及网页体验时，还应说明它如何改变最终公开网站的阅读或反馈路径。

## 9. CI 与网页发布

Pull Request 阶段只验证，不对外发布。合并到 `main` 后，GitHub Actions 会再次执行 source validation、bibliography integrity checks、完整 HTML render 与全站内部链接/锚点检查；全部通过后，把同一次构建得到的 `_book/` 通过官方 GitHub Pages Actions 部署。

仓库另有独立的 `External Link Audit`。相关书稿、书目、网页配置或审计脚本进入 `main` 后会自动运行，并保留每周/手动触发。它不参与正常 Pages 发布门禁；只有明确的 HTTP 404/410 会被标记为断链失败，认证、限流、服务器错误和网络异常作为 warning 留给维护者复核。

因此，一次网页相关修改的完成标准不是“QMD 已修改”或“CI 能 render”，而是：修改进入 `main`、主分支 CI 通过、Pages deployment 成功，公开网页能够显示新的书籍版本。

在线阅读地址：<https://chongliuphil.github.io/epistemology-textbook/>
