# PD-RW v1.12｜新项目与专题路线（从 AGENTS.md 按需进入）

**唯一默认 Agent 入口为 [AGENTS.md](AGENTS.md)**。若不知道当前专题归属，可查看 [按需专题索引](modules/README.md)；其余仍按本文件和真实项目证据执行，索引不是新增步骤。已有项目优先读 RESEARCH_RECORD.md 当前快照、相关 PAPER_BLUEPRINT.md 章节及真实 STATE/Run；本文件用于新项目或需要完整科研路线时按需阅读，不能取代 [WORKFLOW.md](WORKFLOW.md) 的原有六项活动与三个决策循环。

仅在用户明确选择PD-RW时启用。**默认科研目标是形成可信、可发表的科学证据，而不是直接撰写论文。** **禁止自动绘图：只有用户明确要求实际绘制或修改图片才可出图**；否则仅可文字建议，见[FIGURE_POLICY.md](FIGURE_POLICY.md)。本轮研究范围以当前用户指令为准；[WORKFLOW.md](WORKFLOW.md) 是科研决策与权限的唯一总控，**无需预读所有专题**。

1. **已有项目**：先通过项目内已有 STATE/索引确定 RESEARCH_RECORD.md 和 PAPER_BLUEPRINT.md 的实际路径，读当前快照与相关章节，再核真实 STATE/Run、manifest 和用户授权；若两文件不存在，按旧项目继续使用真实工件，不假定有记录。若使用 `STATE.json/EVENTS.jsonl`，先查事件一致性；缺工件不冒充有效结果。仅按当前阻碍读对应专题。
2. **新课题**：在`USER_SCOPE`内按[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)进行**BREADTH_SCAN（广度覆盖）→DEEP_FALSIFICATION（最强近邻/反证）→COMPETING_CHOICE（不同失败前提的竞争机会）**三项可连续完成的科学证据审查（不等于一次性替代 H1–H5 人工选择）；按公开官方元信息先查`PRE_DOWNLOAD_SCIENCE_FIT`，不因第一个可行方向就停搜。在 H3 候选决定后按官方来源比较 D1/必要外部库，深度参与模式经 H4 用户选择或可核委托，再在 H5 确定最终问题→核官方版本/必要文件/许可/容量→**仅在 H4/H5 满足且另有明确数据获取授权后才下载并核验数据**。已有完整副本直接复用；有覆盖当前D1的下载授权的Agent连续完成获取，不再为选库/下载反复请示；无下载授权仅提供已核实的官方来源、文件清单、容量与推荐/授权选项，**不提供下载Agent执行指令或PowerShell命令**，标 `WAITING_FOR_DOWNLOAD_AUTH`，不进入数据实证。详见 [DATA_DISCOVERY.md](DATA_DISCOVERY.md)。
3. **证据就绪后（活动02→03）**：遵循 [research_activity_protocol.v1.json](contracts/research_activity_protocol.v1.json)，实证先分别核文件可读、真值与独立单位、合法输入/观察权限，理论/仿真只按适用的 `PROOF_PATH`；不要求虚构DEV、Run或训练。复用既有完整资产；`DATA_ACQUIRED_VERIFIED` 不等于真值有效，`NO_RELIABLE_INSIGHT_YET` 可触发继续科学构思但不能伪造 H6 正式 Task。记录H1–H5用户选择、H6–H8 AI科学决策、活动进入证据及适用执行范围后推进；H5确认且DEV合法就绪时，安全非付费本地算法开发无需逐次批准，SEALED/付费/写稿等独立门禁不变。
4. **已有任务/运行**：按 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 获取有效Run、诊断负Pilot；**需要设计新算法或连续编码/GPU实验**时，按需读 [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md) 的误差→杠杆→廉价正控→有界执行闭环，实际接口和保护规则读 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)。机制失败先分辨可用信息/公平基线/欠训练，再决定转向或补论文。论文贡献读 [PAPER_FIRST.md](PAPER_FIRST.md)，正式独立确认读 [CONFIRMATION.md](CONFIRMATION.md)。

**选择不等于证据认证**：H4若是理论/形式证明或无需静态数据库的仿真，确认可审计的 `PROOF_PATH`，不虚构D1；必须记录 H3/H4/H5 对同一科研问题的科学适配，不允许因数据方便替换用户选题。记录人工节点用 `REVIEW:H#`，论文蓝图Markdown标题的 H1/H2/H3 用 `HEADING:H#` 区分；上游决定或真值被新证据推翻时，依赖下游须重新核有效性。

