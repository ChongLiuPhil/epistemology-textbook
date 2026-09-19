# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework — **Cloudflare staging complete / production security-profile decision**.

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

Cloudflare account-side staging 技术验证已经闭环：

- GitHub App connection：PASS；
- main Workers Build：PASS；
- non-production preview：PASS；
- main workers.dev runtime：PASS；
- preview runtime：PASS；
- 合并后的 main push 再次触发 Cloudflare Workers Build：PASS。

当前安全研究已经完成：

- Cloudflare-managed default build token 的权限比本项目实际需要更宽；
- individual Worker `Editor` 是 routine deploy 的理论最小权限；
- Cloudflare 当前 granular Worker token 能力要求 account-owned token；
- Workers Builds 当前只支持 user token，account-owned token support 尚未进入当前产品；
- 因此“Workers Builds + per-Worker account-owned Editor token”当前被产品能力阻塞，不应继续盲测。

现在需要的是生产安全 profile 决策，但在要求人类选择前先把 Profile B 推到可验证极限：

- Profile A：保留已验证的 Workers Builds 原生链路，接受当前 managed token scope，等待 Cloudflare 原生 granular support；
- Profile B：GitHub Actions + per-Worker account-owned Editor token。当前已在独立分支实现 validate-only / manual preview / manual production 候选 workflow；尚未创建任何新 token，也未启用自动部署。

## IMMEDIATE_NEXT_ACTION

1. main Workers Build 已通过 GitHub Cloudflare check 自动验证；
2. non-production preview build 已通过 GitHub Cloudflare check 自动验证；
3. workers.dev / preview runtime HTTP verification 已通过；
4. account-side staging 技术验证已闭环；
5. build-token hardening compatibility research 已完成：Workers Builds 当前 user-token-only；
6. 先让 Profile B candidate 的无凭据 validate-only CI 通过；
7. 只有候选实现被证明正确后，才由人类选择 production security profile A 或 B；
8. profile 决定后，再进入 Custom Domain / canonical URL / Pages legacy policy。

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
- Runtime HTTP verification run：`35431565729`
- Latest post-merge Cloudflare check：`105867581534`
- Latest post-merge Cloudflare Build ID：`6eb6fb9a-34c0-4605-8670-98aea31fe2a5`
- Build-token security audit：`docs/cloudflare-build-token-security.zh-CN.md`
- Staging runbook：`docs/cloudflare-staging-runbook.zh-CN.md`
- Human authorization guide：`docs/cloudflare-human-authorization.zh-CN.md`
- Current production：GitHub Pages
- Target delivery：Cloudflare Workers Static Assets via Workers Builds
- workers.dev staging：`https://epistemology-textbook.philosophy-research.workers.dev`
- main Cloudflare Build ID：`d6bc8b62-78ba-4a9e-98ea-7a049a539858`
- preview probe Build ID：`a12446a5-e341-48e4-8c22-1a184b1102c8`
- preview Version ID：`3f8a15d6-9994-4e90-839c-2144c8dc54b7`
- preview URL：`https://3f8a15d6-epistemology-textbook.philosophy-research.workers.dev`
- preview Alias：`https://cloudflare-preview-probe-epistemology-textbook.philosophy-research.workers.dev`

当前阶段不得修改 DNS、绑定正式 Custom Domain、停用 GitHub Pages 或把 token 写入仓库。
