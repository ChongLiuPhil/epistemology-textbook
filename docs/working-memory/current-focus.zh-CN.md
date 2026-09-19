# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework — **Cloudflare ↔ GitHub standard integration / Workers Builds contract validation**.

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

当前 ChatGPT 会话没有真正暴露可调用的 Cloudflare account / Workers Builds MCP tool。

因此尚不能从本会话直接：

- 读取 Cloudflare account；
- 安装/确认 GitHub App connection；
- 创建/确认 Worker；
- 创建 Workers Builds triggers；
- 触发并读取首次 Cloudflare build。

这不是仓库设计 blocker，而是当前会话 account connector availability blocker。

## IMMEDIATE_NEXT_ACTION

1. 普通 Web CI、Governance、Cloudflare Build Contract CI 已全部 PASS；
2. 合并 repository standard；
3. 继续尝试建立 Cloudflare OAuth/MCP account context；
4. 一旦 account context 可用，由 AI 按 `cloudflare-builds.yaml` 自动完成 Git connection / Worker / triggers / preview build；
5. 若最终仍无法在当前 AI 客户端建立 MCP，则只要求人类完成 `docs/cloudflare-human-authorization.zh-CN.md` 中的最少授权步骤；
6. workers.dev staging PASS 前保持 GitHub Pages 为正式公开站点。

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

当前阶段不得修改 DNS、绑定正式 Custom Domain、停用 GitHub Pages 或把 token 写入仓库。
