# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Content Quality — **Chapter 2 review ROUND 2 / validation pending**.

## CURRENT_OBJECTIVE

把项目主工作重心保持在教材质量：第 1 章两轮审校已完成；第 2 章 Round 1 已 main-verified，当前正在做 Round 2 的结构/重复度与剩余引用精度审校。

PR #39 已在 current PPF/Workers baseline 上验证并合并到 `main`（merge `3e36d5dc015d8224ec6e6e98a952c5d77c872eee`）；旧 PR #18 的有效内容/形式改进已经完成 reconciliation：

- D005 学习—整合—梳理型教材定位与问题驱动哲学学习观；
- current publication profile；
- citation click detail + bibliography backlinks；
- “本章参考文献”；
- math-layout source check；
- README / CONTRIBUTING / AGENTS / project metadata 的 Pages/Phase 1 漂移清理。

第 1 章审校重点：

- 是否始终围绕“知识是什么/为什么需要知识”的哲学问题推进；
- 是否存在人物/流派罗列但没有问题功能的段落；
- 概念区分、论证重构、反例与竞争立场是否准确、公平；
- 学术性/历史性陈述是否有可核验文献支持；
- citation key、书目信息与正文主张是否匹配；
- 教学层次、案例、练习和段落路标是否服务学习目标；
- 是否存在重复、泛化、空洞总结或不必要的小标题。

## PRIMARY_BLOCKER

无 infrastructure blocker，也无阻止第 2 章 Round 1 审校的 content blocker。

仍存在但不阻塞书稿工作的 human clarifications：

- CLR-001：项目正式许可；
- CLR-002：外部参考 PDF 的公开分发权利。

## IMMEDIATE_NEXT_ACTION

1. 验证 Chapter 2 Round 2：Governance、canonical Web gate、Cloudflare contract/runtime、External Link Audit；
2. 若通过，合并 Round 2；
3. 合并后做 Chapter 2 closure review：确认是否仍有需要 human Architecture approval 的跨章移动；
4. 若无结构 blocker，把 WM-T031 收敛为 completed，并把下一章审校交给 WM-T032 / Chapter 3。

## PPF / DELIVERY BASELINE

- adopted PPF: `v0.1.0-draft @ 21a5360727167bad6f399477ded073431645fa1d`;
- production security profile: **Profile A — Workers Builds Native**;
- `least_privilege: false` remains explicit for the managed build token;
- Web publication: `authorized / public`;
- Web access: `none`;
- current canonical identity: workers.dev;
- workers.dev post-cutover provider build/runtime verification 已通过;
- legacy GitHub Pages policy: `retire`;
- `Unpublish site` human-confirmed complete on 2026-09-20;
- Verified cutover revision：`63510364ed40a97faf190c484dd80afc91971ecb`;
- Verified cutover runtime run：`35453967021`;
- Verified cutover Cloudflare provider check：`105926103705`;
- Verified post-merge Cloudflare checkpoint check：`105904495866`;
- Verified post-merge Cloudflare checkpoint Build ID：`93823dff-1206-4282-b037-24876840f0c6`;
- deployment/security line is stable maintenance, not the current development objective.


## CHAPTER 1 ROUND 1 FINDINGS

本轮已直接修复：

- 实验哲学不再暗示“文化差异必然很大”，同时加入早期差异研究与后续跨文化 Gettier 稳定性研究；
- JTB “两千年传统定义”历史叙事加入专门历史文献；
- 许可主义/唯一论加入直接基础文献；
- 认识价值小节补入理解与认识价值文献；
- 第 1 章中对第 3/5/7/9 章内容的提前展开增加前瞻链接；
- “自然主义与规范性 / 自然化解释与规范评价”重复内容做局部压缩。

结构观察（尚未授权迁移）：

- 第 1 章仍然承担部分认识规范、分歧、认识价值、实验/比较方法与知识优先内容；
- 是否进一步移动这些高级材料属于跨章 Architecture 问题，暂不在 Round 1 中处理。


## CHAPTER 1 ROUND 2 FINDINGS

Round 1 main verification：

- Governance `35471021367` → PASS;
- Quarto HTML `35471021383` → PASS;
- Cloudflare Build Contract `35471021450` → PASS;
- Cloudflare Runtime HTTP `35471021366` → PASS;
- External Link Audit `35471021375` → PASS.

Round 2 已实施：

- undefeated JTB 就地关联 Lehrer / Paxson；
- relevant alternatives 与 discrimination 明确区分，并分别关联 Dretske / Goldman；
- process reliabilism 从“固定真信念比例”改为更准确的“稳定倾向产生真信念”；
- 因果理论补 Goldman 原始来源；
- safety 与 virtue/ability 路线分开表述，并关联 Sosa / Greco / Pritchard；
- 增加到第二章的范围提示，避免第 1 章把怀疑论/反运气后续讨论伪装成完整处理。


