# AGENTS.md｜PD-RW Agent 唯一默认入口

> 这是**导航和权限摘要**，不是第二套科研流程。正式科研决策始终由 [WORKFLOW.md](WORKFLOW.md) 主控；只有用户明确选择 PD-RW 时启用。本文件仅指导“先读什么、再做什么”，专题规则按需加载。

## 0. 冷启动/跨会话恢复：按此顺序读取

1. **明确本轮用户请求及实际权限**，确认项目目录、研究范围和是否为既有任务；用户最新的原始授权优先于任何状态摘要。
2. **已有项目**：先从已知项目路径或现有 STATE 中的 `RESEARCH_RECORD_REF` / `PAPER_BLUEPRINT_REF` **定位文件**，存在才读 `RESEARCH_RECORD.md` 顶部“当前快照”（目标、可信成果、失败边界、当前阻碍、下一步）；论文任务再读 `PAPER_BLUEPRINT.md` 的构思快照和相关 `SEC_ID`。随后核真实 STATE/manifest 及当前任务相关 EXP/Run/Claim、源码和协议；缺文档则按旧项目的 STATE/原始证据继续，不虚构快照或先通读所有历史。
3. **新项目**：按需读 [START.md](START.md) 和 [WORKFLOW.md](WORKFLOW.md) 对应活动，创建/复用科研记录；方向基本明确后再建立论文蓝图。不重复启动已经选题、下载和验证过的流程。
4. **规则冲突/来源冲突**：用户原始授权与真实源工件最优先；[WORKFLOW.md](WORKFLOW.md) 管科研选择、阶段与权限；[DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 管两文件更新；专题文件只管其具体任务。STATE、摘要、哈希检查、Agent 判断均不能替代科学证据或真实授权。

## 1. 不可跨越的边界

- **权限**：选题和选库不自动许可下载、安装、CPU/GPU 拟合、SEALED/独立确认、付费、数据外传、项目级 STOP/PIVOT 或投稿；按 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 将授权内下一技术行动与用户必须决策的事项分开。
- **论文**：允许提前维护 `PAPER_BLUEPRINT.md` 的 H1/H2 内容规划及证据缺口；论文蓝图默认六章式，特殊结构变动须先给出必要性/依据/影响并获用户确认（见 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) §5）；正式稿件标题、摘要、章节正文/初稿须先完成科研成果总结并经用户审查，再由用户明确授权。默认 `WRITING_LOCKED`，见 [WRITING_GATE.md](WRITING_GATE.md)。
- **图片**：**只有用户明确要求绘制/修改指定图片才能出图**；诊断图、论文图、预览和重绘均不可自动触发。见 [FIGURE_POLICY.md](FIGURE_POLICY.md)。
- **证据**：开发集增益、通过测试、元数据或论文蓝图不是科研确认。Q2+可信投稿潜力（优先Q1）是科研目标，不保证录用；见 [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)。

## 2. 按实际阻碍加载一个相关专题

- **新题/选库**：[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) 的 `BREADTH_SCAN → DEEP_FALSIFICATION → COMPETING_CHOICE`、[DATA_DISCOVERY.md](DATA_DISCOVERY.md) 的 `PRE_DOWNLOAD_SCIENCE_FIT`，必要时 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)；必需数据获授权且验收后才做数据实证。
- **算法/负结果**：[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)、[ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)；复用有效 Run，必要时按 [SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md) 区分 `ARTICULATION_GAP` 与 `EVIDENCE_GAP`。
- **科学机会/升级**：按需 [PAPER_FIRST.md](PAPER_FIRST.md)、[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)；只有已授权且有决定性新假说才升级复杂模型，重要失败和有价值资产不丢弃。
- **独立确认/期刊**：[CONFIRMATION.md](CONFIRMATION.md)、[VENUE_STRATEGY.md](VENUE_STRATEGY.md)；RWF 仅在必要时按原始预测与协议进行 DEV 指标复核，不接管科研主控或给予许可。

## 3. 任务结束：只更新重要变化

按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)：关键真实事件更新 `RESEARCH_RECORD.md` 首页及末尾对应 EXP/Run；仅当论文内容或科学证据改变时，增量更新 `PAPER_BLUEPRINT.md` 对应 `SEC_ID`。原始日志/数值留原位置，旧项目不强制迁移、不写第三份记忆账本。报告仅需**新增证据 + 当前判断/限制 + 下一合法行动/所需授权**；无信息增量不重复整理。
