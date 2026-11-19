# PD-RW v1.14｜唯一科研决策总控（ChatGPT / WorkBuddy / Codex）

> **唯一主控，不是全文阅读清单。** 先按 [AGENTS.md](AGENTS.md) 确认用户目标、授权、规则版本和当前阻碍；本文件仅保留三循环/六活动、决策与边界。具体操作在对应专题，已完成的证据不重做。**三个决策循环（六项活动，不是六道审批门）**；不新增状态机、审批、自动执行器或论文写作许可。

## 0. 研究目标与优先级

- **范围**：本轮 `USER_SCOPE` 和用户最新原始授权优先；仅用户明确“方向不限”才允许跨学科选题。只有用户选择 PD-RW 才启用；既有独立研究/挽救流程不自动迁移。
- **科学优先**：先评价真实问题的重要性、最强具名近邻差额、可区分的竞争解释与证据路径，再比较成本。允许反向假说、物理/理论机制、新能力、负结果和新基准；初期 UNKNOWN 不自动淘汰，不把方便训练、模型叠加、检索零命中或开发集增益当作创新。需要深度构思时按需读 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)。
- **唯一成果目标（论文导向）**：尽可能快地形成真实、可独立支持的高水平、高引用潜力论文成果（Q1优先，可信JCR Q2+投稿潜力为最低门槛）；科研问题、数据、算法和贡献类别均为可调整的手段，不能因完成原先的研究计划就宣称成功。比较知识重要性、最近邻差额、受众与可复用性、形成必要证据的最短周期及资源成本；不保证录用或引用，不因求快跳过真值、强基线、合法评价与独立确认。重要Run后优先识别更强、真实的论文Claim及最快补证据路径；正式写稿/绘图/投稿另守原授权。见 [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)、[VENUE_STRATEGY.md](VENUE_STRATEGY.md)。
- **独立评估**：科学事实 > 证据摘要 > 工具/Agent 判断；`VERIFIED/REPORTED/UNKNOWN/INVALID/STALE` 按原证据标识。CI/结构检查不是新颖性或真实 Agent 提升证据。RWF 仅按需复算合法 DEV 结果，科研主张与授权仍归 PD-RW/用户。

## 1. 三个决策循环（六项活动）

**状态兼容保证**：v1.4不新增H节点、科研活动或Claim状态；只将新项目H3/H4/H6变成三次可核的作者决策，并把H5与H6绑定。已有v1.3单次H6及更早项目的有效选择、科学Run和原许可保持原貌，只有实际受影响的重大战略才局部重开。

**新项目执行入口约束（v1.4）**：可信项目路由器应调用 `core.human_decision_review.review_new_project_choices()`（CLI `--new-project-choices`），活动03交接调用 `core.contracts.review_activity_handoff(packet, new_project=True)`，宿主DEV预检传入 `new_project=True` 和经独立验证的三次选择链。H3/H4/H6分别绑定当前展示选项的摘要与不同原始作者消息；H4引用H3、H6引用H3/H4，H5与H6同一方案及回复。仅声明/哈希不能认证消息。`review_new_project_h6` 只供历史v1.3单次H6包兼容，不用于新v1.4。

**新项目三次论文导向选择（H3→H4→H6）**：启动配置H1/H2已给出的目标、资源和限制不重问。Agent在H3前进行有界宽搜（通常6–10初步机会，视证据扩缩）、强近邻原文与反证、论文重要性/受众/潜在复用、关键真值和成本对照，再提供通常3个不同失败前提的科研问题，等待作者**第一次**具体选择；H3未定不冻结H4。随后针对所选问题核2–3种数据库/理论证据路径的真实标签、独立单位、混杂、许可及确认可达性，给出首选与替代，等待作者**第二次**H4选择；H4不是下载/训练授权。Agent依据H3/H4准备H5论文问题/证据边界草案及H6不同贡献路线（包括传统算法有意义改进、机制、测量、评价、系统或新算法），比较高水平发表差额、最小决定性实验、时间成本与合法转向范围，等待作者**第三次**H6选择；H5与H6同回复确认而非第四次选择。三次须有各自展示卡、独立原始回复与摘要链；泛泛继续、旧宽泛委托或AI自填声明不算。只暂停依赖未选战略的动作，已许可的只读探索可继续。旧项目有效选择不追溯重问；普通H7自主管理。

### 新项目默认使用者深度参与模式：决策、依赖与冲突的唯一总控

