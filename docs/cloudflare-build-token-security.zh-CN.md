# Cloudflare Workers Builds Build Token Security Audit

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**状态：** `REVIEWED / OPERATIONAL / PRODUCT-CONSTRAINT IDENTIFIED / HUMAN PROFILE DECISION PENDING`

## 1. 当前 token

Cloudflare Workers Builds 当前使用 Cloudflare 自动创建/管理的：

`epistemology-textbook build token`

token secret 不进入 Git、不进入聊天、不进入本文档。

它已经真实完成并通过：

- main Workers Build；
- `wrangler deploy`；
- non-production `wrangler versions upload`；
- preview URL；
- main workers.dev runtime；
- preview runtime；
- 后续 main push 自动 build/deploy。

因此：

**Operational compatibility: PASS.**

## 2. 当前默认 token 的权限

Cloudflare 当前 Workers Builds configuration 文档说明，自动创建的 build user token 默认包含：

### Account

- Account Settings — read
- Workers Scripts — edit
- Workers KV Storage — edit
- Workers R2 Storage — edit

### Zone

- Workers Routes — edit
- all zones

### User

- User Details — read
- Memberships — read

对于本项目当前的纯 static-assets Worker，这明显宽于日常部署实际需要。

因此：

**Least privilege: NOT SATISFIED by the managed default token.**

官方参考：

- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- https://developers.cloudflare.com/workers/authorization/workers/
- https://developers.cloudflare.com/workers/authorization/

## 3. 本项目日常部署真正需要什么

日常执行只有：

Production:

`wrangler deploy`

Preview:

`wrangler versions upload`

Worker 已经存在：

`epistemology-textbook`

Cloudflare 当前 Workers roles 文档给出的 minimum：

- deploy existing Worker → Worker `Editor`；
- upload version → Worker `Editor`；
- create new Worker → Workers product `Admin`；
- change Route / Custom Domain → Worker `Editor` + affected zone `Workers Routes Write`。

因此理论最小长期 deployment identity 是：

`Individual Worker: epistemology-textbook -> Editor`

不需要：

- KV；
- R2；
- D1；
- all-zone route write；
- create/delete arbitrary Workers。

## 4. 2026-09 当前产品约束

这里存在一个已经由官方文档确认的产品边界：

### Workers Builds

Workers Builds 当前：

- 支持 **user token**；
- **不支持 account-owned token**；
- Cloudflare 文档明确写明 account-owned token support 尚未成为当前能力。

### Granular Workers permissions

Cloudflare 新权限模型已经支持：

- account-owned API token；
- individual Worker scope；
- `Editor` role；
- Wrangler 使用该 token 做 granular authorization。

也就是说：

```text
理想 least-privilege token
= account-owned
+ individual Worker
+ Editor
```

已经存在于 Cloudflare 的通用 Workers 权限模型中，

但：

```text
Workers Builds
currently accepts only user tokens
```

所以当前 preferred Workers Builds 路线**不能稳定使用我们真正想要的 per-Worker account-owned deployment token**。

这不再是“尚未验证”，而是：

**CURRENT PRODUCT CONSTRAINT.**

## 5. 不做的事情

本项目不会为了理论 hardening 去盲目更换一个已经稳定工作的 build token。

尤其不做：

- 不删除当前 token；
- 不滚动当前 token；
- 不把 token secret 复制到 GitHub；
- 不把 secret 发到聊天；
- 不在没有 rollback path 时尝试未知 custom user-token permission 组合；
- 不把 Custom Domain provisioning 权限加入 daily token。

## 6. 可选安全 profile

### Profile A — Workers Builds Native

```text
Cloudflare GitHub App
-> Workers Builds
-> Cloudflare-managed user build token
-> wrangler deploy / versions upload
```

优点：

- 原生 Git integration；
- preview/production trigger 简单；
- 无需把 Cloudflare secret 放入 GitHub；
- 已在本项目真实验证。

缺点：

- 当前默认 token scope 偏宽；
- 当前不能使用 per-Worker account-owned token。

当前状态：

`OPERATIONAL / VERIFIED / BROAD TOKEN SCOPE`

### Profile B — Hardened External CI

```text
GitHub Actions
-> account-owned Cloudflare API token
-> Individual Worker: epistemology-textbook
-> Editor
-> wrangler deploy
```

优点：

- 可以实现真正 per-Worker least privilege；
- token 可作为 durable service principal；
- 不需要 KV/R2/zone-route 权限做 routine deployment。

代价：

- 需要额外创建 account-owned token；
- 需要把 token + account ID 安全存入 GitHub Secrets；
- 需要由 GitHub Actions 接管 Cloudflare deployment；
- 需要重新设计/验证 preview deployment 与 trigger semantics；
- 人类初次配置步骤更多。

当前状态：

`AVAILABLE / NOT ADOPTED / REQUIRES MIGRATION VALIDATION`

### Profile C — Future Native Granular

```text
Workers Builds
-> account-owned per-Worker Editor token
```

这是理想终局：

- 保留 Workers Builds Git integration；
- 同时满足 per-Worker least privilege。

当前状态：

`NOT SUPPORTED BY WORKERS BUILDS YET`

## 7. 当前安全结论

当前 staging/runtime 链路已经稳定：

`Profile A = operational`

真正的 per-Worker hardening：

`Profile C = product-blocked`

如果现在必须满足 per-Worker least privilege：

`Profile B = available migration path`

因此在 production cutover 前，需要人类明确选择：

1. **保留 Profile A**，接受 Cloudflare-managed build token 的当前较宽 scope，等待 Cloudflare Builds 支持 account-owned token；或
2. **迁移到 Profile B**，用 GitHub Actions + per-Worker account-owned Editor token 换取更严格的 least privilege。

在没有这个人类选择前，不把 broad token 自动解释为已接受风险。

## 8. Custom Domain 权限仍应独立

无论选择 A 或 B：

Custom Domain provisioning 都不应成为 daily deployment credential 的常驻权限。

推荐：

```text
temporary provisioning authority
-> Worker Editor
-> target zone Workers Routes Write
-> attach Custom Domain
-> verify

then

routine deployment identity
-> no zone route write
```

## 9. 当前验收状态

- [x] managed build token operationally verified
- [x] current default scope audited
- [x] theoretical minimum identified
- [x] Workers Builds user-token-only constraint confirmed
- [x] per-Worker account-owned token path identified for external CI
- [ ] human selects production security profile
- [ ] selected profile passes main build
- [ ] selected profile passes non-production preview or equivalent
- [ ] selected profile passes workers.dev/runtime verification
- [ ] obsolete credential safely retired if migration occurs

当前：

`BUILD TOKEN SECURITY = REVIEWED / PRODUCT-CONSTRAINED / HUMAN PROFILE DECISION PENDING`
