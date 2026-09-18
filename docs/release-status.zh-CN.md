# Release Status — 公开版本批准状态

**角色：** 记录“某个具体公开版本是否允许发布”，与 `docs/framework-status.zh-CN.md` 的知识结构/Architecture 状态分离。

## 当前 Web Edition

- 状态：`AUTHOR-PUBLISHED / CONTINUOUSLY-REVISED`
- canonical source：`index.qmd`、`manuscript/*.qmd`、`references.bib`
- active artifact：GitHub Pages HTML Web Edition
- 发布机制：经 main 的 source/bibliography/rendered-HTML checks 后自动部署
- 责任主体：作者 Chong Liu

采用 HARC-lite 不追溯把已经公开的 Web Edition 降级为 provisional。

## 按需电子出版构建

仓库可以通过独立手动 workflow 从 canonical QMD 生成 PDF / DOCX / EPUB，用于排版检查、作者审阅和未来发行准备。

这些 workflow artifact 属于 `BUILD-PREVIEW / NOT-A-RELEASE`：生成成功不等于作者已经批准正式发行，也不解除许可或第三方材料权利要求。

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

正式开放许可 release：受 `CLR-001` 影响。  
包含或再分发外部参考 PDF 的任何 release：受 `CLR-002` 影响。
