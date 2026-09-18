# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- None. HARC-lite governance rollout is complete.

## COMPLETED IN CURRENT CYCLE

- `WM-T001` — 建立 HARC-lite 控制层与 Core / Working Memory — DONE
- `WM-T002` — 清理 website/reference/legacy README 中的仓库真值冲突 — DONE
- `WM-T003` — 增加 PR 模板、CITATION.cff、治理一致性检查与专用 CI — DONE
- `WM-T004` — PR #14 验证、合并 main，并确认 Pages/治理/外链流水线成功 — DONE

Main implementation commit: `691374183198919d8229aaa7216c237348120b92`.

## NEXT ACTIONS

1. 等待下一项人类优先任务。
2. 对新任务按 CONTENT / FORM / PROTOCOL 路由读取最小必要状态。
3. 较大工作循环结束后继续更新 Current Focus / Task Plan / Work Log。

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

## TODO / BACKLOG

- `AI-PROPOSED` — 如人类希望继续内容质量提升，从第 1 章开始逐章学术/教学审校。
- 在真正启用 PDF/EPUB/DOCX release 前设计独立 release workflow。
- 若协作者增多，再评估 main ruleset / required checks。

## SYNC DEFECTS

- None known. Previously stale `website/README.md` was removed; `reference/README.md` and legacy LaTeX documentation were corrected in PR #14.
