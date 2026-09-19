# Working Memory — Task Plan

**状态：** ACTIVE TASK PLAN

## ACTIVE TASKS

- `WM-T029` — reconcile PR #18 content/form improvements with current PPF/Workers baseline — `COMPLETED / MAIN-MERGED`
- `WM-T030` — Chapter 1 academic / pedagogical / citation review — `COMPLETED / ROUND2-MAIN-VERIFIED`
- `WM-T031` — Chapter 2 academic / pedagogical / citation review — `ROUND1 / VALIDATION-PENDING`
- `WM-T023` — Cloudflare ↔ GitHub reusable Workers Builds standard — `COMPLETED / MAIN-VERIFIED`
- `WM-T024` — Cloudflare build-token hardening research — `COMPLETED / PRODUCT-CONSTRAINT`
- `WM-T025` — Cloudflare production security profile — `COMPLETED / PROFILE-A-SELECTED`
- `WM-T026` — Hardened External CI candidate — `COMPLETED / VALIDATE-ONLY-PASS`
- `WM-T028` — workers.dev canonical cutover + GitHub Pages retirement — `COMPLETED / HUMAN-CONFIRMED-UNPUBLISH`

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

> Stable baseline: workers.dev canonical cutover is implemented and verified.
> Security baseline: production security profile selected — Profile A; broad-scope risk acceptance remains recorded; `least_privilege: false` remains explicit.

- [x] target canonical URL — `https://epistemology-textbook.philosophy-research.workers.dev/`
- [x] Cloudflare zone / Custom Domain eligibility — N/A for workers.dev canonical
- [x] Custom Domain — N/A for workers.dev canonical
- [x] post-cutover production verification
- [x] GitHub Pages legacy policy — `RETIRE`
- [x] canonical URL migration — repository config implemented
- [x] GitHub Pages current deployment unpublish — repository-owner human-confirmed

## NEXT ACTIONS

1. Validate Chapter 2 Round 1 on current main architecture.
2. Merge Round 1 only if Governance + Web + Cloudflare contract/runtime + link audit pass.
3. Run Chapter 2 Round 2 for structural repetition, chapter load, and remaining citation/attribution gaps.
4. Escalate only genuine cross-chapter Architecture changes for explicit human approval.
5. Keep Profile A / Workers Builds stable; revisit Profile B/C only if provider capability or threat model materially changes.

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

- GitHub Pages legacy policy is resolved as `RETIRE`; workers.dev post-cutover verification is PASS; provider-side unpublish is human-confirmed complete. No remaining cutover blocker.
- Workers Builds currently supports user tokens only; this product constraint remains tracked, but the human has accepted Profile A for the current project.

## PENDING HUMAN DECISIONS / CLARIFICATIONS

### CLR-001 — 项目正式许可
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING`

### CLR-002 — 外部参考 PDF 的公开分发权利
- Status: `WAITING-HUMAN`
- Severity: `NON-BLOCKING for manuscript work; BLOCKING for repackaging/redistribution decisions`


## RECENTLY RESOLVED / PROMOTED

- WM-T029 PR #18 reconciliation → PR #39 merged as `3e36d5dc015d8224ec6e6e98a952c5d77c872eee`; Governance `35456091399`, Web `35456091339`, Cloudflare Contract `35456091266`, Hardened candidate `35456091221`, Runtime `35456091331` → `PASS`.
- workers.dev canonical cutover post-merge verification → revision `63510364ed40a97faf190c484dd80afc91971ecb`, runtime run `35453967021`, runtime check `105925881599`, Cloudflare provider check `105926103705`, build `42aa93fe-d9b6-49e4-80be-a849951a6b9d` → `PASS`.
- CLR-003 GitHub Pages legacy policy → human decision `RETIRE`; D010 recorded; canonical config migration implemented; provider-side `Unpublish site` human-confirmed complete on 2026-09-20.
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

- WM-T030 Round 1 → merge `62eae7d1f30f6b28eace1d51abc5433fd42ddbcb`; Governance `35471021367`, Web `35471021383`, Cloudflare Contract `35471021450`, Runtime `35471021366`, External Link Audit `35471021375` → `PASS`.
- WM-T030 Round 2 → merge `db1914fb248a503e6dc84424310427bfba254966`; Governance `35471217039`, Web `35471216984`, Cloudflare Contract `35471217109`, Runtime `35471217023`, External Link Audit `35471217048` → `PASS`.
- WM-T030 Chapter 1 audit → `COMPLETED / ROUND2-MAIN-VERIFIED`; no Architecture redistribution promoted.
- During chapter review, flag passages that catalogue thinkers/schools without a clear problem-function.
- If a formal publisher or print specification is later chosen, add provider/channel-specific PDF layout constraints without changing canonical manuscript semantics.
- No further routing/cutover task is active.

## STRUCTURAL WATCH

- Chapter 1 redistribution watch → `CLOSED / NOT-PROMOTED`. Current chapter-length/subsection comparison does not justify a structural move; forward scope links are sufficient for now. Reopen only if later reading/teaching evidence shows a concrete overload or dependency problem.

## SYNC DEFECTS

- None known.
