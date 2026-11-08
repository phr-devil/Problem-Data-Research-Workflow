# AGENTS.md｜PD-RW Agent 唯一默认入口

> 这是**导航和权限摘要**，不是第二套科研流程。正式科研决策始终由 [WORKFLOW.md](WORKFLOW.md) 主控；只有用户明确选择 PD-RW 时启用。本文件仅指导“先读什么、再做什么”，专题规则按需加载。

## 0. 冷启动/跨会话恢复：按此顺序读取

1. **明确本轮用户请求及实际权限**，确认项目目录、研究范围和是否为既有任务；用户最新的原始授权优先于任何状态摘要。
2. **已有项目**：先从已知项目路径或现有 STATE 中的 `RESEARCH_RECORD_REF` / `PAPER_BLUEPRINT_REF` **定位文件**，存在才读 `RESEARCH_RECORD.md` 顶部“当前快照”（目标、可信成果、失败边界、当前阻碍、下一步）；论文任务再读 `PAPER_BLUEPRINT.md` 的构思快照和相关 `SEC_ID`。随后核真实 STATE/manifest 及当前任务相关 EXP/Run/Claim、源码和协议；缺文档则按旧项目的 STATE/原始证据继续，不虚构快照或先通读所有历史。
3. **新项目**：按需读 [START.md](START.md) 和 [WORKFLOW.md](WORKFLOW.md) 对应活动，创建/复用科研记录；方向基本明确后再建立论文蓝图。不重复启动已经选题、下载和验证过的流程。
4. **规则冲突/来源冲突**：用户原始授权与真实源工件最优先；[WORKFLOW.md](WORKFLOW.md) 管科研选择、阶段与权限；[DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 管两文件更新；专题文件只管其具体任务。STATE、摘要、哈希检查、Agent 判断均不能替代科学证据或真实授权。

## 1. 不可跨越的边界

- **权限**：选题和选库不自动许可下载、安装、CPU/GPU 拟合、SEALED/独立确认、付费、数据外传、项目级 STOP/PIVOT 或投稿；按 [NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md) 将授权内下一技术行动与用户必须决策的事项分开。
- **论文**：允许提前维护 `PAPER_BLUEPRINT.md` 的 H1/H2 内容规划及证据缺口；新论文按类型规划：实证算法论文默认六章，Critical Review / Perspective 可采用相应论证蓝图；已获用户确认目录的重大变更仍需说明理由并获确认（见 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) §5）；正式稿件标题、摘要、章节正文/初稿须先完成科研成果总结并经用户审查，再由用户明确授权。默认 `WRITING_LOCKED`，见 [WRITING_GATE.md](WRITING_GATE.md)。
- **Word 格式**：用户要求论文蓝图 Word 审阅版或获授权稿件 Word 排版时，按 [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md) 使用统一格式；仅导出不解除 `WRITING_LOCKED`，不自动生成 Word 文件。
- **高价值科研决策与实证评测**：重要性/负结果/新基准/系统级贡献优先读 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)、[PAPER_FIRST.md](PAPER_FIRST.md) 当前相关节；科研机制和科学证据路径均按用户已授权范围执行。理论/仿真与真实独立数据的确认资格不得混淆，见 [CONFIRMATION.md](CONFIRMATION.md)。真实 Agent 改善只能经 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) 对照，CI 仅证明规则/程序行为，不证明科研质量。
- **科学发现与可信论文的执行主线**：选题按 [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) 考虑现实需求、理论/测量张力、已有合法数据异常与具名文献矛盾；重要机制按 [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md) 区分竞争解释；科研成果按 [SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md) 按 Claim 类型识别证据缺口。论文蓝图用可修订的 `WORKING_THESIS` 保持问题—设计—结果—解释连贯；这些不是新阶段、自动科研/写作许可或固定额外实验。

