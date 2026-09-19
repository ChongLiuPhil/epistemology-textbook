# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T023` — Cloudflare ↔ GitHub reusable Workers Builds standard — `COMPLETED / MAIN-VERIFIED`
- `WM-T021` — Cloudflare account-side staging context — `IN-PROGRESS / PREVIEW-RUNTIME-VERIFYING`

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
- [x] PR normal Web CI PASS
- [x] PR Cloudflare Build Contract CI PASS
- [x] merge + main CI PASS

Account connection:
- [ ] Cloudflare OAuth/MCP actually callable by current AI
- [x] Cloudflare GitHub App authorized for selected repository
- [x] repository connection verified
- [x] Worker `epistemology-textbook` verified/created
- [x] production trigger configured and main build PASS
- [x] preview trigger configured; runtime test in progress
- [ ] build token present; least-privilege review pending
- [ ] non-production preview build PASS

Production cutover:
- [ ] target canonical URL
- [ ] Cloudflare zone / Custom Domain eligibility
- [ ] Custom Domain
- [ ] production verification
- [ ] GitHub Pages legacy policy
- [ ] canonical URL migration

## NEXT ACTIONS

1. 让普通 Web CI 与 Cloudflare Build Contract CI 全部 PASS。
2. 合并 Workers Builds 标准化仓库契约。
3. 继续尝试 Cloudflare OAuth/MCP account context。
4. account context 一旦可用，由 AI 根据 `cloudflare-builds.yaml` 自动创建/验证 Worker、repo connection、production/preview triggers 与 first preview build。
5. 若当前 AI 客户端仍无法接 Cloudflare MCP，人类只执行授权指南中的必要授权步骤。
6. workers.dev staging PASS 前不切 production。

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

- preview probe build is still running;
- workers.dev HTTP/content verification is blocked by current ChatGPT network-fetch limitations;
- Cloudflare-managed build-token least-privilege review remains pending.

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

## CLARIFICATION COMPLETION RULE

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

## TODO / BACKLOG

Cloudflare ↔ GitHub standard remains the only infrastructure priority until first real Cloudflare staging is verified.

Other project standardization work is paused.

## SYNC DEFECTS

- None known.
