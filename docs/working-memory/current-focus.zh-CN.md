# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Content / Form — **PR #18 reconciliation against verified workers.dev + PPF baseline**.

## CURRENT_OBJECTIVE

收敛旧 PR #18 中仍有价值的教材定位、阅读体验与出版形式改进，同时删除其已经过时的 GitHub Pages / pre-PPF 假设；完成后把主要工作重心转回逐章学术/教学审校。

当前 reconciliation 范围：

- D005 学习—整合—梳理型教材定位与问题驱动哲学学习观；
- publication profile 文档与当前 PPF/Workers publication state 对齐；
- citation click detail + bibliography backlinks；
- 章内“本章参考文献”标题；
- math-layout source check；
- README / CONTRIBUTING / AGENTS / project metadata 中的旧 Pages/Phase 1 漂移清理；
- 不改变已验证的 workers.dev canonical production、Profile A 或 PPF adopted commit。

## PRIMARY_BLOCKER

无 infrastructure blocker。

本轮唯一执行 gate 是：reconciliation PR 必须通过当前 Governance、Web publication gate、Cloudflare contract/runtime 与必要的多格式/reader checks，不能用旧 PR 的历史 CI 代替当前验证。

仍存在但不阻塞书稿工作的 human clarifications：

- CLR-001：项目正式许可；
- CLR-002：外部参考 PDF 的公开分发权利。

## IMMEDIATE_NEXT_ACTION

1. 完成 PR #18 reconciliation branch 的 current-main CI；
2. 若通过，合并 reconciliation PR；
3. 将旧 PR #18 标记为 superseded/closed；
4. 把下一阶段切换为第 1 章逐章学术/教学/引用审校。

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