- **已获授权的正式正文写作**：按 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) 以证据→主张→章节→正文→科学审查→语言精修进行；R1 必查 [高水平论文案例库](paper_exemplars/README.md)，按需阅读1–3张相关策略卡。采用6个功能模块/4轮按需连续执行、单一稿件源和增量验证。此路由不解除 [WRITING_GATE.md](WRITING_GATE.md) 的两道门禁，也不允许自动更改已批准目录。
- **论文正文生成的图片编排**：正式稿件撰写时按 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md)“正文生成阶段的图片位置与 Fig. 图题”以及 [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md)：图片全部置于全部文字、声明和 References 后，正文仅保留图号引用；单面板 `Fig.1 Overview.`，多面板 `Fig.1 Overview. (a) ... (b) ...`；不把它误作事后 [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md) 的修复要求，也不授权自行绘图。
- **论文叙述的默认形态**：新论文 Introduction 默认只保留一个一级标题，正文以连贯段落说明问题、最近邻局限、科学缺口、思路和有证据支持的创新，不将蓝图内部小节/项目符号直接导出。核心创新、方法机制和决定性对照按内容需要充分解释，背景简洁，段落不追求等长；稿件审查按 [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md) 的 Q2/Q5/Q8 检查“核心贡献是否真正展开”，可选只读 `core.manuscript_flow` 仅定位引言标题/列表，不评估创新或正文质量。既有获批准目录不得静默改动，仍受写作/改稿授权门禁约束。
- **正文不得清单化或括号堆砌**：所有类型论文的正式叙述性正文应是连续学术段落，**禁止**将多段论述写成 `▪/•/①②③/1.2.3.` 等分点作答；避免频繁圆括号旁注、嵌套或重复缩写，优先融入正常句子。仅保留首次术语缩写、引用、公式/函数、子图与必要统计等专业用途，并区分算法伪代码、表格、期刊强制结构。具体修订与全文 QA 按 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) / [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md)，不影响写作授权门禁。
- **反模板化审稿分级**：正文创作按 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) 的 `HARD / MAJOR / STYLE` 合同：对话式/Markdown 残留、分点正文、投稿版未消解占位和无根据科学结论不得放行；引言空话、近邻差别与方法解释不足、Results/Discussion 重复、段落孤岛和术语漂移必须审查；`delve/underscore/pivotal`、破折号、被动语态等只作语境提示，不机械禁词或设置 AI 率阈值。审稿按 [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md) 路由，保留授权与科研证据门禁。
- **已有完整论文的审核/修订**：按 [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md) 执行独立审稿→证据/引用审计→获授权的局部修订→语言检查→交付回归；十个检查域按需合并为五轮，不重复触发正文生成。审核不授予改写、变更已批准重大结构、读取 SEALED、绘图、实验或投稿权限；修订前须核原始授权。
- **稿件语义和独立确认检查**：优先按现有 [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md) G2/Q3/Q4/R4 复核数字、因果、显著性和 DEV/VAL/CONFIRMATION 真实证据归属；可选 `core.manuscript_claim_guard` 只做离线警报，不保证全文语义正确或独立确认成立。写作阶段先按 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) 保留科学信息，不能为去 AI 味改写事实。

- **稿件 QA 三项必检**：若执行完整稿件审核，Q9 全文风格定位与复检（只报告风格覆盖率，不虚构真实 AI 比例）、Q7 参考文献身份/元数据逐条核验与关键论断原文支持、Q5 最近邻公平差别与 OBSERVED/INTERPRETATION/HYPOTHESIS/VISION 分层均按 [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md)；不可用自动文本评分替代科学审核。
- **图片**：**只有用户明确要求绘制/修改指定图片才能出图**；诊断图、论文图、预览和重绘均不可自动触发。见 [FIGURE_POLICY.md](FIGURE_POLICY.md)。
- **证据**：开发集增益、通过测试、元数据或论文蓝图不是科研确认。Q2+可信投稿潜力（优先Q1）是科研目标，不保证录用；见 [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)。

## 2. 按实际阻碍加载一个相关专题

