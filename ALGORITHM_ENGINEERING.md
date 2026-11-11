# Algorithm Engineering｜从真实误差到可投稿算法的最小工程闭环

**按需读取**：只在 PD-RW 活动03–04 已有真实任务、需要编写/修改算法、批量训练或排查工程阻断时打开；已有有效Run直接续做，不强制重新设计。科研取舍/权限由 [WORKFLOW.md](WORKFLOW.md) 唯一负责，TaskSpec及受保护接口见 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)，论文收敛见 [PAPER_FIRST.md](PAPER_FIRST.md)。本文件是给 WorkBuddy/Codex 等真实执行 Agent 的工作合同，**不是 GPU 执行器、沙箱、新阶段、第二个状态机或训练授权**。

**Q2科研目标**：一项真实算法增益不等于项目成功。按[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)寻找能够支持JCR Q2+投稿竞争力的独立科学结论（Q1更好）；实证证据不足时，优先公平强基线、机制反解释、组级规律或科学升级，而非无意义增加网络。实际期刊录用不作为成功门槛，未审查成果总结/未获单独写作授权不得写稿。

## 1. 先判断该做哪种算法工作，而不是先选网络

| 当前证据/问题 | 最短工程路线 | 不做什么 |
| --- | --- | --- |
| 数据/标签/分组/时间因果/评价不合法 | `REPAIR_EVALUATION`：先修原始契约，版本化受影响协议、重核旧结果 | 不用错误评价器刷分 |
| 最强合法简单基线尚缺/明显不公平 | `BASELINE`：复用或授权后建立同输入、同K、同调优机会的直接参照 | 不先堆新模型 |
| 简单方案有真实残差或可测成本需求 | `SIMPLE_IMPROVEMENT`：校准/残差、特征/融合、阈值、轻量微调或局部组合 | 不把方法简单等同无创新 |
| 相同信息条件下有未解释、可识别的剩余失效模式 | `MECHANISM_CANDIDATE`：一个真正不同的信号/约束/归纳偏置/优化假说 | 不只换backbone或扩大参数 |
| 发现误差可纠正但**预测前信息不可用** | `TASK_INFORMATION_REVIEW`：检查现实合法标定/K、反馈时点；变更Task与协议 | 不追不可部署的Oracle |
| 已有一项潜在增量Claim，缺直接证据而非算法性能 | `PAPER_EVIDENCE`：补公平对照、独立组/成本/关键反解释 | 不为SOTA自动继续训练 |

上表为**选择下一行动**而非六个强制状态；同一真实Run可以同时支持论文证据和方法诊断。没有现成模型也可从物理需求/理论推导启动，但必须写可观察预测，优先以廉价正控核可行性。

**高潜力机制设计与运行反馈**：按[HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md) D，从合法新信息、物理/结构归纳偏置、优化与校准、可靠决策、真实资源约束中找不超过3个不同假设，而不是预订3次训练。用同输入/同K公平强简单参照，明确可区分预言、正控/反解释、失败前提及与Q2科学价值相关的新增知识；只授权内执行最具决策价值的一次，若新证据确实改变科学主张再自主追加有界实验。可借鉴RD-Agent研究—实现—反馈与Optuna的DEV预算内剪枝，但不自动安装外部框架或用HPO替代新颖性。无现有Run/数据时保持`HYPOTHESIZED`；不能用复杂模型容量臆测可辨识性。

### 重要算法机制前的误差来源判别（融入既有 PROBE，不增加关卡）

当设计真正的新机制、拟进行高成本训练或 DEV 失效模式可能由评价伪影造成时，**先复核误差有效性，再比较至少两个有实质区别的合理解释**（如标签/独立组/评价问题、信息不可辨识、容量或优化不足、分布/部署差异、物理先验缺失）。从已有 Run/原始预测/合法元数据选择一个最能区分解释且可能改变算法设计的 `DISTINGUISHING_PROBE`；若某解释已有充分证据被排除，直接引用原证据，不为了凑“两种”而重跑。

