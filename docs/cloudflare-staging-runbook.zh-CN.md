# Cloudflare Workers Builds Staging Runbook

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**状态：** `ACCOUNT CONNECTED / MAIN+PREVIEW+RUNTIME VERIFIED / PRODUCTION CUTOVER PENDING`

## 1. 标准路线

本项目现在把 Cloudflare 的默认接入方式固定为：

```text
GitHub repository
   |
   +--> GitHub Actions
   |      make web-publish-check
   |      (independent quality check)
   |
   +--> Cloudflare Workers Builds
          |
          +--> build:
          |      bash scripts/cloudflare_build.sh
          |        -> pinned Quarto
          |        -> make web-publish-check
          |
          +--> preview:
          |      npm run cloudflare:preview
          |      -> wrangler versions upload
          |
          +--> production:
                 npm run cloudflare:deploy
                 -> wrangler deploy
```

GitHub Actions 与 Cloudflare 不维护两套内容验证逻辑；二者最终都调用：

`make web-publish-check`

## 2. 为什么首选 Workers Builds

Cloudflare Workers Builds 是 GitHub/GitLab 的原生 Git integration：

- push 可自动触发 build；
- production branch 可触发 production deploy；
- non-production branches 可使用 preview deploy；
- GitHub 可显示 build status / PR context；
- Cloudflare 管理 build environment 与 build token；
- 不要求把 Cloudflare API token 作为默认方案复制进 GitHub Secrets。

GitHub Actions + Wrangler token 仍保留为 fallback，不是默认范本。

## 3. 机器契约

所有 account-side 配置应从：

`cloudflare-builds.yaml`

读取。

人类文档不是参数真值源。

## 4. 工具链可重复性

Workers Builds 会使用 `package.json` 中声明的 Wrangler。

本项目固定：

- Node 24：`.nvmrc`
- Wrangler 4.135.0：`package.json`
- Quarto 1.10.18：`scripts/ensure_quarto.sh`

Cloudflare build image 没有被本项目假定为预装 Quarto，因此 build wrapper 会下载固定 Quarto release，并验证 SHA-256 后再渲染。

## 5. Account-side 最小授权模型

首选 Agent-native 路线需要两个一次性连接：

1. **AI ↔ Cloudflare OAuth/MCP**
   - API MCP：`https://mcp.cloudflare.com/mcp`
   - Workers Builds MCP：`https://builds.mcp.cloudflare.com/mcp`
2. **Cloudflare ↔ GitHub App**
   - 只授权所需 repository。

详细的人类操作说明：

`docs/cloudflare-human-authorization.zh-CN.md`

完成这两个授权后，应由 AI 读取 `cloudflare-builds.yaml` 配置剩余内容。

## 6. Workers Builds triggers

目标配置：

### Production trigger

- branch include：`main`
- build command：`bash scripts/cloudflare_build.sh`
- deploy command：`npm run cloudflare:deploy`
- root：`/`

### Preview trigger

- branch include：`*`
- branch exclude：`main`
- build command：`bash scripts/cloudflare_build.sh`
- deploy command：`npm run cloudflare:preview`
- root：`/`

首次账户接入应优先验证 preview / workers.dev 行为；Cloudflare 不成为正式 canonical production，直到后续 cutover gates 全部通过。

## 7. Build token 安全与 production security profiles

当前真实 pilot 已完成 build-token security review。结论不是“再找一个更窄的 Workers Builds user token”，而是明确区分三种 profile：

### Profile A — Workers Builds Native

- 当前状态：`operational-verified`；
- Cloudflare GitHub App + Workers Builds；
- Cloudflare-managed user build token；
- main / preview / workers.dev runtime 已验证；
- 最少人工 secret handling；
- 但 token scope 比纯 static Worker routine deploy 所需更宽；
- `least_privilege: false`，不得描述为 per-Worker least privilege。

### Profile B — Hardened External CI

- 当前状态：`candidate / validate-only PASS`；
- GitHub Actions + account-owned API token；
- 目标权限：individual Worker `epistemology-textbook` + `Editor`；
- candidate workflow 的 repository/build validation 已通过；
- credential / preview / production deployment steps 尚未执行；
- 尚未创建/配置 deployment credential；
- 因此 **不是 production-tested**。

只有人类明确选择 Profile B 后，才进入 credential provisioning 与 manual preview/production revalidation。Token 必须保存到受控 GitHub secret store，不得发送到聊天或写入 repository。

### Profile C — Future Native Granular

目标是 Workers Builds 原生 Git integration + account-owned per-Worker `Editor` token。

当前 machine evidence 记录该组合受 provider product capability 阻塞，因此状态为 `unsupported-currently`。不得为了追求理论 hardening 继续在已验证稳定链路上盲测，也不得伪造为已支持。

### Common credential rules

无论选择 A 或 B：

- token 永不进入 Git；
- token 不写入聊天、README、machine contract；
- GitHub App 限制为 selected repositories only；
- Custom Domain / Route provisioning 与 routine deployment credential 分离；
- production security profile 由项目责任人明确选择。

## 8. Staging 验证

首次成功后至少验证：

- build 使用预期 Git commit；
- `make web-publish-check` PASS；
- workers.dev / preview homepage 200；
- 代表性章节 200；
- CSS / JS / images 正常；
- sidebar / TOC / navigation 正常；
- Chinese text / equations / citations 正常；
- repository/source links 正常；
- 没有 EPUB/PDF/DOCX/LaTeX 意外暴露进 Web artifact；
- GitHub Pages 原站仍正常。

## 9. Custom Domain 与 cutover

在 preview/staging PASS 前不绑定正式 Custom Domain。

之后仍需单独完成：

- target canonical domain；
- Cloudflare zone eligibility；
- Custom Domain；
- production verification；
- GitHub Pages legacy policy；
- canonical links migration。

因此：

`WORKERS BUILDS CONNECTED != PRODUCTION CUTOVER`

## 10. External CI fallback

如果某个环境不能使用 Workers Builds Git integration，可退回：

`GitHub Actions + Wrangler + scoped token`

旧示例保留在：

`docs/examples/cloudflare-staging-workflow.yml`

但它不再是首选标准。

## 11. 当前状态

仓库侧：

**READY / VERIFIED**

GitHub App / repository connection：

**VERIFIED**

Cloudflare main Workers Build：

**PASS**

Cloudflare non-production preview：

**PASS**

main + preview workers.dev runtime：

**PASS**

当前 ChatGPT 会话：

**Cloudflare account tool unavailable**

build-token security：

**REVIEWED / PRODUCT-CONSTRAINED / HUMAN PROFILE DECISION PENDING**

production cutover：

**BLOCKED**
