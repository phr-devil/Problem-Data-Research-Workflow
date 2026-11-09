# AGENTS.md｜PD-RW Agent 唯一默认入口

> **仅导航和权限摘要，不是第二套科研流程。** 用户选择 PD-RW 时才启用；[WORKFLOW.md](WORKFLOW.md) 是科研决策唯一主控。规则按实际阻碍加载，不读全库。

## 0. 冷启动与版本

1. 先核当前用户目标、`USER_SCOPE` 和**原始授权**。已有项目从已知路径/STATE 定位 `RESEARCH_RECORD_REF`，存在才读 `RESEARCH_RECORD.md` 的**当前快照**；论文任务按需读 `PAPER_BLUEPRINT_REF` 对应 `SEC_ID`，再核相关 Run/协议/manifest。新项目再按需读 [START.md](START.md)。
2. 冷启动、来源不明或规则变化时，核本地 Git HEAD 与必要时的远端 commit；同一任务所读文件应来自同一可识别版本，简记 `RULE_REPO | RULE_COMMIT | LOADED_FILES`。本地非 Git 副本、无法联网或未核对时写 `RULE_VERSION_UNVERIFIED`，**不声称最新**。版本已确认且任务不变时复用，不反复拉取/通读。
3. 决策冲突：用户原始授权优先；科研流程由 WORKFLOW 主控；科研事实以实际合法原始工件为准；专业细则仅由对应权威专题负责。既有项目直接续做，不重开选题/数据/训练。

## 1. 不可跨越的边界

- **授权**：下载、安装、CPU/GPU 拟合、SEALED/CONFIRMATION、付费、外传、重大 Task 改变、项目 STOP/PIVOT、投稿不能由 Agent 自授；见 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)、[CONFIRMATION.md](CONFIRMATION.md)。
- **科学价值**：证据严格、构思开放、成本受控；允许科学矛盾、反向假说、跨学科原理、新机制/评价，不以更名、叠模块、DEV 刷分、检索零命中或 LLM 自评认证创新。JCR **Q2+** 是既有最低投稿潜力目标，优先 Q1；详细见 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md) / [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)。**CI 仅证明规则/程序行为**，不证明真实科研能力。
- **论文**：`RESEARCH_RECORD.md` 与 `PAPER_BLUEPRINT.md` 只做增量记录和章节规划；正式标题、摘要、正文/初稿默认 `WRITING_LOCKED`，须科研成果总结经用户审查后另行明确授权。见 [WRITING_GATE.md](WRITING_GATE.md) / [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)。
- **图片**：仅用户明确要求绘制或修改指定图片时出图；图件与写作授权相互独立。见 [FIGURE_POLICY.md](FIGURE_POLICY.md)。

## 2. 按实际阻碍加载专题

| 阻碍 | 只读一个主专题；必要时扩展 |
|---|---|
| 新方向/科学问题/选库 | [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)：`BREADTH_SCAN → DEEP_FALSIFICATION → COMPETING_CHOICE`；科学价值另按需 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)，选库另按需 [DATA_DISCOVERY.md](DATA_DISCOVERY.md) |
| 数据/具体任务 | [DATA_INSIGHT.md](DATA_INSIGHT.md) 或 [TASK_EXPLORATION.md](TASK_EXPLORATION.md) |
| DEV 算法/实验/负结果 | [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 或 [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)；科学信息回收按需 [SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md) |
| 贡献、停止或追加投入 | [PAPER_FIRST.md](PAPER_FIRST.md) 或 [POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md) |
| 正文撰写/已有稿审核/Word | [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) / [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md) / [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md)，按任务选择；写作锁仍有效 |
| 独立确认/期刊/出图 | [CONFIRMATION.md](CONFIRMATION.md) / [VENUE_STRATEGY.md](VENUE_STRATEGY.md) / [FIGURE_POLICY.md](FIGURE_POLICY.md) |
| 工作流维护/测评 | [docs/STRUCTURE.md](docs/STRUCTURE.md) / [evals/EVALUATION_POLICY.md](evals/EVALUATION_POLICY.md)，真实盲评才读 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) |

**专业要求不再复制进默认入口**：正式写作按需参考 [paper_exemplars/README.md](paper_exemplars/README.md)；已授权架构图才读 [ACADEMIC_DIAGRAM_STYLE.md](ACADEMIC_DIAGRAM_STYLE.md)。“正文不得清单化或括号堆砌”与“正文生成阶段的图片位置与 Fig. 图题”由写作专题主责。**已授权的论文数据图**由 FIGURE_POLICY 主责，轴、配色、几何 QA 只在出图任务读取。分类不清才读 [modules/README.md](modules/README.md)（INDEX_ONLY）。

## 3. 任务交接与后续扩展

只输出新增证据及路径、决策或 UNKNOWN、下一合法行动及 AUTH；实质变化才按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 更新两份科研记录。新规则按 [docs/STRUCTURE.md](docs/STRUCTURE.md) 的单一权威、替换优先、最小回归原则落到对应专题，不增状态/重复审批/默认阅读量。
