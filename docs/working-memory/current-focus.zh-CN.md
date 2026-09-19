# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Content Quality — **Chapter 1 review / Round 1 implemented / validation pending**.

## CURRENT_OBJECTIVE

把项目主工作重心从已经完成的 publication infrastructure 转回教材质量：当前正在进行第 1 章学术、教学与引用审校。

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

无 infrastructure blocker，也无阻止第 1 章审校的 content blocker。

仍存在但不阻塞书稿工作的 human clarifications：

- CLR-001：项目正式许可；
- CLR-002：外部参考 PDF 的公开分发权利。

## IMMEDIATE_NEXT_ACTION

1. 验证 Chapter 1 Round 1：书目 integrity、Quarto render、citation/backlink、Web/Cloudflare contract；
2. 若 PR 全绿，合并 Round 1；
3. 继续 Chapter 1 深层审校：JTB/Gettier 论证准确性、章节负载与后续章节重复度；
4. 若需要把大段内容迁移到第 3/5/7/9 章，先把它作为结构性提议提交人类确认，不在普通 content PR 中静默重排。

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