将 `COMPETING_EXPLANATIONS | EVIDENCE_FOR/AGAINST | DIFFERENT_PREDICTIONS | CHEAPEST_PROBE | DECISION_IF_POS/NEG/INCONCLUSIVE` 合并进既有 `PROBE_CANDIDATE`，不另建表。强简单基线既是公平比较对象，也是**机制探针**：研究它在哪些预定义条件失败、失败是否可能源于额外信息或协议差异，而不只看总体得分。只有证据足以区别特定误差来源时才声称机制解释成立；仍无法判别时可做获授权的低成本探索，明确 `HYPOTHESIZED`，**不以“尚不能证明机制”为由禁止合法合理的工程优化或新能力探索**。普通调参、Bug 修复和可信结果的补证据不重复本诊断。

## 2. 新算法先答四个科学问题

1. **哪里错**：用真实DEV的原始预测或观测指出残差发生在哪类独立人/设备/时间/事件，以及量级、统计单位、是否后验挑切片。没有Run就写 `HYPOTHESIZED`。
2. **为什么可改善**：明确合法可用的信息/归纳偏置/优化问题/资源约束；区分`Oracle可纠正`、`预测前可辨识`、`可部署获益`，缺合法信息不得靠模型容量填补。
3. **为什么不是简单方法就行**：先比较真实同输入同K的强简单替代；新机制必须有**不同的可观察预言**，例如只在特定可预定义场景改善、标签减少而性能不减、延迟下降但失真范围明确。
4. **论文能增加什么**：对应最近邻的哪一条有限新知识/能力/成本权衡；**小而真实即有价值**，但不能靠开发集随机小增益宣布论文成立。

**新增模块的反包装限制**：若将注意力、Transformer、多尺度融合、对比学习、额外损失等作为*科学创新*，先说明真实瓶颈、为何该机制必要、与同合法信息强简单替代的不同预言，以及最小能否定其必要性的对照。单纯更名、替换骨干、增加参数和后验挑有利指标不构成新机制；普通工程修复/调参仍可直接按授权执行，不必逐次提交创新假说。简单基线是公平参照而非复杂模型的先决阶梯：当时序记忆、物理约束、几何结构或系统问题确有需要时可直接设计相称的复杂方法。

**新机制派单的科学假说溯源（复用原 PROBE，不增加全任务必填表）**：真正新增模型模块、归纳偏置或科研主张时，确保能从既有 `PROBE_CANDIDATE` 读出 `HYPOTHESIS（为什么该机制可能有用） | FALSIFIER（什么可观察结果会反驳它） | CONTRIBUTION_TYPE（现有 CAPABILITY/MECHANISM/LAW_BOUNDARY 或普通工程） | MINIMAL_SUFFICIENT_CHANGE（相对强简单基线只需改什么）`；可继续引用既有 `ERROR_EVIDENCE / DISTINCT_PREDICTION / MINIMUM_TEST`，不是另造 schema，也不是每次 Bug 修复/小超参变化都要写科研假说。若暂不能区分竞争解释，保留 `HYPOTHESIZED` 并只做明确获授权的探索；不能将新增模块自动宣传成原始科学发现。

机制候选复用现有`PROBE_CANDIDATE`及 `python -m core.cli probe-check --file probe.json`：`ERROR_EVIDENCE | LEGAL_LEVER | SIMPLE_ALTERNATIVE | DISTINCT_PREDICTION | MINIMUM_TEST | IF_POS/NEG/INVALID | COST/AUTH`；不新建复杂候选表。**不要求每个调参都填写机制卡**，只在新机制、重要转向或高成本实验时使用。

