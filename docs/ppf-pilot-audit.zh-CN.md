# PPF Pilot Phase 1 — Runtime Validation Audit

**日期：** 2026-09-19  
**项目：** `ChongLiuPhil/epistemology-textbook`  
**分支：** `ppf-pilot-v0.1`  
**PR：** #20  
**PPF：** v0.1.0-draft @ `9326920e1920d18f0a71eac26d4068da9d6bdffe`  
**状态：** PASS — runtime profile validation completed

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

PR-only format validation workflow 在本审计完成后应删除。

最终进入 `main` 的正常语义仍是：

- Web：automatic / continuous；
- EPUB/PDF/DOCX/LaTeX：manual / explicit / on-demand。

## 9. Phase 1 合并条件

当前核心 runtime validation：**PASS**。

合并前剩余操作：

1. 删除临时 PR-only format validation workflow；
2. 更新 Working Memory / adoption note 为 validation-complete；
3. 让最终 PR head 再通过正常 Governance + Web checks；
4. 合并后验证 `main` GitHub Pages deployment 成功。

Phase 1 不要求 Cloudflare cutover。
