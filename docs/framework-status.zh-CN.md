# Framework / Architecture Status

## 当前基线

- Public manuscript baseline：当前 `main` 上的 canonical QMD。
- Collaboration map：`docs/book-architecture.zh-CN.md`。
- 状态：`CURRENT-PUBLISHED-BASELINE / WORKING MAP`。
- 具体公开版本状态：见 `docs/release-status.zh-CN.md`。

## Approved Framework Snapshot

当前没有采用 HARC 后新创建的 `FW-xxx` 快照。

这不意味着现有公开教材“未经作者批准”或被追溯降级为 provisional；它只表示本项目尚未使用 HARC-lite 的 snapshot 机制记录一次未来的重大结构批准。

## 何时需要新的结构批准

以下变化需要作者明确确认，并可视需要创建版本化 snapshot：

- 全书核心研究/教学问题改变；
- 主要部/章功能发生实质重定义；
- 核心概念或推论关系大规模改变；
- 章节重排会改变全书主要论证/学习路径。

以下通常不需要 Framework Approval：

- 错字、链接、样式、书目元数据；
- 局部表达澄清；
- 不改变章节功能的案例或文献补充；
- 常规教学提示与网页体验改进。

## 与 Release Approval 的边界

Architecture / Framework Approval 回答“核心知识结构是否得到作者确认”；Release Approval 回答“某个具体版本是否允许公开发布”。

二者不得互相替代。重大结构被确认后，具体 release 仍需满足 `docs/release-status.zh-CN.md` 的 release review；反过来，连续修订 Web Edition 的小型发布也不要求每次创建新的 Framework Snapshot。

## 当前 blocker

无结构性 blocker。许可与外部 PDF 权利问题不阻塞教材内容维护，但分别阻塞正式许可发布与该外部文件的再分发决策。
