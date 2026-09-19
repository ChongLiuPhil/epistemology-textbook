# Working Memory — Current Focus

**状态：** ACTIVE

## CURRENT_STAGE

Personal Publishing Framework pilot — Phase 1 runtime validation.

## CURRENT_OBJECTIVE

把本项目作为第一个真实 PPF downstream pilot：

- 用 Quarto profiles 分离共享 canonical source 与各输出格式；
- 保持 Web HTML continuous；
- 把 EPUB / PDF / DOCX / LaTeX 改为单格式显式按需构建；
- 保留现有 GitHub Pages 生产路径完成真实 PR/main runtime validation；
- stage Cloudflare Workers Static Assets 配置，但暂不切换生产。

## PRIMARY_BLOCKER

None for Phase 1.

Cloudflare production cutover 的必要条件尚未完成，但不阻塞 PPF profile/runtime pilot。

## IMMEDIATE_NEXT_ACTION

完成 PPF metadata、validator、README/CONTRIBUTING 同步后创建 PR；让现有 GitHub Actions 在 PR 上真实执行 source validation + Web-profile render。随后分别触发 publication-format runtime builds，验证 EPUB / PDF / DOCX / LaTeX 的 profile 输出。

## HANDOFF POINTERS

- Decision：`core/DECISION_LOG.zh-CN.md` D006
- PPF contract：`publishing.yaml`
- Adoption note：`docs/ppf-adoption.md`
- Release：`docs/release-status.zh-CN.md`
- Quarto base：`_quarto.yml`
- Web profile：`_quarto-web.yml`
- Cloudflare staged config：`wrangler.jsonc`

本轮不迁移 HARC-lite collaboration governance；该工作应独立处理。
