# Current AHICP / Inquiry Publishing Stack Adoption — 《我们如何知道？》

本项目保留 HARC-lite 作为 project-native 历史治理层，并采用 current AHICP 作为当前协议入口。

## Current Stack revisions

Stack v2 distinguishes the stable composition/template revision from the semantic framework revision adopted by this project.

- AHICP template: `02d0b3c02ca23073c760b6e0f761a468e0235a1c`; project adopted: `ed5a60b1016497472072db108072ace59bcdb65d`
- PPF template: `9a6005de85f032095e36eea03fda317e73126538`; project adopted: `e660b48fb216c28c8faa1f0fe2d0816401e1de2c`
- Vault template: `592c6e2e938f995b7b3e7df07a72f7f1e2c50c5a`; project adopted: `79d64b12275a5cc7c09236b144bf4213fa7afc5e`
- Starter source revision: `05857086e240cbd269eae91af8419ea0921c01fa`

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
