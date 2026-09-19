# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T013` — PPF profile/source separation — IN-PROGRESS
- `WM-T014` — PPF publication contract + staged Cloudflare config — IN-PROGRESS
- `WM-T015` — update source/CI validators for PPF model — IN-PROGRESS
- `WM-T016` — PR runtime Web-profile validation — TODO
- `WM-T017` — on-demand EPUB / PDF / DOCX / LaTeX runtime validation — TODO

## NEXT ACTIONS

1. 同步 README / CONTRIBUTING / project metadata / release status。
2. 创建 Pull Request，检查 HTML/governance CI。
3. 修复任何 profile merge、validator 或 rendered HTML defect。
4. PR Web runtime validation 通过后，手动验证四种 on-demand profiles。
5. 记录 PPF pilot audit。
6. Phase 1 验证完成后再决定是否合并。
7. Cloudflare cutover 独立进入 Phase 2，不与本 PR 混合。

## BLOCKERS

- None for Phase 1.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING`

### CLR-002 — 外部参考 PDF 的公开分发权利

- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript work; BLOCKING for repackaging/redistribution decisions`

## RECENTLY RESOLVED / PROMOTED

- PPF adoption / two-phase migration model → D006 → `publishing.yaml` / Release Status / project metadata — `RESOLVED / PROMOTED`.

## TODO / BACKLOG

- Cloudflare Phase 2 cutover：Worker target、credentials、canonical URL、preview verification、redirect/canonical policy。
- HARC-lite → AHICP-based project governance migration（独立 PR）。
- 逐章学术/教学审校。
- 出版级 PDF typography / DOCX styles / EPUB CSS 在实际需要时继续细化。
- 若协作者增多，再评估 main ruleset / required checks。

## SYNC DEFECTS

- None known.
