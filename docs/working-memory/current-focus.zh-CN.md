# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework — **Cloudflare staging complete / Profile A selected / canonical cutover planning**.

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

人类作者已选择 **Profile A — Workers Builds Native**：

- 保留已验证的 Workers Builds 原生链路；
- 明确接受当前 Cloudflare-managed user token 的已知较宽 scope 作为当前项目安全权衡；
- `least_privilege: false` 保持不变，不把 broad token 描述成 least privilege；
- Profile B 继续作为未采用 fallback；
- Profile C 继续等待 provider 原生 granular support。

## IMMEDIATE_NEXT_ACTION

1. main Workers Build 已通过 GitHub Cloudflare check 自动验证；
2. non-production preview build 已通过 GitHub Cloudflare check 自动验证；
3. workers.dev / preview runtime HTTP verification 已通过；
4. account-side staging 技术验证已闭环；
5. build-token hardening compatibility research 已完成：Workers Builds 当前 user-token-only；
6. Profile B candidate 无凭据 validate-only CI 已通过（run `35435831128`）；
7. production security profile：Profile A 已由人类明确选择并记录；
8. 当前进入 Custom Domain / canonical URL / Pages legacy policy 决策与验证。

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
- Verified post-merge Cloudflare checkpoint check：`105904495866`
- Verified post-merge Cloudflare checkpoint Build ID：`93823dff-1206-4282-b037-24876840f0c6`
- Verified checkpoint project revision：`71ad7c5cdfd9cb8cebdf9f4a3ac6a247959e0b15`
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

Profile A 的选择已经解除 security-profile blocker，但不等于 canonical cutover approval。当前仍不得在 target canonical URL / Custom Domain 与 GitHub Pages legacy policy 未明确前修改 DNS、绑定正式 Custom Domain或停用 GitHub Pages；token 继续不得写入仓库。
