# 《我们如何知道？》——问题驱动的认识论

这是一本以问题为中心组织的中文认识论教材项目。当前主稿采用 LaTeX/XeLaTeX 编写，围绕知识、怀疑、证成、认识来源、社会认识论、形式认识论、认识价值、数字与 AI 环境、比较认识论等主题展开。

项目当前处于持续维护状态。教材主稿已经形成“三部九章”的稳定结构；仓库同时保留源稿一致性检查、索引与参考文献构建工具，方便继续修订、审校与出版准备。

## 项目入口

- **教材主稿**：`textbook/main.tex`
- **参考文献库**：`textbook/references.bib`
- **教材内部说明**：`textbook/README.md`
- **源稿一致性检查**：`textbook/tools/check_consistency.py`
- **项目元数据**：`project.yaml`
- **网站发布开关**：`website.yaml`（默认不发布）

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

主章节编排器位于 `textbook/chapters/revised/`；各章还会通过 `\input` 组合扩展阅读、研读实验室、专题研讨、综合论述以及部分深论模块。后置材料位于 `textbook/backmatter/`。

## 快速开始

在仓库根目录运行：

```sh
make check   # 不依赖 LaTeX，检查源稿结构、练习/提示配对和文献引用
make pdf     # 构建完整 PDF
make clean   # 删除临时构建目录
```

也可以直接进入 `textbook/` 使用其原生 `Makefile`。完整构建说明、临时目录策略和索引流程见 `textbook/README.md`。

### 最低工具要求

只运行源稿检查：

- Python 3
- GNU Make（或直接运行 Python 脚本）

构建 PDF 还需要：

- XeLaTeX
- `latexmk`
- Biber
- MakeIndex
- 支持中文排版的 TeX 发行版（例如 TeX Live）

## 目录结构

```text
.
├── README.md                 # 仓库总览（本文件）
├── CONTRIBUTING.md           # 编辑与提交约定
├── Makefile                  # 根目录统一命令入口
├── project.yaml              # 学术项目元数据
├── website.yaml              # 网站发布元数据与发布开关
├── reference/                # 外部参考资料（不属于可编译主稿）
└── textbook/
    ├── main.tex              # 全书入口
    ├── style.tex             # 全局样式与自定义宏
    ├── frontmatter.tex       # 前置材料
    ├── references.bib        # BibLaTeX 文献库
    ├── chapters/             # 章节与内容模块
    ├── backmatter/           # 学习指南、研究工坊、练习提示、术语表等
    └── tools/                # 源稿检查工具
```

## 编辑工作流

建议每次修改遵循以下顺序：

1. 修改对应的章节或模块文件，尽量保持现有模块边界。
2. 新增或删除模块时，同步维护调用它的 `\input` / `\include` 关系和文件头归属说明。
3. 新增文献时同步更新 `textbook/references.bib`，并确保正文或阅读地图实际引用该键。
4. 修改章末练习时，同步更新 `textbook/backmatter/exercise-hints.tex`。
5. 先运行 `make check`；需要交付版面时再运行 `make pdf`。
6. 提交前确认没有把 PDF、LaTeX 临时文件或本地编辑器状态加入版本控制。

更详细的提交约定见 `CONTRIBUTING.md`。

## 自动校验

仓库使用 GitHub Actions 在 push 和 pull request 时运行轻量级源稿检查。该检查不构建 PDF，因此可以快速发现：

- `\input` / `\include` 指向不存在的文件；
- 各章练习数量与练习提示不一致；
- 正文引用了不存在的 BibLaTeX 键；
- `references.bib` 中存在完全未使用的条目。

完整 PDF 构建仍建议在具有完整中文 TeX 环境的本地或专用构建环境中执行。

## 当前基线

当前定稿基线为三部九章，教材内部 README 记录的最近一次完整构建为 216 页，并包含章末练习、详细提示、术语表、索引和分层阅读地图。具体统计与构建记录以 `textbook/README.md` 为准。

## 出版前待办

主稿目前仍保留出版元数据 TODO，包括：

- 补齐 `textbook/main.tex` 中的作者署名；
- 同步补齐 `textbook/style.tex` 中 PDF metadata 的 `pdfauthor`；
- 最终确认封面日期；
- 在明确需要公开发布时，再修改 `website.yaml` 的发布开关与公开说明。
