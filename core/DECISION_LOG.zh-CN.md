# Decision Log — 项目持久决定

本文件只记录会影响未来协作者如何继续项目的持久决定，不复制普通聊天或每次小修。

## RECOVERED-BASELINE — HARC-lite 采用前已经生效的项目基线

**来源：** 现有 README、CONTRIBUTING、Quarto 配置与已部署工作流。  
**分类：** CONTENT / FORM / PROTOCOL。  
**状态：** `RECOVERED-BASELINE`。

- Quarto QMD + 根目录 `references.bib` 是正式教材来源。
- `textbook/` 为 legacy LaTeX 快照，不再参与 active editing/build。
- 当前开发阶段为 Web Edition Development，HTML 是日常构建与公开交付物。
- PDF / EPUB / DOCX 延后到未来独立 release workflow。
- `main` 经验证后通过官方 GitHub Pages artifact pipeline 自动发布。
- 读者界面明确区分“本书目录”和“本章目录”。
- 开放阅读不设置付费门槛，并建立内容反馈/网页反馈两个 Issue Form。
- bibliography integrity、rendered HTML integrity 与 External Link Audit 已作为独立质量层运行。

> 这是对采用 HARC-lite 前已存在仓库状态的恢复记录，不声称重建每项决定的原始聊天过程。

---

## 2026-09-18 — D001 — 采用项目化 HARC-lite 协作层

**来源：** 人类作者明确要求参考 `Human-AI-Research-Collaboration-Protocol` 检查并升级本仓库，随后确认“好，请升级”。  
**分类：** PROTOCOL。  
**决定：**

- 采用 HARC 的 repository-backed context、fresh-fetch、CONTENT/FORM/PROTOCOL 路由、Decision Log 与 Working Memory 原则；
- 不机械复制完整 HARC 主仓库；
- 上游采用基线固定为 HARC `0.2.0-draft`，commit `e741c43c5cd158c43910e3832c7d757226717a97`；
- 上游以后变化不会自动成为本项目规则，升级必须再次成为明确项目决定。

**实现状态：** implemented in this upgrade.

---

## 2026-09-18 — D002 — 内部治理采用中文 canonical，不强制全量双语镜像

**来源：** 本次 HARC-lite 升级方案，经人类作者确认实施。  
**分类：** FORM / PROTOCOL。  
**决定：**

- 教材正文与内部治理以中文为主要规范语言；
- 公共 README 继续维护中英文入口；
- 不为每个 Core、Working Memory 或协作文件强制生成英文 mirror，以避免不必要的同步负担。

**实现状态：** implemented.

---

## 2026-09-18 — D003 — 许可与外部 PDF 权利状态保持显式未决

**来源：** 本次仓库治理审计。  
**分类：** PROTOCOL。  
**决定：**

- AI 不代表作者选择项目开放许可；
- 公开可读不等于已经授予复制、修改或再发布许可；
- `reference/我们如何知道.pdf` 是外部参考资料，其公开分发/再发布权利在仓库中尚未得到确认；
- 在人类明确决定前，不把该 PDF 纳入本项目 authored/open-content 许可，也不把它打包进未来 release artifact。

**实现状态：** pending human licensing/rights decision; operational safeguard implemented.


---

## 2026-09-18 — D004 — 完善 HARC-lite v0.1.1 的协作闭环

**来源：** 人类作者在协议复核后明确确认“好，请完善”。  
**分类：** PROTOCOL。  
**决定：**

- 保持现有 HARC-lite 教材化架构，不扩张成完整 HARC 协议仓库；
- 新 Agent、长中断、高影响 Architecture/Release 工作或状态冲突时执行轻量 Onboarding Check，并使用 `PASS / PARTIAL / FAIL`；
- 明确作者 Chong Liu 保持为项目目的、核心知识判断、重大 Architecture 授权和公开 Release 决定的责任主体；
- 明确 Architecture/Framework Approval 与具体 Release Approval 相互独立；
- clarification 采用 `WAITING-HUMAN -> human resolution -> Decision Log -> promotion -> RESOLVED / PROMOTED` 生命周期，并从 active queue 退出；
- revision 变化触发 `REVISION-CONFLICT`，禁止用旧缓存覆盖新仓库状态；
- governance validator 应优先根据 `HARC_MANIFEST.yaml` 解析和校验声明路径/版本，而不是维护平行的硬编码项目拓扑。

**实现状态：** implemented in HARC-lite profile version `0.1.1` via PR #16 / main commit `1906a4f56739ae1f3039cc3d695093eb986bfdd7`.


---

## 2026-09-18 — D005 — 明确学习整合型教材定位与多格式出版模型

**来源：** 人类作者明确说明本项目主要来自自己的学习过程，是对学习资料、问题、论证与文献的整合和梳理；不以提出大量原创理论为主要目标，但问题选择、材料取舍、判断视角和整体组织需要由作者审核。作者同时要求出版、网页与排版方式可参考 `What-Remains-Human-Epistemic-Agency-and-Human-Value-in-the-Age-of-AI`。  
**分类：** CONTENT / FORM / PROTOCOL。  
**决定：**

