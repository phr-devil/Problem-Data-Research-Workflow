# PD-RW v1.12｜PD-RW唯一决策总控（ChatGPT / WorkBuddy / Codex）

**目标**：**本轮研究学科/方向完全以用户当次指令为准**，只有明确「方向不限」时才跨学科；不默认传感器或具身智能。随后在给定范围内选择可信数据/评估基准（或理论证明），获授权后完成实证。**仅用户明确选择PD-RW时启用**；第八章具体命题研究和第九章挽救工作不被自动覆盖或迁移。

当出现 `Oracle 有空间但实际策略无收益` 或零标签决策不可辨识时，按需做**信息条件三分诊断**（可纠正性/决策前可辨识性/合法实际收益），优先检查能否用现实中可负担的 K-shot/一次标定重新界定问题；不得借新 Task 把原任务写成成功。经验索引：[SAFE-Gait/APACE](LESSONS/SAFE_GAIT_APACE.md)。工具 `core.cli information-check` 仅作只读建议，不拟合/批准训练。

**v1.11 默认成果目标（写作锁下仅指证据目标）：以合理总成本形成真实、完整、能支撑合适专业期刊文章的科研证据，而非最大化突破幅度、网络复杂度或目标IF。** 选题时仅低成本查看真实同类论文的贡献/核心实验；首个可信Run和每次关键负Pilot后，先检查是否已有一项足够明确的小贡献以及最小论文缺口。若有可信Q2+潜力路线，**优先补主张需要的公平对照、独立证据和科研成果总结；不得提前生成论文结构或正文**，不默认`UP/SCIENCE_UPGRADE`。可选高影响探索须有明确投稿价值/应用需求、额外成本合理或用户指示，不能覆盖已保留的真实科学Run。`EVIDENCE_COMPLETION_PRIORITY`只是当前行动建议，非自动状态、授权或可投稿认证。[PAPER_FIRST.md](PAPER_FIRST.md) / [VENUE_STRATEGY.md](VENUE_STRATEGY.md)。

**高价值科研机会与机制升级（现有活动01–05）**：按[HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md) 将问题**重要性/具名最近邻知识差额**、数据**可区分的竞争解释/独立单位**、任务的**不同可观察预言**、算法的**不同合法杠杆/最小决定性实验**作为一条连续证据链。重要性≠易训练；数据可用≠机制可识别；DEV小增益≠Q2潜力。可在已有合法任务/Run时直接进入缺口，不增阶段/审批/多Agent强制流程。可靠Champion与高潜力机制探索共享评价器和失败证据，不自动重复下载或重训。

**统一科研成功目标**：按[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)，证据充分且具名JCR Q2+相关期刊有同类发表先例时可评为`Q2_POTENTIAL_SUPPORTED`（科研成功，优先争取Q1）；**实际录用非必要条件，不能保证**。普通专业期刊可发、自定义B/C、PAPER_PATH_CANDIDATE及DRAFTABLE均非成功。低于Q2且升级路线已耗尽时可建议失败收束；早期未知不自动失败。期刊类别与年度按[VENUE_STRATEGY.md](VENUE_STRATEGY.md)核实。

**下一行动输出规则**：按[NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)先判用户权限与决策权；可自主技术选择/强烈建议且权限已覆盖时给一条可复制的下一步Agent指令，需用户判断/授权的新预算、确认池、任务/研究目标变化、项目级STOP或论文写作则给推荐+选项、不提前给执行指令。现有科研执行可连续处理普通问题，不必频繁询问。

**最高优先级：论文写作锁**：见 [WRITING_GATE.md](WRITING_GATE.md)。在科研成果总结经用户明确审查、且用户另外明确授权本项目论文写作之前，始终 `WRITING_LOCKED`。可信Run、PAPER_PATH_CANDIDATE、DRAFTABLE、确认成功或科研阶段06不会解锁；仅能评估最小可发表证据及补实验，不得自动写论文提纲、章节、摘要或初稿。授权研究实验不受写作锁影响。

## 1. 三个决策循环（六项活动，不是六道审批门）