> **轻量导航层（INDEX_ONLY）**：按下列直接链接读取当前任务需要的权威文件；仅在任务归属不清时查 [专题索引](modules/README.md)。[科研模块](modules/research/README.md)、[论文模块](modules/paper/README.md)、[绘图模块](modules/figures/README.md) 及 [权限索引](policies/README.md) 只是路径清单，不是新规则；勿逐层通读。结构维护见 [STRUCTURE.md](docs/STRUCTURE.md)。

- **新题/选库**：[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) 的 `BREADTH_SCAN → DEEP_FALSIFICATION → COMPETING_CHOICE`、[DATA_DISCOVERY.md](DATA_DISCOVERY.md) 的 `PRE_DOWNLOAD_SCIENCE_FIT`，必要时 [HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md)；必需数据获授权且验收后才做数据实证。
- **算法/负结果**：[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)、[ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)；复用有效 Run，必要时按 [SCIENCE_RESULT_HARVEST.md](SCIENCE_RESULT_HARVEST.md) 区分 `ARTICULATION_GAP` 与 `EVIDENCE_GAP`。
- **科学机会/升级**：按需 [PAPER_FIRST.md](PAPER_FIRST.md)、[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)；只有已授权且有决定性新假说才升级复杂模型，重要失败和有价值资产不丢弃。
- **完整稿件质量复核/投稿前预检**：直接读 [MANUSCRIPT_QA.md](MANUSCRIPT_QA.md)；已有合法稿件按真实证据、原稿→修订稿语义回归与按需真实 Word/PDF 渲染核验；Skill 只按需选用，不安装全套。
- **独立确认/期刊**：[CONFIRMATION.md](CONFIRMATION.md)、[VENUE_STRATEGY.md](VENUE_STRATEGY.md)；RWF 仅在必要时按原始预测与协议进行 DEV 指标复核，不接管科研主控或给予许可。

- **已授权的论文数据图**：优先按 [FIGURE_POLICY.md](FIGURE_POLICY.md) §4.5 使用 PD-RW 图表主题（RWF `styles/figure_theme_pdrw.json` 或同等实现）。普通二维数据图双轴末端箭头，彩色柱体无冗余点；多个可比子图统一布局与文字锚点。导出前执行箭头、柱体和真实子图几何检查，最后检查论文宽度的真实 SVG/PNG。若仅讨论规范，不生成图片。旧项目主题不擅自迁移。
- **已授权的论文架构图／重绘**：优先从项目已有 `figures/<figure_id>.spec.json` 与 `.drawio` 恢复，按 [ACADEMIC_DIAGRAM_STYLE.md](ACADEMIC_DIAGRAM_STYLE.md) §4.1 使用单设计主控、固定 Skill 分工、设计预评估及 `LOCAL_EDIT/LAYOUT_REBUILD/FULL_REDESIGN` 路由：全局布局失败不因科学拓扑未变而持续局部修补；重构隔离旧图坐标，最终核 `GLOBAL_DESIGN_QA` 与科学关系。新图/缓存失效时再核对应真实 Methods/代码。可选 `python -m core.figure_change_scope --before OLD --after NEW` 只读比较规格，绝不自动生成图像、取得绘图授权或省略最终实际渲染检查。

- **仅在用户要求审核/优化工作流时**：可按需读取 [PD-RW-EVAL](evals/EVALUATION_POLICY.md)，先做离线静态/场景合同，可按需使用 [操作型合成测试](evals/OPERATIONAL_TASKS.md)，再按另行授权运行真实 Agent 沙箱测试。评估规则不构成新科研阶段；合成案例不授予下载、SEALED、绘图或正式稿件许可。缺真实执行轨迹、模型遥测与独立科学评价时标 `NOT_MEASURED`，不得声称任务成功率或 Token 下降。

## 3. 任务结束：只更新重要变化

按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)：关键真实事件更新 `RESEARCH_RECORD.md` 首页及末尾对应 EXP/Run；仅当论文内容或科学证据改变时，增量更新 `PAPER_BLUEPRINT.md` 对应 `SEC_ID`。原始日志/数值留原位置，旧项目不强制迁移、不写第三份记忆账本。报告仅需**新增证据 + 当前判断/限制 + 下一合法行动/所需授权**；无信息增量不重复整理。
