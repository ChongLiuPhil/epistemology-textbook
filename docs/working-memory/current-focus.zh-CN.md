# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework pilot — Phase 1 runtime validation completed; final PR cleanup and merge verification.

## CURRENT_OBJECTIVE

完成第一个真实 PPF downstream pilot 的 Phase 1 收尾：

- canonical Quarto source + profile separation 已实现；
- Governance runtime validation 已通过；
- Web profile runtime validation 已通过；
- EPUB / PDF / DOCX / LaTeX 四种 on-demand profile 已真实构建通过；
- PR-only format validation workflow 已在完成四格式验证后删除；
- 让最终 PR head 只保留正式日常 workflow，并再次通过 Governance + Web checks；
- 合并后验证 main 的 GitHub Pages deployment。

## PRIMARY_BLOCKER

None for Phase 1.

Cloudflare production cutover 属于 Phase 2，不阻塞本次合并。

## IMMEDIATE_NEXT_ACTION

确认删除临时 workflow 后的最终 PR head 只运行正常 Governance / Web checks 且全部 PASS；随后合并 PR #20 并验证 main Pages deployment。

## HANDOFF POINTERS

- Decision：`core/DECISION_LOG.zh-CN.md` D006
- PPF contract：`publishing.yaml`
- Adoption note：`docs/ppf-adoption.md`
- Runtime audit：`docs/ppf-pilot-audit.zh-CN.md`
- Release：`docs/release-status.zh-CN.md`
- Quarto base：`_quarto.yml`
- Web profile：`_quarto-web.yml`
- Cloudflare staged config：`wrangler.jsonc`

本轮不迁移 HARC-lite collaboration governance；该工作应独立处理。