## CHAPTER 1 COMPLETION

Round 2 main verification：

- merge `db1914fb248a503e6dc84424310427bfba254966`;
- Governance `35471217039` → PASS;
- Quarto HTML `35471216984` → PASS;
- Cloudflare Build Contract `35471217109` → PASS;
- Cloudflare Runtime HTTP `35471217023` → PASS;
- External Link Audit `35471217048` → PASS.

Chapter 1 audit conclusion：

- Gettier 原始两个案例与两项假设的复述未发现需要修正的实质错误；
- JTB 历史叙事、实验哲学、许可主义、认识价值与主要修补路线的引用/归属已加强；
- 自然主义重复段落已压缩；
- 后续章节主题已通过前瞻链接标清范围；
- 横向比较显示第 1 章虽较长，但第 2–5 章在篇幅与三级标题数量上处于相近区间，因此当前没有足够证据建议跨章迁移大段内容。

## CHAPTER 2 ROUND 1 FINDINGS

本轮已直接修复：

- 删除空的“三条回应路线”三级标题，改为路线地图式引导；
- 标准问题补 Chisholm 直接来源；
- 语境主义首轮介绍补 Cohen / DeRose / Lewis 直接文献，并把“相关可能性”与 speaker-context 标准变化区分得更清楚；
- 把 Pritchard 的 epistemic angst 与 Sosa 的 animal / reflective knowledge 区分开，避免理论归属混合；
- 闭合争论补 Dretske / Nozick / DeRose 文献锚点；
- safety 首次出现补 Sosa / Pritchard，介入运气/环境运气补 Pritchard；
- 修复彩票段落“通常敏感……所以不敏感”的自相矛盾笔误，明确开奖前基于概率的信念通常不敏感；
- 收紧“概率化安全”表述，避免把 safety 简单等同于近邻区域真信念比例；
- 德性认识论可靠主义/责任主义分支补 Greco / Sosa / Zagzebski；
- 认识风险与 sensitivity/safety 系统比较补直接理论来源。

结构观察（尚未授权迁移）：

- 第 2 章前半先给怀疑论回应概览，后半“怎样与怀疑者交锋”再做深描，存在有意的 overview → seminar 重复；目前先保留教学层次，不直接删并；
- 第 2 章后半将模态认识论延伸到工程鲁棒性、制度风险、人机系统，这与第 8 章存在潜在交叉；当前把它视为应用案例，不自动移动；
- 若 Round 2 发现重复导致明显阅读负担，再提出局部压缩或跨章 Architecture proposal。

## CHAPTER 2 ROUND 1 MAIN VERIFICATION

Round 1 merge：`99a27a5e1094b311638022fd7a382b012688bd61`

- Governance `35473757087` → PASS;
- Quarto HTML `35473757089` → PASS;
- Cloudflare Build Contract `35473757094` → PASS;
- Cloudflare Runtime HTTP `35473757090` → PASS;
- External Link Audit `35473757101` → PASS.

## CHAPTER 2 ROUND 2 FINDINGS

量化结构检查：

- Chapter 2 ≈ 27.4k characters / 72 个三级标题；
- Chapter 1 ≈ 28.3k / 65，Chapter 3 ≈ 25.6k / 64，Chapter 5 ≈ 26.0k / 74；
- 因此第 2 章篇幅与标题密度落在当前全书正常区间，没有证据支持跨章搬移大段内容；
- 同章 3-gram 段落相似度检查没有发现高重复段落；最高约 0.14，支持“overview → seminar → application”主要是有意教学层次，而非直接复制。

本轮已直接修复：

- fallibilism 补 Cohen，lottery knowledge 补 Hawthorne；
- 详细 contextualism 与 subject-sensitive invariantism 补 DeRose / Lewis / Fantl-McGrath / Hawthorne；
- Moore 深描段补原始文献；
- relevant alternatives / exclusion 补 Dretske / Vogel / Lewis；
- easy knowledge / warrant transmission 补 Wright；
- 最近世界/相关世界选择补 Nozick / Pritchard；
- modal reading 与 safety/closure 补 Nozick / Sosa / Comesaña；
- 彩票个案补 Hawthorne；
- “模态条件可以转译为系统测试”改为“设计启发式”，避免把哲学模态条件与工程指标写成严格等价。

结构结论：

- 不建议在 Round 2 删除 overview / seminar / application 三层；
- 与 Chapter 8 的工程/人机案例交叉仍作为应用层保留，不自动升级为跨章 Architecture move；
- 若后续真实教学/阅读反馈显示负载问题，再重新打开结构 watch。

