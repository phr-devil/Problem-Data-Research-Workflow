# Dual Document Workflow｜持续科研记录与论文蓝图

> 每个实际科研项目维护两份核心 Markdown：RESEARCH_RECORD.md（科研事实、历史与恢复）以及 PAPER_BLUEPRINT.md（论文 H1/H2 结构与证据规划）。不新增科研阶段、CLI 状态、固定 Agent 数量或授权门禁。旧项目可复用等价已有文件，不强制迁移。

## 1. 文件职责

- **RESEARCH_RECORD.md**：回答做了什么、为何做、尝试及有效和负向结果、原因与限制、资产与下一步、失败后如何重启。首页为当前状态，重要事件按序追加；原始 Run/日志/代码/哈希只作来源引用，不复制日志，不编造执行。
- **PAPER_BLUEPRINT.md**：在方向基本明确后按文章类型规划候选论文的一级/二级标题、各节拟写内容、潜在 Claim、证据指针、缺失实验、文献和图表的文字需求。没有结果的部分标 TENTATIVE、PLANNED、NOT_RUN 或 UNKNOWN；不以蓝图冒充真实论文稿件。
- 研究记录是实验决策的事实索引；论文蓝图按 EXP/Run/Claim 引用研究记录与原始证据，不重复编一套结果。若二者和合法原始工件冲突，以原始证据/协议为准并标待更正。二者既不是科学确认，也不是用户授权凭证。
- **规划不等于正式写作**：未经科研成果总结的用户审查和单独的稿件写作授权，可维护章节 H1/H2 和“本节要写什么”的要点，但不得自动写投稿标题、摘要、完整正文段落、论文式图注或初稿。见 [WRITING_GATE.md](WRITING_GATE.md)。文字图表规划不授权出图，任何图片只在用户明确请求时生成，见 [FIGURE_POLICY.md](FIGURE_POLICY.md)。

## 2. 事件驱动的时间顺序

1. **真实项目开始或接手**：核现有 STATE/Run 和权限，若无等价文件则创建 RESEARCH_RECORD.md，记录范围、资产、UNKNOWN、当前阻碍、已知真实证据及下一步。整理工作不能自行下载新库、开启SEALED或生成授权；H5已批准且DEV合法就绪时本地安全非付费CPU/GPU研发按`AI_DEV_AUTONOMY`执行，无需额外逐次确认。
2. **科学方向或候选贡献初步明确**：建立 PAPER_BLUEPRINT.md 的简要 H1/H2 和逐节“目标、拟写要点、来源、反例、缺口、状态”。可以在实验尚未结束时建立；科研主张尚不确定则保持候选，不强行填完章节/标题。
3. **发生重要科研事件**：任务/协议/假设变化，有意义的真实 Run、负 Pilot、工程故障、有效修复、科研取舍、HOLD/交接时，优先追加科研记录的简短事件，并刷新首页的有效成果、阻碍与唯一下一行动。纯命令、无变化的重复测试、普通无影响 Debug 不逐条记录。保留旧失败史，不能以成功覆盖、删除或改变评价结论。
4. **事件改变论文故事或证据时**：维护已有 `PAPER_BLUEPRINT.md` 的 `WORKING_THESIS`（问题重要性→新增知识/能力→关键证据与边界）及受影响的 H1/H2、Claim–Evidence 映射；新证据支持或反驳时允许修订/撤回中心论证，**不锁死第一版故事线**。用中心论证选择支持性、反证性和必要限制的证据并映射章节；不为满足故事而删真实负结果、夸大机制或改变原始 Run。只修订相关节，不复制大段日志、不每轮重复全篇计划。负结果和最强反解释必须反映在适用章节。
5. **暂停/失败/转向/交接**：科研记录突出当前最佳合法 Run、已证实无效/失败路线、未验证替代、可复用资产、恢复条件和下一项区别性 Probe；论文蓝图标记应撤回/更正的主张。项目级STOP/超H5 PIVOT、付费/云资源、新数据获取及SEALED仍需用户决策；合法本地DEV算法计算/机制选择无须逐次问。
6. **正式写作阶段**：两道用户条件满足后才以蓝图为基础生成稿件，按新证据有界回填、审稿与修订。正式投稿/外传/付费、图片生成分别需要自己的许可。

