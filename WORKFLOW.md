# PD-RW v1.12｜唯一科研决策总控（ChatGPT / WorkBuddy / Codex）

> **唯一主控，不是全文阅读清单。** 先按 [AGENTS.md](AGENTS.md) 确认用户目标、授权、规则版本和当前阻碍；本文件仅保留三循环/六活动、决策与边界。具体操作在对应专题，已完成的证据不重做。**三个决策循环（六项活动，不是六道审批门）**；不新增状态机、审批、自动执行器或论文写作许可。

## 0. 研究目标与优先级

- **范围**：本轮 `USER_SCOPE` 和用户最新原始授权优先；仅用户明确“方向不限”才允许跨学科选题。只有用户选择 PD-RW 才启用；既有独立研究/挽救流程不自动迁移。
- **科学优先**：先评价真实问题的重要性、最强具名近邻差额、可区分的竞争解释与证据路径，再比较成本。允许反向假说、物理/理论机制、新能力、负结果和新基准；初期 UNKNOWN 不自动淘汰，不把方便训练、模型叠加、检索零命中或开发集增益当作创新。需要深度构思时按需读 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)。
- **目标**：以可信 JCR Q2+ 投稿潜力为既有最低成果目标，优先 Q1；实际录用不可保证，`Q2_POTENTIAL_SUPPORTED` 需要证据和具名期刊近似先例，普通可发表性与 `DRAFTABLE` 不等于科研成功。期刊核查与成功标准分别见 [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)、[VENUE_STRATEGY.md](VENUE_STRATEGY.md)。高影响力探索可先保留为假说，不得伪装为已确认贡献。
- **独立评估**：科学事实 > 证据摘要 > 工具/Agent 判断；`VERIFIED/REPORTED/UNKNOWN/INVALID/STALE` 按原证据标识。CI/结构检查不是新颖性或真实 Agent 提升证据。RWF 仅按需复算合法 DEV 结果，科研主张与授权仍归 PD-RW/用户。

## 1. 三个决策循环（六项活动）

**外循环 A｜研究机会：01 搜索→02 数据观察→03 任务。**
01 在用户范围内先 `BREADTH_SCAN → DEEP_FALSIFICATION → COMPETING_CHOICE`，不能因找到首个可行题目就停止；按 [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) 核真实重要性、原始近邻、反例和少量不同失败前提的选择。选定方向后自主筛选主库 D1，基于官方元信息完成 `PRE_DOWNLOAD_SCIENCE_FIT`，提出 `PRE_DOWNLOAD_PLAN`；**选库不等于下载许可**。有授权才获取/复用必需数据、校验并隔离确认池；02 在合法 DEV 观察真实现象和混杂，03 按 [TASK_EXPLORATION.md](TASK_EXPLORATION.md) 确定可评价 Task、合法信息、独立单位、最小判别探针。只读构思可以先于数据到位；不能据此冻结未经证实的实证结论。

**内循环 B｜有效实证：04 算法与评价。**
复用可信简单 Champion、当前 Run 和强公平参照；按 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 先核误差/可学信号，再选有区别预测的机制、系统、理论或测量路线；编码迭代才读 [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md) / [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)。简单基线不是复杂模型的准入门槛，后者应由科学问题、合法信息和预算证明必要性。保护协议、逐样本预测、分组、选择史与评价器，不通过换 seed、换名称或后验切片造增益。负 Pilot 不自动停止 Task。

**外循环 C｜科研价值：05 主张→06 独立确认。**
05 并行核 `CLAIM_EVIDENCE_MAP`：能力/性能、机制、规律/边界、测量或资源权衡，必须与最近邻的真实差额和证据相匹配。首个有效 Run 或重要负结果按需读 [SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md)；区分 `ARTICULATION_GAP` 与 `EVIDENCE_GAP`，优先补重要且可判别的证据，而非自动加模型。可 `UP / DOWN / NARROW / LATERAL / HOLD`，但必须核合法信息和权限；06 只在 Claim、方法、评价协议与选择史冻结，且有独立授权时按 [CONFIRMATION.md](CONFIRMATION.md) 确认。

