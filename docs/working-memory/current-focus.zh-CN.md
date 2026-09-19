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
- canonical Web: `https://epistemology-textbook.philosophy-research.workers.dev/`;
- provider: Cloudflare Workers Builds;
- Web publication: `authorized / public`;
- access: `none`;
- GitHub Pages: `RETIRE`, Unpublish site human-confirmed complete;
- deployment/security line is stable maintenance, not the current development objective.
