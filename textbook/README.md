# 《我们如何知道？》构建说明

主稿是 `main.tex`。全书由三部、九章构成，九章主文件位于 `chapters/revised/`；每章围绕一个大问题组织基础论证、理论扩展、研读实验室、专题研讨与综合论述。第六至九章另有深论模块位于 `chapters/deepening/`，用完整算例、竞争解释、反对意见和审计表扩展既有大节，不增加碎片化标题。自学与写作指南、全书综合研究工坊、练习提示和术语表位于 `backmatter/`，文献数据位于 `references.bib`。

从本目录构建（编译产物写入项目外的临时目录）：

```sh
make            # 等价于下方三步：latexmk → makeindex → latexmk
```

或手动执行三步流程：

```sh
mkdir -p /tmp/epistemology-build
latexmk -norc -xelatex -interaction=nonstopmode -halt-on-error -outdir=/tmp/epistemology-build main.tex
(cd /tmp/epistemology-build && makeindex -o main.ind main.idx)
latexmk -norc -xelatex -interaction=nonstopmode -halt-on-error -outdir=/tmp/epistemology-build main.tex
```

注意：makeindex 需在构建目录内运行；直接以绝对路径向 `/tmp` 写 `.ind` 会被 TeX 的
openout 安全策略（`openout_any = p`）拒绝。

第二步必须在正文索引记录生成后执行；否则首次构建可能得到空索引。

项目目录只保留可继续编辑的源稿；编译缓存、PDF 和历史版本不纳入工作树。需要交付 PDF 时，可将临时目录中的 `main.pdf` 另行复制到项目外部。

## 工具链与版本控制

- `Makefile`：`make` 全量构建，`make check` 源稿校验，`make clean` 清理构建目录；构建目录可用 `BUILD_DIR=` 覆盖。
- `tools/check_consistency.py`：不依赖 LaTeX 的源稿一致性校验——章文件 `\input` 图谱完整性、54 道章末练习与 54 条练习提示逐章配对、正文引用键与 `references.bib` 双向对账（含 `\readingstrand` 阅读地图键）、统计快照。任何修改后建议先跑 `make check` 再构建。
- 各内容模块（基础正文、extensions、readings、seminars、syntheses、deepening）文件首行均有归属注释，标明所属章与引入它的编排器文件；调整章节结构时同步更新注释头。
- 项目根目录已纳入 git 版本控制：定稿基线打有 `v1.0-baseline` 标签。`.gitignore` 排除一切 LaTeX 编译产物与 PDF（`reference/` 下外部参考资料除外）。
- 出版前待办：补齐 `main.tex` 的 `\author` 与 `style.tex` 的 `pdfauthor`（源码中已有 TODO 标注），并确认封面日期。

## 三部九章结构

第一部：知识、怀疑与理由

1. 知识是什么，我们为什么需要它
2. 怀疑、运气与知识的边界
3. 理由如何支持信念

第二部：认识来源、社会系统与理性模型

4. 经验、记忆与先验怎样成为知识来源
5. 他人、专家与制度如何共同生产知识
6. 概率、模型与理性决策

第三部：认识价值、技术环境与比较方法

7. 知识、理解与智慧为什么有价值
8. 数字环境与人工智能怎样重塑认识
9. 比较认识论如何改变我们的问题

## 定稿规模与检查记录

- 3 部、9 章、59 个大节；每章约 16,350--21,161 个正文汉字，每节约 1,500--6,100 个汉字，中位数约 2,400 个汉字。
- 活跃 TeX 源稿约 19.3 万个汉字；定稿 PDF 可提取约 19.7 万个汉字，共 216 页。三个部页承担全书导航，九章末各有一页完整的分层阅读地图。
- 9 份章末自测，54 道练习与 54 条详细提示逐题对应；另有十二周自学路线与全书综合研究工坊。
- 113 条核心术语释义；201 处索引标记形成 169 个不同索引词条。
- 236 条参考文献全部在正文论证或章末阅读地图中实际引用；293 个引用命令、541 次文献键调用均可解析，没有缺失键或闲置文献。各章覆盖 29--32 条独立来源，并按“问题奠基—主要争论—专门研究—研究入口”分层。
- 书目通过 Biber 数据模型校验，116 个 DOI 与 5 个稳定 URL 均完成解析或人工核验；XeLaTeX、Biber 与 MakeIndex 全量构建通过，无溢出版心、未定义交叉引用、缺失文献键或 Biber 数据警告。
- 定稿完成了 216 页逐页联系表检查，并对封面、目录、三个部页、九个章首页、九张阅读地图、公式、表格、练习提示、术语表、参考文献和索引作高分辨率抽查。