- 本项目定位为学习—整合—梳理型、问题驱动的认识论教材工程，不以建立作者原创理论体系为主要目标；
- 作者判断主要体现于问题选择、材料取舍、概念区分、争议组织、教学层次与评价性判断；
- 教学取向明确区分哲学研究与单纯的思想研究、思想史研究、哲学史研究：哲学学习应训练问题提出、概念区分、理由比较、反例构造与立场检验；
- 上述哲学教育取向主要作为项目级组织原则，通过章节结构、练习、研究工作坊与阅读路线体现，不要求在正文中设置大篇幅宣言；
- 出版形式采用一套 Quarto canonical source 服务 HTML / PDF / DOCX / EPUB；
- HTML 继续自动发布到公开 GitHub Pages；
- PDF / DOCX / EPUB 通过独立手动 workflow 按需生成 artifact，不自动等于正式 Release Approval；
- 排版与网页阅读逻辑可以参考 `What-Remains-Human...`，但不复制其私有 Cloudflare 发布方式，也不移植与本项目书目结构不兼容的 citation interaction。

**实现状态：** implementing in current branch.


---

## 2026-09-19 — D006 — 采用 Personal Publishing Framework 作为出版生命周期框架

**来源：** 人类作者确认前述 AHICP / PPF /个人治理架构及 PPF reference implementation，并明确要求继续实施。  
**分类：** FORM / PROTOCOL。  
**决定：**

- 本项目作为第一个真实 downstream pilot，采用 **Personal Publishing Framework (PPF) v0.1.0-draft**；
- 采用的 PPF 上游 commit 固定为 `9326920e1920d18f0a71eac26d4068da9d6bdffe`，未来上游变化不自动成为本项目规则；
- canonical source 继续是 `index.qmd`、`manuscript/*.qmd`、`references.bib` 及共享 Quarto metadata；
- Quarto 配置改为 profile model：`web` 为默认 profile，EPUB / PDF / DOCX / LaTeX 为独立 on-demand profiles；
- Web HTML 保持 continuous publication；其他格式只有在作者明确请求时才构建；
- `BUILD` 不自动等于 `RELEASE`，`RELEASE` 也不自动等于外部平台发布；
- Phase 1 继续使用现有 GitHub Pages 生产路径，以真实 PR/main CI 验证 PPF profile model；
- `wrangler.jsonc` 仅用于 staging Cloudflare Workers Static Assets 实现；在 Worker target、凭据、canonical URL、preview 验证与 cutover/redirect policy 未确认前，不切断 GitHub Pages；
- 本 PR 只迁移出版生命周期，不同时把 HARC-lite 项目治理迁移到 AHICP，以保持故障域与审计边界清楚。

**实现状态：** implementing in `ppf-pilot-v0.1`.

---

## 2026-09-19 — D007 — 选择 Cloudflare Production Security Profile A

**来源：** 人类作者明确选择 `A`。  
**分类：** PROTOCOL / INFRASTRUCTURE SECURITY。  
**决定：**

- 本项目选择 **Profile A — Workers Builds Native** 作为当前 Cloudflare production delivery security profile；
- 继续使用已经真实验证的 Cloudflare GitHub App + Workers Builds + Cloudflare-managed user build token；
- 人类作者明确接受当前 managed build token 的已知较宽权限范围，作为本项目当前生产接入的已知安全权衡；
- 该接受**不**改变事实判断：当前 token 仍不是 per-Worker least privilege，`least_privilege: false` 保持不变；
- 不创建新的 account-owned deployment token，不启用 Hardened External CI 自动部署，不把 Profile B 描述为已采用；
- Profile B 继续保留为未激活的 hardened fallback / migration path；
- Profile C 继续等待 Workers Builds 原生支持 account-owned granular credential；
- 如果 Cloudflare 后续支持 Workers Builds + account-owned per-Worker Editor token，或项目 threat model / security requirement 改变，应重新评估本决定；
- 本决定只解除 production security-profile blocker，不等于批准 canonical production cutover；
- Custom Domain、target canonical URL、GitHub Pages legacy policy 与最终 cutover 仍需独立决定和验证。

**实现状态：** human-approved；本轮 repository migration 负责把该选择传播到 machine readiness、security audit、Working Memory 与 validators。

---

## 2026-09-19 — D008 — 选择 workers.dev 作为目标 canonical URL

**来源：** 人类作者明确选择选项 `2`。  
**分类：** FORM / INFRASTRUCTURE / PUBLICATION ROUTING。  
**决定：**

- 本项目选择 `https://epistemology-textbook.philosophy-research.workers.dev/` 作为 **target canonical URL**；
- 该选择使用已经真实验证的 Cloudflare Workers `workers.dev` endpoint，不需要额外 Custom Domain；
- 因此 Cloudflare zone / Custom Domain eligibility 与 Custom Domain binding 对当前路线标记为 `NOT_APPLICABLE`，不再作为 cutover blocker；
- 本决定只确定**目标 canonical URL**，不自动把 Cloudflare 标记为 canonical production active；
- 当前 `_quarto-web.yml`、GitHub Pages publication URL 与 reader-facing absolute links 暂不修改，因为 GitHub Pages legacy policy 尚未决定；
- 在 legacy policy 决定和相应 migration 验证前，GitHub Pages 继续是 current canonical production；
- 下一个人类 cutover decision 是 GitHub Pages legacy URL policy；
- canonical URL migration 只有在 legacy policy 明确、相关 source/config 更新并通过 runtime verification 后才算完成。

**实现状态：** human-approved target intent；本轮 repository migration 只写入 target URL 与 N/A Custom Domain 状态，不执行 canonical cutover。