**更新粒度**：关键事件发生当轮及时整理，同一证据没有变化则复用；两文档均是轻量人机可读的索引，不新增第三本项目日志、不替代原 STATE 或任何真实 Run。

**输出与持久化的分工**：以 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 的自适应 L1/L2/L3 汇报任务结果：**聊天简报=这次取得的结果/必要证据/合法下一步；已有MD=重要科研事实和可恢复记忆**，并非每轮必须同时产出两份完整报告。只有 Task/协议、可信Run、重要负结果、科研选择和恢复风险发生实质变化才增量修改 `RESEARCH_RECORD.md`；只有中心科学主张、论文结构或 Claim–Evidence 发生变化才修改 `PAPER_BLUEPRINT.md`。无影响的普通Debug或重复测试无需新建结果MD。用户要求独立交付，或大型验收/跨团队复核确有独立归档需求时才单独生成报告，只在科研记录中保存引用，**不新增第三份常设台账**。

**Token高效且证据可靠**：按现有快照、相关 EXP/Run/Claim/SEC_ID 和实际受影响文件定向读取，复用已核权限/工件/测试；在已有授权内连续完成相关检查、修复和必要回归，不机械分批、重复规划或无意义多Agent调用。关键真值、组独立性、最强反证、SEALED、授权及可复现性不能因为压缩输出而遗漏。即便最终聊天极简，原始失败与依据仍需可追溯。

**正式稿件接口**：仅在 [WRITING_GATE.md](WRITING_GATE.md) 两道用户条件满足后，按 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) 从已批准蓝图及真实 Claim/Run 构建临时写作证据合同；`MANUSCRIPT_TEXT.md` 作为唯一正文源，引用/公式/图表待办可使用 `MANUSCRIPT_OPEN_ITEMS.md`，两者不替代这两份持续科研文档，也不授权修改已批准章节结构。

**前期用户选择与后期AI科学决定的事件记忆**：新科研项目按 [WORKFLOW.md](WORKFLOW.md) H1–H10 及 H6/H7/H8的AI自主科学决定及H9/H10适用的用户节点，在当前 `RESEARCH_RECORD.md` 快照区分USER的H1–H5/H9/H10原消息与AGENT的H6–H8决定证据、当前有效选择及待决依赖，在第5节既有事件历史保留每次重要改变的原因和证据（不单独建立审批日志或重写旧Run）。用户曾一次批准多个节点、明确有限委托或旧项目已有实际决策，则复用其原指令，不机械追加十条事件。`STATE.md` 仅留 `HUMAN_REVIEW_CURRENT/HUMAN_DECISION_REF` 导航；`PAPER_BLUEPRINT` 只受真实科学贡献与用户已确认论文结构影响，不写成人工审批表。新证据触发的局部回退记录受影响节点和更正理由，保留历史。

**不同 H 标识必须分开**：`REVIEW:H1–H10` 仅用于人工科研选择与可核原消息，`HEADING:H1/H2/H3` 仅表示论文蓝图 Markdown 标题层级，不能以论文大纲 H2 代替人工 H2 来源/贡献路线的真实选择。上游决策因数据、合法输入或主张改变而失效时，在研究记录标明下游待复核的依赖并保留旧决定；蓝图仅同步真正受影响的章节/Claim 指针。

**活动交接不新增科研档案**：统一 [research_activity_protocol.v1.json](contracts/research_activity_protocol.v1.json) 的六活动证据指针仅写到既有 RESEARCH_RECORD 快照/受影响第5节事件；STATE 只保留 `CURRENT_ACTIVITY_HANDOFF` 路径。论文蓝图只在实际中心主张/章节证据变化时增量更新，不把活动04的普通调参复制成长期论文故事；活动05允许并行复盘，不改变写作锁或图件许可。