**`USER_DEEP_PARTICIPATION`**：新项目真正需要作者分别选择的是H3论文问题、H4证据路径、H6具体Task与贡献/可变策略（H1/H2复用启动配置，H5由AI草拟并与H6确认）。H8仅核心主Claim冻结/实质升级或跨战略转向时由作者选择；H7由AI连续自主。每次有首选、可信近邻/反证、独立证据、成本及不同失败前提备选；普通调参、旧算法替代新算法及原范围内的DEV不重问。具体卡片见 [AUTHOR_STRATEGY_REVIEW.md](AUTHOR_STRATEGY_REVIEW.md)。

| 人工节点 | 科学决策对象 | 证据与依赖 |
|---|---|---|
| H1｜01 | 学科范围、科学目标、资源与风险偏好 | 用户当前原始指令；已明确的不重问 |
| H2｜01 | 六类选题来源、五类兼容贡献倾向及搜索重点（可按需参考12类贡献×6条研究路线） | AI 比较可多选的路线；贡献类型只是预期而非已证实结果 |
| H3｜01｜作者选择 | 具有高水平发表/引用潜力的核心科学问题与合理备选 | Agent先广搜、深查具名近邻和反证，作者第一次选题 |
| H4｜01｜作者选择 | 支持所选H3问题的数据/理论证据路径 | 真值/独立性/混杂、许可、外部确认成本经比较后由作者第二次选择；选库不授下载 |
| H5｜01｜Agent草案、H6同意 | 最终研究问题和可证明的论文主张边界 | Agent基于已选H3/H4及真实合法数据/理论证据草拟，随H6第三次回复确认，不另设人工步骤 |
| H6｜03｜作者选择 | **核心Task与研究策略RSS**：AI推荐1个首选与1–2个可行替代，比较科学价值、12类主贡献、6路线、5类竞争力、真值/对照/反证、验证时间/成本与风险；作者选择/明确委托后方可冻结主Task与策略 |
| H7｜04｜AI决策 | 主要算法机制、实验策略与本地DEV算力调度 | AI依据强替代、机制预言和成本自主实施；非算法路径可说明不适用 |
| H8｜05｜作者选择 | **核心科学Claim与重大贡献升级SCU**：AI在可信正负结果/近邻差额基础上推荐KEEP、UPGRADE、NARROW/REFRAME/HOLD及科学主张/成本/确认缺口；作者选择或明确委托；普通DEV增量无需重问 |
| H9｜06 | 最终确认主张/协议冻结及独立确认执行许可 | H8、选择史、确认资格；SEALED与其他原授权不变 |
| H10｜06/成果 | 科研总结审查、论文下一步选择 | H8及已完成或不可用确认的真实结果；正式写作再单独授权 |

**H6战略选定后的持续自主研发（AI_DEV_AUTONOMY）**：作者通过H6选定/有限委托主科研策略后，且实际H5研究范围、数据验收、合法安全非付费DEV条件成立，AI可以自主完成H7、算法设计、安装可信本地依赖、CPU/GPU训练/调参/消融、失败修复、复现实验、DEV评价纠错与普通分支HOLD，无须逐次确认。首个Run和关键负结果允许AI在原选定策略下连续补证与科学审计，不能把未经作者选择的新主Claim或重大投入转型冒充H8已批准。H8作者选定核心主张/升级范围后继续自动研发，只有超出选择/委托范围的实质性策略更换才重新提交H6/H8。新数据下载/外传、真实付费、危险设备/人体风险、SEALED/正式确认、超H5科研方向和整体STOP、绘图、正式稿件及投稿依旧分别核独立门禁。**H6/H8的作者科学选择不等于每次实验授权，也不能替代工具宿主独立校验实际操作权限。** 任何未知权限只阻断相关受限动作；已授权部分继续。

**统一的人工审核协议（v1.4）**：[human_review_protocol.v1.json](contracts/human_review_protocol.v1.json) 是本文件H1–H10的机器镜像。新项目H3/H4/H6分别确认，H5与H6共同确认；原选择、版本、任务及依赖必须可复核；`review_new_project_choices`只能检查声明结构，执行权限须宿主认证原消息。v1.3单次H6及v1.2历史结果保持兼容、不可自动升级为v1.4已批准。

**作者节点的最小交互**：只呈现当前待选卡片H3、H4或H6；前两步加深科学思考而不是固定等待时长，按真实信息收益决定检索深度。H3选科研问题，H4选证据资源，H6选具体论文贡献、Task和技术转向范围；H5是草案不另问。H8仍为重要主Claim变更选择。用户可明确有限委托，但未经真实对应卡片的选择不能直接代替三次独立决定；不重复询问已确认内容或已有有效旧项目。

