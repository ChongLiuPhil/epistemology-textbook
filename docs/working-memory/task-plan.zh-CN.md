# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T020` — PPF Phase 2 Cloudflare readiness audit — `WAITING-PREREQUISITES / NEXT`

## COMPLETED PPF PILOT TASKS

- `WM-T013` — PPF profile/source separation — `COMPLETED`
- `WM-T014` — PPF publication contract + staged Cloudflare config — `COMPLETED`
- `WM-T015` — source/CI validators for PPF model — `COMPLETED`
- `WM-T016` — PR runtime Web-profile validation — `COMPLETED / PASS`
- `WM-T017` — on-demand EPUB / PDF / DOCX / LaTeX runtime validation — `COMPLETED / PASS`
- `WM-T018` — final PR cleanup + normal Governance/Web checks — `COMPLETED / PASS`
- `WM-T019` — merge Phase 1 and verify main GitHub Pages deployment — `COMPLETED / PASS`

Runtime evidence：
- PR Governance：PASS
- PR Web：PASS
- EPUB：PASS
- DOCX：PASS
- LaTeX：PASS
- PDF：PASS
- main Governance：PASS
- main Web build：PASS
- main Pages deployment：PASS
- main External Link Audit：PASS
- Phase 1 merge commit：`96b91691bd776136e156c384eee619d52ff2e3a4`
- Audit：`docs/ppf-pilot-audit.zh-CN.md`

## NEXT ACTIONS

1. 执行 Cloudflare Phase 2 readiness audit。
2. 确认 Worker / Static Assets target。
3. 确认最小权限部署凭据或其他授权部署机制。
4. 确认 target canonical production URL。
5. 先做 preview/staging deployment，再做 production verification。
6. 明确旧 GitHub Pages URL 的 redirect/canonical policy。
7. 只有上述条件满足后，才把 Web automatic deployment 从 Pages 切换到 Cloudflare。

## BLOCKERS

Phase 1：None — completed.

Phase 2 prerequisites：
- Worker target — unresolved
- deployment credentials / mechanism — unresolved
- target canonical URL — unresolved
- redirect/canonical policy — unresolved

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
- PR #20 merge + main Pages deployment verification → Phase 1 completion — `RESOLVED / VERIFIED`.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

PPF work does not alter this HARC-lite clarification lifecycle.

## TODO / BACKLOG

- HARC-lite → AHICP-based project governance migration（独立 PR）。
- 逐章学术/教学审校。
- 出版级 PDF typography / DOCX styles / EPUB CSS 在实际需要时继续细化。
- 若协作者增多，再评估 main ruleset / required checks。

## SYNC DEFECTS

- None known.
