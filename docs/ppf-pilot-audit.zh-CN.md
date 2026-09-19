# PPF Pilot Phase 1 — Runtime Validation Audit

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**分支：** `ppf-pilot-v0.1`  
**PR：** #20  
**PPF：** v0.1.0-draft @ `9326920e1920d18f0a71eac26d4068da9d6bdffe`  
**状态：** PASS — Phase 1 completed and main deployment verified

> **Historical Phase 1 audit.** 本文件保留 PPF Phase 1 当时的 source/profile/runtime/GitHub Pages 验证事实，不代表当前 Cloudflare Phase 2 状态。当前 Cloudflare readiness 以 `docs/cloudflare-readiness.yaml` 为机器可读 durable state，并由 `docs/cloudflare-readiness.zh-CN.md` 提供人类可读解释。

## 1. 审计目的

本项目是 Personal Publishing Framework 的第一个真实 downstream pilot。

Phase 1 要验证：

```text
one canonical Quarto source
        |
        +--> continuous Web profile
        |
        +--> explicit on-demand profiles
             EPUB / PDF / DOCX / LaTeX
```

同时保持：

- GitHub Pages 继续承担现有 production Web；
- Cloudflare 只处于 staged configuration；
- BUILD 不自动变成 RELEASE；
- HARC-lite collaboration governance 不与本轮 publishing migration 混合。

## 2. 第一次 PR runtime run 发现的缺陷

首次 PR checks：

- Repository Governance CI：FAIL
- Quarto HTML CI and Pages：FAIL

共同失败原因不是 Quarto profile，而是我在重写 Working Memory Task Plan 时误删了既有 governance validator 要求的：

`CLARIFICATION COMPLETION RULE`

修复方式：

- 恢复 clarification lifecycle 标题与状态转换；
- 明确 PPF pilot 不改变原 HARC-lite clarification governance。

修复后 Governance CI：PASS。

这证明 PPF migration 必须服从项目现有 governance invariants，而不能为了新的 publishing model 静默简化项目状态结构。

## 3. Web runtime validation

GitHub Actions run：

- workflow run：`35421469632`
- job：`validate-html`
- conclusion：`success`

通过步骤：

- repository / canonical source checks；
- Quarto setup；
- `quarto render --profile web`；
- rendered HTML integrity checks；
- 关键页面、目录、阅读 UI、repository links 验证；
- 确认 `_book/` 中没有意外 EPUB / PDF / DOCX / LaTeX artifact。

PR 环境正确跳过 GitHub Pages deployment。

结论：

**现有 Web Edition 可以在 profile separation 后继续从同一 canonical source 完整构建。**

## 4. Governance runtime validation

GitHub Actions run：

- workflow run：`35421469640`
- job：`governance`
- conclusion：`success`

结论：

PPF publication-lifecycle migration 没有破坏当前 HARC-lite repository-backed governance、release gates、rights state 与 handoff invariants。

## 5. On-demand format runtime validation

由于当前 GitHub connector 没有 workflow-dispatch 写入能力，本 pilot 临时增加了一个 **PR-only** matrix workflow：

`.github/workflows/ppf-pilot-format-validation.yml`

它只用于本次 runtime audit，不属于最终 PPF 日常工作流，并将在合并前删除。

验证 workflow run：

`35421469666`

### EPUB

- job：`validate-epub`
- conclusion：`success`
- runtime 约 20 秒
- 输出：`_publication/epub/*.epub`

### DOCX

- job：`validate-docx`
- conclusion：`success`
- runtime 约 21 秒
- 输出：`_publication/docx/*.docx`

### LaTeX

- job：`validate-latex`
- conclusion：`success`
- runtime 约 29 秒
- 输出：`_publication/latex/*.tex`

### PDF

- job：`validate-pdf`
- conclusion：`success`
- runtime 约 1 分 51 秒
- 环境步骤：
  - Quarto：PASS
  - Noto CJK fonts：PASS
  - TinyTeX：PASS
  - PDF render：PASS
  - artifact verification：PASS
- 输出：`_publication/pdf/*.pdf`

## 6. 架构结论

真实运行支持 PPF 的核心分离：

