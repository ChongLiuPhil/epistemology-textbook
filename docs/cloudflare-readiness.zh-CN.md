# Cloudflare Phase 2 Readiness Audit

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**状态：** `CLOUDFLARE-CANONICAL-ACTIVE-VERIFIED / PAGES-RETIREMENT-PENDING`

> 本文件是 `docs/cloudflare-readiness.yaml` 的人类可读解释。机器可读 readiness state 是本仓库对当前已验证 Cloudflare 状态的 durable record；本文不得与其形成第二套冲突真值。

## 1. 当前 production 与 legacy 边界

本轮 repository cutover 已把 canonical Web config 切换到：

```text
GitHub main
-> source validation
-> Quarto web profile
-> rendered HTML validation
-> Cloudflare Workers Builds
-> https://epistemology-textbook.philosophy-research.workers.dev/
```

同时：

- main 分支不再生成新的 GitHub Pages deployment；
- `_quarto-web.yml` 与 rendered-HTML validator 已切换到 workers.dev；
- GitHub Pages policy = `retire`；
- 旧 GitHub Pages deployment 尚未实际 unpublish，因此 legacy retirement 仍是 pending；
- post-cutover workers.dev canonical runtime verification 已由 main push 的真实 Cloudflare provider build 与 GitHub Actions runtime check 验证通过。

因此当前精确状态是：

```text
Cloudflare canonical identity = active / verified
GitHub Pages = legacy endpoint / retirement pending
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

Account-side Cloudflare readiness：**VERIFIED**；canonical activation 的 post-cutover verification 已完成。

## 4. Runtime verification

当前 runtime verifier 已真实验证：

- HTTP 200；
- 5 个代表性页面；
- 最多 30 个本地 CSS / JS / image / font assets；
- UTF-8 / 中文内容 marker；
- main workers.dev endpoint；
- non-production preview endpoint。

运行证据由 `docs/cloudflare-readiness.yaml` 的 `runtime_http_verification` 指向 GitHub Actions run。

历史 staging/runtime checks 已证明 provider endpoint 可访问；cutover 后 main runtime run `35453967021` 进一步确认 workers.dev 已收敛到新的 canonical build：canonical marker 命中，5 个代表性页面与 30 个本地资源均通过。Cloudflare provider check `105926103705` / build `42aa93fe-d9b6-49e4-80be-a849951a6b9d` 同样通过。详细 evidence 仅以 machine readiness 为准。

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

本项目当前 adopted PPF 是：

- version：`v0.1.0-draft`
- adopted commit：`21a5360727167bad6f399477ded073431645fa1d`

上游后续变化仍不会自动成为本项目 adopted state。

## 7. Remaining cutover verification / retirement gates

已完成：

- [x] repository Web/profile/runtime validation
- [x] Workers Builds machine contract
- [x] Cloudflare account / GitHub App / repository connection
- [x] Worker target
- [x] main Workers Build
- [x] non-production preview
- [x] main + preview workers.dev runtime
- [x] production security profile = Profile A
- [x] target canonical URL = workers.dev
- [x] GitHub Pages legacy policy = `retire`
- [x] canonical source/config migration to workers.dev
- [x] future GitHub Pages deploy path removed from main workflow

仍需完成并验证：

- [x] post-cutover main Workers Build + workers.dev canonical runtime verification
- [ ] GitHub Pages current deployment actual unpublish

因此：

`CANONICAL CUTOVER = COMPLETE / VERIFIED`

`LEGACY RETIREMENT = SELECTED / UNPUBLISH PENDING`

## 8. 当前结论

**Repository cutover configuration: IMPLEMENTED.**

**Current canonical identity: workers.dev.**

**Cloudflare production delivery: ACTIVE / VERIFIED.**

**GitHub Pages legacy policy: RETIRE / CURRENT DEPLOYMENT UNPUBLISH PENDING.**

canonical cutover 已完成；唯一尚未完成的基础设施收尾，是使用 repository admin/maintainer 权限对现存 GitHub Pages deployment 执行一次 `Unpublish site`，随后验证旧 URL 已不可用。

当前 GitHub connector 不暴露完成该 Pages administration 动作所需的仓库管理写权限。仓库已经停止后续 Pages deployment，因此完成一次 unpublish 后不会被正常 main workflow 自动重新发布。
