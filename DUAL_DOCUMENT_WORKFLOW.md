# Dual Document Workflow｜持续科研记录与论文蓝图

> 每个实际科研项目维护两份核心 Markdown：RESEARCH_RECORD.md（科研事实、历史与恢复）以及 PAPER_BLUEPRINT.md（论文 H1/H2 结构与证据规划）。不新增科研阶段、CLI 状态、固定 Agent 数量或授权门禁。旧项目可复用等价已有文件，不强制迁移。

## 1. 文件职责

- **RESEARCH_RECORD.md**：回答做了什么、为何做、尝试及有效和负向结果、原因与限制、资产与下一步、失败后如何重启。首页为当前状态，重要事件按序追加；原始 Run/日志/代码/哈希只作来源引用，不复制日志，不编造执行。
- **PAPER_BLUEPRINT.md**：在方向基本明确后规划候选论文的一级/二级标题、各节拟写内容、潜在 Claim、证据指针、缺失实验、文献和图表的文字需求。没有结果的部分标 TENTATIVE、PLANNED、NOT_RUN 或 UNKNOWN；不以蓝图冒充真实论文稿件。
- 研究记录是实验决策的事实索引；论文蓝图按 EXP/Run/Claim 引用研究记录与原始证据，不重复编一套结果。若二者和合法原始工件冲突，以原始证据/协议为准并标待更正。二者既不是科学确认，也不是用户授权凭证。
- **规划不等于正式写作**：未经科研成果总结的用户审查和单独的稿件写作授权，可维护章节 H1/H2 和“本节要写什么”的要点，但不得自动写投稿标题、摘要、完整正文段落、论文式图注或初稿。见 [WRITING_GATE.md](WRITING_GATE.md)。文字图表规划不授权出图，任何图片只在用户明确请求时生成，见 [FIGURE_POLICY.md](FIGURE_POLICY.md)。

## 2. 事件驱动的时间顺序

1. **真实项目开始或接手**：核现有 STATE/Run 和权限，若无等价文件则创建 RESEARCH_RECORD.md，记录范围、资产、UNKNOWN、当前阻碍、已知真实证据及下一步。尚未授权的下载、CPU/GPU、SEALED 不能借整理自动执行。
2. **科学方向或候选贡献初步明确**：建立 PAPER_BLUEPRINT.md 的简要 H1/H2 和逐节“目标、拟写要点、来源、反例、缺口、状态”。可以在实验尚未结束时建立；科研主张尚不确定则保持候选，不强行填完章节/标题。
3. **发生重要科研事件**：任务/协议/假设变化，有意义的真实 Run、负 Pilot、工程故障、有效修复、科研取舍、HOLD/交接时，优先追加科研记录的简短事件，并刷新首页的有效成果、阻碍与唯一下一行动。纯命令、无变化的重复测试、普通无影响 Debug 不逐条记录。保留旧失败史，不能以成功覆盖、删除或改变评价结论。
4. **事件改变论文故事或证据时**：再更新 PAPER_BLUEPRINT 的受影响 H1/H2、Claim–Evidence 映射与缺口；只修订相关节，不复制大段日志、不每轮重复全篇计划。负结果和最强反解释必须反映在适用章节。
5. **暂停/失败/转向/交接**：科研记录突出当前最佳合法 Run、已证实无效/失败路线、未验证替代、可复用资产、恢复条件和下一项区别性 Probe；论文蓝图标记应撤回/更正的主张。项目级 STOP/PIVOT、额外资源和 SEALED 仍需用户决策。
6. **正式写作阶段**：两道用户条件满足后才以蓝图为基础生成稿件，按新证据有界回填、审稿与修订。正式投稿/外传/付费、图片生成分别需要自己的许可。

**更新粒度**：关键事件发生当轮及时整理，同一证据没有变化则复用；两文档均是轻量人机可读的索引，不新增第三本项目日志、不替代原 STATE 或任何真实 Run。

## 3. 最小事件/章节合同