**机会→算法→科学贡献的最短闭环**：活动01从领域瓶颈、论文矛盾、失效边界、数据/评价缺陷、跨领域原理及可信负面/异常六类线索按需发现问题，先核重要性、具名近邻和最危险未知；活动02–03核真实变量与可反证任务；活动04从**合法实测失败→竞争原因→缺失能力→不同机制预言→最小公平试验**推导算法，而非先叠模块；活动05–06按重大创新、性能突破、科学发现、基础设施、认知纠正五类论文路线对应真实证据，**不新增 Claim 状态或阶段**。详则只由对应专题维护，结果与科研假设允许迭代但保持 EX_ANTE/EX_POST 和独立确认边界。

**高价值实验的升级条件**：真实重要的部署失效、不同科学预测、**新基准或实验范式**、系统级能力、理论/物理约束都可触发研究设计，不强制新网络。按科学主张规划有界 `CLAIM_EVIDENCE_PACKAGE`（公平强对照、关键消融、条件边界、必要部署证据），不是要求所有项目全跑。新增下载、成本、真实 Task/评价协议或 SEALED 改变**须按原门禁由用户批准**；不要把最便宜的 Probe 当作唯一科学目标。

**数据先行是实证执行依赖，不是思想淘汰门槛**：必需数据没有完整验收时只能做文献、公开元信息、理论假说与下载计划，不得拟合、冻结实证 Task 或基于未获得的数据宣称结果；无授权为 `WAITING_FOR_DOWNLOAD_AUTH`，资源不可用记 `WAITING_FOR_DATA`，`DATA_ACQUIRED_VERIFIED` 仅代表文件验收，不代表科学可辨识性。理论证明和无需静态数据的研究按适用方法处理；详见 [DATA_DISCOVERY.md](DATA_DISCOVERY.md)。

## 2. 当前阻碍 → 唯一按需路由

| 阻碍 | 读一份主专题 | 当前交付 |
|---|---|---|
| 新问题/近邻/科学机会 | [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) | `SEARCH_HANDOFF`、未知和最佳不同前提候选 |
| 方向已定、数据源/验收缺口 | [DATA_DISCOVERY.md](DATA_DISCOVERY.md) | `DIRECTION_CARD / PRE_DOWNLOAD_PLAN / DATA_MANIFEST`，按授权行动 |
| 数据现象或可信度 | [DATA_INSIGHT.md](DATA_INSIGHT.md) | 可靠信号、混杂或 `NO_RELIABLE_INSIGHT_YET` |
| Task/信息条件/上探下探 | [TASK_EXPLORATION.md](TASK_EXPLORATION.md) | `PRIMARY_TASK`、合法真值、最小探针；层级问题按需 [TASK_LADDER.md](TASK_LADDER.md) |
| 真实 Run、实现、Bug、负 Pilot | [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) | 有效 Run/定向修复/`NEXT_PROBE` |
| 有效残差且需要新机制设计 | [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md) | 可证伪机制、强替代与授权内实验 |
| 稳定成果、续投/结束评估 | [PAPER_FIRST.md](PAPER_FIRST.md) | 科学 Claim、最近邻差额、决定性证据；复杂收口按需 [POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md) |
| 正式确认 | [CONFIRMATION.md](CONFIRMATION.md) | 合法的独立确认或 `CONFIRMATION_UNAVAILABLE` |
| 工作流/论文/图件专项 | 从 [AGENTS.md](AGENTS.md) 专题路由 | 只读当前需求文件，不启动科研活动 |

项目已有 STATE/Run 时直接续做，首次遇到新阻碍才加载相应专题；不得沿入口→索引→全部文件逐层通读。**授权与下一步回复**统一由 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 决定。

## 3. 下一行动和止损决策