**默认原则：最小可学问题优先，复杂度按证据升级。** 必需数据按权限验收后，优先寻找①可重复的个体/设备/时间差异、②可纠正的误差、③简单方法的真实失效；也可从明确应用需求或物理先验出发。用最低成本合法对照区分`LEGAL_SIGNAL`（预测前可用信息）、`MINIMUM_RELIABLE_RESULT`（可信有效结果）和`MINIMUM_INDEPENDENT_CLAIM`（近邻尚未覆盖的科学贡献）。三者不能相互替代。简单有效结果先保留、验证边界与创新性；只有明确瓶颈、不同可检验预测或真实部署要求才增加算法复杂度。复杂方法负结果不自动否定任务，高风险新想法仍可进行廉价正控。**此路径可跳跃、不增审批门，已完成证据不重复。**


- **外循环 A｜研究机会**：01 在本轮`USER_SCOPE`内按[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)自适应广搜/深查热点与空白、核最强近邻，明确「方向不限」才跨学科推荐1–3个AREA_DATA组合；**先核一个有合法评价路径的主库D1，外部/备用库根据独立验证、不同失败前提和成本按需配置，不凑数量**，核跨库标签/科学命题可比性，**第一步确定方向后AI立即自主筛库，不等用户再选数据库** → 完成PRE_DOWNLOAD_PLAN → 有下载授权时先获取/验收本轮必需原始数据（已有完整副本则复用），无授权时输出DOWNLOAD_READY_NOTICE并等待 → `DATA_ACQUIRED_VERIFIED` 后02按[DATA_INSIGHT.md](DATA_INSIGHT.md)在开发池核真实现象与假象 → 03 接[TASK_EXPLORATION.md](TASK_EXPLORATION.md)选具体可检验TASK与最廉价判别，按需构建L0–L3任务阶梯。一个有依据的机会就可开展有界实验；**不要求完整方法假说**、穷尽任务、复现所有强基线或先证明算法增益。[DATA_DISCOVERY.md](DATA_DISCOVERY.md) / [TASK_EXPLORATION.md](TASK_EXPLORATION.md) / [TASK_LADDER.md](TASK_LADDER.md)。
- **内循环 B｜算法实证**：04 默认先复用/建立同信息同K的强简单参照，定位真正可学信号和剩余误差，再按需升级；并行考虑`RELIABLE_TRACK`（稳妥性能/现象）和`NOVELTY_TRACK`（机制/规律探索），在已授权范围内按证据动态投入，**不要求双模型同时训练**；新机制先有可区分假设，按症状修复与学习负结果。首次负Pilot不自动STOP，不为GPU占用率扩大无信息实验。[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)；真正需要新方法/工程迭代时按需读[ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)选择`BASELINE/SIMPLE_IMPROVEMENT/MECHANISM_CANDIDATE/PAPER_EVIDENCE`，明确可证伪预言、受保护边界和Agent执行结果。这里是科研路线选择，不增加第二个主控或声称已具备GPU执行器。
- **外循环 C｜科研价值**：05 与04并行更新`CLAIM_EVIDENCE_MAP`，区分稳健性能、能力/机制/规律三类独立贡献候选及证据缺口；有Q2+潜力候选路线时按信息价值科学升级，不因普通期刊可发提前停止；可继续当前层级、`UP`挑战更难信息条件、`DOWN`使用更现实的合法标定、`NARROW`收窄主张，或`LATERAL`比较备用科研任务。06 只有冻结 Claim/方法/协议并获授权后才严格独立确认。层级切换必须更新Claim与公平评价，**L0/L1没有天然论文保底**。[TASK_LADDER.md](TASK_LADDER.md) / [CONFIRMATION.md](CONFIRMATION.md)。

