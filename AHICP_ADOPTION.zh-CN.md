# Current AHICP / Inquiry Publishing Stack Adoption — 《我们如何知道？》

本项目保留 HARC-lite 作为 project-native 历史治理层，并采用 current AHICP 作为当前协议入口。

## Current pins

- AHICP: `0.3.0-draft @ ed5a60b1016497472072db108072ace59bcdb65d`
- PPF: `0.1.1-draft @ e660b48fb216c28c8faa1f0fe2d0816401e1de2c`
- Vault Interface: `79d64b12275a5cc7c09236b144bf4213fa7afc5e`
- Starter: `4889739d448a9bf68bedb42ce3182315eda0caeb`

## Functional mapping

| Stack role | Project-local authority |
| --- | --- |
| Content Core | `core/CONTENT_CORE.zh-CN.md` |
| Form Core | `core/FORM_CORE.zh-CN.md` |
| Decision Log | `core/DECISION_LOG.zh-CN.md` |
| Working Memory | `docs/working-memory.zh-CN.md` + `docs/working-memory/` |
| Architecture / Framework | `docs/book-architecture.zh-CN.md` + `docs/framework-status.zh-CN.md` |
| Release | `docs/release-status.zh-CN.md` |
| Publication | `publishing.yaml` + `docs/publication-profile.zh-CN.md` |

## Preserved production state

- Web publication: public / authorized
- Provider: Cloudflare Workers
- Canonical URL: `https://epistemology-textbook.philosophy-research.workers.dev/`
- Integration: Workers Builds Native / Profile A
- GitHub Pages legacy policy: RETIRE / unpublish human-confirmed complete
- On-demand PDF/DOCX/EPUB/LaTeX remain build artifacts, not releases by default

本次升级只更新 Stack/current-protocol pins 与 lifecycle contract 版本；不改变 Workers Builds、token security profile、canonical URL、教材正文或 Chapter 3 工作计划。
