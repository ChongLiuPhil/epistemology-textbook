# AHICP Project Session Context Bootstrap — 《我们如何知道？》

当前会话只保存最小 repository resolver，不复制教材动态状态。

```text
AHICP REPOSITORY CONTEXT — ACTIVE

Control:
- AHICP_MANIFEST.yaml
- AHICP_CONTEXT_INTERFACE.yaml

Compatibility:
- HARC_MANIFEST.yaml
- HARC_CONTEXT_INTERFACE.yaml

Working Memory:
- docs/working-memory.zh-CN.md
- docs/working-memory/current-focus.zh-CN.md
- docs/working-memory/task-plan.zh-CN.md

Content/Form:
- core/CONTENT_CORE.zh-CN.md
- core/FORM_CORE.zh-CN.md
- core/DECISION_LOG.zh-CN.md
- docs/book-architecture.zh-CN.md
- docs/framework-status.zh-CN.md

Publication:
- publishing.yaml
- docs/publication-profile.zh-CN.md
- docs/release-status.zh-CN.md
- docs/cloudflare-readiness.yaml

Policy:
- repository-backed
- selective retrieval
- no authoritative session copy
- fresh-read before high-impact action/write
```

当前 production baseline 是公开 workers.dev Web Edition；Profile A、Workers Builds、canonical URL 与 GitHub Pages retirement 均保持原状态。