**新项目统一交互路线（执行镜像 [`contracts/human_review_protocol.v1.json`](contracts/human_review_protocol.v1.json)）**：使用 `protocol_version=pd-rw-human-review-v1.1`；`H1→H2→H3→H4→H5` 的**节点名称、必审维度和顺序固定**，而论文/实验内容与搜索深度可自适应。开始先从用户原指令逐项映射已明确的决定，不能因为只知道研究领域就假定用户选择了六类课题来源或五类贡献路线；对未确定的当前节点给推荐、证据和待确认维度，其他节点保持待决。用户可一条消息同时选择多个节点或明确委托，不需强制五轮；已有项目旧记录不得仅按同名H编号无证据地自动转新版。每轮展示简洁的 H1–H5 进度和**当前节点**，不是让AI自行选取当前要问的科学问题。

**新项目默认 `USER_DEEP_PARTICIPATION`**：按 [WORKFLOW.md](WORKFLOW.md) H1–H5 逐步完成研究范围、六类问题来源与五类贡献路线、候选科学问题、D1数据资源、最终课题及下一步计划的**真实用户选择或明确委托**。AI 在每轮先做足合法只读核查与备选比较；用户可一条消息决定多个已披露事项，已有项目复用旧选择而不强制重审。`PREFERRED`、下载计划或 AI 自选库均不能冒充用户批准；选库、下载、拟合、SEALED 和写稿权限严格分开。待决期间可继续不依赖该节点的合法只读研究，不中断普通技术任务。

**高价值科学设计**：选题、选库、冻结Task或增加复杂机制前按需核[HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)：重要知识差额、数据能否区分竞争解释、决定性科学实验及Q2潜力。已有Run直接续做，不增加强制阶段。

**Q2科研目标**：按[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)，最低成功标准是有证据支持的JCR Q2+投稿潜力（Q1更好），**不要求实际发表**；Q3/Q4或仅小发现不等于项目成功，但未知/负Pilot不自动失败。

**下一步交付方式**：遵守[NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)：可在既有授权范围内自主决定的技术任务/强烈推荐任务，直接给一段最小可执行Agent指令；需用户判断或新增授权的，先给建议与2–3个选项，不提前输出Agent指令。

**双文件科研记忆与写作锁（贯穿全程，非第六项新步骤）**：阅读 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 和 [WRITING_GATE.md](WRITING_GATE.md)。有实际项目工作区时持续维护 `RESEARCH_RECORD.md`；科研方向基本明确后提前规划 `PAPER_BLUEPRINT.md` 的一级/二级标题、各节拟写内容/证据缺口。未经科研总结的用户审查及单独正文授权，不得生成投稿标题、摘要、章节正文或初稿；继续科研及规划不受影响，图片单独授权。

**完成算法后（按需）**：稳定可信Run且拟HOLD/结束/再堆模型时，参考[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)判断一次小规模科学升级是否值得；不新增必经阶段，不自动拟合或写稿。

**论文证据优先触发**：新Task形成时可按需读 [VENUE_STRATEGY.md](VENUE_STRATEGY.md) §0 的真实类似论文，不先做正式期刊评级。首个可信Run、关键负Pilot、拟新建高成本模型或HOLD/PIVOT时，应按需读 [PAPER_FIRST.md](PAPER_FIRST.md) §0，先判断现有主张相对具名近邻有何重要新知识、能否支撑Q2+潜力；满足时优先补决定性证据，不满足时比较可证伪的高价值升级，不默认为升级算法或启动论文写作。稿件确认仍须读 [CONFIRMATION.md](CONFIRMATION.md)；无需每次重载这三个文件。

**证据索引**：新项目出现首个有效Run且有Python环境时按 [core/README.md](core/README.md) 初始化和记录工件；既有项目不强制迁移，无法执行则保留真实原始路径并标`INDEX_PENDING`。

**统一输出**：`NEW_EVIDENCE+PATH | DECISION_CHANGE/UNKNOWN | NEXT_PROBE+可能结果 | AUTH/COST`。不编造运行或检索，不使用封存集调参。新规则不代表额外审批门，现有合法授权范围内可连续执行。

**出现 Oracle 有收益、可部署策略却无增益的症状时**：按需读[SAFE-Gait/APACE 复盘](LESSONS/SAFE_GAIT_APACE.md)并选择 `information-check` 的只读核对；平常项目不要预读此案例或新增审批步骤。

**关键DEV结果独立复算（按需）**：若已有适配RWF的同一原始预测工件，在正式基线/明显增益/异常评审时使用 `core.cli forge-verify`，只得到指标算术验证；旧Run无条件不升级、没有RWF也不阻断探索。先读 [core/README.md](core/README.md) 对应说明，不预加载RWF源码。
