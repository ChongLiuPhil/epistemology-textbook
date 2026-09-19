# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T023` — Cloudflare ↔ GitHub reusable Workers Builds standard — `COMPLETED / MAIN-VERIFIED`
- `WM-T024` — Cloudflare build-token hardening research — `COMPLETED / PRODUCT-CONSTRAINT`
- `WM-T025` — Cloudflare production security profile — `COMPLETED / PROFILE-A-SELECTED`
- `WM-T026` — Hardened External CI candidate — `COMPLETED / VALIDATE-ONLY-PASS`

## COMPLETED PPF TASKS

- `WM-T027` — adopt PPF visibility/access/canonical-identity semantics — `COMPLETED / PR-VALIDATED`
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
- [x] hardened external-CI validate-only candidate PASS
- [x] production security profile selected — Profile A
- [x] non-production preview build PASS
- [x] main workers.dev HTTP/content verification PASS
- [x] preview workers.dev HTTP/content verification PASS

Production cutover:
- [x] target canonical URL — `https://epistemology-textbook.philosophy-research.workers.dev/`
- [x] Cloudflare zone / Custom Domain eligibility — N/A for workers.dev canonical
- [x] Custom Domain — N/A for workers.dev canonical
- [ ] production verification
- [ ] GitHub Pages legacy policy
- [ ] canonical URL migration

## NEXT ACTIONS

1. PPF `21a53607...` downstream adoption 已完成 PR validation；保持 adopted commit 固定，后续 upstream 变化继续要求显式 adoption。
2. 保持已经验证通过的 Cloudflare-managed build token，不在稳定 staging 链路上继续盲测。
2. Profile B candidate 已验证：PR validate-only PASS，不需要 Cloudflare secret，不部署。
3. Profile A 已由人类选择；保留 Workers Builds native / managed user token，并记录 broad-scope risk acceptance。
4. target canonical URL 已选择 workers.dev；Custom Domain 路线 N/A；现在只处理 GitHub Pages legacy policy 与其后的 canonical migration verification。
5. Profile B 保留为未采用 fallback，不创建 deployment token、不启用 external CI deployment。
6. Future：Cloudflare Workers Builds 支持 account-owned per-Worker token 或 threat model 变化后，重新评估 Profile C / Profile B。

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

- GitHub Pages legacy policy remains unresolved before final cutover; target canonical URL is workers.dev and Custom Domain is N/A.
- Workers Builds currently supports user tokens only; this product constraint remains tracked, but the human has accepted Profile A for the current project.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING`

### CLR-002 — 外部参考 PDF 的公开分发权利
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript work; BLOCKING for repackaging/redistribution decisions`

### CLR-003 — GitHub Pages legacy policy
- Target canonical URL: `RESOLVED -> https://epistemology-textbook.philosophy-research.workers.dev/`
- Custom Domain: `NOT_APPLICABLE`
- Status: `WAITING-HUMAN`
- Severity: `BLOCKING FOR PRODUCTION CUTOVER, NOT FOR WORKERS.DEV STAGING`

## RECENTLY RESOLVED / PROMOTED

- PPF `21a5360727167bad6f399477ded073431645fa1d` visibility/access/canonical-identity downstream adoption → Governance `35451267209`, Web `35451267208`, Cloudflare Contract `35451267235`, Hardened candidate `35451267205` → `PASS`.
- Hardened External CI candidate `35435831128` → validate-only `PASS`; credential/preview/production deploy steps → `SKIPPED`.
- Cloudflare Workers Builds repository contract validation → Governance `35427051865`, Web `35427051858`, Contract CI `35427051853` → `PASS`.
- PPF Phase 1 source/profile/runtime validation → `COMPLETED / VERIFIED`.
- Repository-side Cloudflare readiness → `COMPLETED / PASS`.
- Cloudflare staging runbook + least-privilege model → `COMPLETED`.
- Canonical Web publication gate design → promoted into `Makefile`, `scripts/check_rendered_html.py`, and CI.
- Workers Builds machine contract → promoted into `cloudflare-builds.yaml` and `docs/cloudflare-readiness.yaml`.
- Main Workers Build `d6bc8b62-78ba-4a9e-98ea-7a049a539858` → `PASS`.
- Preview Workers Build `a12446a5-e341-48e4-8c22-1a184b1102c8`, Version `3f8a15d6-9994-4e90-839c-2144c8dc54b7` → `PASS`.
- Runtime HTTP verification `35431565729` → main + preview, each 5 pages + 30 local assets → `PASS`.
- Verified post-merge main Cloudflare checkpoint: project revision `71ad7c5cdfd9cb8cebdf9f4a3ac6a247959e0b15`, Cloudflare Build `93823dff-1206-4282-b037-24876840f0c6`, check `105904495866` → `PASS`.
- Checkpoint semantics intentionally replace a moving `latest_main_build` claim: later main pushes may create newer provider builds without invalidating this verified evidence checkpoint.
- Cloudflare-managed build token scope audit → `REVIEWED / OPERATIONAL / BROAD-SCOPE`; human risk acceptance recorded under Profile A.
- Workers Builds hardening compatibility research → `COMPLETE / PRODUCT-CONSTRAINT`: account-owned/per-Worker token cannot currently be used by Workers Builds.

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

Cloudflare staging is verified, Profile A is selected, and workers.dev is the selected target canonical URL. The GitHub Pages legacy-policy / canonical-migration line remains the only infrastructure priority until explicitly resolved.

Other project standardization work remains paused.

## SYNC DEFECTS

- None known.