### Continuous Web

```text
QMD / BibTeX
-> source validation
-> web profile
-> HTML
-> rendered validation
-> production delivery
```

### On-demand publication

```text
same QMD / BibTeX
-> explicitly selected profile
-> one requested format
-> build artifact
-> no automatic release
```

特别是 PDF 明显比 Web / EPUB / DOCX / LaTeX 构建更重。把 PDF 从日常 Web CI 中分离，不只是概念上的整洁，而是实际减少 continuous publication latency 和 TeX 环境耦合。

## 7. Cloudflare 状态

本审计**没有**声称 Cloudflare production 已验证。

当前：

- `wrangler.jsonc`：staged；
- target provider：Cloudflare Workers Static Assets；
- current production provider：GitHub Pages；
- target canonical URL：未确认；
- Cloudflare credentials / Worker target：未在本 pilot 中验证。

Cloudflare cutover 属于 Phase 2。

## 8. 临时验证基础设施处理

PR-only format validation workflow 已在四格式 runtime validation 完成后删除。

最终进入 `main` 的正常语义仍是：

- Web：automatic / continuous；
- EPUB/PDF/DOCX/LaTeX：manual / explicit / on-demand。

## 9. Phase 1 合并条件

当前核心 runtime validation：**PASS**。

合并前剩余操作：

1. ~~删除临时 PR-only format validation workflow；~~ `COMPLETED`
2. ~~更新 Working Memory / adoption note 为 validation-complete；~~ `COMPLETED`
3. ~~让最终 PR head 再通过正常 Governance + Web checks；~~ `COMPLETED / PASS`
4. ~~合并后验证 `main` GitHub Pages deployment 成功。~~ `COMPLETED / PASS`

Phase 1 不要求 Cloudflare cutover。


## 10. Main merge and production-path verification

PR #20 已合并：

- merge commit：`96b91691bd776136e156c384eee619d52ff2e3a4`

`main` push 验证：

### Repository Governance CI

- run：`35422349988`
- conclusion：`success`

### Quarto HTML CI and Pages

- run：`35422349914`
- source validation：PASS
- `quarto render --profile web`：PASS
- rendered HTML validation：PASS
- Pages configuration：PASS
- Pages artifact upload：PASS
- `deploy-pages`：PASS

### External Link Audit

- run：`35422349888`
- Web profile render：PASS
- external-link audit：PASS

通用网页读取工具无法直接读取该 GitHub Pages URL，因此本审计不声称完成了独立于 GitHub 的外部 HTTP 内容抓取。可确认的是：GitHub 平台侧 Pages production deployment 已成功，且仓库自身的外部链接审计通过。

## 11. Phase 1 final conclusion

**PASS — PPF Phase 1 is complete.**

已验证的架构事实：

`one canonical source -> continuous Web + explicit on-demand publication profiles`

并且：

- daily Web pipeline 不依赖 PDF/TeX；
- EPUB/PDF/DOCX/LaTeX 不会自动构建或自动 release；
- GitHub Pages 保持当前 production provider；
- Cloudflare 保持 staged Phase 2 target；
- HARC-lite collaboration governance 未被本轮 publishing migration 静默改写。

这句话是 Phase 1 结束时的历史 next step。后续 Phase 2 staging/runtime 已实际完成验证，但 canonical production cutover 仍未完成。

## 12. Post-Phase-1 current-state pointer

截至 2026-09-19 的后续持久状态：

- Cloudflare account / GitHub App / repository connection：VERIFIED；
- main Workers Build：PASS；
- non-production preview：PASS；
- main + preview workers.dev runtime：PASS；
- Profile A：operationally verified，但 managed token 不是 per-Worker least privilege；
- Profile B：candidate / validate-only PASS，**不是 production-tested**；
- Profile C：当前 unavailable；
- current canonical production：GitHub Pages；
- Custom Domain / canonical URL migration：NOT DONE；
- GitHub Pages legacy policy：UNRESOLVED；
- production security profile：WAITING HUMAN DECISION。

因此本 Phase 1 audit 不应被用来推断“Cloudflare account 尚未连接”，也不应把后来 staging/runtime 验证误写成 production cutover。
