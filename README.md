# 《我们如何知道？》——问题驱动的认识论

这是一本以问题为中心组织的中文认识论教材，也是一个 **Quarto-first 的电子书项目**。项目的正式正文现在直接采用 `.qmd` 维护；同一套源文件生成网页阅读版与 EPUB，不再维护一套独立的 LaTeX 主稿。

## 正式内容入口

- **全书配置**：`_quarto.yml`
- **首页**：`index.qmd`
- **正文与前后置材料**：`manuscript/*.qmd`
- **参考文献**：`references.bib`
- **网页样式**：`book.css`
- **EPUB 样式**：`epub.css`
- **项目元数据**：`project.yaml`
- **发布元数据**：`website.yaml`

`manuscript/` 与 `index.qmd` 是今后编辑教材时的唯一正文 source of truth。

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

## 构建

需要 Python 3、GNU Make 和 Quarto。**不需要安装 LaTeX/XeLaTeX。**

```sh
make check   # 检查 QMD 结构与文献键
make html    # 生成网页阅读版
make epub    # 生成 EPUB 电子书
make all     # 生成全部配置格式（HTML + EPUB）
make clean   # 清理构建输出
```

Quarto 输出位于 `_book/`。EPUB 文件名固定为 `_book/how-do-we-know.epub`。

## 在线阅读与电子书

GitHub Actions 会在正文或构建配置变化时验证 HTML 与 EPUB。合并到 `main` 后，验证通过的网页自动发布到：

`https://chongliuphil.github.io/epistemology-textbook/`

同一次构建会上传 `epistemology-textbook-epub` artifact；网页侧栏也提供 EPUB 下载入口。

## 编辑原则

直接编辑 `manuscript/*.qmd`。引文使用 Quarto/Pandoc citation 语法，文献键维护在 `references.bib`；公式、脚注、表格和 callout 均使用 Quarto 可直接处理的 Markdown/Pandoc 语法。提交前至少运行 `make check`，需要检查最终阅读效果时运行 `make all`。

详细约定见 `CONTRIBUTING.md`。

## 旧 LaTeX 目录

`textbook/` 保存迁移前的 LaTeX 历史稿，仅作为审计与版本追溯材料。它**不再参与正式构建，也不应继续编辑**。迁移说明见 `textbook/LEGACY.md`。
