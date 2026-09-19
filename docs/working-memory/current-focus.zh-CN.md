# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework — **Phase 2 repository readiness complete / account-side staging pending**.

## CURRENT_OBJECTIVE

仓库侧 Cloudflare readiness 已实现并通过 CI 验证：

- `wrangler.jsonc` 保持纯 static-assets Worker 形态；
- `assets.directory = ./_book`；
- `publishing.yaml` 明确 current provider = GitHub Pages、target provider = Cloudflare Workers；
- `docs/cloudflare-readiness.yaml` 记录账户侧未知状态；
- `scripts/check_cloudflare_readiness.py` 防止 prerequisites 未完成时提前出现 `wrangler deploy` / Cloudflare deploy action；
- `make check` 已纳入 readiness validator。

当前目标不是切换生产，而是把 repository side 固化为：

`REPOSITORY-READY / ACCOUNT-SIDE-UNVERIFIED / CUTOVER-BLOCKED`

## PRIMARY_BLOCKER

Cloudflare account-side prerequisites 未验证：

- Cloudflare account / account ID；
- Worker target；
- GitHub Secrets 中的 deployment credentials；
- Cloudflare-managed zone / target canonical URL；
- preview/staging deployment；
- GitHub Pages legacy URL policy。

当前 ChatGPT 环境没有可用 Cloudflare account connector，因此不能把这些未知项升级成“已配置”。

## IMMEDIATE_NEXT_ACTION

1. repository-side readiness PR #22 已合并并在 `main` 验证通过；
2. Cloudflare staging runbook 与非执行 workflow example 已准备；
3. 保持 GitHub Pages production 不变；
4. 账户侧建立 Cloudflare deployment context 后，先确认/创建目标 Worker；
5. 配置最小权限 CI credential 后，通过 `workers.dev` 做 staging deployment；
6. staging PASS 后再讨论 Custom Domain 与生产 cutover。

## HANDOFF POINTERS

- PPF contract：`publishing.yaml`
- Cloudflare readiness audit：`docs/cloudflare-readiness.zh-CN.md`
- Machine readiness state：`docs/cloudflare-readiness.yaml`
- Readiness validator：`scripts/check_cloudflare_readiness.py`
- Wrangler：`wrangler.jsonc`
- Staging runbook：`docs/cloudflare-staging-runbook.zh-CN.md`
- Non-executable workflow example：`docs/examples/cloudflare-staging-workflow.yml`
- Current production：GitHub Pages
- Target provider：Cloudflare Workers Static Assets
- Readiness merge commit：`f0af87ea5c060a69141eeb82c5992de8126af55d`
- Main Governance run：`35422807542`
- Main Web/Pages run：`35422807549`
- Main External Link Audit：`35422807546`

本阶段不得添加 active Cloudflare deployment workflow，除非 account-side prerequisites 已被实际验证并持久化。
