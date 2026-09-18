# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T005` — 轻量 Onboarding Check + PASS/PARTIAL/FAIL — IN-PROGRESS
- `WM-T006` — 明确人类责任主体与独立 Release Approval gate — IN-PROGRESS
- `WM-T007` — 补全 clarification promotion 与 revision-conflict 行为 — IN-PROGRESS
- `WM-T008` — 将 governance validator 改为 manifest-driven，并验证 PR/main — IN-PROGRESS

## NEXT ACTIONS

1. 完成 manifest-driven repository governance checker。
2. 更新 Governance CI 路径覆盖。
3. 创建 PR 并通过 governance checks。
4. 合并 main 后确认 main governance run。
5. 更新 Current Focus / Task Plan / Work Log 到完成状态。

## BLOCKERS

- None for the current HARC-lite v0.1.1 refinement.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING`
- Uncertain point: authored textbook text、文档、脚本应采用什么法律许可。
- Current rule: 不把“公开仓库/开放阅读”解释成已经授予开放许可。
- Promotion destination: `LICENSE-DECISION.md` + repository LICENSE file(s).

### CLR-002 — 外部参考 PDF 的公开分发权利

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript work; BLOCKING for repackaging/redistribution decisions`
- Uncertain point: `reference/我们如何知道.pdf` 是否具有允许本公开仓库继续分发的明确权利依据。
- Current rule: 不将其视为项目 authored/open-content，也不纳入未来 release artifact。
- Promotion destination: `reference/README.md` / license or provenance record.

## RECENTLY RESOLVED / PROMOTED

- None in the current active queue. Future resolved clarifications should be kept here only briefly as `CLR-xxx -> Dxxx -> promoted target`, then moved to Work Log.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

- `AI-PROPOSED` — 如人类希望继续内容质量提升，从第 1 章开始逐章学术/教学审校。
- 在真正启用 PDF/EPUB/DOCX release 前设计独立 release workflow。
- 若协作者增多，再评估 main ruleset / required checks。

## SYNC DEFECTS

- None known.
