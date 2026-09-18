# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- None. HARC-lite `0.1.1` refinement is complete.

## COMPLETED IN CURRENT CYCLE

- `WM-T005` — 轻量 Onboarding Check + PASS/PARTIAL/FAIL — DONE
- `WM-T006` — 明确人类责任主体与独立 Release Approval gate — DONE
- `WM-T007` — 补全 clarification promotion 与 revision-conflict 行为 — DONE
- `WM-T008` — governance validator 改为 manifest-driven，并验证 PR/main — DONE

Main implementation commit: `1906a4f56739ae1f3039cc3d695093eb986bfdd7`.

Validation on that main commit:

- Repository Governance CI — success
- External Link Audit — success
- Quarto HTML CI and Pages — success

## NEXT ACTIONS

1. 等待下一项人类优先任务。
2. 对新任务按 CONTENT / FORM / PROTOCOL 路由读取最小必要状态。
3. 新 Agent / 长中断 / 高影响 Architecture 或 Release 工作时执行轻量 Onboarding Check。
4. 较大工作循环结束后继续更新 Current Focus / Task Plan / Work Log。

## BLOCKERS

- None for normal manuscript, bibliography, website, or governance maintenance.

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

- None in the active clarification queue.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

- `AI-PROPOSED` — 如人类希望继续内容质量提升，从第 1 章开始逐章学术/教学审校。
- 在真正启用 PDF/EPUB/DOCX release 前设计独立 release workflow。
- 若协作者增多，再评估 main ruleset / required checks。

## SYNC DEFECTS

- None known.
