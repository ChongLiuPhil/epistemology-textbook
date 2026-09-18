# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T009` — 持久化学习—整合—梳理型教材定位与问题驱动哲学教育原则 — IN-PROGRESS
- `WM-T010` — 配置 HTML/PDF/DOCX/EPUB 同源输出与手动 publication workflow — IN-PROGRESS
- `WM-T011` — 移植兼容的网页阅读形式：移动端“本章目录”与相关样式 — IN-PROGRESS
- `WM-T012` — 更新 source/CI checks，验证 PR/main 与 publication-format build — TODO

## NEXT ACTIONS

1. 修改 `_quarto.yml` 声明多格式输出。
2. 新增手动 publication-format workflow。
3. 加入移动端章节 TOC include 与 CSS。
4. 调整 `scripts/check_quarto.py`：允许手动 release build，但继续禁止日常 CI 生成/部署非 HTML。
5. 更新 README / CONTRIBUTING。
6. PR 验证；必要时执行一次性 publication-format 构建测试。
7. 合并 main 并更新 Working Memory。

## BLOCKERS

- None for this implementation.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING`

### CLR-002 — 外部参考 PDF 的公开分发权利

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript work; BLOCKING for repackaging/redistribution decisions`

## RECENTLY RESOLVED / PROMOTED

- Human project-positioning / publication-form instruction → D005 → Content Core / Form Core / Release Status — `RESOLVED / PROMOTED`.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

- 逐章学术/教学审校。
- 出版级 PDF typography / DOCX styles / EPUB CSS 在实际需要时继续细化，不把工具默认值提前升级为作者永久偏好。
- 若协作者增多，再评估 main ruleset / required checks。

## SYNC DEFECTS

- None known.
