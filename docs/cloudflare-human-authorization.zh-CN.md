# Cloudflare ↔ GitHub 一次性授权指南
## 面向完全没有技术背景的操作者

**目标：** 完成一次账户授权后，让 AI Agent 可以按仓库中的机器契约配置和维护 Cloudflare Workers Builds，而不要求操作者理解 API、YAML、Wrangler 或 GitHub Actions。

**当前项目：** `ChongLiuPhil/epistemology-textbook`

**重要：** 在本指南完成前，现有 GitHub Pages 继续是正式公开站点。不要删除 Pages，不要改 DNS，不要添加 Custom Domain。

---

## 推荐路径：只做两次授权

### 授权 1 — 允许 AI Agent 访问 Cloudflare

这一步的目的，是让支持 MCP 的 AI Agent 能读取并配置你的 Cloudflare Workers / Builds 状态，而不是让你复制 API token。

Cloudflare 官方 MCP：

- API MCP：`https://mcp.cloudflare.com/mcp`
- Workers Builds MCP：`https://builds.mcp.cloudflare.com/mcp`

操作：

1. 在你正在使用、且支持 MCP 的 AI 客户端里打开 **Plugins / Connectors / MCP / Integrations** 一类的设置。
2. 添加 Cloudflare 官方 MCP。
3. 浏览器会打开 Cloudflare 登录/授权页面。
4. 使用你的 Cloudflare 账户登录。
5. 如果授权页提供 **Edit Permissions / 编辑权限**：
   - 保留完成 Workers / Workers Builds 管理所必需的权限；
   - 不主动增加与本项目无关的 DNS、R2、KV、D1 等权限。
6. 点击允许/授权。
7. 回到 AI 客户端。

完成标准：

> AI Agent 能实际读取你的 Cloudflare account / Workers / Workers Builds 状态。

如果 AI 客户端根本不支持添加 Cloudflare MCP，跳到本文件后面的 **Dashboard-only fallback**。

---

### 授权 2 — 允许 Cloudflare 访问指定 GitHub 仓库

这一步建立：

`Cloudflare Workers Builds ↔ GitHub repository`

操作：

1. 打开 Cloudflare Dashboard。
2. 进入 **Workers & Pages**。
3. 选择一个 Worker 后进入 **Settings → Builds → Connect**；
   如果还没有 Worker，也可以从 **Create application / Import a repository** 开始。
4. 选择 **GitHub**。
5. GitHub 会显示 Cloudflare Workers & Pages App 的授权页面。
6. 如果 GitHub 提供：
   - **All repositories**
   - **Only select repositories**

   请选择：

   **Only select repositories**

7. 只勾选：

   `ChongLiuPhil/epistemology-textbook`

8. 点击安装/授权。
9. 返回 Cloudflare。

完成标准：

> Cloudflare 能看到并选择 `ChongLiuPhil/epistemology-textbook`，但没有被授予访问其他不相关仓库的权限。

---

## 完成两次授权后，请不要自己配置其余字段

如果当前 AI Agent已经能调用 Cloudflare MCP，请只告诉它：

> “Cloudflare OAuth 和 GitHub App 都已经授权，请按仓库根目录的 `cloudflare-builds.yaml` 完成配置和首次 staging 验证。”

AI 应负责：

1. 确认 Cloudflare account；
2. 确认或创建 Worker `epistemology-textbook`；
3. 读取 GitHub repository connection；
4. 使用仓库定义的 build command；
5. 创建 production trigger；
6. 创建 preview trigger；
7. 触发首次 build；
8. 检查 build log；
9. 验证 workers.dev / preview URL；
10. 将实际状态写回 `docs/cloudflare-readiness.yaml`；
11. 在所有验证通过前保持 GitHub Pages 为现有 production。

---

# Dashboard-only fallback
## 只有在 AI Agent 无法接 Cloudflare MCP 时才使用

这条路径仍然不需要写代码。

### 1. 打开 Import repository

在 Cloudflare：

**Workers & Pages → Create application → Import a repository**

选择 GitHub，然后选择：

`ChongLiuPhil/epistemology-textbook`

### 2. 填写这些固定值

如果页面要求填写 Worker name：

`epistemology-textbook`

Production branch：

`main`

Root directory：

`/`

Build command：

`bash scripts/cloudflare_build.sh`

Deploy command：

`npm run cloudflare:deploy`

如果有 **Non-production branch builds**，开启它。

Non-production / Preview deploy command：

`npm run cloudflare:preview`

不要修改这些命令；它们来自仓库中的 `cloudflare-builds.yaml`。

### 3. API token

如果 Cloudflare 让你在：

- 自动创建 token
- 选择已有 token

之间选择：

**最简单路径：** 允许 Cloudflare 创建其 Workers Builds token。

这个 token 保存在 Cloudflare 侧，不需要复制进 GitHub。

安全说明：Cloudflare 自动创建的默认 build token 权限可能比本项目最小需求更宽。因此首次连接后应执行一次权限审计；对于包含许多敏感 Cloudflare 资源的账户，优先改用受限 custom user token。

**永远不要：**

- 把 token 粘贴到 GitHub 文件；
- 把 token 发到聊天；
- 把 token 写进 README；
- 把 token 截图公开；
- 把 token 放进 `cloudflare-builds.yaml`。

### 4. 首次部署

点击 Cloudflare 页面上的 Save / Deploy / Connect 等确认按钮。

此时即使 Cloudflare 把 `main` 视为其 production branch，也**不要添加 Custom Domain**。

项目对公众的正式入口仍然是 GitHub Pages。

Cloudflare 首次成功只视为：

`workers.dev staging`

### 5. 成功后你只需要告诉 AI

请把以下信息告诉 AI：

- “Cloudflare 已连接 GitHub”
- “首次 build 成功/失败”
- 如果成功：把普通的 `workers.dev` URL 发给 AI

**不要发送 token、secret 或密码。**

---

# 当前仓库定义的标准参数

权威机器契约：

`cloudflare-builds.yaml`

当前值：

- Worker：`epistemology-textbook`
- GitHub repo：`ChongLiuPhil/epistemology-textbook`
- Production branch：`main`
- Root directory：`/`
- Build：`bash scripts/cloudflare_build.sh`
- Deploy：`npm run cloudflare:deploy`
- Preview deploy：`npm run cloudflare:preview`
- Node：24
- Wrangler：4.135.0
- Quarto：1.10.18

任何 AI Agent 或人类操作者都不应凭记忆重写这些参数，应以仓库机器契约为准。

---

# 安全边界

在第一次 workers.dev staging 完成前，不做：

- Custom Domain；
- DNS 改动；
- GitHub Pages 停用；
- canonical URL 修改；
- Cloudflare-only production cutover；
- 删除旧部署；
- 把 Cloudflare token 放入仓库。

如果操作界面与你看到的说明不一致，停止在当前页面，把页面名称和可见选项告诉 AI；不要猜。
