# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T023` — Cloudflare ↔ GitHub reusable Workers Builds standard — `COMPLETED / MAIN-VERIFIED`
- `WM-T024` — Cloudflare build-token hardening — `IN-PROGRESS / COMPATIBILITY-VALIDATION`

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
- [ ] hardened least-privilege replacement compatibility validated
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

1. 保持已经验证通过的 Cloudflare-managed build token，不在稳定链路上盲目替换。
2. 验证 Workers Builds 当前是否能使用满足 existing Worker deploy 的更小权限 custom token。
3. 如果兼容，重新运行 main / preview / runtime verification 后迁移。
4. 如果当前产品不兼容，则把 broad default token 作为显式 temporary risk，等待 Cloudflare Builds 对更细粒度 token 的稳定支持。
5. hardening 结论明确后，再进入 Custom Domain / canonical URL / Pages legacy policy。

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

- Cloudflare-managed default token is broader than required;
- Workers Builds compatibility with the preferred per-Worker least-privilege token model still needs validation.

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
- Cloudflare-managed build token scope audit → `REVIEWED / OPERATIONAL / NOT-YET-HARDENED`.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

Cloudflare ↔ GitHub standard remains the only infrastructure priority until first real Cloudflare staging is verified.

Other project standardization work is paused.

## SYNC DEFECTS

- None known.