**数据先行是执行依赖，不是新增科研淘汰门槛**：新实证任务的顺序是 `方向→自主选库→完整必需原始文件下载/本地复用→文件级验收/确认池封存→数据观察→具体任务→基线/算法`。确定方向不等于许可下载；无授权停在 `WAITING_FOR_DOWNLOAD_AUTH`，源不可用或文件不完整停在 `WAITING_FOR_DATA`，先交付可执行获取/续传方案，不把缺数据解释为任务科学失败。`DATA_ACQUIRED_VERIFIED` 只证明约定文件完整且可访问，不能取代标签/独立组/可见信息的科学审计。理论证明、无需静态数据的仿真，或已有完整可信数据不重复下载；大库只有在用户明确批准收窄研究数据范围、同步收窄主张后，才可将该预定义范围视为完整，不能默认拿样例代替全库。**未就绪时禁止正式TASK冻结、基线拟合、算法训练和基于数据的结果宣称；不依赖真实数据的文献核查、假说草拟、下载脚本可提前做**。

**单次循环可跳转**：已有 STATE/Run 直接续做；低门槛 EXPLORE、中门槛追加投入、高门槛正式确认。**当前最优选择并不由L2的名称决定**：L1若科学价值更明确可先研究L1；L3若有廉价关键正控可先尝试L3。初始 UNKNOWN 不自动否决；论文确认仍核独立真值、时间因果、公平强基线、独立组、效应不确定性与直接近邻。

**增量论文路由（不是新状态/审批门）**：可信开发结果出现后，按 [PAPER_FIRST.md](PAPER_FIRST.md) 检查是否存在**至少一项**具名近邻尚未回答、可证伪且有独立确认路径的贡献：包括适用边界、同信息条件下局部增益、资源/标定成本—性能权衡、可解释负结果、或有价值的已知组件组合。符合则记`PAPER_PATH_CANDIDATE`并安排最少必要证据，可同步记录科研主张和证据缺口（非论文提纲/正文）；不以全数据集SOTA、新网络、多项贡献或预设全量跨库作为门槛。没有实质新意保留`NO_INDEPENDENT_CLAIM`；论文确认质量不降低。工程资产、增量贡献与高影响扩展必须分开判断；按需使用 [VENUE_STRATEGY.md](VENUE_STRATEGY.md) 的 **S/A/B/C稿件潜力（NONE/UNKNOWN）** 与 **冲刺/主投/保守期刊策略** 两轴，既不能把B/C档小创新自动判STOP，也不能把分档当官方JCR/CAS分区、客观质量分或录用概率。该档次只是阶段性建议、不是机器状态或新审批门。

## 2. 单入口事件路由