按优先级选择**最能改变当前判断的一项行动**，可在已授权范围内连续完成相互依赖的技术修复：
1. **真实性/权限**：污染、泄漏、非法真值、确认协议冲突或权限不足，先隔离受影响证据；未授权停止在建议/授权需求，不能自动执行。
2. **环境/数据阻断**：完整数据和评价器不可用时先按授权修复前置依赖；工程 PASS 不是科研发现。
3. **科学辨识**：有可信数据而无 Task 就寻找重要科学问题；有 Task 优先最有判别力的合法 Probe，不单凭单次 F1 调整方向。
4. **Claim/再投资**：核不同竞争解释、真实独立差额、资源成本及既有负结果；有重要 Q2+ 候选时按需补必要证据，而非无界训练。
5. **确认**：独立确认必须另获授权，资源污染/不可得时限缩主张或记录 `CONFIRMATION_UNAVAILABLE`。

**科学机会型止损复核**：负 Pilot 先区分评价失效、欠训练、合法信息不足、强基线已解释收益、科学 Claim 不足或独立组不足；一次负结果只约束相应前提，不自动判死整个 Task。若仍有不同且可证伪、成本可承受的下一 Probe，可以建议继续；否则 HOLD 当前机制。不能以“仍有未试假说”作为**无限续投**理由，**项目 STOP/PIVOT 仍归用户**。可选失败诊断见 [FEASIBILITY_ENVELOPE.md](FEASIBILITY_ENVELOPE.md)、[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)。

| 决策范围 | 允许动作 |
|---|---|
| RUN / 机制 | `REPAIR / KEEP / DISCARD / HOLD`，保护旧 Run |
| TASK / 信息条件 | `UP / DOWN / NARROW / LATERAL`，协议与证据独立更新 |
| AREA_DATA / 项目 | 提出保留、暂停或转向选项；重大决策由用户批准 |

**每次最小交接**：`CURRENT_EVIDENCE + SOURCE | BLOCKER/UNKNOWN | NEXT_DISCRIMINATING_ACTION | IF_POS/NEG/INVALID | AUTH/COST`。无新增信息不复写长报告、不重复审阅全部论文/源码。

## 4. 不可覆盖的边界与项目资产

- **权限唯一来源**：用户真实原始指示；方向/数据选择不授予下载、安装、CPU/GPU 拟合、SEALED、付款/外传、重大研究 Task/PIVOT、投稿或写稿。需新授权先交推荐、选项和必要资源，不先给越权执行命令；见 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)。无执行证据记 `NOT_RUN`。
- **科学可复核**：保持原始数据血缘、train-only 预处理、分组独立性、时序因果、真值可靠性、冻结协议和 holdout 隔离。新 Task 不自动继承旧确认资格；DEV/VAL/CONFIRMATION 不混用。工具哈希/JSON/Agent 判断不能替代真实来源。
- **项目记忆**：按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 增量维护 `RESEARCH_RECORD.md` 当前状态/重大失败/下一步，论文内容规划更新 `PAPER_BLUEPRINT.md` 的 H1/H2 与对应 `SEC_ID`；保留 STATE、Run 和原始工件，不新建第三份科研日志。早期规划不是正式文章。
- **写作锁**：科研成果总结经用户审查并独立授权前 `WRITING_LOCKED`，不能自动写投稿标题、摘要、正式正文/初稿。见 [WRITING_GATE.md](WRITING_GATE.md)；既有稿件写作/审核才按需读 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) / [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md)；Word 排版见 [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md)。
- **图片严格 OPT-IN**：只有用户明确要求指定图片才绘制、重绘或生成预览，见 [FIGURE_POLICY.md](FIGURE_POLICY.md)；写作授权不等于绘图授权，反之亦然。无需出图时保留原始证据、提供文字或表格即可。

## 5. 工作流评价与后续扩展

静态/合成检查按 [evals/EVALUATION_POLICY.md](evals/EVALUATION_POLICY.md)；真实改进需同来源、模型、工具、授权、预算的历史盲回放及独立评价，见 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md)。没有真实 Agent 轨迹或可信 Token 遥测则 `NOT_MEASURED`，不能把 CI PASS 写成科研成功率或创新能力提高。

**规则扩展不在此无限追加**：明确规则归属，优先替换/合并旧条款；新科研方法写入对应专题，主控仅增加确实改变全局决策的最短路由。见 [docs/STRUCTURE.md](docs/STRUCTURE.md)。保留原有权限、冻结协议、实验资产和已获确认的研究结果。
