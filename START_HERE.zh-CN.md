# START HERE — 《我们如何知道？》零上下文接管入口

本文件面向第一次接手本项目、没有旧聊天记录或平台记忆的人类协作者与 AI Agent。

## 第一原则

**GitHub 仓库是项目持久状态的权威来源。聊天、模型记忆、摘要与本地缓存都不是规范真值源。**

在进行重大正文重写、章节重构、形式制度变更或发布策略调整前，先从仓库重建当前状态。

## 最小读取顺序

1. `AHICP_MANIFEST.yaml`
2. `AHICP_CONTEXT_INTERFACE.yaml`
3. `START_HERE.zh-CN.md`
4. `SESSION_CONTEXT_BOOTSTRAP.zh-CN.md`
5. `AGENTS.md`
6. `docs/working-memory.zh-CN.md`
7. `docs/working-memory/current-focus.zh-CN.md`
8. `docs/working-memory/task-plan.zh-CN.md`
9. `core/DECISION_LOG.zh-CN.md`
8. 根据当前任务选择性读取：
   - CONTENT：`core/CONTENT_CORE.zh-CN.md`、`docs/book-architecture.zh-CN.md`、`docs/framework-status.zh-CN.md`、相关 QMD 与文献；
   - FORM：`core/FORM_CORE.zh-CN.md`、`_quarto.yml`、`book.css`；
   - PROTOCOL：本文件、`AGENTS.md`、manifest/context interface、CI 与维护文档。
9. 如果属于新 Agent、长中断、高影响 Architecture/Release 工作或出现状态冲突，按 `ONBOARDING_CHECK.zh-CN.md` 输出轻量接管报告。

`docs/working-memory/work-log.zh-CN.md` 主要用于历史回顾，默认不属于接管必读项。

## Current AHICP / HARC-lite 的项目化规则

本项目以 current AHICP 作为当前协议入口，并保留 HARC-lite 的仓库持久化、任务路由、决策追踪和 fresh-fetch 历史规则；不机械复制第二套治理真值：

- 教材治理文件以中文为 canonical，不强制为每份内部文档维护英文镜像；
- 公共入口 README 继续维护中英版本；
- 普通错字、链接、书目元数据和局部样式修复不需要 Framework Approval；
- 只有会改变全书核心问题、重大概念关系、章节功能或整体架构的修改，才进入结构批准门；
- Architecture Approval 与 Release Approval 是不同的 gate；
- 已公开的现有教材不因采用 HARC-lite 被追溯标记为“AI provisional”。

## 接管成功标准

开始高影响工作前，应能仅凭仓库回答：

- 当前 Web Edition 处于什么阶段？
- 哪些内容/形式/协议决定已经稳定？
- 现在最重要的目标、阻塞与下一步是什么？
- 哪些事项仍需作者决定？
- 当前 Architecture 与 Release 状态是什么？
- 当前任务属于 CONTENT、FORM、PROTOCOL 中哪一类？
- 修改后应运行哪些检查、何时才算完成？

如果无法回答，先修复仓库状态或提出 clarification，不要用旧聊天填空。


## 当前 Stack baseline

- AHICP: `0.3.0-draft @ ed5a60b1016497472072db108072ace59bcdb65d`
- PPF: `0.1.1-draft @ e660b48fb216c28c8faa1f0fe2d0816401e1de2c`
- Vault Interface: `79d64b12275a5cc7c09236b144bf4213fa7afc5e`
- Starter: `4889739d448a9bf68bedb42ce3182315eda0caeb`
- production/security baseline：Workers Builds Native / Profile A / workers.dev canonical / GitHub Pages retired，全部保持不变。
