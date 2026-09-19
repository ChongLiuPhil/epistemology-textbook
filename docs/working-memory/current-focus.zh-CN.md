# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework — **Phase 1 completed / Phase 2 readiness pending**.

## CURRENT_OBJECTIVE

PPF Phase 1 已正式完成：

- PR #20 已合并到 `main`；
- canonical Quarto source + profile separation 已实现；
- Governance runtime validation：PASS；
- Web profile runtime validation：PASS；
- EPUB / PDF / DOCX / LaTeX 四种 on-demand profile：全部真实构建 PASS；
- PR-only format validation workflow 已删除；
- `main` Web build：PASS；
- `main` GitHub Pages deployment：PASS；
- `main` External Link Audit：PASS。

下一发布基础设施目标是 **PPF Phase 2 / Cloudflare readiness**，但在以下条件具备前不执行生产 cutover：

- confirmed Cloudflare Worker / Static Assets target；
- authorized deployment credentials / mechanism；
- target canonical production URL；
- preview/staging deployment；
- production verification；
- existing GitHub Pages URL 的 redirect/canonical policy。

## PRIMARY_BLOCKER

Phase 1：`NONE — COMPLETED`

Phase 2：`WAITING-PREREQUISITES`

这不是书稿编辑或现有 GitHub Pages Web Edition 的 blocker。

## IMMEDIATE_NEXT_ACTION

对 Cloudflare Phase 2 做 readiness audit，仅准备可验证的 cutover 条件与最小权限部署方案；在生产目标、凭据、canonical URL 与 redirect/canonical policy 明确前，不改变当前 Pages production path。

## HANDOFF POINTERS

- Decision：`core/DECISION_LOG.zh-CN.md` D006
- PPF contract：`publishing.yaml`
- Adoption note：`docs/ppf-adoption.md`
- Runtime audit：`docs/ppf-pilot-audit.zh-CN.md`
- Release：`docs/release-status.zh-CN.md`
- Quarto base：`_quarto.yml`
- Web profile：`_quarto-web.yml`
- Cloudflare staged config：`wrangler.jsonc`
- Phase 1 merge commit：`96b91691bd776136e156c384eee619d52ff2e3a4`
- Phase 1 main Web/Pages run：`35422349914`
- Phase 1 main link-audit run：`35422349888`

本轮没有迁移 HARC-lite collaboration governance；该工作仍应独立处理。
