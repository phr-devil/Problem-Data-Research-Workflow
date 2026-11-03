# PD-RW v1.4｜AI 最短入口

仅在用户明确选择PD-RW时启用。本轮研究范围以当前用户指令为准；[WORKFLOW.md](WORKFLOW.md) 是科研决策与权限的唯一总控，**无需预读所有专题**。

1. **已有项目**：先核真实STATE/Run、manifest和用户授权。若使用 `STATE.json/EVENTS.jsonl`，先查事件一致性；缺工件不冒充有效结果。仅按当前阻碍读对应专题。
2. **新课题**：按 [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) 查机会→ [DATA_DISCOVERY.md](DATA_DISCOVERY.md) 自主选可评价主数据库D1，外部库/备用库按科学需要规划而不凑数量；立即通知用户下载计划，无下载授权不实际获取。
3. **已有开发数据**：按 [DATA_INSIGHT.md](DATA_INSIGHT.md) 看真实现象，再到 [TASK_EXPLORATION.md](TASK_EXPLORATION.md) 选可检验任务；Task Ladder仅在不同合法信息/任务层级有意义时读。
4. **已有任务/运行**：按 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 获取有效Run、诊断负Pilot，编码才读 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)；需要贡献判断读 [PAPER_FIRST.md](PAPER_FIRST.md)，正式独立确认读 [CONFIRMATION.md](CONFIRMATION.md)。

**统一输出**：`NEW_EVIDENCE+PATH | DECISION_CHANGE/UNKNOWN | NEXT_PROBE+可能结果 | AUTH/COST`。不编造运行或检索，不使用封存集调参。新规则不代表额外审批门，现有合法授权范围内可连续执行。