**执行与验证边界**：结构校验器 `core.human_decision_review` 的 `can_present_review_declarations_only` 仅意味着**所声明的前置条件**可安排本节点审核；`can_advance_declarations_only` 仅意味着**所声明的本节点与依赖**字段完整。二者都须人工核真实原消息/证据，均**不是下载、CPU/GPU、SEALED、绘图、稿件授权**。旧项目的无版本决策记录保留旧读取路径，未核同义性不得仅根据同名H编号自动迁移到新版。真实交互效果需按 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) 另做真实轨迹回放；静态CI不证明AI履约。

**标识与非数据路径**：人工审核 `H1–H10` 在记录中写 `REVIEW:H1` 等，避免与论文章节的 Markdown `H1/H2/H3`（`HEADING:H2`）混同。理论、形式证明、仿真或无静态数据库的研究仍执行 H4，但审的是 `PROOF_PATH` / 模拟器/证据约束与成本，不强制虚构D1、下载文件或已获得的DEV实验。用户此前已明确题目/来源/预算/资源时可在一条消息内满足多个H节点，旧项目已有合法决定直接复用。

**严格依赖（v1.4）**：H1/H2启动配置 → H3问题作者选择 → H4证据路径作者选择 → Agent形成H5最终问题草案 → H6论文贡献/Task作者选择并确认H5 → H7合法DEV连续执行 ↔ H8重大主Claim/策略作者选择 → 适用H9/H10。H4卡绑定H3，H6卡绑定H3/H4，不能同一条作者消息补造三个回应。证据导致问题改变才重开H3；数据路径失效只重开H4及其受影响依赖；普通算法路线与基线切换在已批准DEV范围内由AI自主，不因偏离原“新算法”主张而强迫终止。

**冲突优先级**：科学事实/独立性/合法权限不可越界 > 最新可核用户选择及有限委托 > 具名来源与决策依赖 > AI推荐、热度、成本启发式。用户可以选择高风险方向，不能使无效真值变可靠证据。不能同时满足的目标须列“保留/牺牲/成本/关键未知”并交用户取舍，不暗中以加权评分替代。

**局部回退与机会型转向**：原先研究目标/贡献和算法只是论文成果的暂定路径：有效Run若显示有意义的传统方法改进、可靠性/机制/测量等更强论文机会，Agent主动比较最近邻、真实差额、确认成本、替代解释与发表价值，在H6授权边界内可继续低成本DEV；正式更换主Claim、超出H6允许的科学策略则触发H8；改变核心研究问题重开H3并局部审H4/H6；新数据库/受限操作仍需独立授权。探索性发现不得改写成事前预注册；旧Run/负结果保留。

**论文框架强制事件检查**：01方向或03具体Task明确后建立 `PAPER_BLUEPRINT.md`；04重要有效Run/关键负结果、05核心Claim及路线变化、06科研总结与任一阶段/项目交接，在原 `RESEARCH_RECORD.md` 重要事件记录 `EVENT_KIND | BLUEPRINT_CHECK: UPDATED/NO_CHANGE_NEEDED | BLUEPRINT_SECTIONS | BLUEPRINT_EVIDENCE | BLUEPRINT_REASON`。Agent从合法原始证据检查逐节拟写内容、Claim–Evidence、反证和适用范围，确需变化则只更新受影响章节，否则给出有证据的 `NO_CHANGE_NEEDED`。普通调参/重复测试/无实质Debug不触发。交接前复核真实检查结果与SEC_ID；`core.doc_integrity` 仅验证结构，不授科研正确、结构变更、正式写作或图片许可。详见 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)。
**六活动交接**：科研义务见 [research_activity_protocol.v1.json](contracts/research_activity_protocol.v1.json)。交接字段、活动进入证据、H 节点选择与**实际操作授权**分开；仅声明齐备不等于合法推进。理论/仿真 Claim 使用有界 `NON_DATA` 证据与独立核验，不伪造 Run/SEALED；实证 Run 规则不放宽。H7/H9 的不适用须有理由、来源且不能冒充成功。

**决策记忆（约束与策略分层）**：继续复用`RESEARCH_RECORD.md`/STATE，不增第三账本。H3/H4/H6分别记录选项卡摘要、真实作者消息引用、选中或委托的范围及依赖；恢复时区分 HARD（学科/预算/数据许可/SEALED及操作授权）、ADAPTIVE（初始算法、贡献、Task的已批可变范围）、EVIDENCE（真假与新颖性随Run更新）。被改变的依赖局部重核；硬约束不得因论文目标被覆盖。H7重要变化登记AGENT_DECISION_REF，H8新主Claim登记真实作者选择。

