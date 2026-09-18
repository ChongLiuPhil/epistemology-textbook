# HARC-lite Onboarding Check

本文件提供《我们如何知道？》的**轻量零上下文接管握手**。它不是每次小修都要重复的仪式。

## 何时执行

以下情况应执行完整 Onboarding Check：

- 新 AI Agent / 新模型第一次接管；
- 无法访问先前对话或长时间中断后恢复；
- 将进行重大正文重写、章节重构、Framework/Architecture 批准或正式 release 决策；
- 发现 manifest、Working Memory、Core、Architecture 或 Release 状态存在明显冲突；
- 人类明确要求重新 onboarding。

同一 Agent 的连续、小范围工作不必重复完整检查，但写入前仍须 fresh-fetch 相关文件。

## 接管前允许与禁止

完成检查前可以：

- 读取仓库；
- 重建状态；
- 检查 revision / path / sync defect；
- 报告 onboarding infrastructure defect。

完成检查前不得：

- 把 AI 提议提升为人类承诺；
- 自行解决 WAITING-HUMAN clarification；
- 批准重大 Architecture / Framework；
- 进行大规模正文重写；
- 宣布新的正式 release 已获作者批准。

## 最小输出

新 Agent 应向人类给出一个简短报告：

```text
BOOK REPOSITORY CONTEXT — ACTIVE

Protocol/profile:
Repository revision:
Current stage:
Current objective:
Primary blocker:
Pending human decisions:
Current task route: CONTENT / FORM / PROTOCOL
Authoritative files:
Architecture status:
Release status:
Permitted next action:
Onboarding status: PASS / PARTIAL / FAIL
```

该报告只是人类校验界面，不是新的权威状态副本。后续工作仍从 GitHub 最新 canonical revision 按需读取。

## PASS / PARTIAL / FAIL

### PASS

Agent 能仅根据仓库准确重建当前任务所需状态，没有阻止当前工作的 onboarding defect。

### PARTIAL

大部分状态可重建，但当前任务的某部分被 clarification、缺失文件、revision conflict、rights/license 或同步缺陷限制。只能执行不受影响的工作。

### FAIL

Agent 无法可靠判断以下任一项：

- 哪些内容是稳定的人类/项目决定，哪些仍是 AI 提议；
- 当前 blockers / pending human decisions；
- 当前 Architecture / Release 状态；
- canonical source 与 legacy/generated source 的边界；
- 当前允许的下一步。

FAIL 时先修复持久化/接管缺陷，不继续高影响工作。

## Repository Context

Onboarding Check 通过时必须确认：

`BOOK REPOSITORY CONTEXT — ACTIVE`

其含义仅是：

- source of truth = GitHub；
- selective retrieval；
- no authoritative session copy；
- read latest before high-impact action；
- read latest before write；
- revision changed => stop / refresh / reconcile；
- invalidate touched cache after write；
- write-through to repository。

动态项目状态不得长期复制进会话作为第二份真值源。
