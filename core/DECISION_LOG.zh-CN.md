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
