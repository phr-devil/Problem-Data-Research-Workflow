# 11月9日精简前规则继承审计（只供仓库维护）

> 本文件是**一次性历史审计索引**，不是新的科研政策、权限源或第三份项目日志；普通Agent任务不默认读取。现行权威仍在下列专题文件。发现新证据时仅更正受影响行，不反复全量重审。

历史基线：A = [精简前 AGENTS.md](https://github.com/phr-devil/Problem-Data-Research-Workflow/blob/822c44ed633d/AGENTS.md)（`822c44ed633d`）；W = [精简前 WORKFLOW.md](https://github.com/phr-devil/Problem-Data-Research-Workflow/blob/13390243b5bf/WORKFLOW.md)（`13390243b5bf`）。对照主分支：`ff08def90841761d5ffa9ad22b1e0c7acfa5b5d9`（PR #29 后）。`A:L` 和 `W:L` 是历史文件行号；表中见证文本仅供定位，不代表执行证明。

审计分类：`PRESERVED`（主控/入口保留）；`MOVED`（专题承接）；`MERGED`（相同语义归并）；`REPLACED`（后续明确的新规则替代）。按旧文件的主要独立义务逐行归类，紧邻同义句按语义合并；不等于证明每个字词都被保存，也不等于证明Agent真实履约。查到具体的 `WEAKENED/MISSING/CONFLICT` 时先在对应owner修复并更新受影响行，不能凭文件名存在就标通过。

**必须保留的正式替代**：W04旧“选题约2–3轮”由H1–H5审核依赖和可一次确认多个节点替代；W15旧“AI默认自行定D1”由H4用户选择或明确委托替代；W11旧Title段距例外由后来“全部段落0/0pt”要求替代。恢复旧版本不得重新启用这些相冲突条件。

| ID | 旧来源位置 | 当前唯一详细owner | 见证文本 | 归宿 | 核查要点 |
|---|---|---|---|---|---|
| `A01` | A:L3-10 | `AGENTS.md` | `唯一默认入口` | `PRESERVED` | 入口与原始用户指示优先 |
| `A02` | A:L7-9 | `DUAL_DOCUMENT_WORKFLOW.md` | `当前快照` | `MOVED` | 已有项目优先恢复状态和真实证据 |
| `A03` | A:L10 | `WORKFLOW.md` | `冲突优先级` | `MERGED` | 用户权限与真实科学事实分轴 |
| `A04` | A:L14 | `NEXT_ACTION_POLICY.md` | `独立许可` | `MOVED` | 选题选库不自动授权实际操作 |
| `A05` | A:L15 | `DUAL_DOCUMENT_WORKFLOW.md` | `PAPER_BLUEPRINT.md` | `MOVED` | 科研记录和稿件规划分开 |
| `A06` | A:L16 | `PAPER_WORD_STYLE.md` | `Times New Roman` | `MOVED` | Word只在相关任务加载 |
| `A07` | A:L17-18 | `HIGH_VALUE_RESEARCH_DESIGN.md` | `科学价值` | `MOVED` | 高价值机会和机制来源不唯分数 |
| `A08` | A:L20 | `WORKFLOW.md` | `创新` | `MERGED` | 构思开放但需要科学证据 |
| `A09` | A:L22 | `MANUSCRIPT_WRITING.md` | `R1 必查` | `MOVED` | 授权写作才需匹配相关策略卡 |
| `A10` | A:L23 | `MANUSCRIPT_WRITING.md` | `正文生成阶段的图片位置` | `MOVED` | 图片后置及Fig.标题留在写作专题 |
| `A11` | A:L24 | `MANUSCRIPT_WRITING.md` | `Introduction（` | `MOVED` | 引言段落连贯不机械分小标题 |
| `A12` | A:L25 | `MANUSCRIPT_WRITING.md` | `括号` | `MOVED` | 正式正文避免清单和括号堆砌 |
| `A13` | A:L26 | `MANUSCRIPT_WRITING.md` | `反模板化学术表达分级合同` | `MOVED` | 反模板风格按严重性审查 |
| `A14` | A:L27 | `MANUSCRIPT_QA.md` | `R1 独立审稿` | `MOVED` | 稿件审查与原写作许可分开 |
| `A15` | A:L28 | `MANUSCRIPT_QA.md` | `Q3` | `MOVED` | 语义与真实独立证据复核 |
| `A16` | A:L30 | `MANUSCRIPT_QA.md` | `Q9` | `MOVED` | Q5/Q7/Q9归属于稿件QA |
| `A17` | A:L31 | `FIGURE_POLICY.md` | `FIGURE_DRAWING_LOCKED` | `MOVED` | 图片绘制严格用户OPT-IN |
| `A18` | A:L32 | `Q2_PUBLICATION_GOAL.md` | `Q2` | `MOVED` | Q2潜力不等于稿件录用 |
| `A19` | A:L34-43 | `AGENTS.md` | `按实际阻碍加载专题` | `PRESERVED` | 不遍历全仓而按任务导航 |
| `A20` | A:L44 | `FIGURE_POLICY.md` | `AXIS_ARROW_QA` | `MOVED` | 数据图轴箭头和柱图QA归专题 |
| `A21` | A:L45 | `ACADEMIC_DIAGRAM_STYLE.md` | `GLOBAL_DESIGN_QA` | `MOVED` | 局部修图与整体重构各有触发条件 |
| `A22` | A:L47 | `evals/EVALUATION_POLICY.md` | `NOT_MEASURED` | `MOVED` | CI不能声称科学或Token效能 |
| `A23` | A:L49-51 | `DUAL_DOCUMENT_WORKFLOW.md` | `RESEARCH_RECORD.md` | `MOVED` | 重要结果增量持久化 |
| `A24` | A:L15 | `WRITING_GATE.md` | `WRITING_LOCKED` | `MOVED` | 成果审查与正文授权为独立条件 |
| `A25` | A:L39 | `EXPERIMENT_LOOP.md` | `BEST_VALID_RUN` | `MOVED` | 已有实验可信结果和负结果复用 |
| `A26` | A:L40 | `POST_ALGORITHM_SCIENCE_AUDIT.md` | `科学` | `MOVED` | 收口前按需查真实创新价值 |
| `A27` | A:L42 | `CONFIRMATION.md` | `SEALED` | `MOVED` | 独立确认严格隔离 |
| `W01` | W:L3-5 | `WORKFLOW.md` | `USER_SCOPE` | `PRESERVED` | 科研范围遵循当次用户指示 |
| `W02` | W:L7 | `EXPERIMENT_LOOP.md` | `ORACLE_GAIN` | `MOVED` | Oracle空间不等于实际可辨识 |
| `W03` | W:L9 | `SEARCH_DISCOVERY.md` | `BREADTH_SCAN` | `MOVED` | 广搜深证伪和竞争选择 |
| `W04` | W:L9 | `WORKFLOW.md` | `H1→H2→H3→H4→H5` | `REPLACED` | 旧2–3轮选题改为依赖审核但允许一次确认多个节点 |
| `W05` | W:L11 | `Q2_PUBLICATION_GOAL.md` | `Q2` | `MOVED` | 科研重要性优先于廉价小论文 |
| `W06` | W:L13 | `WORKFLOW.md` | `创新` | `MERGED` | 不同科学假说可探索但不能造假创新 |
| `W07` | W:L15 | `SCIENCE_RESULT_HARVEST.md` | `ARTICULATION_GAP` | `MOVED` | 表述缺口不等于证据缺口 |
| `W08` | W:L17 | `HIGH_VALUE_RESEARCH_DESIGN.md` | `机制` | `MOVED` | 明确竞争解释与不同科学预言 |
| `W09` | W:L19 | `Q2_PUBLICATION_GOAL.md` | `Q2_POTENTIAL_SUPPORTED` | `MOVED` | Q2候选须有真实证据 |
| `W10` | W:L21 | `NEXT_ACTION_POLICY.md` | `USER_DECISION_REQUIRED` | `MOVED` | 待用户决策时不得预发执行命令 |
| `W11` | W:L23 | `PAPER_WORD_STYLE.md` | `全部样式` | `REPLACED` | 旧Title段距例外被后续所有段落0/0pt覆盖 |
| `W12` | W:L25 | `WRITING_GATE.md` | `WRITING_LOCKED` | `MOVED` | 论文蓝图不是正文许可 |
| `W13` | W:L29 | `WORKFLOW.md` | `CLAIM_EVIDENCE_PACKAGE` | `PRESERVED` | 高价值系统或理论升级可以有界验证 |
| `W14` | W:L31 | `EXPERIMENT_LOOP.md` | `Champion` | `MOVED` | 简单可靠参考不作为复杂方法禁令 |
| `W15` | W:L34 | `DATA_DISCOVERY.md` | `H4 由用户选D1` | `REPLACED` | 旧自动定D1被明确的用户选择或委托取代 |
| `W16` | W:L34 | `DATA_DISCOVERY.md` | `PRE_DOWNLOAD_SCIENCE_FIT` | `MOVED` | 正式下载前先核官方元信息 |
| `W17` | W:L35 | `EXPERIMENT_LOOP.md` | `RELIABLE_TRACK` | `MOVED` | 双轨按证据投入不是双模型强制 |
| `W18` | W:L36 | `PAPER_FIRST.md` | `PAPER_PATH_CANDIDATE` | `MOVED` | 潜在贡献路径不等于确认或写作 |
| `W19` | W:L38 | `WORKFLOW.md` | `局部回退` | `PRESERVED` | 数据或协议变化只撤回受影响的下游决定 |
| `W20` | W:L40 | `DATA_DISCOVERY.md` | `DATA_ACQUIRED_VERIFIED` | `MOVED` | 数据文件完整不代表真值可用 |
| `W21` | W:L42 | `TASK_LADDER.md` | `L0` | `MOVED` | L层级随合法信息与科学价值调整 |
| `W22` | W:L44 | `PAPER_FIRST.md` | `PAPER_PATH_CANDIDATE` | `MOVED` | 可信增量知识允许独立论文候选 |
| `W23` | W:L46-67 | `AGENTS.md` | `按实际阻碍加载专题` | `MERGED` | 旧总控路由归纳为默认入口 |
| `W24` | W:L69-75 | `contracts/research_activity_protocol.v1.json` | `research_flow` | `MOVED` | 六活动合同是结构镜像不是新的授权 |
| `W25` | W:L79 | `PAPER_FIRST.md` | `EVIDENCE_COMPLETION_PRIORITY` | `MOVED` | 补关键证据比无界训练优先 |
| `W26` | W:L81-89 | `WORKFLOW.md` | `下一行动和止损决策` | `MERGED` | 行动按当前科学障碍选择 |
| `W27` | W:L91-95 | `EXPERIMENT_LOOP.md` | `CUMULATIVE_COST` | `MOVED` | 重要负Pilot及成本记账不自动STOP |
| `W28` | W:L97 | `NEXT_ACTION_POLICY.md` | `IF_POS/NEG/INVALID` | `MOVED` | PR29恢复交接分支具体算法定义仍归实验专题 |
| `W29` | W:L101-105 | `WORKFLOW.md` | `RUN / 机制` | `PRESERVED` | RUN和Task及整个方向分开止损 |
| `W30` | W:L107 | `DUAL_DOCUMENT_WORKFLOW.md` | `RESEARCH_RECORD.md` | `MOVED` | 重要事件写回两个已有文档 |
| `W31` | W:L109-115 | `CONFIRMATION.md` | `SEALED` | `MOVED` | 冻结协议独立确认不得用于DEV选模 |
| `W32` | W:L116 | `EXPERIMENT_LOOP.md` | `RWF` | `MOVED` | RWF可选复算不生成科研许可 |
| `W33` | W:L117 | `NEXT_ACTION_POLICY.md` | `L1` | `MOVED` | 原证据优先输出改为L1/L2/L3自适应 |
| `W34` | W:L118 | `FIGURE_POLICY.md` | `FIGURE_DRAWING_LOCKED` | `MOVED` | 图片仍由用户明确请求 |
| `W35` | W:L119 | `NEXT_ACTION_POLICY.md` | `Token` | `MOVED` | 优化完整任务而非单轮最短 |
| `W36` | W:L123-125 | `REPLAY_PROTOCOL.md` | `NOT_MEASURED` | `MOVED` | 真实Agent性能必须历史盲回放 |
| `W37` | W:L129-142 | `EXPERIMENT_LOOP.md` | `UNDERTRAINED` | `MOVED` | 负Pilot优先诊断有效性与可学习性 |
| `W38` | W:L144 | `FEASIBILITY_ENVELOPE.md` | `UNKNOWN` | `MOVED` | 可选可行性探针不是自动STOP |
| `W39` | W:L147-151 | `EXPERIMENT_LOOP.md` | `forge-verify` | `MOVED` | 证据复核只在可验证真实Run时进行 |
| `W40` | W:L113 | `NEXT_ACTION_POLICY.md` | `费用/算力上限` | `MOVED` | PR29恢复原用户许可对象时效与费用上限 |

## 当前已修复的历史弱化及执行边界

1. PR #29已将交接六项检查、原用户授权对象/时效/成本和 `IF_POS/NEG/INVALID` 的分支恢复到相应权威文件；不可在精简时再删去具体条件，实验细则由 `EXPERIMENT_LOOP.md` 主责。
2. 本轮新增审计表和离线回归会检查旧要求的**权威位置与关键条件**，但静态存在性、JSON声明或Agent自述**不能证明**真实执行许可、论文质量或科研新颖性。
3. 真实新旧版本Agent对照、跨会话加载、SEALED工具层拦截和Token节省尚未实测：`NOT_MEASURED`。若某历史项目无原时点冻结数据，记 `NOT_REPLAYABLE`，不借后验最佳结果评价前瞻决策。
4. 维护时只核本次PR受影响的旧ID、权威文件、操作前授权及反例；`REPLACED` 项不得机械回滚。若有未知重大旧要求，先补证据而非伪造归宿。
