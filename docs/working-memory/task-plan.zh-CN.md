# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T001` — 建立 HARC-lite 控制层与 Core / Working Memory — IN-PROGRESS
- `WM-T002` — 清理 website/reference/legacy README 中的仓库真值冲突 — IN-PROGRESS
- `WM-T003` — 增加 PR 模板、CITATION.cff、治理一致性检查与专用 CI — IN-PROGRESS
- `WM-T004` — 通过 PR、合并 main，并确认 Pages/治理 CI 成功 — TODO

## NEXT ACTIONS

1. 完成分支文件变更。
2. 跑 governance + HTML CI。
3. 修复任何失败。
4. 更新 Working Memory 为完成状态。
5. 合并并核对 main workflow。

## BLOCKERS

- None for the current governance upgrade.

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

- `AI-PROPOSED` — HARC-lite 稳定后，从第 1 章开始做逐章学术/教学审校。
- 在真正启用 PDF/EPUB/DOCX release 前设计独立 release workflow。
- 若协作者增多，再评估 main ruleset / required checks；不在本次通过不确定 API 权限强行设置。

## SYNC DEFECTS

- 当前已知：旧 `website/README.md` 与 `reference/README.md` 的 active-workflow 描述过时；本升级负责修复。
