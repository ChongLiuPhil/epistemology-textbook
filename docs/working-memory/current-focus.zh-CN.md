# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Content Quality — **PR #18 reconciliation validated / Chapter 1 review next**.

## CURRENT_OBJECTIVE

把项目主工作重心从已经完成的 publication infrastructure 转回教材质量：从第 1 章开始逐章进行学术、教学与引用审校。

PR #39 已在 current PPF/Workers baseline 上验证通过，旧 PR #18 的有效内容/形式改进已经完成 reconciliation：

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

1. 合并已通过 current-main CI 的 PR #39；
2. 将旧 PR #18 关闭并标记为 superseded；
3. 以当前 main 为基线开始 Chapter 1 academic / pedagogical / citation audit；
4. 对审校发现的问题按普通 content/refs 修订处理；只有重大 Architecture 变化才重新进入人类确认。

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
