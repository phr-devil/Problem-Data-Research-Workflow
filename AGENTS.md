# AGENTS.md｜PD-RW Agent 唯一默认入口

> **仅导航和权限摘要，不是第二套科研流程。** 用户选择 PD-RW 时才启用；[WORKFLOW.md](WORKFLOW.md) 是科研决策唯一主控。规则按实际阻碍加载，不读全库。

## 0. 冷启动与版本

1. 先核当前用户目标、`USER_SCOPE` 和**原始授权**。已有项目先核编号/研究线/数据集是否指向同一真实目录，按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 做 `PROJECT_IDENTITY_CHECK`；再从已知路径/STATE 定位 `RESEARCH_RECORD_REF`，存在才读 `RESEARCH_RECORD.md` 的**当前快照**；论文任务按需读 `PAPER_BLUEPRINT_REF` 对应 `SEC_ID`，再核相关 Run/协议/manifest。新项目再按需读 [START.md](START.md)。
2. 冷启动、来源不明或规则变化时，在可用访问权限内核**本地 Git HEAD 与远端最新 commit**；有 `.git` 不等于已同步。不一致标 `RULE_SOURCE_STALE`，优先按确定的远端 commit 只读必要规则；未经授权不覆盖本地文件或运行 pull/rebase，获同步许可且工作树干净才允许 fast-forward。不能核远端/来源时记 `RULE_VERSION_UNVERIFIED`，**不声称最新**。同一任务只用可识别版本，简记 `RULE_REPO | RULE_COMMIT | LOADED_FILES`；版本和任务未变就复用。
3. 决策冲突：用户原始授权优先；科研流程由 WORKFLOW 主控；科研事实以实际合法原始工件为准；专业细则仅由对应权威专题负责。既有项目直接续做，不重开选题/数据/训练。
4. **适用规则重核（不是全库重读）**：新会话/Agent接手或上下文压缩后，先核 `RULE_REPO | RULE_COMMIT | LOADED_FILES` 与当前任务的可恢复证据；切换项目、Task/活动、版本或受影响协议时，只重核新增适用的权威专题；新数据下载、收费/危险安装、超范围CPU/GPU、SEALED、绘图、写稿、费用、投稿等受限操作**执行前**再核对应规则和原始许可；H5/H6已选定或原旧项目范围有效时的安全非付费本地DEV安装和CPU/GPU拟合按 [WORKFLOW.md](WORKFLOW.md) 的 `AI_DEV_AUTONOMY` 自主执行，无须逐次确认。已知版本、任务、权限与证据未变时复用；不能确认受限操作的许可时停止该操作并定位原指示，允许无依赖只读工作。Markdown被阅读过不等于工具实际具备权限拦截或Agent会永久记忆。

**人工科学决策冷启动**：新项目H1–H5沿用原选择流程；**H6核心Task/研究组合与H8核心Claim/重大升级需先由AI给带依据的首选和可行备选，再由作者选择或明确范围委托**。H7技术方案、既定策略内DEV算法/训练/修复仍由AI自主，不逐次询问。旧项目H6/H8原记录保留但旧AGENT_DECIDED不能伪装为新作者确认，只有实质战略变动时按新版审核。详见 [AUTHOR_STRATEGY_REVIEW.md](AUTHOR_STRATEGY_REVIEW.md)、[WORKFLOW.md](WORKFLOW.md)；原H9/H10、SEALED与写稿门禁不变。

**最小防漏检查**：核当前活动、适用 H 节点、原证据和实际操作许可；按 [research_activity_protocol.v1.json](contracts/research_activity_protocol.v1.json) 将进入条件、H 决定、交接声明分别审查，禁止用 `declared_activity_ready_not_authenticated` 自授行动。H7/H9 可据证据说明不适用；`REVIEW:H1` ≠ `HEADING:H1`。

**统一人工审核启动合同**：使用 [human_review_protocol.v1.json](contracts/human_review_protocol.v1.json) v1.3。H1–H5仍按用户原选择依次完成；到H6/H8重大科研节点，AI读 [AUTHOR_STRATEGY_REVIEW.md](AUTHOR_STRATEGY_REVIEW.md) 生成 `首选+证据/关键未知+1–2个不同失败前提的备选+作者可选择/委托/暂缓`，核真实原作者消息后才记录已选战略。H7单独由Agent自主决定，普通DEV无需新审批；`can_advance_declarations_only`只是结构检查，不认证作者授权。

