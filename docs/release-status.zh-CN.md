# Release Status — 公开版本批准状态

**角色：** 记录“某个具体公开版本是否允许发布”，与 `docs/framework-status.zh-CN.md` 的知识结构/Architecture 状态分离。

## 当前 Web Edition

- 状态：`AUTHOR-PUBLISHED / CONTINUOUSLY-REVISED`
- canonical source：`index.qmd`、`manuscript/*.qmd`、`references.bib`
- active artifact：HTML Web Edition
- 当前生产发布机制：经 main 的 canonical Web gate 后由 Cloudflare Workers Builds 自动部署到 workers.dev
- 责任主体：作者 Chong Liu

采用 HARC-lite 不追溯把已经公开的 Web Edition 降级为 provisional。

## PPF Pilot 状态

- Framework：Personal Publishing Framework v0.1.0-draft @ `21a5360727167bad6f399477ded073431645fa1d`
- contract：`publishing.yaml`
- default profile：`web`
- 当前 Web provider：Cloudflare Workers Static Assets
- previous / legacy Web provider：GitHub Pages（policy = `retire`）
- migration status：`canonical-active-verified`
- source visibility：`public`
- Web publication authorization：`authorized`
- Web publication visibility：`public`
- Web access policy：`none`
- current canonical identity：`https://epistemology-textbook.philosophy-research.workers.dev/`
- provider endpoint：workers.dev
- Cloudflare cutover 必须作为独立发布基础设施变更验证。

## 按需生成的电子出版格式

PDF / DOCX / EPUB / LaTeX 可以从同一 canonical Quarto source 通过手动 GitHub Actions workflow 按需生成；每次请求只构建一种格式。

这些输出默认状态是：

`BUILD-ARTIFACT / NOT-RELEASED`

含义：

- 可以用于作者校对、跨格式检查、离线阅读或后续出版准备；
- 不因 artifact 已成功生成而自动成为正式出版版本；
- 不自动创建 GitHub Release；
- 不改变 HTML Web Edition 作为当前主要持续发布版本的地位。

## 未来重大版本

当未来发生大规模正文/架构重写，或准备正式 PDF / EPUB / DOCX / v1.0 等 release 时，使用以下轻量状态：

```text
MAJOR-REVISION
→ AUTHOR-REVIEW
→ RELEASE-APPROVED
→ RELEASED
```

只有人类作者明确完成 release review 后，才能进入 `RELEASE-APPROVED`。

## Release Review 至少确认

- 当前具体 artifact 与 canonical source 一致；
- blocking clarification 已解决或明确 deferred；
- 重大 Architecture 变化已经获得相应人类确认；
- 关键事实、引用、书目与网页/发行格式检查完成；
- 许可与第三方材料权利满足该 release 的要求；
- 发布渠道特定约束（如有）已处理；
- 可识别的人类责任主体仍然明确。

## 与 Architecture Approval 的区别

- **Architecture / Framework Approval**：作者确认核心知识结构、关键概念关系和章节功能。
- **Release Approval**：作者确认某个具体版本可以进入公开发布。

前者不自动等于后者；后者也不要求每次小型 Web Edition 修订都创建新的 Framework Snapshot。

## 当前 blocker

正常 Web Edition 修订：无。  
手动生成 PDF / DOCX / EPUB / LaTeX build artifact：无，但不构成正式 release.

PPF Web continuous publication：无内容发布 blocker；canonical config 已切换到 workers.dev。  
Cloudflare cutover：**VERIFIED**；workers.dev 已完成 post-cutover provider build/runtime verification。GitHub Pages legacy policy = `retire`，旧 deployment 的 `Unpublish site` 已由 repository owner 于 2026-09-20 确认完成；当前会话无法独立 HTTP 探测旧 URL。  

正式开放许可 release：受 `CLR-001` 影响.  
包含或再分发外部参考 PDF 的任何 release：受 `CLR-002` 影响。
