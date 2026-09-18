# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T009` — 将学习资料整合/问题化组织定位写入 Content Core、Decision Log、Book Architecture 和适量公开说明 — IN-PROGRESS
- `WM-T010` — 将“哲学研究不等于前人思想研究”的方法立场以简短方式进入前言/项目定位 — IN-PROGRESS
- `WM-T011` — 参考 What-Remains-Human 建立 publication profile、移动章目录与 citation navigation — IN-PROGRESS
- `WM-T012` — 增加 PDF/DOCX/EPUB 手动构建 workflow，并验证多格式可生成 — IN-PROGRESS
- `WM-T013` — 完成 PR/main 验证与 handoff — TODO

## NEXT ACTIONS

1. 更新 index / preface 和 README 定位。
2. 更新 Quarto/CSS/HTML includes。
3. 增加 publication-format workflow 和必要 source checks。
4. 通过 Governance CI + HTML CI + publication-format build。
5. 合并并更新 Working Memory。

## BLOCKERS

- None for current content/form implementation.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for Web Edition and build previews; BLOCKING for formal open-license declaration`

### CLR-002 — 外部参考 PDF 的公开分发权利

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript/build preview; BLOCKING for redistribution/repackaging of that file`

## RECENTLY RESOLVED / PROMOTED

- Human decision in current cycle -> D005 -> Content Core / Form Core / Book Architecture / Publication Profile.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

- 在后续逐章审校中检查是否存在“人物/学说堆叠但没有明确问题功能”的段落。
- 若以后确定正式出版社或纸质版规格，再增加 PDF 具体版式约束。

## SYNC DEFECTS

- Current public README/preface and HTML-only source checker still reflect the pre-D005 publication scope; this cycle will reconcile them.
