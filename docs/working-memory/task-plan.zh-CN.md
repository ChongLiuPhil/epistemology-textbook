# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T023` — Cloudflare ↔ GitHub reusable Workers Builds standard — `IN-PROGRESS / CI-PENDING`
- `WM-T021` — Cloudflare account-side staging context — `WAITING-CONNECTOR-AUTHORIZATION`

## COMPLETED PPF TASKS

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
- [ ] PR normal Web CI PASS
- [ ] PR Cloudflare Build Contract CI PASS
- [ ] merge + main CI PASS

Account connection:
- [ ] Cloudflare OAuth/MCP actually callable by current AI
- [ ] Cloudflare GitHub App authorized for selected repository
- [ ] repository connection verified
- [ ] Worker `epistemology-textbook` verified/created
- [ ] production trigger configured
- [ ] preview trigger configured
- [ ] build token reviewed
- [ ] first workers.dev / preview build PASS

Production cutover:
- [ ] target canonical URL
- [ ] Cloudflare zone / Custom Domain eligibility
- [ ] Custom Domain
- [ ] production verification
- [ ] GitHub Pages legacy policy
- [ ] canonical URL migration

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

The current ChatGPT session does not expose a callable Cloudflare account/Builds MCP tool.

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

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

Cloudflare ↔ GitHub standard remains the only infrastructure priority until first real Cloudflare staging is verified.

Other project standardization work is paused.

## SYNC DEFECTS

- None known.
