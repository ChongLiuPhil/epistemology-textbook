# Cloudflare Phase 2 Readiness Audit

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**状态：** `ACCOUNT-CONNECTED / MAIN+PREVIEW+RUNTIME-VERIFIED / PROFILE-A-SELECTED / CUTOVER-BLOCKED`

> 本文件是 `docs/cloudflare-readiness.yaml` 的人类可读解释。机器可读 readiness state 是本仓库对当前已验证 Cloudflare 状态的 durable record；本文不得与其形成第二套冲突真值。

## 1. 当前 production 与 staging 边界

当前 canonical production 仍是：

```text
GitHub main
-> source validation
-> Quarto web profile
-> rendered HTML validation
-> GitHub Pages
```

当前 Cloudflare 状态是：

```text
GitHub repository
-> Cloudflare Workers Builds
-> main Workers Build: PASS
-> non-production preview: PASS
-> main workers.dev runtime: PASS
-> preview workers.dev runtime: PASS
```

Cloudflare workers.dev 已完成 staging/runtime verification，但尚未完成 canonical production cutover。

因此：

```text
Cloudflare production-branch build/deploy verified
!= PPF canonical production active
```

## 2. Repository-side readiness

以下仓库侧条件已验证：

- canonical Web publication gate：`make web-publish-check`；
- Worker config：`wrangler.jsonc`；
- Worker name：`epistemology-textbook`；
- static assets directory：`./_book`；
- Workers Builds machine contract：`cloudflare-builds.yaml`；
- Node / Wrangler / Quarto toolchain pins；
- clean-runner Cloudflare build wrapper；
- independent GitHub Web validation；
- non-deploying Cloudflare Build Contract CI；
- read-only workers.dev runtime verification；
- Hardened External CI candidate 的 validate-only path。

Repository-side readiness：**PASS**。

## 3. Account-side observed state

根据当前 repository durable evidence：

- Cloudflare account：human-confirmed；
- GitHub App：verified via GitHub provider checks；
- repository connection：VERIFIED；
- Worker target：VERIFIED；
- main production-branch trigger：VERIFIED / build PASS；
- non-production preview trigger：VERIFIED / preview PASS；
- workers.dev endpoint：assigned；
- main workers.dev HTTP/content verification：PASS；
- preview workers.dev HTTP/content verification：PASS；
- latest recorded later-main Workers Build：PASS。

详细 build/check/version identifiers 保留在：

- `docs/cloudflare-readiness.yaml`
- `cloudflare-builds.yaml`
- Working Memory handoff pointers

本文不复制完整 identifier 列表，避免形成第二个详细 evidence source。

Account-side staging readiness：**VERIFIED**。

## 4. Runtime verification

当前 runtime verifier 已真实验证：

- HTTP 200；
- 5 个代表性页面；
- 最多 30 个本地 CSS / JS / image / font assets；
- UTF-8 / 中文内容 marker；
- main workers.dev endpoint；
- non-production preview endpoint。

运行证据由 `docs/cloudflare-readiness.yaml` 的 `runtime_http_verification` 指向 GitHub Actions run。

这证明 staging/runtime 可访问，不证明 canonical cutover 已完成。

## 5. Security profiles

### Profile A — Workers Builds Native

当前状态：

`selected-production-profile / operationally-verified`

特点：

- Cloudflare GitHub App + Workers Builds；
- Cloudflare-managed user build token；
- 最少人工 secret handling；
- main / preview / workers.dev runtime 已在真实 pilot 验证。

安全边界：

- 当前 managed token scope 比纯 static Worker routine deploy 所需更宽；
- `least_privilege: false`；
- 不得描述成 per-Worker least privilege；
- 人类作者已于 2026-09-19 明确选择 Profile A，并接受这一已知 broad-scope trade-off 作为当前项目的 production delivery security decision。

### Profile B — Hardened External CI

当前状态：

`candidate / validate-only PASS`

已经验证：

- candidate workflow 能执行 canonical Cloudflare build gate；
- PR validate-only path：PASS；
- credential-dependent steps：SKIPPED；
- preview deployment step：SKIPPED；
- production deployment step：SKIPPED。

尚未发生：

- account-owned per-Worker Editor token 配置；
- GitHub deployment secret/variable 激活；
- Profile B preview deployment；
- Profile B production deployment。

因此 Profile B **不是 production-tested**。

### Profile C — Future Native Granular

目标是：

```text
Workers Builds
+ account-owned token
+ individual Worker
+ Editor
```

当前 repository evidence 记录 provider product capability blocker：Workers Builds 当前不能使用所需 account-owned token path。

因此当前状态是：

`unsupported-currently`

不得伪造为已支持。

## 6. PPF adoption boundary

本项目当前 adopted PPF 仍是：

- version：`v0.1.0-draft`
- adopted commit：`9326920e1920d18f0a71eac26d4068da9d6bdffe`

上游 PPF 后续演进不自动改变本项目 adopted state。是否升级 adopted commit 必须作为独立 downstream adoption decision 和验证工作处理。

## 7. Remaining production-cutover gates

已完成：

- [x] repository Web/profile/runtime validation
- [x] Workers Builds machine contract
- [x] Cloudflare account / GitHub App / repository connection
- [x] Worker target
- [x] main Workers Build
- [x] non-production preview
- [x] main workers.dev runtime
- [x] preview workers.dev runtime
- [x] build-token scope review
- [x] Profile B candidate / validate-only validation

尚未完成：

- [x] human production security-profile selection：Profile A
- [ ] target canonical URL
- [ ] Cloudflare zone / Custom Domain eligibility
- [ ] Custom Domain binding
- [ ] canonical production verification after cutover
- [ ] GitHub Pages legacy URL policy
- [ ] canonical URL migration

在这些条件完成前：

`PRODUCTION CUTOVER = BLOCKED`

## 8. 当前结论

**Repository readiness: PASS.**

**Cloudflare account/build/preview/runtime staging: VERIFIED.**

**Current canonical production: GitHub Pages.**

**Cloudflare canonical production cutover: NOT DONE / BLOCKED.**

当前 blocker 不再是 account connection、runtime verification 或 security-profile decision，而是：

1. target canonical URL / Custom Domain；
2. GitHub Pages legacy policy。

Profile A 已选定，但这**不等于** production cutover approval。在 target canonical URL / Custom Domain 与 GitHub Pages legacy policy 明确并验证前，不修改 DNS、不绑定正式 Custom Domain、不停用 GitHub Pages，也不把 workers.dev staging 描述成 canonical production。