- 一次重要尝试：EXP ID / 目的假说 / 实际实施与协议 / 数据与分组 / Run或文件指针 / 观察及负结果 / VALID、INVALID、INCONCLUSIVE 或 NOT_RUN / 原因确定性与最强替代解释 / 后续实验或重启价值。INVALID 不等于科学证伪，未知写 UNKNOWN。
- 每个论文章节：H1/H2 / 本节任务 / 2–5 个要点 / Claim–EXP–Run 证据及真实文献 / 反例和适用范围 / 缺失实验 / 规划状态。显示结果/数字时需指向原始来源、独立统计单位、分母、评价协议和选择历史，不得从图表或项目愿望虚构结论。
- 跨会话 STATE 只需按需保留 RESEARCH_RECORD_REF、PAPER_BLUEPRINT_REF 两个路径；Agent 优先读两份文件首页与当前任务的相关事件/章节，再按需打开真实证据，避免无意义的全库重读。

参考 [MLflow](https://github.com/mlflow/mlflow) 的 Run 追踪、[RD-Agent](https://github.com/microsoft/RD-Agent) 的反馈闭环、[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 的结果到 Claim 与 Paper Plan、[latex-paper-skills](https://github.com/yunshenwuchuxun/latex-paper-skills) 的章节/实验需求规划及 [K-Dense](https://github.com/K-Dense-AI/scientific-agent-skills) 的 Claim–Evidence 对齐。只是参考设计，不依赖安装这些项目或额外调用模型。
## 4. AI 冷启动读取优先级（非额外状态机）

- 入口只有 [AGENTS.md](AGENTS.md)。收到既有项目任务时，**先用已知项目目录或既有 STATE 的 RESEARCH_RECORD_REF/PAPER_BLUEPRINT_REF 定位文件**，若存在则优先读 RESEARCH_RECORD.md 的**当前快照 → 当前可信成果/失败边界 → 下一步及权限依赖**；如涉及论文，再读 PAPER_BLUEPRINT.md 的构思快照和受影响 SEC_ID。随后读 STATE/manifest 与相关 EXP/Run/Claim 的**真实原始证据**。只有当前问题需要时才读旧事件全文、其他论文节、专题 Skill 或历史日志。新项目按需读 START.md，WORKFLOW.md 仍是唯一科研总控。
- **分轴核实而不是混排权限与数据**：用户原始指令与正式授权记录仅决定**允许做什么**；合法原始工件/冻结协议决定**实验事实及可比性**；STATE/Run 索引提供定位、版本和追溯；研究记录与论文蓝图只是摘要/规划。不可用用户意愿推翻数据事实，也不可用已验证 Run 自动授予权限。若有矛盾，标 `SOURCE_CONFLICT` 并核证，不能默默选择对论文最有利的一项。STATE 保留原来的 Run/机器状态职责，**两份 Markdown 仅提供可读索引**，不能反向改写底层证据。
- **旧项目与并发安全**：真实项目若未建立两份 Markdown，可先按既有 STATE/Run 工作，并在有信息增量时按需建立；同一项目有多个 Agent 时，先比较文件最新版本/内容，再以单一写入者或串行合并局部差异，禁止无条件覆盖、误删另一 Agent 的更新。对现有历史追加更正说明并保留原始 Run。内容可核查但不自动拥有任何授权。
- **文件中状态要有时点与依据**：快照记录最近实质更新标识（事件/Run/版本）；不知道时间或路径写 UNKNOWN。锁定权限依然须查原始用户指令，文档只能存其引用，不能生成批准。

## 5. ID、章节层级与局部更新

- 复用项目真实的 Task/Run/Claim ID；新记一次重要科研尝试可用 `EXP-001`，新增 Claim 可用 `CLM-001`，但**不强制将已有 C01 或外部 Run 改名**。原始 Run ID 与其数据版本、评估协议、独立组及证据路径一起保留，重跑不得复用旧实验结果来伪装同一运行。
- 论文结构在 Markdown 中固定为：一个文档 H1（`# PAPER_BLUEPRINT`），论文一级标题用 H2（`## 1. Introduction`），二级标题用 H3（`### 1.1 Research Background`）。章节可有稳定 `SEC_ID`（如 `SEC-INTRO-01`），即使后续改名/调整显示编号也不重用 ID。文档元信息使用未编号的 H2，不能混入论文章节序号。
- **算法/机器学习论文标准六章（默认必须优先保持）**：`1. Introduction → 2. Related Work → 3. Proposed Method → 4. Experiments → 5. Discussion → 6. Conclusion`。`Proposed Method` 是常规称法，避免 `Proposal Method`。第4章记录协议、主结果与必要的公平对照/消融；第5章解释机制、证据边界、局限与应用意义，避免复述结果。Abstract、References及目标期刊要求的声明属稿件要素，不占用六章编号；规划阶段不得撰写正式摘要/投稿正文。
- **六章结构优先，例外先确认（论文框架的人工确认，不是科研实验新关卡）**：初次规划以及获授权的正式写稿均优先使用以上六章，不得仅为简洁、追逐范文风格或 Agent 自主判断擅自合并、删除、增加、调序或重命名六个一级论文章节。确有客观必要时（例如期刊强制格式、理论证明需单列章节、研究性质明显不宜称 `Proposed Method`、篇幅硬限制），**先向用户展示现行章节 → 拟议章节、调整的具体必要性、官方指南/真实证据依据、对主张及实验呈现的影响，并等待该项目对应的明确确认，才可改动**。在确认前保留六章，仅在 Planning Snapshot 记录简短候选变更，禁止将提案当作已批准。可选例外包括将 Related Work 并入 Introduction、合并 Experiments/Discussion、理论稿增 Preliminaries / Theoretical Analysis、工程稿改 Methodology / System Design 或按期刊强制的 Results → Discussion → Methods 排序；以上都不是自动许可。若真实研究结论需要更正，应立即更正 Claim/证据状态，不可等待目录确认或虚构结果。
- **结构决策留痕**：在蓝图 Planning Snapshot 简记论文类型、结构选择（默认六章/例外提议待确认/用户已确认）、具体调整原因、期刊官方格式来源或 `UNKNOWN`，已确认时须留原始用户确认消息指针；无可核验确认不得标为已确认。保持原 `SEC_ID` 与 Claim–EXP–Run 映射，即使经批准合并/移动节也不伪造证据。优先确保问题/近邻差额、可复现方法、合法实验、主要发现、反解释与局限、结论得到清晰呈现；不因模板漂亮而增加无用实验或改变原科学结论。参考 [IEEE Journal Structure](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/)、[NeurIPS 2026 Handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook) 与 [Nature Machine Intelligence Content Types](https://www.nature.com/natmachintell/content)（仅作差异化结构案例）。
- 每个计划小节只记录**目标、拟写要点、真实 Claim/EXP/Run/文献指针、负证据与缺口、状态**。新科学结论改变局部时，只修改相应 SEC_ID 和首页索引，不批量重排整篇；涉及上述实质结构变更须先获得用户明确确认。图表规划只写文字，未获具体绘图请求不得生成任何图片。
- RESEARCH_RECORD.md 推荐首页快照保持简短（通常约 20–40 行，具体按事实增减）；先放当前成果、失败边界与下一合法行动，**完整事件历史放在文档末尾按时间追加**。旧历史原则上保留，明确作废/纠错应追加来源及原因，而不是覆盖原失败。

## 6. 冷启动交接验收（不宣称自动测得 AI 理解提升）

接手者不必先读全部历史，也应能从当前快照和所指证据回答：项目问题与用户范围、最佳真实有效 Run 及协议、最重要的负结果/故障原因、下一步及权限、论文受影响的 SEC_ID 和待补证据。静态测试只能检查**结构/链接/权限语句**；真正的 AI 接手成功率和 Token 成本必须通过后续真实或受控的 Agent 接手对照测量，不得宣称 CI 已证明科研质量提升。

## 7. 按需只读文档结构核查（可选，不新增审批）

如果新建/大量修改两份文件、发现断链或 Agent 接手时怀疑 ID 重复，可用标准库运行以下**只读**检查（需在 PD-RW 源码环境）：

```bash
python -m core.doc_integrity --project PROJECT_DIR
# 如两份文件不在项目根目录，显式指定相对于 PROJECT_DIR 的路径：
python -m core.doc_integrity --project PROJECT_DIR --record docs/RESEARCH_RECORD.md --blueprint docs/PAPER_BLUEPRINT.md --json
```

此工具**只打开指定两份 Markdown**，检查唯一文档 H1、论文 H2/H3 层级、重复 EXP/SEC_ID、简要断链警告；不会打开 Run 数据、SEALED、图片或执行任何训练/生成，不改写文件。缺少两份文件的旧项目返回 INFO 而非失败，旧引用不完整只给 WARN；真正结构错误标 ERROR。项目有多 Agent 并发写入时，需在写前协调最新文件版本，检查器**不**进行文件锁定或自动冲突合并。核查通过仅是格式/ID 一致，**不是科学真实性、用户授权、引用正确性或 AI 接手成功的证明**。没有相关症状无需每轮运行。
