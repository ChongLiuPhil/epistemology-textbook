# Cloudflare Phase 2 Staging Runbook

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**状态：** `PREPARED / ACCOUNT-SIDE-EXECUTION-PENDING`

## 1. 目标

在不影响当前 GitHub Pages production 的前提下，把已经通过 PPF Phase 1 验证的：

```text
canonical QMD/BibTeX
-> make check
-> quarto render --profile web
-> rendered HTML validation
-> _book/
```

部署到 Cloudflare Workers Static Assets 做 staging 验证。

本阶段不修改 canonical production URL，不停用 GitHub Pages，不自动修改 DNS。

## 2. 关键原则

### 2.1 Provisioning 与持续部署分离

Cloudflare 当前权限模型区分：

- **创建新 Worker**：需要 Workers product-level `Admin`；
- **部署到已存在 Worker**：只需要该 Worker 的 `Editor`；
- **部署时新增/修改 Route 或 Custom Domain**：除 Worker `Editor` 外，还需要对应 zone 的 `Workers Routes Write`。

因此本项目采用：

```text
one-time provisioning
    |
    +--> create/confirm Worker
    +--> optionally attach Custom Domain later
    |
long-lived GitHub Actions deployment
    |
    +--> individual Worker Editor only
```

长期 CI 不应保留为了创建 Worker 或修改 zone route 才需要的高权限。

官方参考：

- https://developers.cloudflare.com/workers/authorization/workers/
- https://developers.cloudflare.com/workers/authorization/
- https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/

## 3. Staging strategy

### 3.1 Target Worker

预期 Worker name：

`epistemology-textbook`

当前状态仍是 `unverified`：不能假设 Cloudflare 账户中已经存在它。

### 3.2 First staging endpoint

如果该 Worker 创建/确认成功，先使用其 Cloudflare-provided `workers.dev` endpoint 做 staging。

不要在第一次 deployment 前就把正式 Custom Domain 指向 Worker。

这使验证顺序保持：

```text
Pages production stays live
        |
        +--> target Worker on workers.dev
                  |
                  +--> verify full site
                  +--> verify links/assets/navigation
                  +--> verify deployment workflow
                  |
                  +--> only then consider Custom Domain
```

Cloudflare 官方说明 Worker 可部署到 `workers.dev` 或 Custom Domain；生产更适合 route / Custom Domain，而 `workers.dev` 可用于初始验证。

参考：

- https://developers.cloudflare.com/workers/static-assets/get-started/
- https://developers.cloudflare.com/workers/configuration/routing/

## 4. Account-side provisioning

以下操作必须在 Cloudflare 账户上下文中完成；当前 ChatGPT 会话无法验证或执行。

### Step A — confirm account

记录：

- Cloudflare account ID；
- 可使用的 Cloudflare zone；
- account owner / responsible operator；
- 是否已有名为 `epistemology-textbook` 的 Worker。

禁止把 account ID 或 token value 写入仓库文本。

### Step B — ensure Worker exists

如果 Worker **不存在**：

- 用 Cloudflare dashboard 手动创建，或
- 用一次性/临时 provisioning credential 创建。

创建 Worker 需要 product-level Workers `Admin`。

创建完成后，长期 GitHub CI token 不应继续保留该 Admin 权限。

如果 Worker **已经存在**：

- 确认它属于正确账户；
- 确认它可以被该 CI identity 以 individual Worker `Editor` 访问；
- 不要仅凭名称相同假定它就是本项目目标。

## 5. Long-lived CI credential

