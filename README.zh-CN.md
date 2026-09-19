# 《我们如何知道？》——问题驱动的认识论

[English](README.md) | [中文](README.zh-CN.md)

这是一个由 Chong Liu 持续维护、以问题为中心组织的中文认识论教材与学习工程。它首先服务于作者自身学习过程中对概念、问题、论证和文献的整合与梳理，并进一步开放给学生、自学者、教师与研究者使用；项目不以建立一套作者原创认识论理论为主要目标，但问题选择、材料取舍、比较框架与评价性判断由作者负责审核和组织。

## 当前阶段：Web Edition Development

Web Edition 已经是经过验证的 canonical continuous publication。当前正常发布路径是：

`canonical QMD → make web-publish-check → Cloudflare Workers Builds → workers.dev`

在线阅读：<https://epistemology-textbook.philosophy-research.workers.dev/>

开放阅读与支持：<https://epistemology-textbook.philosophy-research.workers.dev/manuscript/00-open-access-and-support.html>

PDF、DOCX、EPUB、LaTeX 是显式按需构建 artifact。手动 `Build Publication Format` workflow 每次选择一种 profile；构建成功可用于校对、离线阅读与出版准备，但不自动构成正式 release approval。

## 项目定位

本项目采用**学习—整合—梳理 + 问题驱动**的方式组织认识论材料。这里的“问题驱动”也体现一种哲学教育判断：哲学研究不能被简单等同于研究前人的思想。思想研究、思想史和哲学史当然重要，但哲学训练还要求直接面对问题、区分概念、比较理由、构造反例并检验立场。

因此，本书尽量不是按哲学家或流派罗列“谁说过什么”，而是让历史观点、当代研究与作者的组织判断共同服务于问题本身。这个原则主要体现在章节结构、练习、研究工作坊和阅读路线中，而不是把教材变成长篇方法论宣言。

## Source of truth

正式书稿只有以下来源：

- 首页与教材入口：`index.qmd`
- 正文与前后置材料：`manuscript/*.qmd`
- 参考文献数据库：`references.bib`

共享书籍结构位于 `_quarto.yml`；Web 配置位于 `_quarto-web.yml`；PDF、DOCX、EPUB、LaTeX 分别使用独立 profile。发布意图记录在 `publishing.yaml`，网页样式位于 `book.css`。

`textbook/` 保存迁移前的 LaTeX 历史稿，仅用于审计与版本追溯。它不是正式书稿来源，不参与编辑、检查或构建。数学公式中的 TeX/LaTeX 风格语法属于 Quarto/Pandoc 数学语法，不意味着恢复 LaTeX 文档工作流。

## 在线阅读体验

当前 Web Edition 将网页本身视为开发阶段的主要交付物，而不是构建过程的副产品。站点提供：

- 左侧“本书目录”用于跨章导航；桌面右侧“本章目录”用于当前章节内部定位，窄屏设备在正文标题下提供可折叠的“本章目录”
- 全站搜索、前后章节导航与返回顶部
- reader mode，用于长章的专注阅读
- 引文与脚注悬浮预览；引文点击可查看文献详情，并从章末参考文献返回正文引用位置
- 右侧“报告问题”和“查看源码”入口
- 全书页脚中的开放阅读、反馈与版本状态提示
- GitHub 上区分“书稿纠错与内容建议”和“网页显示与阅读问题”的结构化反馈表单

开放阅读不设置付费门槛。经济支持完全自愿，不影响阅读范围或后续公开更新；纠错、讨论、教学反馈、传播和文献建议同样被视为对项目的支持。

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

此外还包含开放阅读与支持说明、写在前面、学习与写作指南、研究工作坊、练习提示、术语表和参考文献。

## 反馈与维护

读者可以在任一长章右侧直接使用“报告问题”，或进入 GitHub Issues：

<https://github.com/ChongLiuPhil/epistemology-textbook/issues/new/choose>

反馈书稿内容时，建议附上页面链接、章节或小节、问题说明，以及可能的修改建议或参考来源。反馈网页问题时，建议同时注明设备与浏览器环境。

对于需要精确追踪的学术引用，除作者、书名、章节、页面链接和访问日期外，还可以记录对应的 Git commit，从而定位持续修订中的具体版本。

## 本地开发

需要 Python 3、GNU Make 和 Quarto；当前开发流程不需要 LaTeX/XeLaTeX。

