# Cloudflare Hardened External CI 候选方案

**状态：** CANDIDATE / VALIDATE-ONLY / NOT ACTIVE PRODUCTION

本文件用于把生产安全 Profile B 准备到“只差凭据”状态。它不会自动替换已经验证通过的 Workers Builds。

## 目标

日常 deployment identity：

`Account-owned API token -> Individual Worker: epistemology-textbook -> Editor`

Cloudflare 当前官方权限模型允许 account-owned API token 只作用于指定 Worker，并以 Editor 身份部署 existing Worker。这个 token 不需要 KV、R2 或所有 zone 的 Workers Routes 权限。

## 当前候选 workflow

`.github/workflows/cloudflare-external-ci.yml`

默认 PR 行为：

`validate-only`

它会真实完成：

- 固定 Node / Wrangler；
- 固定 Quarto；
- `make cloudflare-build`；
- rendered HTML validation；

但不会读取 Cloudflare secret，也不会调用 Cloudflare deployment API。

只有手工 `workflow_dispatch` 选择：

- `preview`
- `production`

时才需要 credentials。

Production mode 还要求 workflow ref 必须是 `main`。

因此把候选 workflow 合并到 `main` 本身**不会**自动启用外部 CI deployment。

## 如果未来选择 Profile B，人类只需做的事情

在当前 AI 客户端仍不能直接管理 Cloudflare account token / GitHub secrets 的情况下，需要账户所有者完成一次性凭据设置。

### 1. 创建 Cloudflare account-owned API token

Cloudflare Dashboard：

**Manage Account → Account API Tokens → Create Token**

权限目标：

- Scope：**Specified Workers**
- Worker：**epistemology-textbook**
- Role：**Editor**

不要增加：

- KV；
- R2；
- D1；
- all-zone Workers Routes；
- Workers Admin。

如果创建页面与上述字段不同，不要猜，先把页面截图交给 AI。

### 2. GitHub 保存 token

GitHub repository：

`ChongLiuPhil/epistemology-textbook`

进入：

**Settings → Secrets and variables → Actions**

添加 repository secret：

`CLOUDFLARE_API_TOKEN`

值：刚创建的 account-owned API token。

不要把值提交进文件或发到聊天。

### 3. GitHub 保存 Account ID

同一页面的 **Variables** 中添加：

`CLOUDFLARE_ACCOUNT_ID`

值：Cloudflare account ID。

Account ID 不是 deployment secret，但仍由 GitHub variable 管理，避免写死在 workflow。

## 真正迁移前的验证顺序

1. workflow manual mode = `preview`
2. preview alias = `hardened-ci-probe`
3. preview build PASS
4. preview runtime PASS
5. workflow manual mode = `production`，ref 必须为 `main`
6. production deploy PASS
7. production workers.dev runtime PASS
8. 才关闭 Workers Builds trigger
9. 再确认 GitHub push 自动部署设计
10. 最后撤销/删除旧 broad build token

在步骤 1–7 完成前：

**Workers Builds Profile A 继续保留，GitHub Pages 继续是现有正式公开站点。**

## 不可逆动作

不要在候选验证前：

- 删除现有 Workers Builds token；
- 关闭 GitHub Pages；
- 绑定正式 Custom Domain；
- 改 canonical URL；
- 删除现有 Worker；
- 让两个 CI 系统同时自动生产部署。

Profile B 的采用必须是“验证后切换”，不是“先拆旧链路再测试新链路”。
