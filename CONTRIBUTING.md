# 编辑与贡献约定

本项目以 Quarto `.qmd` 作为正式书稿格式。编辑目标是让一套源文件同时服务网页阅读和 EPUB 电子书，避免多格式正文长期分叉。

## 1. 编辑哪些文件

- 全书结构与输出格式：`_quarto.yml`
- 首页：`index.qmd`
- 九章正文及前后置材料：`manuscript/*.qmd`
- 参考文献：`references.bib`
- HTML 阅读样式：`book.css`
- EPUB 阅读样式：`epub.css`

`textbook/` 是迁移前的历史 LaTeX 快照，不再是正文来源，也不应继续编辑。

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

不要在正文中重新引入 `.tex` 文件、`\\input` / `\\include` 或依赖 LaTeX 主稿的生成步骤。数学表达式中的 TeX-style math notation 属于 Quarto/Pandoc 数学语法，可以继续使用。

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

需要检查最终电子阅读效果时运行：

```sh
make all
```

这会从同一套 QMD 构建 HTML 与 EPUB；无需 XeLaTeX、Biber 或 MakeIndex。

## 7. Commit 与 Pull Request

建议一个提交只处理一类问题：

- `docs:` 项目文档与编辑说明
- `content:` 教材正文、案例与练习
- `refs:` 书目与引用
- `style:` HTML/EPUB 阅读样式
- `chore:` Quarto 构建、检查和仓库维护

Pull Request 应说明改动内容、理由、是否改变章节结构或核心论证、文献变化，以及已运行的检查。

## 8. 发布

`website.yaml` 的 `publish: true` 表示项目处于公开电子书发布模式。`main` 分支构建通过后，HTML 自动发布到 GitHub Pages，同时生成 EPUB artifact。涉及书名、作者、封面、许可证或正式版本号等出版元数据时，应作为明确的发布改动处理。