**基准/任务/系统级路线（沿用原路由，不新增状态）**：当合法证据表明现有 benchmark 无法测试关键能力、评价条件与部署目标错配，或研究需要新的真值/时间因果定义时，先提出**哪些问题在旧评估中不可被识别**，规划可复现的新任务/评价合同、有效真值和公平参照，再评估新测量是否带来独立学术价值。新的协议是**新版本 Task/Claim**，不能静默改变既有冻结评价器或用重新定义指标制造“提升”；公开基准、标签收集和实验仍按授权门禁。创新也可来自**新传感/决策系统组合、物理/生物学归纳偏置、在线学习范式或真实资源边界**，但须映射到具体可观察预言与公平替代，不能用概念灵感或组件数量冒充科学机制。只有确定需要时才增加算法复杂度。

### 从失效机制推导新算法，而非先挑骨干网络（活动04）

1. **定位观察**：用同评价合同的合法 DEV 证据描述 `OBSERVED_FAILURE`；没有有效 Run 时写 `HYPOTHESIZED`，不要把文献猜测伪装为实测。
2. **枚举竞争原因**：优先检查数据真值/泄漏、信息不可辨识、分布变化、任务时序、标定、优化欠充分与资源约束，指定最可能区分这些解释的一项合法核查。
3. **推导缺失能力**：只有排除简单原因后，才在 `LEGAL_INFORMATION / PHYSICAL_OR_STRUCTURAL_BIAS / STATE_ESTIMATION / OPTIMIZATION_OR_CALIBRATION / RELIABILITY_DECISION / RESOURCE_BUDGET` 中选科学上必要的杠杆；纯测量/新评价更适合改变 Task/Claim，不强造网络。
4. **构建对照候选**：按决策需要比较简单修复、机制驱动方法和学习型方案；候选数量不固定，不要求全训练。每个新机制写 `WHY_SIMPLE_BASELINE_FAILS | MISSING_ALGORITHMIC_CAPABILITY | NEW_MECHANISM | STRONGEST_SAME_INFORMATION_ALTERNATIVE | DISTINCT_PREDICTION | MINIMUM_TEST | COST/AUTH`，复用既有 `PROBE_CANDIDATE`。
5. **四重反证**：机制是否已被具名近邻实现？无该机制是否同样有效？相同输入/标注/调参/计算预算下是否公平？能否在主张要求的独立条件下成立？任何结论按真实证据强度记录，缺强基线时标 BASELINE_PENDING。

复杂模型可以是必要选择，但 Transformer/注意力/对比学习等模块叠加本身不构成论文创新。算法提案必须解释它解决哪项可验证的失败前提；满足有效H5和合法DEV持续研发范围后可直接进入代码、拟合与真实实验；超范围另核门禁。

### 功能互补的成熟模块组合：一种合法的机制候选生成方式（按需）

**入口**：只有当前问题存在具体未解决的能力或约束时，才选择模块组合路线；不得以热门程度、Star 数或模块数量直接当创新指标。与从第一性原理设计新方法并列，不要求所有项目使用模块。

1. **按能力检索**：从 `MISSING_ALGORITHMIC_CAPABILITY` 反向查已有可复用技术及近年完整组合（包括不同术语和开源实现）：例如时空表示 CNN/GNN/ViT、时序记忆 SSM/Transformer、状态估计/变点检测、不确定性校准/选择性预测、主动观测/信息预算、物理约束。记录每个候选的 `CAPABILITY | SOURCE/PAPER_OR_CODE | EXISTING_NEIGHBOR_COMBINATION | LICENSE/DEPENDENCY | LEGAL_INPUT`；未核原文或许可记 UNKNOWN。**模型热度仅可作为检索线索**。
2. **检查互补与接口**：明确两个模块各自补什么缺口、是否功能重复，以及它们在 `输入维度/时间因果/标签可得性/同步/数据量/梯度训练/延迟/显存/能耗` 上是否兼容。先排除需要未来标签、测试组统计或额外不可用传感器的方案。
3. **搜索不同耦合方式**：在科学上有理由时比较 `SERIAL（串联） / PARALLEL（并联） / GATED（条件路由） / FEEDBACK（在线反馈） / SHARED_STATE（共享状态）`；不要将这些名称直接等同创新。写清模块间**具体交换什么合法信息、何时交换、为何单独模块和朴素串/并联不能获得目标能力**，以及相对于最强具名近邻的新差额。
4. **有界筛选**：允许在思考阶段生成多个不同机制，实际仅选少量（通常不超过3个不同前提的）候选并优先复用现有组件和代码；先做只读接口检查/可观测预测，再按授权运行最能否定该组合必要性的最小试验。不默认 NAS、排列组合穷举、插件安装或多 Agent 并行训练。
5. **复用原 PROBE**：按需在已有 `PROBE_CANDIDATE` 记录 `MODULE_A_ROLE | MODULE_B_ROLE | COUPLING_RULE | NEAREST_COMBINATION | SIMPLE_COMPOSITION_COMPARATOR | COUPLING_SPECIFIC_PREDICTION | LEGAL_BUDGET | MINIMUM_TEST`，只在组合为科研主张时填写；不是新表单/状态/审批。区分 `ENGINEERING_COMBINATION`（有效工程复用）与有待实验支持的原创耦合 Claim，不能凭新结构图自行升级贡献等级。