Cloudflare 的 GitHub Actions / Wrangler 非交互部署需要：

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`

建议长期 token：

- scope：individual Worker `epistemology-textbook`
- role：`Editor`
- 不授予 Worker delete 权限
- 不授予其他 Worker 访问
- 不授予 KV / R2 / D1 权限，因为本项目当前不用这些资源
- 不授予 zone route write，除非 CI 被明确设计为管理 Custom Domain/Route

GitHub repository secrets：

```text
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
```

token value 只能进入 GitHub Secrets / authorized secret store，不得提交到 Git。

Cloudflare 官方 GitHub Actions 文档要求 CI 使用 account ID + API token，并建议把 token scope 尽量收窄。

参考：

- https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/

## 6. Manual staging workflow

正式启用前，workflow 应保持**手动触发**，而不是 main push 自动部署。

建议逻辑：

```text
workflow_dispatch
-> checkout
-> Python
-> make check
-> Quarto
-> quarto render --profile web
-> python3 scripts/check_rendered_html.py
-> Wrangler deploy
-> record deployment URL
-> verify URL
```

示例文件：

`docs/examples/cloudflare-staging-workflow.yml`

它只是文档示例，不位于 `.github/workflows/`，因此不会自动执行。

## 7. Staging verification checklist

首次 `workers.dev` staging deployment 后至少验证：

- homepage 200；
- representative chapter pages 200；
- CSS / JS / images 正常；
- Quarto sidebar / TOC / navigation 正常；
- internal relative links 正常；
- external-link audit 不出现 Cloudflare-specific regression；
- repository/source links 正常；
- Chinese text / equations / citations 正常；
- no EPUB/PDF/DOCX/LaTeX exposed as unintended Web artifacts；
- deployment came from the expected Git commit；
- existing GitHub Pages URL 仍正常。

只有 staging PASS 后，`docs/cloudflare-readiness.yaml.validation.preview_deployment` 才可改为 `passed`。

## 8. Custom Domain provisioning

生产 Custom Domain 必须属于 active Cloudflare zone。

Cloudflare 当前要求：

- active Cloudflare zone；
- existing Worker；
- hostname 属于该 zone；
- hostname 不能与现有 CNAME 冲突。

Cloudflare 会为 Worker Custom Domain 创建相关 DNS 并管理证书。

参考：

- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/

### Recommended permission split

推荐把 Custom Domain 作为一次性 provisioning 操作：

- operator / temporary provisioning credential：
  - Worker access；
  - 对目标 zone 的 `Workers Routes Write`；
- ongoing GitHub CI：
  - individual Worker `Editor`；
  - 不管理 routes/domain。

这样日常内容发布不需要长期 zone-write 权限。

## 9. Canonical URL decision

当前：

`https://chongliuphil.github.io/epistemology-textbook/`

属于 GitHub 的 `github.io` 域名，不能直接变成 Cloudflare Worker Custom Domain。

正式 cutover 前必须确认一个由作者控制、并由 Cloudflare 管理的 domain/subdomain。

例如逻辑上可以是：

`<book-subdomain>.<owned-domain>`

但实际 domain 在人类确认前保持 `unresolved`。

## 10. Cutover sequence

只有 staging 与 domain prerequisites 全部通过后：

1. attach/verify Custom Domain；
2. 在 Cloudflare URL 上做完整 production-like verification；
3. 决定 GitHub Pages legacy policy；
4. 更新 `publishing.yaml` target/canonical URL；
5. 更新 `_quarto-web.yml` 的 `site-url` 与任何 canonical public links；
6. 让 source/render validation 重新通过；
7. 才把 Cloudflare deploy 加入 main-push publication gate；
8. 先保留 Pages 直到 Cloudflare production verification 完成；
9. 最后再根据 legacy policy 决定 mirror / redirect / retirement。

## 11. GitHub Pages legacy policy

正式切换前必须选择并记录：

- `mirror`：Pages 继续提供相同内容；
- `legacy-with-canonical`：Pages 保留，但页面 canonical 指向新域名；
- `redirect`：Pages 尽可能引导到新域名；
- `retire`：确认所有重要入口迁移后停止 Pages。

目前：`UNRESOLVED`。

## 12. 当前结论

**Staging runbook: PREPARED.**

**Cloudflare account-side access: UNAVAILABLE IN CURRENT CHATGPT SESSION.**

**Worker existence: UNVERIFIED.**

**GitHub Cloudflare secrets: UNVERIFIED.**

**Custom Domain: UNRESOLVED.**

**Production cutover: BLOCKED.**