## 3. 最小事件/章节合同

- 一次重要尝试：EXP ID / 目的假说 / 实际实施与协议 / 数据与分组 / Run或文件指针 / 观察及负结果 / VALID、INVALID、INCONCLUSIVE 或 NOT_RUN / 原因确定性与最强替代解释 / 后续实验或重启价值。INVALID 不等于科学证伪，未知写 UNKNOWN。
- 每个论文章节：H1/H2 / 本节任务 / **按信息需要而非固定个数**的内部论证要点 / Claim–EXP–Run 证据及真实文献 / 反例和适用范围 / 缺失实验 / 规划状态。核心创新可有较多要点，普通背景可只有一项；要点属于内部规划，正式稿件必须转化为连贯英文段落。显示结果/数字时需指向原始来源、独立统计单位、分母、评价协议和选择历史，不得从图表或项目愿望虚构结论。
- 跨会话 STATE 只需按需保留 RESEARCH_RECORD_REF、PAPER_BLUEPRINT_REF 两个路径；Agent 优先读两份文件首页与当前任务的相关事件/章节，再按需打开真实证据，避免无意义的全库重读。

参考 [MLflow](https://github.com/mlflow/mlflow) 的 Run 追踪、[RD-Agent](https://github.com/microsoft/RD-Agent) 的反馈闭环、[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 的结果到 Claim 与 Paper Plan、[latex-paper-skills](https://github.com/yunshenwuchuxun/latex-paper-skills) 的章节/实验需求规划及 [K-Dense](https://github.com/K-Dense-AI/scientific-agent-skills) 的 Claim–Evidence 对齐。只是参考设计，不依赖安装这些项目或额外调用模型。
## 4. AI 冷启动读取优先级（非额外状态机）

- 入口只有 [AGENTS.md](AGENTS.md)。收到既有项目任务时，**先用已知项目目录或既有 STATE 的 RESEARCH_RECORD_REF/PAPER_BLUEPRINT_REF 定位文件**，若存在则优先读 RESEARCH_RECORD.md 的**当前快照 → 当前可信成果/失败边界 → 下一步及权限依赖**；如涉及论文，再读 PAPER_BLUEPRINT.md 的构思快照和受影响 SEC_ID。随后读 STATE/manifest 与相关 EXP/Run/Claim 的**真实原始证据**。只有当前问题需要时才读旧事件全文、其他论文节、专题 Skill 或历史日志。新项目按需读 START.md，WORKFLOW.md 仍是唯一科研总控。
- **项目身份最小核验（`PROJECT_IDENTITY_CHECK`，非新增审批）**：接手用户以项目编号、研究线名、数据库名或旧文件名指代的既有任务时，优先用真实路径和现有 `STATE/ARCHIVE_MANIFEST/RESEARCH_RECORD` 确认 `PROJECT_PATH | TASK | PRIMARY_DATA | ARCHIVE_STATUS | EVIDENCE_REF`。**编号、研究线、数据集与相同受试者 ID 不能自动视为同一项目**，不得在名称相似的目录间混拼 Run、Claim、封存分组或稿件。身份冲突标 `PROJECT_IDENTITY_UNVERIFIED` 并限定只读证据定位；可依据实际记录消除歧义就自主处理，不能消除且影响科研执行才请用户确定，不建立第三份常设索引。
- **分轴核实而不是混排权限与数据**：用户原始指令与正式授权记录仅决定**允许做什么**；合法原始工件/冻结协议决定**实验事实及可比性**；STATE/Run 索引提供定位、版本和追溯；研究记录与论文蓝图只是摘要/规划。不可用用户意愿推翻数据事实，也不可用已验证 Run 自动授予权限。若有矛盾，标 `SOURCE_CONFLICT` 并核证，不能默默选择对论文最有利的一项。STATE 保留原来的 Run/机器状态职责，**两份 Markdown 仅提供可读索引**，不能反向改写底层证据。
- **旧项目与并发安全**：真实项目若未建立两份 Markdown，可先按既有 STATE/Run 工作，并在有信息增量时按需建立；同一项目有多个 Agent 时，先比较文件最新版本/内容，再以单一写入者或串行合并局部差异，禁止无条件覆盖、误删另一 Agent 的更新。对现有历史追加更正说明并保留原始 Run。内容可核查但不自动拥有任何授权。
- **文件中状态要有时点与依据**：快照记录最近实质更新标识（事件/Run/版本）；不知道时间或路径写 UNKNOWN。锁定权限依然须查原始用户指令，文档只能存其引用，不能生成批准。
- **规则恢复不等于授权复制**：冷启动/跨Agent/上下文压缩、项目或Task改变、版本更新时，先复用已知 `RULE_REPO | RULE_COMMIT | LOADED_FILES`、现有 STATE/事件/原 Run 指针，按 [AGENTS.md](AGENTS.md) 重核新增适用专题；执行敏感操作前必须再核原用户消息中的对象、时效、资源和依赖。只在恢复信息实际缺失时补充现有 STATE/科研记录的**路径或版本引用**，不另建规则副本、第三份永久台账或自我授权标志。并发Agent不能覆盖对方新增的关键失败、决定或证据，冲突按来源核证并保留纠错历史。

## 5. ID、章节层级与局部更新

- 复用项目真实的 Task/Run/Claim ID；新记一次重要科研尝试可用 `EXP-001`，新增 Claim 可用 `CLM-001`，但**不强制将已有 C01 或外部 Run 改名**。原始 Run ID 与其数据版本、评估协议、独立组及证据路径一起保留，重跑不得复用旧实验结果来伪装同一运行。
- 论文结构在 Markdown 中固定为：一个文档 H1（`# PAPER_BLUEPRINT`），论文一级标题用 H2（`## 1. Introduction`），**仅确有必要的二级标题**用 H3（例如 `### 3.2 Core Method`）；**Introduction 默认无 `1.1/1.2` 等 H3 级小节**，Conclusion 通常也不需要 H3。其内部证据片段/SEC_ID 保留在 H2 下的要点中，不能自动提升为投稿正文的可见标题。章节可有稳定 `SEC_ID`（如 `SEC-INTRO-01`），即使后续改名/调整显示编号也不重用 ID。文档元信息使用未编号的 H2，不能混入论文章节序号。
- **初次论文规划按文章类型选择结构**：`EMPIRICAL_RESEARCH`（实验/算法）优先使用 [六章蓝图](templates/PAPER_BLUEPRINT.md) 的 Introduction → Related Work → Proposed Method → Experiments → Discussion → Conclusion；`CRITICAL_REVIEW` 参考 [综述蓝图](templates/PAPER_BLUEPRINT_REVIEW.md) 综合证据、争议、原创框架和未来议程；`PERSPECTIVE` 参考 [观点蓝图](templates/PAPER_BLUEPRINT_PERSPECTIVE.md) 组织核心论点、反论点、可证伪假说及研究倡议。专用模板为建议骨架，不机械限定章节数；目标期刊的官方要求优先。初次选类型**不是例外审批**，不需要额外人工确认或新科研阶段。
- **引言与篇幅的默认写作映射**：新稿件的 Introduction 默认是无分节的连续学术叙述，不用 bullet/numbered-list 逐项交付背景、文献或创新点；研究蓝图中列出的 `SEC-INTRO-*` 只供内部定位。正文长度根据科学主张的重要性、与最近邻的差别、解释难度及必要证据决定，**不根据模板给段落平均配字数**；已批准项目的具体子标题除非获本项目用户同意，不自动删除。
- **已经确认的结构不能自动改动**：不论论文类型，用户已批准的一级标题、重大二级结构及稳定 `SEC_ID` 应保留；若确有科学/官方指南上的必要性，先展示当前→拟议结构、依据及对证据表达的影响，经用户明确确认后修改。对尚未确认的新蓝图，Agent 可以按研究内容选初始类型及常见章节；若类型不确定，标 `TYPE_TENTATIVE` 而非反复询问。正式标题/摘要/正文依然由 [WRITING_GATE.md](WRITING_GATE.md) 独立授权。
- **不同文章的论证职责**：实证稿重点完成 Method↔Result、合法评价、竞争解释及局限；综述重点完成证据覆盖与分歧比较、跨文献新分类和未来研究议程；Perspective 重点完成明确立场、最强反论点、可检验假说与倡议。未来愿景区分 `OBSERVED/INTERPRETATION/HYPOTHESIS/VISION`，不因尚未全面实现就删除有依据的设想，也不能写成既成事实。
- **结构与证据最小留痕**：Planning Snapshot 记录论文类型、初始模板/期刊要求与已批准目录的原始消息指针。多章节共用的重要证据缺口可以在 `RESEARCH_RECORD.md` 只定义一次 `GAP_ID: GAP-001`，在 `PAPER_BLUEPRINT.md` 中引用其 ID 和受影响 SEC_ID，不复制详细现状。对单一局部缺口继续复用 EXP/Run/Claim 指针，不强制建 GAP ID、迁移旧项目或新增状态机。
- 每个计划章节或必要小节只记录**目标、拟写要点、真实 Claim/EXP/Run/文献指针、负证据与缺口、状态**。写作时先转换成真正的科学论证，不能将要点标签复制成小标题、清单或长度均匀的段落。新科学结论改变局部时，只修改相应 SEC_ID 和首页索引，不批量重排整篇；涉及上述实质结构变更须先获得用户明确确认。图表规划只写文字，未获具体绘图请求不得生成任何图片。
- RESEARCH_RECORD.md 推荐首页快照保持简短（通常约 20–40 行，具体按事实增减）；先放当前成果、失败边界与下一合法行动，**完整事件历史放在文档末尾按时间追加**。旧历史原则上保留，明确作废/纠错应追加来源及原因，而不是覆盖原失败。

- **Word 蓝图导出**：用户明确要求 Word 框架审阅版时，从现有 `PAPER_BLUEPRINT.md` 按 [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md) 的固定标题层级、零段距与自动编号生成；不新建第三份长期科研文件，也不自动写正文、生成图片或导出 `.docx`。非 Title 段前/段后为 `0/0 pt`，Title 为 `0/18 pt`；官方期刊格式优先于通用工作版。

## 6. 冷启动交接验收（不宣称自动测得 AI 理解提升）

接手者不必先读全部历史，也应能从当前快照和所指证据回答：项目问题与用户范围、最佳真实有效 Run 及协议、最重要的负结果/故障原因、下一步及权限、论文受影响的 SEC_ID 和待补证据。静态测试只能检查**结构/链接/权限语句**；真正的 AI 接手成功率和 Token 成本必须通过后续真实或受控的 Agent 接手对照测量，不得宣称 CI 已证明科研质量提升。

## 7. 按需只读文档结构核查（可选，不新增审批）

如果新建/大量修改两份文件、发现断链或 Agent 接手时怀疑 ID 重复，可用标准库运行以下**只读**检查（需在 PD-RW 源码环境）：

```bash
python -m core.doc_integrity --project PROJECT_DIR
# 如两份文件不在项目根目录，显式指定相对于 PROJECT_DIR 的路径：
python -m core.doc_integrity --project PROJECT_DIR --record docs/RESEARCH_RECORD.md --blueprint docs/PAPER_BLUEPRINT.md --json
```

此工具**只打开指定两份 Markdown**，检查唯一文档 H1、论文 H2/H3 层级、重复 EXP/SEC_ID、可选 GAP_ID 定义及简要断链警告；不会打开 Run 数据、SEALED、图片或执行任何训练/生成，不改写文件。缺少两份文件的旧项目返回 INFO 而非失败，旧引用不完整只给 WARN；真正结构错误标 ERROR。项目有多 Agent 并发写入时，需在写前协调最新文件版本，检查器**不**进行文件锁定或自动冲突合并。核查通过仅是格式/ID 一致，**不是科学真实性、用户授权、引用正确性或 AI 接手成功的证明**。没有相关症状无需每轮运行。
