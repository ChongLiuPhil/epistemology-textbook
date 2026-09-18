# Working Memory — Work Log

本文件保存阶段性里程碑，主要供人类回顾与审计。新 Agent 默认不需要读取完整历史。

## 2026-09-18 — HARC-lite 升级启动

- 对照 `Human-AI-Research-Collaboration-Protocol` 审计教材仓库的协作基础设施；
- 判断现有 Quarto/Pages/质量检查工程成熟，主要缺口在长期状态持久化、决策追踪与零上下文接管；
- 发现 `website/README.md`、`reference/README.md` 与现行工作流存在真值冲突；
- 人类作者确认执行 HARC-lite 升级；
- 固定上游采用基线：HARC `0.2.0-draft` @ `e741c43c5cd158c43910e3832c7d757226717a97`；
- 许可选择与外部参考 PDF 权利状态保留为显式人类待决事项。

## 2026-09-18 — HARC-lite 升级完成

- PR #14 “建立 HARC-lite 协作治理与仓库状态检查”通过 Repository Governance CI 与完整 Quarto HTML CI；
- squash merge 到 `main`：`691374183198919d8229aaa7216c237348120b92`；
- `main` 的 Repository Governance CI：success；
- `main` 的 Quarto HTML validation：success；
- GitHub Pages `deploy-pages`：success；
- External Link Audit：success；
- 九章正文与 `references.bib` 未在本轮治理升级中改写；
- 当前已无已知 repository-truth sync defect；
- 两项仍待人类决定：正式许可模型、外部参考 PDF 的公开分发权利依据。

HARC-lite 现已成为后续协作的仓库级控制层；上游 HARC 后续变化不会自动进入本项目。


## 2026-09-18 — HARC-lite v0.1.1 协作闭环完善完成

- 人类作者在二次复核后明确确认继续完善当前协作框架；
- 新增轻量 `ONBOARDING_CHECK.zh-CN.md`，仅在新 Agent、长中断、高影响 Architecture/Release 工作或状态冲突时要求 PASS/PARTIAL/FAIL 接管报告；
- 明确作者 Chong Liu 保持为项目目的、核心知识判断、重大 Architecture 授权与公开 Release 决定的责任主体；
- 新增独立 `docs/release-status.zh-CN.md`，区分 Architecture/Framework Approval 与 Release Approval；
- clarification lifecycle 补全为 `WAITING-HUMAN -> resolution -> Decision Log -> promotion -> RESOLVED/PROMOTED -> leave active queue`；
- revision conflict 补全为 stop-write / fresh-fetch / inspect / reconcile / revalidate / write；
- repository governance checker 改为 manifest-driven，并动态核对 manifest 与 `project.yaml` 的 profile、profile version、HARC version 与 adopted commit；
- validator 首轮真实发现 `HARC-lite-book` / `harc-lite-book` metadata casing drift，修复后 PR #16 两个门禁均通过；
- PR #16 合并实现 commit：`1906a4f56739ae1f3039cc3d695093eb986bfdd7`；
- 该 main commit 的 Repository Governance CI、External Link Audit、Quarto HTML CI and Pages 全部成功；
- 本轮没有修改九章正文、`references.bib`、Quarto book config 或 CSS。

HARC-lite profile version 现为 `0.1.1`。
