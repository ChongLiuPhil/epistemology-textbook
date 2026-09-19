# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T021` — Cloudflare account-side staging context — `WAITING-EXTERNAL-ACCESS`

## COMPLETED PPF TASKS

- `WM-T020` — PPF Phase 2 Cloudflare repository readiness — `COMPLETED / PASS`

- `WM-T013` — PPF profile/source separation — `COMPLETED`
- `WM-T014` — PPF publication contract + staged Cloudflare config — `COMPLETED`
- `WM-T015` — source/CI validators for PPF model — `COMPLETED`
- `WM-T016` — PR runtime Web-profile validation — `COMPLETED / PASS`
- `WM-T017` — EPUB / PDF / DOCX / LaTeX runtime validation — `COMPLETED / PASS`
- `WM-T018` — Phase 1 cleanup + normal CI — `COMPLETED / PASS`
- `WM-T019` — Phase 1 merge + main Pages verification — `COMPLETED / PASS`

## PHASE 2 READINESS GATES

Repository side:
- [x] static-assets `wrangler.jsonc`
- [x] `_book` as deployment directory
- [x] machine-readable readiness state
- [x] readiness validator
- [x] no active Cloudflare deploy workflow before prerequisites
- [x] readiness PR CI PASS

Account side:
- [ ] Cloudflare account access verified
- [ ] Worker target verified/created
- [ ] `CLOUDFLARE_ACCOUNT_ID` secret verified
- [ ] `CLOUDFLARE_API_TOKEN` secret verified
- [ ] staging/preview deployment PASS
- [ ] target canonical URL confirmed
- [ ] Cloudflare zone / Custom Domain eligibility confirmed
- [ ] GitHub Pages legacy URL policy confirmed
- [ ] production deployment PASS
- [ ] production HTTP verification PASS

## NEXT ACTIONS

1. ~~Merge repository-side readiness.~~ `COMPLETED / MAIN VERIFIED`
2. Keep GitHub Pages as current production.
3. Establish Cloudflare account-side access/context.
4. Perform staging/preview deployment.
5. Confirm canonical domain and legacy Pages policy.
6. Only then add the active main-push Cloudflare deployment step.

## BLOCKERS

Production cutover is blocked by all unchecked account-side gates.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING`

### CLR-002 — 外部参考 PDF 的公开分发权利
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript work; BLOCKING for repackaging/redistribution decisions`

### CLR-003 — Cloudflare target canonical URL / legacy Pages policy
- Status: `WAITING-HUMAN / ACCOUNT-CONTEXT`
- Severity: `BLOCKING FOR CLOUDFLARE PRODUCTION CUTOVER`

## RECENTLY RESOLVED / PROMOTED

- PPF Phase 1 → `COMPLETED / VERIFIED`.
- Cloudflare repository-side readiness architecture → `docs/cloudflare-readiness.zh-CN.md` + `docs/cloudflare-readiness.yaml`.
- PR #22 merged at `f0af87ea5c060a69141eeb82c5992de8126af55d`; main Governance/Web/Pages/External Link checks → `PASS`.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

- HARC-lite → AHICP-based project governance migration（独立 PR）。
- 逐章学术/教学审校。
- 出版级 PDF typography / DOCX styles / EPUB CSS 在实际需要时继续细化。

## SYNC DEFECTS

- None known.