| 当前最主要阻碍 | 读哪个文件 | 下一项有效交付 |
|---|---|---|
| 新课题待搜索、热点/空白和近邻未明 | [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) | SEARCH_HANDOFF：范围/覆盖/首选与最强近邻 |
| 方向已定、数据或评估资源待选 | [DATA_DISCOVERY.md](DATA_DISCOVERY.md) | DIRECTION_CARD→必需数据/基准→PRE_DOWNLOAD_PLAN |
| 已选D1但数据缺失/未完整验收 | [DATA_DISCOVERY.md](DATA_DISCOVERY.md) §4 | 下载授权内获取/续传→文件级验收；无授权给可执行方案并等待 |
| D1不适配TASK的真值/合法评价 | [DATA_DISCOVERY.md](DATA_DISCOVERY.md)转题地图＋[TASK_EXPLORATION.md](TASK_EXPLORATION.md) | 复用同库任务/备用库/定向搜替代库，标注授权缺口 |
| 数据已可读，需观察真实现象/排除数据假象 | [DATA_INSIGHT.md](DATA_INSIGHT.md) | DATA_INSIGHT_CARD、证据与关键混杂；无现象可标NO_RELIABLE_INSIGHT_YET |
| 数据或文献已提供机会，但具体TASK未定 | [TASK_EXPLORATION.md](TASK_EXPLORATION.md) | 主TASK、必要备选、性能空间/信息条件的最小探针 |
| 同一问题可用不同标签预算/部署条件完成分层任务，或考虑上探/下探 | [TASK_LADDER.md](TASK_LADDER.md) | 一项主层级与L0共享资产、层级间公平协议、切换判据 |
| TASK需要真实编码/评价器尚未固定 | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)；可用[core/README.md](core/README.md)只读TaskSpec检查 | 合法TaskSpec／保护范围／评价器指纹或明确UNKNOWN（不自动授权拟合） |
| 真实DEV残差已核、需要设计新算法或连续工程迭代 | [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)（按需） | 误差/合法杠杆/直接简单替代/一条不同预言、最小正控、授权内执行结果和论文机会 |
| 有 TASK/基线/负 Pilot/普通代码故障 | [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)；写代码才读 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | 有效 Run、定向修复或 NEXT_PROBE |
| 稳定可信算法、拟HOLD/结束/继续投入，或想用小修改提高科学性 | [POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)（按需） | 区分性科学问题、最小有界验证或保留成果并总结；不自动写稿 |
| 可信Run/关键负Pilot/拟继续堆模型，需要判断“现有结果是否已足够做一篇论文” | [PAPER_FIRST.md](PAPER_FIRST.md) | 可发表主张的证据地图（非论文提纲）、必需证据缺口、补证据vs升级模型的选择 |
| 有可信结果、需要收敛论文贡献或判断创新价值 | [PAPER_FIRST.md](PAPER_FIRST.md)；确需转任务才读[TASK_EXPLORATION.md](TASK_EXPLORATION.md) | CLAIM_EVIDENCE_MAP、具名近邻差额与下一必要实验 |
| 有可信增量Claim且需判断稿件档次/目标期刊 | [VENUE_STRATEGY.md](VENUE_STRATEGY.md)（仅按需） | 非强制的稿件潜力、期刊适配梯队、关键证据缺口；不预测录用率 |
| 正式科学确认、公开主张、投稿 | [CONFIRMATION.md](CONFIRMATION.md) | 预冻结协议、独立证据或 CONFIRMATION_UNAVAILABLE |
| 用户改变研究范围/权限/预算 | 本文件＋最新 STATE | 影响范围与真实用户决策 |

已有项目先核STATE/有效Run的索引，再按阻碍只读一份专题与受影响证据；无需每轮重读全章、旧Prompt、历史失败和完整训练日志。规则/协议或证据变化时才重读相关内容。ChatGPT 优先公开资料与科学论证，WorkBuddy/Codex 在用户实际授权范围内核本地资产并执行。状态缓存与现场不符时以原始证据和最新授权为准。

## 2.5 各阶段的最短交接（不是每轮填写全部字段）

- **01**：`SEARCH_HANDOFF → DIRECTION_CARD → 主库D1＋本轮必需的外部数据 → PRE_DOWNLOAD_PLAN → (授权下载/复用) → DATA_MANIFEST:DATA_ACQUIRED_VERIFIED`；无下载授权先给 `DOWNLOAD_READY_NOTICE` 和保存/校验命令，标等待；不应提前进入02–04。
- **02–03**：验收本轮必需数据后 `DATA_INSIGHT_CARD → PRIMARY_TASK / VALUE_HYPOTHESIS / MINIMUM_PROBE`；无真实现象可从合法需求/文献提出可检验任务，不冒充已观察；数据没到位时只能草拟 `HYPOTHESIZED_TASK`，不能冻结实证协议。
- **04↔05**：任务进入实际执行时按需冻结TaskSpec/评价器；公平Champion–Challenger和`ALGORITHM_HYPOTHESIS → 有效Run → CLAIM_EVIDENCE_MAP → NEXT_PROBE`，按需读[PAPER_FIRST.md](PAPER_FIRST.md)；`PERFORMANCE_FLOOR/PAPER_PATH_CANDIDATE/SCIENCE_UPGRADE`不是强制阶段。
- **算法完成后的可选增值**：需要收束或投资取舍时，可调用`POST_ALGORITHM_SCIENCE_AUDIT`（非CLI事件/必经阶段）：保护原Run→近邻差额/竞争解释→最小合法证伪→升级或总结，见[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)；写作门禁不变。
- **06**：冻结当前Task/Claim/方法/协议及选择史，按[CONFIRMATION.md](CONFIRMATION.md)核独立证据。级间转换按[TASK_LADDER.md](TASK_LADDER.md)更新合法信息、评估和Claim。