**外循环 A｜研究机会：01 搜索→02 数据观察→03 任务。** 六活动是默认研发组织方式，不是额外六道审批，按事实局部回退。
01 在用户范围内先进行论文机会广度搜索、具名近邻反证与竞争性假设比较，经过H3作者问题选择再深入H4数据/PROOF_PATH可辨识性、真实群组与证据路径比较；没有H4作者选择不得视为已选数据库。H4及下载真实授权齐备才按需获取/复用数据。观察合法DEV后由Agent准备H5草案，在H6作者选中具体贡献/Task后开始已许可技术研发；理论路径不虚构数据。仍按[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)、[DATA_DISCOVERY.md](DATA_DISCOVERY.md)与[TASK_EXPLORATION.md](TASK_EXPLORATION.md)开展相关部分。

**内循环 B｜有效实证：04 算法与评价（机制按需）。**
复用可信简单 Champion、当前 Run 和强公平参照；按 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 先核误差/可学信号，再选有区别预测的机制、系统、理论或测量路线；编码迭代才读 [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md) / [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)。简单基线不是复杂模型的准入门槛，后者应由科学问题、合法信息和预算证明必要性。保护协议、逐样本预测、分组、选择史与评价器，不通过换 seed、换名称或后验切片造增益。负 Pilot 不自动停止 Task。

**外循环 C｜科研价值：05 主张↔04 研发→06 独立确认。**
05 并行核 `CLAIM_EVIDENCE_MAP`：能力/性能、机制、规律/边界、测量或资源权衡，必须与最近邻的真实差额和证据相匹配。首个有效 Run 或重要负结果按需读 [SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md)；区分 `ARTICULATION_GAP` 与 `EVIDENCE_GAP`，优先补重要且可判别的证据，而非自动加模型。可 `UP / DOWN / NARROW / LATERAL / HOLD`，但必须核合法信息和权限；06 只在 Claim、方法、评价协议与选择史冻结，且有独立授权时按 [CONFIRMATION.md](CONFIRMATION.md) 确认。

**科研策略RSS与贡献升级SCU（H6/H8作者真正做选择）**：问题来源六类、贡献C01–C12、路线R1–R6及五类竞争力P1–P5是不同轴，不枚举360种组合。H6 AI应提出优先候选：评价纠错(C09+C12)、机制/失效(C08+C11)、问题与评价(C05+C09)、机制驱动新算法(C08+C02)、高价值突破(C05+C02+C11)，以及领域更适合的理论/系统/基准路线；根据真实数据与论文近邻挑选，不按组合预设质量等级。作者选择主Task与科研策略/有限委托。H8 AI先回收重要正负证据、比较至少一条确有不同失败前提的战略选项，向作者推荐KEEP/UPGRADE/NARROW/REFRAME/HOLD及主Claim；作者决定重大科学方向，AI在所选范围内连续执行。**不要求所有研究开发新网络，也不能把算法复杂度视为必然升级**。具体卡片与例外只维护 [AUTHOR_STRATEGY_REVIEW.md](AUTHOR_STRATEGY_REVIEW.md)，权威分类见 [CONTRIBUTION_TAXONOMY.md](CONTRIBUTION_TAXONOMY.md)。

**高价值实验的升级条件**：真实重要的部署失效、不同科学预测、**新基准或实验范式**、系统级能力、理论/物理约束都可触发研究设计，不强制新网络。按科学主张规划有界 `CLAIM_EVIDENCE_PACKAGE`（公平强对照、关键消融、条件边界、必要部署证据），不是要求所有项目全跑。新增数据库下载、付费/云资源、超H5研究目标及独立确认协议变更须用户决定；已获H6作者选择/限定委托的DEV Task与评价在该范围内由AI版本化调整、复核科学有效性；超出H6已选核心Task/主要评价则重新提交作者选择，SEALED仍独立许可；不要把最便宜的 Probe 当作唯一科学目标。

**数据先行是实证执行依赖，不是思想淘汰门槛**：必需数据没有完整验收时只能做文献、公开元信息、理论假说与下载计划，不得拟合、冻结实证 Task 或基于未获得的数据宣称结果；无授权为 `WAITING_FOR_DOWNLOAD_AUTH`，资源不可用记 `WAITING_FOR_DATA`，`DATA_ACQUIRED_VERIFIED` 仅代表文件验收，不代表科学可辨识性。理论证明和无需静态数据的研究按适用方法处理；详见 [DATA_DISCOVERY.md](DATA_DISCOVERY.md)。

