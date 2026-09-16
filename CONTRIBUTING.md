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

所有正式引文键必须存在于根目录 `references.bib`。新增条目后应在正文或阅读地图中实际使用，并运行：

```sh
make check
```

## 5. 练习与后置材料

修改章末练习、提示或术语时，直接维护相应的 `manuscript/*.qmd`。若题目数量、顺序或术语定义发生变化，应同步检查练习提示和术语表是否仍对应。

## 6. 构建与检查

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

## 7. Commit 与 Pull Request

建议一个提交只处理一类问题：

- `docs:` 项目文档与编辑说明
- `content:` 教材正文、案例与练习
- `refs:` 书目与引用
- `style:` HTML 阅读样式
- `chore:` Quarto 构建、检查和仓库维护

Pull Request 应说明改动内容、理由、是否改变章节结构或核心论证、文献变化，以及已运行的检查。

## 8. CI 与网页发布

Pull Request 阶段只验证，不对外发布。合并到 `main` 后，GitHub Actions 会再次执行 source validation、完整 HTML render 和关键页面检查；全部通过后，把同一次构建得到的 `_book/` 通过官方 GitHub Pages Actions 部署。

因此，一次网页相关修改的完成标准不是“QMD 已修改”或“CI 能 render”，而是：修改进入 `main`、主分支 CI 通过、Pages deployment 成功，公开网页能够显示新的书籍版本。

在线阅读地址：<https://chongliuphil.github.io/epistemology-textbook/>
