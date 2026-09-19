# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework — **Cloudflare account-side Workers Builds runtime validation**.

## CURRENT_OBJECTIVE

把 Cloudflare ↔ GitHub 接入固化为可复用范本，而不是只完成一次临时部署。

当前首选架构：

```text
GitHub repository
    |
    +--> GitHub Actions
    |      make web-publish-check
    |
    +--> Cloudflare Workers Builds
           bash scripts/cloudflare_build.sh
             -> pinned Quarto
             -> make web-publish-check
           preview -> npm run cloudflare:preview
           main    -> npm run cloudflare:deploy
```

已在当前分支实现：

- `make web-publish-check` 作为唯一 Web publication quality gate；
- GitHub Actions 改为调用该 gate；
- `cloudflare-builds.yaml` 作为 Workers Builds 机器契约；
- Node 24 / Wrangler 4.135.0 / Quarto 1.10.18 固定；
- Cloudflare build wrapper 可从没有 Quarto 的环境安装并校验固定版本；
- 独立 Cloudflare Build Contract CI，不执行 deployment；
- 非技术操作者授权指南；
- Workers Builds + GitHub App + Cloudflare OAuth/MCP 成为默认方案；
- GitHub Actions + Wrangler token 降为 fallback。

## PRIMARY_BLOCKER

Cloudflare ↔ GitHub account-side connection 已实际建立，不再是 blocker：

- Cloudflare account：human-confirmed；
- GitHub App：通过 GitHub check-run 自动验证；
- repository connection：verified；
- Worker target：verified；
- main production-branch trigger：真实 build PASS；
- workers.dev endpoint：已分配。

当前剩余 blocker：

- non-production preview build 仍在运行；
- 当前 ChatGPT Web/HTTP 工具无法直接抓取新 workers.dev endpoint，因此页面内容验证尚未由 AI 自动完成；
- Cloudflare-managed build token 的最小权限安全审计尚未完成；
- Custom Domain / canonical URL / GitHub Pages legacy policy 尚未决定。

## IMMEDIATE_NEXT_ACTION

1. main Workers Build 已通过 GitHub Cloudflare check 自动验证；
2. 等待 preview probe branch 的 Cloudflare build 完成；
3. preview PASS 后删除 probe branch；
4. 完成 workers.dev 页面内容验证；
5. 对 Cloudflare-managed build token 做最小权限审计；
6. staging 全部 PASS 后再进入 Custom Domain / canonical URL / Pages legacy policy。

## HANDOFF POINTERS

- Machine build contract：`cloudflare-builds.yaml`
- Canonical Web gate：`make web-publish-check`
- Cloudflare wrapper：`scripts/cloudflare_build.sh`
- Pinned Quarto installer：`scripts/ensure_quarto.sh`
- Wrangler：`wrangler.jsonc`
- Machine readiness state：`docs/cloudflare-readiness.yaml`
- Governance validation run：`35427051865`
- GitHub Web validation run：`35427051858`
- Cloudflare Build Contract run：`35427051853`
- Staging runbook：`docs/cloudflare-staging-runbook.zh-CN.md`
- Human authorization guide：`docs/cloudflare-human-authorization.zh-CN.md`
- Current production：GitHub Pages
- Target delivery：Cloudflare Workers Static Assets via Workers Builds
- workers.dev staging：`https://epistemology-textbook.philosophy-research.workers.dev`
- main Cloudflare Build ID：`d6bc8b62-78ba-4a9e-98ea-7a049a539858`
- preview probe Build ID：`a12446a5-e341-48e4-8c22-1a184b1102c8`

当前阶段不得修改 DNS、绑定正式 Custom Domain、停用 GitHub Pages 或把 token 写入仓库。
