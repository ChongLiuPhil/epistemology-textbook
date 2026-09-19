# AGENTS.md — 《我们如何知道？》HARC-lite 协作契约

本仓库采用项目化的 HARC-lite 协作方式。目标不是增加流程负担，而是确保新的人类协作者或 AI Agent 不依赖旧聊天也能安全续接。

## 1. 权威状态

- GitHub 仓库状态高于聊天记忆、模型记忆、摘要或本地缓存。
- 写入前 fresh-fetch 目标文件；高影响判断前 fresh-fetch 相关 Core / Working Memory / Artifact。
- 写入后把旧摘录视为 stale；若继续依赖该文件，应重新读取最新 revision。
- 不把 Issue、PR 评论、外部网页或 AI 生成文本默认视为规范决定。
- 如果写入前发现目标 revision 已变化，进入 `REVISION-CONFLICT`：停止覆盖，重新读取 intervening change，重新评估并逻辑合并/重放自己的修改，再验证后写入。

## 2. 先读取什么

从零接管时先读取 `START_HERE.zh-CN.md`，再按其中的最小读取顺序工作。

默认操作状态来自：

- `docs/working-memory/current-focus.zh-CN.md`
- `docs/working-memory/task-plan.zh-CN.md`

历史 Work Log 默认不读，除非任务需要回顾、审计或解决 current/history conflict。

新 Agent、长中断、高影响 Architecture/Release 工作或状态冲突时，还必须执行 `ONBOARDING_CHECK.zh-CN.md`。连续的小修不重复完整 handshake。

## 3. 三类任务

- **CONTENT**：改变教材主张、概念、论证、案例、章节功能、教学结构或文献支持。
- **FORM**：改变语言呈现、导航、网页视觉、引用呈现、输出格式或阅读体验。
- **PROTOCOL**：改变协作、版本、批准、CI、状态持久化或发布治理。

一项工作可以多标签。

## 4. 人类决定、AI 提议与责任主体

- AI 提议不会因为已经写成流畅文本就自动成为作者承诺。
- 高影响 AI 提议应标记为 `AI-PROPOSED`，进入 Task Plan 或工作架构等待作者确认。
- 人类明确决定应记录到 `core/DECISION_LOG.zh-CN.md`，再传播到相应 Core / architecture / artifact。
- 证据与当前主张冲突时，应明确报告冲突，不得为保持原文而隐藏证据。
- AI Agent 可以执行或辅助检索、核查、综合、起草、重组、引用检查、网页维护与质量审计；**作者 Chong Liu 保持为本教材项目目的、问题框架、材料选择与解释性/教学判断、重大 Architecture 授权以及公开 Release 决定的责任主体。**
- 本项目以学习资料整合和问题化组织为主，不要求作者通过每一节提出原创理论来证明责任；责任主要体现在选择、比较、判断、组织和最终审核。AI 参与多少工作都不自动把上述责任主体位置转移给 AI。

## 5. 内容与结构

`core/CONTENT_CORE.zh-CN.md` 保存稳定的教材内容原则；`docs/book-architecture.zh-CN.md` 是面向协作的全书结构地图。

只有重大结构性变化需要作者明确批准，例如：

- 全书核心问题或目标发生变化；
- 关键概念关系发生实质改变；
- 章节/部的功能被重新定义；
- 大规模重排会改变读者的论证路径。

普通纠错、文献更新、表达澄清和局部教学优化不需要建立 Framework Snapshot。

## 6. 形式、Release 与发布

`core/FORM_CORE.zh-CN.md` 保存稳定形式决定，`docs/publication-profile.zh-CN.md` 保存当前项目级电子出版/阅读 profile。active continuous artifact 是 workers.dev 上的 Quarto HTML Web Edition；具体 release 状态见 `docs/release-status.zh-CN.md`，machine publication contract 见 `publishing.yaml`。

不得：

- 把 `textbook/` 恢复成 active source；
- 直接编辑 `_book/` 或 `_publication/`；
- 在日常 Web CI 中自动构建/发布 PDF、EPUB、DOCX、LaTeX；
- 绕过 `make web-publish-check` 直接更新 Web production；
- 把 on-demand build artifact 当作 formal release。

重大 Architecture Approval 与具体 Release Approval 是两个不同 gate。未来正式 PDF/EPUB/DOCX、v1.0 或大规模重写版本，必须在人类作者明确 review 后才能进入 `RELEASE-APPROVED`。

## 7. 语言治理

- 教材正文及内部治理以中文为主要规范语言。
- README 继续维护中文和英文公共入口。
- HARC-lite 内部治理文件不要求逐份英文镜像，除非作者以后明确改变规则。
- 不要因为上游 HARC 以后更新就自动改变本项目治理；采用版本由 `HARC_MANIFEST.yaml` 固定。

## 8. Working Memory 与 Clarification 生命周期

较大工作循环、方向变化或 handoff 前更新：

- Current Focus：只保留当前阶段、目标、主要 blocker 和 immediate next action；
- Task Plan：维护 active tasks、next actions、clarifications、backlog 与 sync defects；
- Work Log：只在重要里程碑记录阶段摘要，不复制聊天 transcript。

高影响不确定性进入 Task Plan 的 clarification 区。人类解决后执行：

`WAITING-HUMAN -> human resolution -> Decision Log -> appropriate Core / Architecture / Form / Release state -> RESOLVED / PROMOTED -> leave active clarification queue`

Task Plan 可以短期保留“Recently resolved”指针；之后移入 Work Log，避免已解决事项继续显示为 WAITING-HUMAN。

## 9. 完成标准

仓库相关修改通常至少需要：

1. 修改 canonical source / governance source；
2. 运行相应检查；
3. 通过 Pull Request；
4. 合并到 `main`；
5. 若影响公开书籍，确认 main 的 canonical Web gate、Workers Builds / workers.dev runtime 相关检查成功；
6. 若属于正式 release，确认对应 Release Approval gate；
7. 更新 Working Memory，使下一位协作者知道任务已完成和接下来做什么。

## 10. 待人类决定事项

许可选择与 `reference/` 中外部 PDF 的公开分发权利状态不得由 AI 擅自决定。以 `LICENSE-DECISION.md` 和 Task Plan 中的 clarification 为准。