**示例（仅概念，不是已证实创新）**：在线接触状态估计决定有限触觉观测的选择，历史预测风险反馈下一时刻的预算；如果状态切换发生时耦合策略对同预算固定选择/独立风险阈值/朴素拼接没有稳定可辨增益，应修正或放弃“耦合必需”假说。真实机器人能耗节省不能仅凭离线遮挡数据宣称。
**H7 算法机制路线AI自主决策（仍须真实科学证据）**：在 H6 已确定科学任务后，AI 对有实质不同科学前提的 `SIMPLE_BASELINE / PRINCIPLE_DERIVED / MODULAR_COUPLING / MEASUREMENT_OR_SYSTEM` 路线提出对照，说明最强近邻、真实失败证据（不足时 `HYPOTHESIZED`）、合法信息、区别性预言、资源与失效风险；AI在有效H5范围内自主选择主要研发路线和非付费本地DEV资源策略，记录强替代、可证伪预言与预计成本，必要时自行实施相应验证。**该选择不授权超H5、付费、危险操作、SEALED或正式确认**。普通已授权 Bug 修复、超参微调、同一机制内有界比较无需逐次回到 H7；确实改变主机制、真实输入/任务、预算上限、外部依赖或科研 Claim 才定向复审。无算法作为核心贡献的测量/科学发现项目可按 H6→H8 直接评估，不强制发明网络。详见 [WORKFLOW.md](WORKFLOW.md)。

## 3. 代码 Agent 的连续有界执行循环

**一次授权内尽量连续完成同一可判别假设**（参考 AIDE、autoresearch 的试验–反馈思想，非直接复制训练器）：

`READ CURRENT STATE/RUN → SELECT ONE ROUTE → CODE DIFF → TARGETED TEST → AUTHORIZED DEV RUN → INDEPENDENT METRIC/FAIRNESS REVIEW → KEEP/REPAIR/DISCARD/NARROW/PAPER_EVIDENCE`