**执行保障接入**：遵循 [EXECUTION_ASSURANCE.md](EXECUTION_ASSURANCE.md)：H6_TASK/H8_CLAIM增加作者策略选项、首选理由与作者选择/委托的声明检查；`AUTHOR_CHOICE_REQUIRED` 时只能呈现推荐并等待真正作者选择，禁止谎称核心战略已冻结；`READY_FOR_SCIENTIFIC_REVIEW` 也只说明字段齐全，不认证消息真实性或科研正确性。NEW_ALGORITHM/普通DEV实验仍由AI处理，重大Run/负Pilot只触发证据审计，不每次触发用户选择。宿主工具权限、SEALED文件隔离等仍未通过此离线检查自动实现。

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

按优先级选择**最能改变当前判断的一项行动**，可在已授权范围内连续完成相互依赖的技术修复。**在产生下一项`NEXT_PROBE`/证伪行动之前，而不是选定后补理由**，先核对其对本轮Task/Claim/可靠性/关键决定的影响、可区别结果、是否已由既有Run回答，以及新信息与成本；未发现关键阻断且同前提检查无新增决策价值时，暂停该细节分支并选更有价值的合法行动（细则只在 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)）。重大真实性、SEALED、权限问题不能按成本跳过：
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

**每次最小交接**：`ACTIVITY | EVIDENCE_REF/UNKNOWN | NEXT_PROBE | H_REVIEW_REF | ACTION_AUTH`。若下一 Probe 是有区别性结果的实验，还需按 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 的 `DECISION_IF_POS/NEG/INVALID | COST_CAP` 说明结果如何改变下一决定；若依赖用户授权，核 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 的对象、期限/时效、资源与费用范围。普通修复及理论/无算法任务不凑实验分支；复用旧 Run，活动05与04可并行。

## 4. 不可覆盖的边界与项目资产

- **权限唯一来源**：用户真实原始指示；H5与H6科研策略有效且本轮DEV数据合法验收后，安全、非付费、符合主机规定的本地CPU/GPU拟合与可信依赖安装按持续AI自主研发权限执行；单纯H4选库/H5选择不授权新数据下载、SEALED、真实付费/外传、跨H5项目PIVOT、投稿或写稿。只有超持续DEV自主范围的操作才先交推荐、选项和必要资源，不先给越权执行命令；见 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)。无执行证据记 `NOT_RUN`。
- **科学可复核**：保持原始数据血缘、train-only 预处理、分组独立性、时序因果、真值可靠性、冻结协议和 holdout 隔离。新 Task 不自动继承旧确认资格；DEV/VAL/CONFIRMATION 不混用。工具哈希/JSON/Agent 判断不能替代真实来源。
- **项目记忆**：按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 增量维护 `RESEARCH_RECORD.md` 当前状态/重大失败/下一步，论文内容规划更新 `PAPER_BLUEPRINT.md` 的 H1/H2 与对应 `SEC_ID`；保留 STATE、Run 和原始工件，不新建第三份科研日志。早期规划不是正式文章。
- **写作锁**：科研成果总结经用户审查并独立授权前 `WRITING_LOCKED`，不能自动写投稿标题、摘要、正式正文/初稿。见 [WRITING_GATE.md](WRITING_GATE.md)；既有稿件写作/审核才按需读 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) / [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md)；Word 排版见 [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md)。
- **图片严格 OPT-IN**：只有用户明确要求指定图片才绘制、重绘或生成预览，见 [FIGURE_POLICY.md](FIGURE_POLICY.md)；写作授权不等于绘图授权，反之亦然。无需出图时保留原始证据、提供文字或表格即可。

## 5. 工作流评价与后续扩展

静态/合成检查按 [evals/EVALUATION_POLICY.md](evals/EVALUATION_POLICY.md)；真实改进需同来源、模型、工具、授权、预算的历史盲回放及独立评价，见 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md)。没有真实 Agent 轨迹或可信 Token 遥测则 `NOT_MEASURED`，不能把 CI PASS 写成科研成功率或创新能力提高。

**规则扩展不在此无限追加**：明确规则归属，优先替换/合并旧条款；新科研方法写入对应专题，主控仅增加确实改变全局决策的最短路由。见 [docs/STRUCTURE.md](docs/STRUCTURE.md)。保留原有权限、冻结协议、实验资产和已获确认的研究结果。