每次只交当前阻碍所需的最少字段；授权、证据、机制/任务/区域级止损仍由本文件统一决定。

**科研证据优先决策（非写作授权）**：有效Run形成后，且尤其在拟启动高成本机制/多库训练、拟HOLD/PIVOT时，对照现有Claim做一次`Q2_EVIDENCE_REVIEW`（决策动作名，非CLI状态）：`ONE_CLAIM | NEAREST_GAP | CORE_RESULT | REQUIRED_EVIDENCE_GAPS (最多3项) | LOWEST_COST_PATH | CONTINUE_ALGO_ONLY_IF_WORTH_IT`。若可信Q2+目标路线存在且补证据更划算，优先科研证据补齐（`EVIDENCE_COMPLETION_PRIORITY`，不授权写稿）；只有必要核心证据不可获得/近邻完全覆盖，才优先不同任务或机制。无新结果不反复复核；已完成的核查不重做。不能把开发集高分误当确认。

## 3. 唯一下一行动算法（不机械全跑检查表）

依当前决定的影响顺序选择：
0. **实证数据依赖**：若本轮必需数据未验收，优先调用数据获取/本地复用/续传并验收；无权限时给可执行下载清单并等待。不要先启动TaskSpec、Pilot或训练；纯理论/无静态数据库仿真不适用。
1. **真实性/权限**：证实泄漏、伪真值、确认集污染、越权或必要平台阻断 → 仅隔离受影响动作和 Claim；UNKNOWN 只核当前最危险且廉价可验的事实。
2. **实验能力**：数据、评价、同步、平台或训练链缺失 → `ENABLEMENT`，局部修复与定向验证；工程 PASS 不等于科研发现。
3. **机会与实验**：无 TASK → `DISCOVERY`（从简单真实规律或应用需求入手）；有 TASK → `LOW_COST_PROBE`（优先复用合法简单参照、验证信号/剩余瓶颈）。只有可区分机制或部署条件值得解决时才升级复杂度；正控、双规模、完整强基线按需，不为跑GPU而训练。
4. **主张与任务比较**：可信新发现（哪怕只是窄口径增量贡献）或有不同失败前提的更好备用机会 → `CLAIM_REVIEW`，比较可行性、独立价值和续投成本；若已有一项真实差额，优先最小论文证据路线，不为追逐全面SOTA强制UP。若同问题有可靠层级转化路径，按 [TASK_LADDER.md](TASK_LADDER.md) 选择 `UP / DOWN / NARROW / LATERAL / HOLD`，不需要先把当前方法“彻底判死”；但任何切换都**不得跨级继承不合法的标签/未来信息**，也不能把同一失败前提包装成新Task。
5. **确认**：匹配、未污染确认资源可用且 Claim/协议冻结、获用户确认性实验授权 → `CONFIRMATION`；不满足则限缩 Claim 或记 CONFIRMATION_UNAVAILABLE。

**分支记账（仅有负结果、转向或重大新证据时更新）**：复用已有Run/STATE记录`BRANCH_ID | FAILED_PREMISE | NEXT_DISTINCT_PROBE | CUMULATIVE_COST`。继续/暂停看下一实验的信息价值、可复用能力和GPU/Token/人工总成本；到达预算复盘点**触发重新判断而非自动STOP**。无法提供不同可检验预测时不靠换模型名续命。

**每轮最小合同**：`CURRENT_EVIDENCE | BLOCKER_OR_UNKNOWN | NEXT_PROBE | POSSIBLE_OUTCOMES_AND_DECISION | AUTH/BUDGET | DELIVERABLE`。NEXT_PROBE 可以产生观察、能力或判别信息，不要求每次提高分数。优先单一主实验，原授权内连续完成关联修复和验证；无新增信息/能力且成本不值得才 HOLD 对应分支，不无限循环。

## 4. 止损层级和状态分账

