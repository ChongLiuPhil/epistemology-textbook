# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T023` — Cloudflare ↔ GitHub reusable Workers Builds standard — `COMPLETED / MAIN-VERIFIED`
- `WM-T024` — Cloudflare build-token hardening research — `COMPLETED / PRODUCT-CONSTRAINT`
- `WM-T025` — Cloudflare production security profile — `WAITING-HUMAN-AFTER-CANDIDATE-VALIDATION`
- `WM-T026` — Hardened External CI candidate — `IN-PROGRESS / VALIDATE-ONLY-CI`

## COMPLETED PPF TASKS

- `WM-T021` — Cloudflare account-side staging context — `COMPLETED / STAGING-PASS`
- `WM-T022` — Cloudflare staging runbook + least-privilege deployment model — `COMPLETED`
- `WM-T020` — PPF Phase 2 Cloudflare repository readiness — `COMPLETED / PASS`
- `WM-T013`–`WM-T019` — PPF Phase 1 source/profile/runtime/main Pages validation — `COMPLETED / PASS`

## STANDARD INTEGRATION GATES

Repository contract:
- [x] `wrangler.jsonc` static-assets Worker
- [x] canonical `make web-publish-check`
- [x] GitHub Actions uses canonical gate
- [x] `cloudflare-builds.yaml`
- [x] pinned Node / Wrangler / Quarto
- [x] build wrapper for environments without Quarto
- [x] non-deploying Cloudflare contract CI
- [x] nontechnical human authorization guide
- [x] PR normal Web CI PASS
- [x] PR Cloudflare Build Contract CI PASS
- [x] merge + main CI PASS

Account connection:
- [ ] Cloudflare OAuth/MCP actually callable by current AI
- [x] Cloudflare GitHub App authorized for selected repository
- [x] repository connection verified
- [x] Worker `epistemology-textbook` verified/created
- [x] production trigger configured and main build PASS
- [x] preview trigger configured and preview build PASS
- [x] default build token present and operationally verified
- [x] default token permission scope reviewed
- [x] Workers Builds account-owned/per-Worker token incompatibility documented
- [ ] hardened external-CI validate-only candidate PASS
- [ ] production security profile selected
- [x] non-production preview build PASS
- [x] main workers.dev HTTP/content verification PASS
- [x] preview workers.dev HTTP/content verification PASS

Production cutover:
- [ ] target canonical URL
- [ ] Cloudflare zone / Custom Domain eligibility
- [ ] Custom Domain
- [ ] production verification
- [ ] GitHub Pages legacy policy
- [ ] canonical URL migration

## NEXT ACTIONS

1. 保持已经验证通过的 Cloudflare-managed build token，不在稳定 staging 链路上继续盲测。
2. 先验证 Profile B candidate：PR 只运行 validate-only，不需要 Cloudflare secret，不部署。
3. candidate PASS 后，人类选择 production security profile：
   - A：Workers Builds native / managed user token；
   - B：GitHub Actions external CI / per-Worker account-owned Editor token。
4. 如果选 A：记录 risk acceptance，进入 Custom Domain / canonical URL / Pages legacy policy。
5. 如果选 B：只需创建 per-Worker account-owned Editor token + GitHub secret/variable，然后运行 manual preview/production revalidation。
6. Future：Cloudflare Workers Builds 支持 account-owned token 后，重新评估 Profile C。

## DEFAULT ACCOUNT-SIDE ROUTE

Preferred:

`Cloudflare OAuth/MCP + Cloudflare Workers Builds + GitHub App`

Human should only need to authorize:

1. AI ↔ Cloudflare OAuth/MCP；
2. Cloudflare ↔ selected GitHub repository。

Everything after those authorizations should be agent-executable from the machine contract where the client exposes the Cloudflare tools.

Fallback:

`GitHub Actions + Wrangler + scoped token`

Fallback is not enabled while Workers Builds remains viable.

## BLOCKERS

- Production security profile requires human choice before final cutover.
- Workers Builds currently supports user tokens only; the desired per-Worker account-owned token is therefore not available on the preferred native path.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING`

### CLR-002 — 外部参考 PDF 的公开分发权利
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript work; BLOCKING for repackaging/redistribution decisions`

### CLR-003 — Cloudflare target canonical URL / legacy Pages policy
- Status: `WAITING-HUMAN / AFTER-STAGING`
- Severity: `BLOCKING FOR PRODUCTION CUTOVER, NOT FOR WORKERS.DEV STAGING`

## RECENTLY RESOLVED / PROMOTED

- Cloudflare Workers Builds repository contract validation → Governance `35427051865`, Web `35427051858`, Contract CI `35427051853` → `PASS`.
- PPF Phase 1 source/profile/runtime validation → `COMPLETED / VERIFIED`.
- Repository-side Cloudflare readiness → `COMPLETED / PASS`.
- Cloudflare staging runbook + least-privilege model → `COMPLETED`.
- Canonical Web publication gate design → promoted into `Makefile`, `scripts/check_rendered_html.py`, and CI.
- Workers Builds machine contract → promoted into `cloudflare-builds.yaml` and `docs/cloudflare-readiness.yaml`.
- Main Workers Build `d6bc8b62-78ba-4a9e-98ea-7a049a539858` → `PASS`.
- Preview Workers Build `a12446a5-e341-48e4-8c22-1a184b1102c8`, Version `3f8a15d6-9994-4e90-839c-2144c8dc54b7` → `PASS`.
- Runtime HTTP verification `35431565729` → main + preview, each 5 pages + 30 local assets → `PASS`.
- Post-merge main Cloudflare Build `6eb6fb9a-34c0-4605-8670-98aea31fe2a5`, check `105867581534` → `PASS`.
- Cloudflare-managed build token scope audit → `REVIEWED / OPERATIONAL / BROAD-SCOPE`.
- Workers Builds hardening compatibility research → `COMPLETE / PRODUCT-CONSTRAINT`: account-owned/per-Worker token cannot currently be used by Workers Builds.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

Cloudflare ↔ GitHub standard remains the only infrastructure priority until first real Cloudflare staging is verified.

Other project standardization work is paused.

## SYNC DEFECTS

- None known.
