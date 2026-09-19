# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T018` — final PR cleanup + normal Governance/Web checks — IN-PROGRESS
- `WM-T019` — merge Phase 1 and verify main GitHub Pages deployment — TODO

## COMPLETED PPF PILOT TASKS

- `WM-T013` — PPF profile/source separation — COMPLETED
- `WM-T014` — PPF publication contract + staged Cloudflare config — COMPLETED
- `WM-T015` — source/CI validators for PPF model — COMPLETED
- `WM-T016` — PR runtime Web-profile validation — COMPLETED / PASS
- `WM-T017` — on-demand EPUB / PDF / DOCX / LaTeX runtime validation — COMPLETED / PASS

Runtime evidence：
- Governance：PASS
- Web：PASS
- EPUB：PASS
- DOCX：PASS
- LaTeX：PASS
- PDF：PASS
- Audit：`docs/ppf-pilot-audit.zh-CN.md`

## NEXT ACTIONS

1. ~~删除临时 PR-only format validation workflow。~~ `COMPLETED`
2. ~~更新 adoption note 为 Phase 1 runtime validation complete。~~ `COMPLETED`
3. 最终 PR head 再跑正常 Governance + Web checks。
4. checks PASS 后合并 PR #20。
5. 验证 `main` Pages deployment 与公开网页。
6. Phase 2 Cloudflare cutover 另开工作流/PR，不与 Phase 1 混合。

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
- PPF Phase 1 runtime profile validation → `docs/ppf-pilot-audit.zh-CN.md` — `RESOLVED / VERIFIED`.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

PPF pilot work does not alter this HARC-lite clarification lifecycle.

## TODO / BACKLOG

- Cloudflare Phase 2 cutover：Worker target、credentials、canonical URL、preview verification、redirect/canonical policy。
- HARC-lite → AHICP-based project governance migration（独立 PR）。
- 逐章学术/教学审校。
- 出版级 PDF typography / DOCX styles / EPUB CSS 在实际需要时继续细化。
- 若协作者增多，再评估 main ruleset / required checks。

## SYNC DEFECTS

- None known.