| 决策范围 | 可继续的条件 | 何时暂停/转向 |
|---|---|---|
| **RUN/机制** | 欠训练、评价问题或有不同预测的机制机会仍可廉价辨别 | 公平负证据或成本失衡 → DISCARD/HOLD 本机制 |
| **TASK** | 可在相同问题下改变合法信息/标定约束、尝试不同物理解释或备用机会；记录各层级证据 | 共同失败前提已否定、真值不可达、无新信息 → 当前TASK或L层级HOLD；必要时DOWN/NARROW/LATERAL |
| **AREA_DATA** | 数据仍支持合法、可评价的其他研究任务 | 关键前提不可达且成本不值得 → 建议更换组合；由用户决定 |

**科研证据 ≠ 运行状态 ≠ 投资决定 ≠ AUTH**。`RUN_STATUS=COMPLETE`、`KEEP` 或 GPU 小时不等于 `CONFIRMED`。缺资源/未验证标 UNKNOWN 或 `WAITING_FOR_AUTH`，不写科学 REFUTED。项目级 HOLD/STOP、核心研究方向/数据库变化须用户决定；不能靠换 Backbone 名称重复预算和同一失败前提。普通 Bug 不强制多轮询问。

## 5. 边界、可复现证据与交付

- 用户选择**宽研究方向或多数据库研究组合**不代表授权下载、安装、外传、CPU Ridge等拟合、GPU训练、付费、正式确认或投稿。下载前需`DIRECTION_CARD`＋AI已选`DATA_PORTFOLIO`＋逐库`PRE_DOWNLOAD_PLAN`；获授权后优先完成下载/复用与 `DATA_ACQUIRED_VERIFIED`，未经授权则通知并停在等待状态。只有本轮主张必需的库受数据先行依赖约束；仅作未来可能备用的D2/D3可延后，不可冒充跨库确认。逐项以真实用户消息为准。无权限/工具写 NOT_RUN。实质更改科研目标、资源、冻结确认协议须再次批准。
- 保护原始数据血缘、训练/开发隔离、train-only 预处理、合法分组/评价器与封存确认集。`task_id/protocol_id/eligible_holdout` 必须支持当前新任务：提前封存不代表任何任务都能用；任务搜索或确认集污染不可靠换 seed、重划分洗白。
- 复用 `research/STATE.md`、`RUNS.tsv`、`CLAIMS.md` 等资产，不新建空目录；保存 `BEST_VALID_RUN`、任务选择史、失败原始 Run、源码和数据/评价版本。协议更改只重算受影响证据。
- **可执行证据层**：v1.5新增TaskSpec预检与显式`task-pin`固定受保护文件、机制Probe合同、可复现元数据检查、显式文献元数据查询；新项目有有效Run可执行Python时优先启用索引，既有项目不强制迁移。[core/README.md](core/README.md) 的`STATE.json/EVENTS.jsonl`及Run比较器用于工件哈希、断点一致性和已记录协议可比性；不替代Markdown、科学判断或真实授权，不自动推进固定阶段。有证据Claim必须关联真实Run/工件，缺工件仅能标假设。
- **EVIDENCE_FIRST_OUTPUT（01–06统一）**：默认仅`NEW_EVIDENCE+PATH | DECISION_CHANGE/UNCERTAINTY | NEXT_PROBE(+不同结果如何改变决定) | AUTH/COST`；无新证据只报阻碍/下一动作。日志、代码、图、失败Run完整**落盘但不回显全文**；Agent只读/报相关diff、关键指标和必要报错尾部。避免重复总结、长报告、无效多Agent审核。用户要完整文档时再展开。**单次负Pilot** ≠ 整个 AREA_DATA 失败。
- **图片三档**：01–05默认纯文本和紧凑表格；不自动生成装饰图、论文级美图、PPT/PDF、仪表盘、未实测成功曲线。仅当能判别假设/错误或支持必要科研证据时制作**简单可复现诊断图**（Loss、残差、group对照等）；复用旧图与脚本，不反复美化。活动05只形成证据草图，正式论文图片排版延至活动06**证据可靠且用户确需交付**时。必要统计图不可为省Token省略。
- **上下文与执行**：复用STATE、manifest、缓存、有效Run；只在新信息可能改变结论时重查/复跑/绘图。已授权的关联修复连续完成，局部回归按影响执行；关键科学验证与合并CI不删。比较Token、GPU、人工总成本，不牺牲可复现性。

