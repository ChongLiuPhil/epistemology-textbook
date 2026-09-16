# 《我们如何知道？》——问题驱动的认识论

这是一本以问题为中心组织的中文认识论教材，也是一个以 Quarto 为唯一正式写作系统的电子教材项目。

## 当前阶段：Web Edition Development

目前只开发和验证网页版。日常工作流是：

`QMD → validation → HTML`

EPUB、PDF、DOCX 暂不生成，也不属于当前 CI。等网页版稳定后，再通过独立的 release workflow 统一建立发行格式。

## Source of truth

正式书稿只有以下来源：

- 首页与教材入口：`index.qmd`
- 正文与前后置材料：`manuscript/*.qmd`
- 参考文献数据库：`references.bib`

全书结构与 HTML 配置位于 `_quarto.yml`，网页样式位于 `book.css`。

`textbook/` 保存迁移前的 LaTeX 历史稿，仅用于审计与版本追溯。它不是正式书稿来源，不参与编辑、检查或构建。数学公式中的 TeX/LaTeX 风格语法属于 Quarto/Pandoc 数学语法，不意味着恢复 LaTeX 文档工作流。

## 全书结构

### 第一部：知识、怀疑与理由

1. 知识是什么，我们为什么需要它
2. 怀疑、运气与知识的边界
3. 理由如何支持信念

### 第二部：认识来源、社会系统与理性模型

4. 经验、记忆与先验怎样成为知识来源
5. 他人、专家与制度如何共同生产知识
6. 概率、模型与理性决策

### 第三部：认识价值、技术环境与比较方法

7. 知识、理解与智慧为什么有价值
8. 数字环境与人工智能怎样重塑认识
9. 比较认识论如何改变我们的问题

此外还包含写在前面、学习与写作指南、研究工作坊、练习提示、术语表和参考文献。

## 本地开发

需要 Python 3、GNU Make 和 Quarto；当前开发流程不需要 LaTeX/XeLaTeX。

```sh
make check    # 检查 QMD、bibliography、项目结构和 HTML-only 配置
make preview  # 启动 Quarto 本地 HTML 预览
make html     # 生成 HTML 阅读版
make all      # 当前阶段等同于完整 HTML 开发构建
make clean    # 删除 _book/ 与 .quarto/
```

Quarto HTML 输出位于 `_book/`。

## 当前不生成的格式

当前默认流程和 CI 都不生成：

- EPUB
- PDF
- DOCX

这些格式将在网页版定稿后通过独立 release 流程统一生成，而不是在每次正文修改时构建。

## CI 与部署

GitHub Actions 当前只负责：检查 canonical QMD sources、验证 bibliography citation keys 与项目结构、安装 Quarto、完整渲染 HTML，并确认关键 HTML 页面存在。

当前 CI **不部署 GitHub Pages，不更新 `gh-pages`，也不上传 EPUB/PDF/DOCX artifacts**。

## 编辑原则

直接编辑 `index.qmd`、`manuscript/*.qmd` 和 `references.bib`。引文使用 Quarto/Pandoc citation 语法；公式、脚注、表格和 callout 使用 Quarto 可直接处理的 Markdown/Pandoc 语法。提交前至少运行 `make check`，检查最终网页效果时运行 `make preview` 或 `make html`。

详细约定见 `CONTRIBUTING.md`。
