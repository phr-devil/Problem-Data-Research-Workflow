# High-value research design｜从可发表的小结果到更有价值的科学贡献

> **按需方法库，不新增阶段/审批/评分器。** 服务既有活动01–05：问题搜索→数据能力→任务与科学假设→高潜力机制→决定性实证。论文导向项目的最低成功标准仍是有真实证据支持的 **JCR Q2+ 投稿潜力，优先Q1**；发表/录用无法保证。遵守 [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)、[NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 和 [WRITING_GATE.md](WRITING_GATE.md)。不自动训练、下载、打开封存集或写论文。

**执行优先级（旧文档出现“最小论文优先”时覆盖旧口径）**：先对知识价值、最近邻差额和科学辨识力做可审计的比较，再寻找可执行的最低成本试验；**不能以最便宜的训练、最容易提高F1或任何Q3/Q4可发性代替Q2+科研目标**。可信小成果仍保护。已有数据/Run可直接跳到决定性缺口，不重启搜索。

**可用工具（均为非强制只读辅助）**：`python -m core.scientific_discriminability --metadata DEV_METADATA.json --factor-a device --factor-b class --group subject --role DEV` 检查已获许可元数据的交叉/独立组结构；`python -m core.science_choice_replay --cases evals/science_choice_cases.synthetic.json --blind` 导出不含专家答案的构造场景。两者**不能证明因果关系、选题价值、Q2水平或真实行为改进**。历史冻结回放必须独立准备真实来源和专家参考后另行执行，见[REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md)。

**活动01防首个满意解**：不要求固定3次ChatGPT回复，而要在同一次或2–3轮内先作`BREADTH_SCAN`广搜重要且不同的科学问题，接`DEEP_FALSIFICATION`核最强原文/反证，再以`COMPETING_CHOICE`用至少一次**不同失败前提的替代机会搜索**挑战首选；没有可比备选可以保留唯一首选，但必须记录搜索限制。D1正式选定前通过官方公开元数据做`PRE_DOWNLOAD_SCIENCE_FIT`，未知仅`PREFERRED_PROVISIONAL`，不在未授权情况下读取DEV/test或自动下载。详情见[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)与[DATA_DISCOVERY.md](DATA_DISCOVERY.md)。

## A｜研究问题发现：先评价知识价值，再比较实现难度

借鉴 [STORM](https://github.com/stanford-oval/storm) 的多视角提问、[PaperQA2](https://github.com/Future-House/paper-qa) 的有出处原文核查、[AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) 的不同假说探索思想。**不引入其全文撰稿、自动科研执行或复杂树搜索。**

- 对新方向做一次**互补视角**检查（不是三套Agent）：①现实需求/工程或临床失败造成何种后果；②物理/统计/标注与采集局限说明现有方法**为什么**不足；③现有方法与评价契约的真实边界。跨学科/理论方向用对应领域的知识视角，不默认传感器。
- 对最多3个**不同失败前提**的候选，记录 `PROBLEM_IMPORTANCE`（谁受影响/为何非玩具问题）、`NAMED_NEAREST_ORIGINAL`（已证明什么及未证明什么）、`UNANSWERED_KNOWLEDGE`（成功后领域学到什么）、`DECISIVE_UNKNOWN`、`EVIDENCE_PATH`、`COST`。未读原文、文献证据冲突时记UNKNOWN。**没有论文 ≠ 创新；高被引/高Star ≠ 科学价值。**
- **优先查反例与负面证据**：用户真实需求是否存在；最近邻是否已有同等功能；所谓差异是否仅是数据泄漏/指标不一致；假设成立是否只是换一种表述的已知事实。优先回答一个可能改变选题决定的最危险未知，不无限增长检索清单。
- 高质量机会可能是**重要新能力、机制/规律、可靠边界、现实标注/算力成本，或可推广测量结论**；不限于大模型新网络。不机械地以难题压倒真实可完成的、有Q2潜力的窄问题。
- **Q2校准要真实**：只在候选价值或成稿路线上查真正相关的1–3篇Q1/Q2近年同类型文章，比较知识增量/核心证据。Q2仅目标快照，不按影响因子筛“高分课题”，不推测录用概率。

### 正向科研重要性判断（活动01已有比较内执行，不设新关卡）

在 `UNANSWERED_KNOWLEDGE` 上额外检查三个问题：①**若结果成立或被否定，谁的理论理解、测量方案或实际决策会改变，改变什么**；②能否提出**不同解释对应的可观察结果**，让研究产生新知识而不仅是新分数；③新知识或能力是否存在可信的**迁移、推广或复用价值**（跨约束、场景、研究群体或评估范式），重要的单场景发现也可能成立。简记 `SCIENTIFIC_CONSEQUENCE | DISCRIMINATING_VALUE | TRANSFER_SCOPE_OR_JUSTIFIED_NARROWNESS`，不机械打分、不强求两个场景、不另建文件。负结果能改变重要理解或决策时同样可构成高价值问题。

**科学重要性与实验成本分开决策**：先选择更重要、值得回答的科学问题，再按信息价值/成本选下一实验；廉价 Probe 是切入方式而非对研究价值的降级。已有窄 Claim 时，最多问一次是否存在可信的更一般规律/更高能力，只有对应证据路径值得投资才升级；没有时保留真实窄贡献，不硬造宏大叙事。

## B｜数据库科学辨识力：从“能训练”到“能区分哪些解释”

为每个核心问题列出 **主张→竞争解释→需要独立变化的因素→现有DEV元数据/真值→混杂→确认资源**。下载前仅查官方文档与元数据；依既有授权验收完整必需数据后，才能在合法DEV分析数据；绝不读封存集来择题。

| 检查项 | 必须避免的错误 |
|---|---|
| `CONTRAST` | 所谓条件比较是否只有单一设备/单一人/单一日期，根本无可比对照？ |
| `CONFOUNDING` | 设备、受试者、类别、时间、场景是否完全或近乎绑定？即使交叉出现也不自动因果可识别 |
| `INDEPENDENT_N` | 用真正独立的人/实验批/场景/设备数而非窗口/帧数描述样本支持；标稀疏交叉单元 |
| `LEGAL_INFO` | 预测时点可见的特征/标签预算K、support/query和所用模态是否合法？ |
| `MEASUREMENT` | 标签或代理真值是否实际回答科学主张？数据版本/采集条件/测量仪器是否可靠？ |
| `CONFIRMATION` | 是否存在与最终主张相容、未被选题/调参污染的独立组、数据库或理论/模拟验证？ |

- 结果标`DESCRIPTIVELY_CROSSED`（仅有数据交叉，不证明因果）、`PARTIAL_OR_CONFOUNDED`、`UNIDENTIFIABLE_WITH_CURRENT_DATA` 或 `UNKNOWN`。**不是自动决策或数据合格评分**：研究某条件的预测性边界，可能不需要识别该条件的因果效应；此时收窄主张，不能把相关性写成硬件因果机制。
- 若 D1 无法区分目标假设且还未开始下载，可在**已授权研究范围内**改选更适配的候选数据库；需要新下载/研究范围变更按 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 返回推荐＋用户选择，不提前输出下载Agent指令。
- 仅在独立科学主张真正需要时选择D2；不要用多个共享同一主体/标签源的数据库伪装外部确认。理论/仿真任务对应做参数域、反例与可重复性检查。

## C｜科学问题设计：竞争性解释及区分性预言

候选科学主张最短合同（允许在真实证据未到位时填UNKNOWN）：

`IMPORTANT_QUESTION | NAMED_NEAREST_GAP | LEGAL_SIGNAL | PRIMARY_CLAIM | STRONGEST_ALTERNATIVE | DISTINCT_PREDICTIONS | DISCRIMINATING_EVIDENCE | INDEPENDENCE/CONFIRMATION | Q2_RELEVANCE | IF_POS/NEG/INVALID`

- 同一对照条件下两个解释**预期不同的结果**，才称机制可辨识；若两者都预测同一F1提升，这不是判别实验。不同原因需要不同控制（容量/预算、时间因果、label shift、设备与人、预处理、选择历史等）。
- 有些工作以**能力/测量/成本—性能**为核心，并不具备可识别的因果机制；改用可反驳的功能性差额、可比预算及实际价值，**不强迫伪因果故事**。
- 选择任务前自问：即使模型有效，**新增知识是否超出现有任务定义**？如果只剩已有方法复现/极小DEV增益，保留工程资产，不宣称Q2新贡献；可优先审查另一个科学问题。
- 只有获得合法且真实已验收DEV数据、冻结合适评价协议后，才进入正式Task/基线。探索观察和已证实规律严格分开；独立确认资源不能随选题复用已污染的组。

## D｜高潜力算法机制：保护可靠成果，主动寻找不同杠杆

参考 [RD-Agent](https://github.com/microsoft/RD-Agent) 的研究—开发—实证反馈、[AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) 的差异化分支，以及 [Optuna](https://github.com/optuna/optuna) 的有界自适应试验/剪枝。只复用方法论，不自动安装依赖、多Agent全量搜索或伪称算法创新。

- 默认先复用**可信简单Champion**及其失败组。仅在存在区分性科学预测时生成最多3种不同的 `MECHANISM_OPTION`（**不是三条必须训练的分支**）：合法新信息利用、结构/物理归纳偏置、优化与校准、测量/决策可靠性、资源—性能约束。强制解释`WHY_SIMPLE_BASELINE_FAILS`与`WHY_NEW_LEVER_SHOULD_WORK`。
- **信息价值优先**：先选最能区分假说与强简单替代的零拟合分析或最小正控；有合法证据且预期能改变Q2核心Claim时，才在既有真实授权内做小规模实现/调参。复杂时空结构确实必要可直接选择相称方法，**不强制线性模型成为永久上限**。
- 每次有限探索记录 `BRANCH_PREMISE | DISTINCT_PREDICTION | FAIR_COMPARATOR | FIXED_EVALUATOR | POS/NEG/INVALID | COST_CAP | IF_RESULT_THEN`。优先**淘汰失败前提而非淘汰整个Task**，不通过反复选择seed、DEV切片或同一封存集刷“显著性”。
- 当需要优化同一真实机制时，可借 Optuna 的有界试验/剪枝思想，但不同模型公平比较仍需反映真实调优预算，剪枝只能基于**合法DEV**，不触及holdout。更强方法仍需证实相较公平简单策略的**新增能力**。
- **投入原则**：首轮试验以成本最低为主；若获得可复核的信息，后续允许一组有界实验完成真正Q2/Q1主张，不固定只准一次，也不无界升级。已有可靠小结论不因探索更难机制被覆盖。
- 负结果记录`MECHANISM_REFUTED / INCONCLUSIVE / INVALID`及现存有效证据；没有可辨识改进时按[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)判断是否只补科学证据或用户选择项目级转向。

**阶段04–05的重要反馈**：选题时没预想到的科学现象，可能在真实DEV Run、负结果或成本数据中出现。按需读[SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md)，利用真实新证据比较不同科学主张，防止把首个最低成本小增益过早确认为唯一研究价值。新增条件性规律保持探索性；证据缺失和已证实贡献表述不足是不同问题，不自动追加训练或生成论文稿件。

## E｜选择何时停止“提高论文层次”

只在新方向、主数据选择、Task冻结、**关键机制证据改变**或拟高成本升级/结束时审查一次，不要求每个Run重复文献检索或Q2评级。对每条候选给出：

`SCIENTIFIC_DELTA | CURRENT_EVIDENCE_STATUS | NEXT_DISTINGUISHING_TEST | HIGHEST_CREDIBLE_CLAIM | GAP_TO_Q2/Q1 | EXTRA_COST | PERMISSION`。

若新增实验不能改变**核心新知识、证据可信度或真实应用价值**，优先保留成果并形成**科研成果总结（非论文稿件）**。满足Q2潜力只表示合理投稿竞争力，仍需用户审查科研总结及单独授权写作。没有确认/原始文献/真实资源时保持UNKNOWN。

## F｜最短来源与执行边界

- 来源：STORM（多视角提问）、PaperQA2（原文证据与矛盾）、RD-Agent（研究—开发反馈）、AI-Scientist-v2（不同假说）、Optuna（自适应预算/剪枝）、WILDS/DomainBed（独立环境/公平选模）、Cleanlab（疑似标注问题）。每种工具仅在与当前决策有关时用，**不下载其系统/模型、不复制科研内容**。
- PD-RW 负责**为什么值得研究、什么科学主张、数据能否回答、是否具备Q2潜力**及机制实验决策；实际算法实现/训练由获得用户许可的执行 Agent 承担。RWF 只在存在匹配的真实工件时按需开展 **DEV 指标与协议的独立复算/一致性验证**，不自动负责机制训练、不接管科研主控，也不授予新增权限（见 [WORKFLOW.md](WORKFLOW.md) §v1.7）。任一结构检查、提示词或工具返回均不能自我认证科研创新。
- **NEXT_ACTION_OWNER**：不改变用户授权的只读诊断、已授权技术选择→直接给下一步精简Agent指令；新数据下载/训练预算、重大Task转向、封存/投稿/论文写作→先推荐与选项，绝不提前给执行指令。
