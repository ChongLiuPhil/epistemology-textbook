# Cloudflare Phase 2 Readiness Audit

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**状态：** `REPOSITORY-READY / ACCOUNT-SIDE-UNVERIFIED / CUTOVER-BLOCKED`

## 1. 目的

本文件记录 PPF Phase 2 在**不改变当前 GitHub Pages production path** 的前提下，对 Cloudflare Workers Static Assets 迁移条件进行的 readiness 审计。

当前生产仍是：

```text
GitHub main
-> source validation
-> Quarto web profile
-> rendered HTML validation
-> GitHub Pages
```

目标架构仍是：

```text
GitHub main
-> source validation
-> Quarto web profile
-> rendered HTML validation
-> Wrangler deploy
-> Cloudflare Workers Static Assets
```

Cloudflare 不成为 canonical source，也不独立构建书稿。

## 2. 仓库侧已满足条件

### Wrangler configuration

当前 `wrangler.jsonc`：

- Worker name：`epistemology-textbook`
- compatibility date：已设置
- static assets directory：`./_book`
- 无 `main` Worker script
- 无 assets binding

这符合纯 static-assets Worker 的最小形态：仓库只需要把已经验证的 `_book/` 作为静态资产交给 Workers。

### PPF source/build boundary

已验证：

- canonical source：QMD + BibTeX；
- Web output：`_book/`；
- EPUB/PDF/DOCX/LaTeX：独立 on-demand profiles；
- current production provider：GitHub Pages；
- target provider：Cloudflare Workers；
- current Cloudflare migration status：`staged`。

### No premature deployment path

当前 active GitHub Actions workflows 中**不应**存在：

- `cloudflare/wrangler-action`
- `wrangler deploy`
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

只要账户、Worker target、canonical URL 与 preview verification 尚未确认，自动 Cloudflare deployment 必须保持关闭。

## 3. Cloudflare 官方约束

Cloudflare Workers Static Assets 使用 Wrangler 的 `assets.directory` 指向静态输出目录。纯静态 Worker 不需要为了部署静态资产而增加 Worker script。官方文档：

- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/static-assets/binding/

GitHub Actions 中的非交互式 Wrangler deployment 需要：

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`

Cloudflare 官方建议 API token 按最小权限、账户/zone 范围尽量收窄，并把 token 存在 CI secret 中，而不是仓库。官方 action 示例使用 `cloudflare/wrangler-action@v3`：

- https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/

生产域名方面，Worker Custom Domain 需要：

- active Cloudflare zone；
- existing Worker；
- 目标 hostname 属于该 zone；
- hostname 不能与现有 CNAME 冲突。

Cloudflare 会为 Custom Domain 建立相应 DNS 并处理证书：

- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- https://developers.cloudflare.com/workers/configuration/routing/

## 4. 当前 Pages URL 与未来 canonical URL

当前 production URL：

`https://chongliuphil.github.io/epistemology-textbook/`

这个 hostname 属于 `github.io`，不是本项目可交给 Cloudflare 管理的 zone。

因此 Cloudflare production cutover **不能**简单把同一个 GitHub Pages hostname 变成 Worker Custom Domain。

Phase 2 必须明确选择：

1. 一个由作者控制、并由 Cloudflare 管理 DNS 的 domain/subdomain，作为新的 canonical production URL；或
2. 在 staging 阶段使用 Workers preview / `workers.dev`，但不把它自动视为最终 canonical URL。

GitHub Pages 原 URL 在 cutover 后是保留为 mirror、保留为 legacy URL、还是设置页面级 redirect/canonical，需要单独决定。

## 5. 账户侧尚未验证条件

本次 ChatGPT 环境没有可用的 Cloudflare account connector，因此以下状态不能从账户侧核实：

- Cloudflare account ID；
- 是否已经存在名为 `epistemology-textbook` 的 Worker；
- GitHub repository secrets 是否已经配置；
- 可用 Cloudflare zone；
- target custom domain；
- DNS conflict；
- certificate state；
- preview deployment；
- production deployment。

机器可读状态见：

`docs/cloudflare-readiness.yaml`

这些未知项必须保持 `unverified / unresolved`，不能由 AI 猜测成已配置。

## 6. 最小权限部署方案

详细执行手册：

`docs/cloudflare-staging-runbook.zh-CN.md`

当前权限模型进一步区分：

- 一次性 Worker provisioning；
- 一次性 Custom Domain provisioning；
- 长期 GitHub Actions 内容部署。

Cloudflare 当前权限规则下，创建 Worker 需要 Workers product-level `Admin`；对已存在的指定 Worker 部署只需要该 Worker 的 `Editor`；如果部署过程修改 Custom Domain/Route，则还需要目标 zone 的 `Workers Routes Write`。

因此推荐先由人工/临时 provisioning credential 创建并确认 Worker，再为长期 GitHub Actions 使用仅限该 Worker 的 `Editor` token。Custom Domain 也优先作为独立 provisioning 操作处理，使日常内容发布不必长期持有 zone-write 权限。

当账户侧条件具备后，推荐仍由 GitHub Actions 作为唯一 publication gate：

1. `make check`
2. `quarto render --profile web`
3. `scripts/check_rendered_html.py`
4. 只有上述全部通过后，main push 才运行 `wrangler deploy`
5. Wrangler 从 GitHub Secrets 读取 Cloudflare account ID / API token
6. 部署后验证 staging/production URL

不要让 Cloudflare 自己在另一个独立 Git build pipeline 中绕过当前 scholarly validation。

## 7. Cutover gates

正式把 Web automatic deployment 从 GitHub Pages 切到 Cloudflare 前，必须全部满足：

- [x] Quarto Web profile 已真实运行验证
- [x] `_book/` rendered HTML integrity 已验证
- [x] Wrangler static-assets config 已存在
- [x] repository-side readiness validator 已存在
- [ ] Cloudflare account access 已验证
- [ ] Worker target 已验证/创建
- [ ] GitHub secrets 已配置
- [ ] staging/preview deployment PASS
- [ ] target canonical URL 已确认
- [ ] Cloudflare zone / Custom Domain 条件已确认
- [ ] GitHub Pages legacy URL policy 已确认
- [ ] production deployment PASS
- [ ] production HTTP verification PASS

在所有未勾选项完成前：

`CUTOVER = BLOCKED`

## 8. 当前结论

**Repository-side readiness: PASS.**

**Account-side readiness: UNVERIFIED.**

**Production cutover: BLOCKED.**

下一步不是改掉 Pages workflow，而是建立/连接 Cloudflare account-side deployment context，然后先做 staging deployment。
