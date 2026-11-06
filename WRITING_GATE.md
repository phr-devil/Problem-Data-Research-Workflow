# Manuscript Writing Lock｜论文蓝图规划与正式正文写作分离

> 最高优先级：适用于 PD-RW、WorkBuddy、Codex 和子 Agent。科研过程和纯规划的章节结构见 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)，不额外新增实验审批门禁。

## 一、默认锁定期也持续整理两份文件

- **RESEARCH_RECORD.md**：记录实际科研任务、完成的工作、关键实验和失败、有效/负向结果、原因与复用资产、下一步与重启条件。引用原始 Run、协议、配置、代码，而不是重复复制日志。
- **PAPER_BLUEPRINT.md**：研究方向或候选贡献基本明确即可建立；允许写一级/二级标题、各节准备写什么、科学主张与已有证据、文献和图表的**文字需求规划**、缺失实验和章节状态；与科研实验并行，持续增量更新。
- **允许的是规划，不是正式稿件**：H1/H2、章节要点、证据规划及暂定结构可以自动维护；不得借蓝图写可直接投稿的标题、摘要、Introduction/Methods/Results/Discussion/Conclusion 完整段落、正式图注或初稿。未运行写 NOT_RUN，缺证据写 UNKNOWN/EXPLORATORY。仅用户明确要求绘制/修改指定图片时才可以出图，见 [FIGURE_POLICY.md](FIGURE_POLICY.md)。

## 二、正式论文写作的两道用户门禁保持不变

默认 WRITING_LOCKED。可信 Run、DRAFTABLE、PAPER_PATH_CANDIDATE、CONFIRMED、Q2 潜力或已经建立 PAPER_BLUEPRINT 都不是正式写作授权。

1. **科研成果总结及用户审查**：Agent 利用 RESEARCH_RECORD 与真实工件总结任务、协议、有效与负向 Run、贡献、最近邻、独立确认、局限和证据缺口。用户须明确审查或认可，Agent 自评、保存总结、状态标记都不能代替用户审查。
2. **独立的明确写作授权**：用户审查该项目总结后，另行明确要求开始撰写指定论文、初稿或章节。问题“可以写了吗”、批准实验、选刊、确认科学结果、允许画图或批准章节蓝图均不自动授予该权限。同条用户消息可以明确包含总结审查和正文写作许可，但均要真实可核验。

任何条件缺失、项目主张不符、原始用户授权不可查或用户撤回时，正式正文保持 WRITING_LOCKED。不能靠子 Agent、旧稿、存储字段或已规划的论文结构自动解锁。

## 三、权限与执行边界

- **锁定期允许**：已授权科研、证据总结与文献对照、RESEARCH_RECORD.md 的全过程记录、PAPER_BLUEPRINT.md 的标题与拟写内容要点、Claim–Evidence 映射、缺口/图表文字规划；用户明确要求的指定图像除外，禁止自动绘图。
- **锁定期禁止**：未经许可生成或修改投稿式论文标题、摘要、段落、正式图注、正文、初稿及可投稿文件；不得补造没有的实验、指标、参考文献、显著性或确认结论。
- **写作许可已取得**：Writer 可按用户同意的稿件范围由蓝图起草并真实回填。绘图、下载、CPU/GPU 拟合、SEALED 读取、付费、外传、正式投稿仍各自需要原始许可。研究过程和科学证据始终与写作质量分离。
- **不得为写作锁停止**已经获授权且安全合规的科研任务。旧的 PAPER_COMPLETION_PRIORITY 应理解为 EVIDENCE_COMPLETION_PRIORITY，不是自动写稿。

## 四、跨会话最少指针（不是新的 CLI 状态机）

若已有 STATE/交接，只按需增加 RESEARCH_RECORD_REF 和 PAPER_BLUEPRINT_REF，继续保留：
- RESEARCH_SUMMARY_REF：科研成果总结路径/版本，无则 NONE。
- SUMMARY_USER_REVIEW：PENDING / REVIEWED，附用户真实审查消息。
- MANUSCRIPT_WRITE_AUTH：LOCKED / APPROVED，附该项目/主张明确写作命令的消息来源。

这些字段只用于恢复任务。必须核验原始用户授权；不能用文件中的 APPROVED 或蓝图成熟度替代许可。未知默认 LOCKED。