- **范围**：保留受保护数据血缘、目标标签、group split、评价器、封存确认集；只修改TaskSpec允许的 `EDITABLE`。改协议/信息预算必须创建新版本，不覆盖旧Run。外部编码 Agent 在本机实际授权范围内工作；可信来源的本地非付费依赖安装及CPU/GPU训练按H5后的`AI_DEV_AUTONOMY`自主执行；不运行不可信安装脚本、不突破主机安全/组织政策、不付费或外传，SEALED仍需独立许可。
- **代码正确性**：先针对数据形状、mask、时间窗、标签时点、梯度/损失、预测与评价ID对齐做相关测试；在合法DEV和H5自主研发范围核实后可自行tiny-set拟合、真实batch冒烟与正式DEV训练。修复 Bug 时仅重跑受影响用例；科学效果以实际DEV Run判，不写“F1必须提高”的伪单测。
- **训练容错**：每个Run唯一目录记录命令、环境、seed、代码commit/config、数据/协议/评价版本、stdout/stderr、逐样本预测、checkpoint和CPU/GPU/Token/人工成本（可测多少记多少）。OOM、NaN、预处理失败、系统重启先定因并保留原Run为`CRASH/INVALID/PARTIAL`，从合法checkpoint恢复；无法复现明确`NOT_RUN`，不重复全库下载或静默复写历史。
- **预算与公平**：按本轮获授权的时间/算力上限执行；有必要才比较短/长、小/大或不同nuisance超参，同条件给强简单基线合理调优。固定墙钟时间可能不等于同等优化机会，必须按Task说明比较口径；不可仅挑最佳seed/后验切片报告收益。
- **候选管理**：默认始终保留一个最简单可信Champion和一个不同失败前提的Challenger；旧代码/逐样本结果及失败证据永不丢失。连续实验若无新可证伪预测或投稿必要证据，暂停当前机制，而非自动停止Task；允许新证据支持的横向转题。
- **无信息实验止损**：同质调参、换网络名称、重复 seed 或后验切片若不能改变机制判断、可信能力、核心 Claim 或证据可靠性，不因一次最好分数继续扩张；先复用历史结果判断是否需要新的失败前提、新任务或新评价。暂停的是当前分支而不是自动 STOP 项目；不得规定固定三次失败即停止，也不得把高不确定但可判别的研究机会过早淘汰。
- **并行**：只在互不污染的独立任务、授权和GPU/存储资源许可时并行；同一受保护评价器不允许多Agent各自偷偷改。多个开发分支共享对照/预测工件，减少重复训练。

## 4. 每个关键Run之后：先比较，再判断科学证据与小修改价值

先查 `VALIDITY`（指标/数据/评价器/合法输入）→ `COMPARABILITY`（同K、独立组、预算、聚合、调优公平）→ `EFFECT/UNCERTAINTY`（含负面指标与选择历史）→ `NEAREST_WORK_DELTA` → `MANUSCRIPT_GAP`。可用时按 [core/README.md](core/README.md) 调 `run-check` 及 RWF 的独立指标复算；结构通过不代表科学真值或真实确认。

| 实验结果 | 下一动作 |
| --- | --- |
| 有效且支持独立窄Claim，论文只缺1–3项决定性证据 | `EVIDENCE_COMPLETION_PRIORITY`：优先补科学证据；初稿须由用户审查成果总结并另行明确授权，不默认更大模型 |
| 同公平参照有增益，但组数/调参/近邻不明确 | 保留Run，补最便宜的公平性/反解释/文献核查；不立刻宣称论文 |
| 新模型输给简单法，但发现可复现失效规律/成本优势 | 保留简单法和窄Claim候选，规划一个独立验证 |
| 无有效科学增量且新机制没有区别性预言 | 暂停该机制，保留基线与数据，尝试有不同前提的问题 |
| 评价错误或欠收敛 | 只修受影响错误或成对补训练证据，不给科学NO_GAIN判决 |

**已完成算法的小修改**：用[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)选择零训练诊断→最小授权实验→独立验证；没有额外独立知识则保留算法、进入科研成果总结。

**短交接（仅关键结果或转向时更新）**：`BEST_VALID_RUN+ARTIFACT | WHAT_CHANGED | FAIR_DELTA+UNCERTAINTY | NEXT: FIX/PROBE/PAPER | COST/AUTH`。代码、日志与全文在项目文件中，不粘贴长日志，不制作装饰图，不额外启动多Agent投票。

## 5. 来源边界

设计参考（**概念借鉴，不安装/克隆其框架**）：[AIDE ML](https://github.com/WecoAI/aideml)（候选树与保留有效分支）、[autoresearch](https://github.com/karpathy/autoresearch)（有限预算单任务训练反馈）、[RD-Agent](https://github.com/microsoft/RD-Agent)（假说–实验–反馈循环）、[mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent)（轻量代码执行与隔离）；这些项目不能替代PD-RW的合法数据、原始证据、独立确认及真实用户授权。