```sh
make check    # 检查 QMD、数学布局风险、bibliography 元数据、项目结构、阅读/反馈、PPF 与发布边界
make preview  # 启动 Quarto 本地 HTML 预览
make html     # 生成 HTML 阅读版
make all      # 当前阶段等同于完整 HTML 开发构建
make clean    # 删除 _book/ 与 .quarto/
```

Quarto HTML 输出位于 `_book/`。`make check` 会阻止缺失 citation key、重复或格式错误的 DOI、非法 URL 等确定性文献错误；当前未被正文引用的书目条目会作为审计信息报告，而不会自动删除。

外部网站可达性受出版社、限流、认证与网络状态影响，因此不放进 canonical Web publication gate。电子出版与网页阅读约定见 `docs/publication-profile.zh-CN.md`。仓库另有独立的 `External Link Audit`：相关书稿、书目、网页配置或审计脚本进入 `main` 时会自动运行，同时保留每周与手动触发。它完整渲染网站后检查最终 HTML 中的外部链接，只把明确的 HTTP 404/410 作为断链失败，其余网络异常保留为 warning。

## 按需电子出版格式

`_quarto.yml` 现在只保存共享母配置，并把 `web` 设为默认 profile。日常 PR / `main` 流程只渲染并发布 `_quarto-web.yml` 定义的 HTML；需要校对、离线阅读或出版准备时，手动运行 `Build Publication Format` workflow，并明确选择 EPUB、PDF、DOCX 或 LaTeX 中的一种。

这些 artifact 与 HTML 使用完全相同的 `index.qmd`、`manuscript/*.qmd` 和 `references.bib`，不会形成第二套正文。Web 输出位于 `_book/`，按需格式位于 `_publication/<format>/`。手动构建成功也不自动代表正式 release 已获批准；正式版本状态见 `docs/release-status.zh-CN.md`。

## PPF 与 Cloudflare 发布状态

本项目采用 Personal Publishing Framework v0.1.0-draft，并固定 adopted commit 为 `21a5360727167bad6f399477ded073431645fa1d`。具体 contract 见 `publishing.yaml`，采用说明见 `docs/ppf-adoption.md`。

Cloudflare Workers 已是经过验证的当前 Web provider，workers.dev URL 是 current canonical publication identity。GitHub Pages 已按记录的 `RETIRE` policy 退出当前发布路径。source visibility、publication authorization、publication visibility、access policy 与 canonical identity 在 PPF 中保持彼此独立；当前教材是 public publication，access mode 为 `none`。

## CI 与部署

Pull Request 阶段会验证 canonical QMD sources、bibliography 元数据、PPF/Cloudflare contracts、读者界面配置、完整 Web render、内部链接/资源/锚点与 rendered HTML integrity。

`make web-publish-check` 是唯一 canonical Web publication quality gate。GitHub Actions 用它做验证；Cloudflare Workers Builds 在更新 workers.dev production 之前调用同一个 gate。正常 CI 不再部署 GitHub Pages。

外部 HTTP 链接继续由独立 audit 处理，避免第三方临时故障混入 canonical publication gate。

## 编辑原则

直接编辑 `index.qmd`、`manuscript/*.qmd` 和 `references.bib`。引文使用 Quarto/Pandoc citation 语法；公式、脚注、表格和 callout 使用 Quarto 可直接处理的 Markdown/Pandoc 语法。提交前至少运行 `make check`，检查最终网页效果时运行 `make preview` 或 `make html`。

详细约定见 `CONTRIBUTING.md`。


## 协作治理：HARC-lite

本仓库采用针对教材项目裁剪的 HARC-lite 协作层，使新的协作者或 AI Agent 不依赖旧聊天也能重建当前项目状态。

从零接管请先读 `START_HERE.zh-CN.md`。长期稳定的内容/形式原则分别位于 `core/CONTENT_CORE.zh-CN.md` 与 `core/FORM_CORE.zh-CN.md`；持久决定记录在 `core/DECISION_LOG.zh-CN.md`；当前目标、任务与待确认事项位于 `docs/working-memory/`。

项目采用的上游 HARC revision 固定在 `HARC_MANIFEST.yaml`，不会自动跟随上游变化。内部治理以中文为 canonical，不要求为每份协作文档维护英文镜像；公共 README 仍保留中英文入口。

`make check` 除书稿与书目检查外，还会验证 repository-backed collaboration state，防止旧发布说明、legacy 路径或未决许可状态被误写成当前真值。