**执行前最小规则路由**：H6/H8作者战略选择使用 [AUTHOR_STRATEGY_REVIEW.md](AUTHOR_STRATEGY_REVIEW.md) 和 [EXECUTION_ASSURANCE.md](EXECUTION_ASSURANCE.md) 的选项/选择声明检查；重要Run与负结果仍只做技术/科研证据回收，不把每次实验提升为H8作者审核。没有作者选择时不得宣称新核心Task/Claim已冻结；本地安全非付费已选范围DEV开发由AI继续，权限按原有效消息独立校验。

## 1. 不可跨越的边界

- **授权**：H6作者选定/明确委托策略且H5、DEV及实际运行权限有效后，AI在选定范围内持续自主决定H7算法、依赖安装、CPU/GPU实验、消融、普通机制修复及DEV补证，不逐次问作者；H8只在主Claim或重大贡献升级/科学战略变化时交作者选择。已有旧项目研究授权在无实质变化时继续适用。新库下载、付费/云资源、危险操作、外传、SEALED/正式确认、实际图件/写稿/投稿、超H5方向和项目整体STOP仍守独立门禁。
- **科学价值**：证据严格、构思开放、成本受控；允许科学矛盾、反向假说、跨学科原理、新机制/评价，不以更名、叠模块、DEV 刷分、检索零命中或 LLM 自评认证创新。JCR **Q2+** 是既有最低投稿潜力目标，优先 Q1；详细见 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md) / [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)。**CI 仅证明规则/程序行为**，不证明真实科研能力。
- **论文**：`RESEARCH_RECORD.md` 与 `PAPER_BLUEPRINT.md` 只做增量记录和章节规划；正式标题、摘要、正文/初稿默认 `WRITING_LOCKED`，须科研成果总结经用户审查后另行明确授权。见 [WRITING_GATE.md](WRITING_GATE.md) / [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)。
- **图片**：仅用户明确要求绘制或修改指定图片时出图；图件与写作授权相互独立。见 [FIGURE_POLICY.md](FIGURE_POLICY.md)。

## 2. 按实际阻碍加载专题

| 阻碍 | 只读一个主专题；必要时扩展 |
|---|---|
| 新方向/科学问题/选库 | [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)：`BREADTH_SCAN → DEEP_FALSIFICATION → COMPETING_CHOICE`；高影响力科学问题构思时再读 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)，选库另按需 [DATA_DISCOVERY.md](DATA_DISCOVERY.md) |
| 数据/具体任务 | [DATA_INSIGHT.md](DATA_INSIGHT.md) 或 [TASK_EXPLORATION.md](TASK_EXPLORATION.md) |
| DEV 算法/实验/负结果 | [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 或 [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)；科学信息回收按需 [SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md) |
| 贡献、停止或追加投入 | [PAPER_FIRST.md](PAPER_FIRST.md) 或 [POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md) |
| 正文撰写/已有稿审核/Word | [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) / [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md) / [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md)，按任务选择；写作锁仍有效 |
| 独立确认/期刊/出图 | [CONFIRMATION.md](CONFIRMATION.md) / [VENUE_STRATEGY.md](VENUE_STRATEGY.md) / [FIGURE_POLICY.md](FIGURE_POLICY.md) |
| **跨项目成功/失败/身份追溯** | [LESSONS/CASE_REGISTRY.md](LESSONS/CASE_REGISTRY.md)，仅在明确复盘、案例核查、历史回放时加载；非项目原始科研真值 |
| 工作流维护/测评 | [docs/STRUCTURE.md](docs/STRUCTURE.md) / [evals/EVALUATION_POLICY.md](evals/EVALUATION_POLICY.md)，真实盲评才读 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) |

**专业要求不再复制进默认入口**：正式写作按需参考 [paper_exemplars/README.md](paper_exemplars/README.md)；已授权架构图才读 [ACADEMIC_DIAGRAM_STYLE.md](ACADEMIC_DIAGRAM_STYLE.md)，需要判断局部修改还是全图重构时再用只读工具 `core.figure_change_scope`；不自动绘图。“正文不得清单化或括号堆砌”与“正文生成阶段的图片位置与 Fig. 图题”由写作专题主责。**已授权的论文数据图**由 FIGURE_POLICY 主责，轴、配色、几何 QA 只在出图任务读取。分类不清才读 [modules/README.md](modules/README.md)（INDEX_ONLY）。

## 3. 任务交接与后续扩展

结果按 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 自适应 L1/L2/L3，简报结果、证据及合法下一步；无价值的重复读取、长报告不做。重要科研变化才按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 增量记载；按 [docs/STRUCTURE.md](docs/STRUCTURE.md) 单一权威、最小回归原则修规则，不新增审批。
