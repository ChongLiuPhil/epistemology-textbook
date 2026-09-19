# Cloudflare Workers Builds Build Token Security Audit

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**状态：** `REVIEWED / OPERATIONAL / NOT-YET-HARDENED`

## 1. 当前 token

Cloudflare Workers Builds 当前使用 Cloudflare 自动创建/管理的：

`epistemology-textbook build token`

token secret 不进入 Git、不进入聊天、不进入本文档。

该 token 已被真实验证能够完成：

- main Workers Build；
- `wrangler deploy`；
- non-production `wrangler versions upload`；
- 后续 main push 自动 build/deploy。

因此：

**Operational compatibility: PASS.**

## 2. Cloudflare 当前默认自动 token 权限

Cloudflare 当前官方 Workers Builds 文档说明，选择 “Create new token” 时自动生成的 user token 默认包含：

### Account

- Account Settings — read
- Workers Scripts — edit
- Workers KV Storage — edit
- Workers R2 Storage — edit

### Zone

- Workers Routes — edit
- scope：账户中的 all zones

### User

- User Details — read
- Memberships — read

对于本项目当前的纯 static-assets Worker，这个权限范围明显大于日常内容部署实际需要。

因此：

**Least privilege: NOT YET SATISFIED.**

官方参考：

- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- https://developers.cloudflare.com/workers/authorization/workers/

## 3. 本项目实际需要的能力

本项目日常 Workers Builds 只执行：

Production:

`wrangler deploy`

Preview:

`wrangler versions upload`

Worker 已经存在：

`epistemology-textbook`

当前 `wrangler.jsonc` 不管理：

- KV；
- R2；
- D1；
- Routes；
- Custom Domain。

Cloudflare 当前 Workers permissions 文档说明：

- 部署 existing Worker：minimum = `Editor` for that Worker；
- upload version：minimum = `Editor` for that Worker；
- 创建新 Worker：需要 product-level `Admin`；
- 修改 Routes / Custom Domains：需要 Worker `Editor` + affected zone 的 `Workers Routes Write`。

因此本项目长期 deployment credential 的理想权限是：

`Individual Worker: epistemology-textbook -> Editor`

而不是：

`all Workers + KV + R2 + all-zone route edit`

## 4. 当前产品兼容性约束

Cloudflare Workers Builds 当前 configuration 文档同时说明：

- Builds 当前使用 user token；
- account-owned token support 尚未作为当前默认支持能力。

而 Cloudflare 2026-09 的 granular Workers roles 已经支持：

- API token；
- individual Worker scope；
- `Editor` role。

这意味着“最小理论权限”已经明确，但 **Workers Builds 当前 token picker 与最新 per-Worker account-owned token model 的完整兼容路径仍需要真实验证**。

因此本项目不在已经稳定工作的 staging pipeline 上盲目替换 token。

## 5. 当前安全决策

当前状态：

```text
Cloudflare-managed default token
        |
        +--> operationally verified
        +--> secret kept outside Git
        +--> broader than necessary
        |
        +--> HARDENING REQUIRED BEFORE FINAL PRODUCTION CUTOVER
```

本阶段：

- 保留当前 token；
- 不复制 token secret；
- 不在 GitHub Secrets 中重复保存；
- 不把它复用于其他 Worker；
- 不增加新权限；
- Custom Domain provisioning 与 daily deployment credential 保持分离。

## 6. Hardened target

优先目标：

```text
one deployment identity
-> only epistemology-textbook
-> Worker Editor
-> no KV/R2/D1 access
-> no zone route write for routine deploy
```

如果 Workers Builds 当前 UI/API 尚不能稳定使用这一 token 类型，则：

1. 保持当前 build token；
2. 将 broad scope 明确记录为接受中的 temporary infrastructure risk；
3. 等 Cloudflare Workers Builds 正式支持 compatible account-owned/per-Worker build token；
4. 再迁移并重新运行 main + preview + runtime verification。

## 7. Custom Domain 权限

Custom Domain 不应由 daily build token 管理。

正式绑定域名时，采用：

```text
temporary provisioning authority
-> Worker Editor
-> target zone Workers Routes Write
-> attach Custom Domain
-> verify

then

daily deployment credential
-> Worker Editor only
```

## 8. 安全验收条件

Build-token hardening 只有满足以下条件才可标记 PASS：

- [ ] replacement token 类型被 Workers Builds 当前产品明确支持；
- [ ] token scope 不超出所需 Worker / deployment capability；
- [ ] main build PASS；
- [ ] non-production preview PASS；
- [ ] workers.dev runtime HTTP PASS；
- [ ] 不需要 KV / R2 / D1 权限；
- [ ] routine deploy 不需要 all-zone Workers Routes write；
- [ ] old broad token 被安全撤销或不再被 trigger 使用。

在此之前：

`BUILD TOKEN SECURITY = REVIEWED / NOT HARDENED`