## 6. 评测与来源（非 Agent 必走关卡）

`SCENARIOS.json`及部分测试仅覆盖设计/结构，core单测仅覆盖程序行为，不证明科研效能。实际需按 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) 在相同信息/授权/预算下做**历史盲回放**（遮蔽后续结局）及**前瞻性跟踪**，比较首个真实有效结果、任务价值、过早停止、无效实验、科研确认与 GPU/Token/人工总成本；同时评估复杂模型无效试验、首个可信信号成本、独立贡献候选与创新性损失风险。未运行标 NOT_MEASURED。



## v1.6｜证据先于机制的最短诊断（并入原决策，不增关卡）

当出现负Pilot、简单基线反超、Oracle有空间但策略失败或评价反常时，先核受影响的**原始Run及其可比较性**，按最危险的一个原因路由：

| 有证据的主要原因 | 首选下一动作 | 不能推断 |
|---|---|---|
| 评价错误/泄漏/因果不合法 | INVALID → REPAIR受影响证据 | 修复前的GO有效 |
| 欠训练/容量/不公平预算 | 有界成对训练诊断 | 机制已被证伪 |
| 预测前缺必需信息 | 核合法K、成本和support/query；必要时提出新Task | Oracle空间=可学习空间 |
| 强简单基线已解释增益 | 保留基线，寻找不同的合法杠杆/科学问题 | 简单基线成功=新算法成功 |
| 近邻覆盖或科研Claim不足 | 收窄Claim或探索真实失效规律 | 工程/开发F1就是论文 |
| 独立组不足、区间宽 | INCONCLUSIVE＋最廉价判别 | 未显著=无真实效应 |

工具 `python -m core.cli failure-check --file failure.json` 是**可选只读建议**，不能从输入的文字断言科学事实、不读原始Run、不自动STOP或训练；优先复用已有效的`information-check`。只有原始证据支持才用`OBSERVED`，其他为`HYPOTHESIZED`。当多项问题共存，先修会污染后续判断的评价错误。没有新的不同失败前提时不靠换模型名重启预算。正式确认标准不变。

**新增按需资源：** 当已有 DEV Run 且准备投入复杂机制时，可先读取 [FEASIBILITY_ENVELOPE.md](FEASIBILITY_ENVELOPE.md) 产生短画像；没有 Run 的项目仍可合法开展选题和必要观察。其 `UNKNOWN`、负增益或组级波动仅指向下一最小判别，不自动变成方向性 STOP、科研确认或用户授权。


## v1.7 · 主控与验证的唯一边界（不增加新阶段）

PD-RW 仍是**唯一科研主控**（机会、数据、合法Task、机制实验、科研Claim与授权），RWF是关键 DEV 工件的**按需独立复算器**。先有真实数据和公平简单参照，再按 [FEASIBILITY_ENVELOPE.md](FEASIBILITY_ENVELOPE.md) 判断合法信号、可纠正性、独立论文价值，不用残差/Oracle推算成功概率。关键实验首次建立正式基线、显著正增益或评价异常时，如已有标准RWF Run才调用`forge-verify`；数据/评价/预测文件未变时复用审计证据，不重复创建全套状态。未匹配原始预测或未运行验证的历史Run仍为`REPORTED`，不能在正式科学判断中称作已独立核实。

分工原则：**复杂算法仍由实际获授权的外部Agent执行；可信Run不等于公平强基线、在线因果、创新或论文确认。** 同一负证据先局部纠错/机制转向；不强制多seed/多模型/多Agent和长报告，也不因为没有RWF就自动停止探索。真实效能应由 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) 的历史冻结节点与前瞻任务对照检验。
