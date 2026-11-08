# MANUSCRIPT_QA｜完整论文独立审核、局部修改与投稿前验收

> **定位**：这是 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) R4 之后的完整稿件 QA 合同，不是新的科研阶段或写作许可。前者负责**生成过程中的增量 M5/M6 审校**；本文件负责**对已有完整稿件进行独立复核、修订及回归验证**。项目仍遵守 [WORKFLOW.md](WORKFLOW.md)、[WRITING_GATE.md](WRITING_GATE.md)、[DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)、[FIGURE_POLICY.md](FIGURE_POLICY.md) 及 [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md)。无完整稿件时不强制运行。

## 0. 入口、授权与来源

- **触发**：已有经许可完成的稿件；或用户明确要求审核其提供的既有论文。只读审查不隐含正文生成/改写授权；**修改只在用户明确要求修改时进行**。审核权限不授予新稿件写作、重大已批准结构调整、实际绘图、训练、额外下载、SEALED/CONFIRMATION 访问、外传或投稿。研究总结审查与写作许可仍由 `WRITING_GATE.md` 决定。
- **单一可编辑稿件源**：优先现有 `MANUSCRIPT_TEXT.md` 或用户指定原稿；Word/PDF 是来源或按需导出，不与 Markdown 建立相互竞争的完整版。保留修改前可恢复版本；不因审核重建论文。
- **按需加载证据**：已有 `RESEARCH_RECORD.md` 当前快照、`PAPER_BLUEPRINT.md` 相关 SEC_ID、合法 Run/协议/图表源数据、真实 Methods、已提供的文献原文及目标期刊指南。只读审核完整文本；深查仅访问涉及问题的证据，不全量扫描历史数据。缺文件标 `NOT_AVAILABLE`，不得凭摘要或模型记忆补造。
- **可信度与冲突**：原始合法数据/有效 Run/原始文献及授权 > 经核验的研究记录 > 稿件表述 > AI 提议。冲突标 `SOURCE_CONFLICT`；DEV、VAL、合法独立确认、外部验证严格区分，不能在修稿时提升证据级别。
- **文章类型**：`EMPIRICAL_RESEARCH` 使用 Method↔Result↔图表/统计闭环；`CRITICAL_REVIEW` 审证据覆盖、分歧解释、选文准则、原创综合；`PERSPECTIVE` 审立场、最强反论点、可证伪设想与条件。不能向综述强加实验数据，亦不能把未来倡议写成已完成实验。

## 1. 十个检查域（按需适配稿件类型，不是十个 Agent）

| ID | 检查域 | 核查问题 |
|---|---|---|
| Q1 | 科研定位/贡献/近邻 | 中心问题和新增能力/机制/规律清楚吗？与具名强近邻、合理简单基线的差额是否有据？综述是否形成新综合？ |
| Q2 | 整体结构/段落逻辑 | 标题—摘要—引言—方法—结果—讨论—结论的任务分工、段落论点、过渡、重复及已批准目录是否一致？ |
| Q3 | 方法/可复现性 | 输入输出、合法特征、数据划分、训练/选模/测试隔离、超参、公式/变量、基线和算法实现是否足以理解/复核？ |
| Q4 | 结果/统计/负证据 | 指标、比较对象、独立统计单位、n、分母、置信区间/显著性、多重尝试、消融和失败边界是否正确？ |
| Q5 | 结论力度/解释边界 | 已证实结果是否过度保守？是否把相关写成因果、DEV 写成确认、条件性优势写成普遍最优？ |
| Q6 | 图表/公式/正文 | 实际存在的主图及 SI panel、图注、图例、符号、单位、颜色含义、数字、正文交叉引用是否对应？ |
| Q7 | 引文/相关工作 | DOI/版本/作者年份可信？引用的**具体段落**支持当前句子吗？无法读原文不声称已核验。 |
| Q8 | 英文可读性 | 语法、术语、时态、段落主句、长句、重复、学术表达和自然的论证节奏。 |
| Q9 | AI 痕迹/文本相似 | 机械化句式、空泛总结、重复/近似段落、可疑未标引用与 AI 使用披露；**不将 AI 检测器数值当事实**。 |
| Q10 | 投稿/文档交付 | 目标期刊稿型/格式、投稿清单、图表位置、补充材料、声明、Word 字段/样式及真实渲染。 |

## 2. 五轮执行（一个 Agent 按需连续工作，不强制五次确认）

| 轮次 | 范围与行为 | 最小产出 | 参考 Skill/工具（仅已安装且实际可用时调用） |
|---|---|---|---|
| R1 独立审稿 | Q1/Q2/Q5；**只读**，独立给出中心 Claim、反解释、审稿风险和问题优先级；不先润色全文。 | 定位清楚的 BLOCKER/MAJOR 问题与受影响章节 | K-Dense `peer-review`、`scholar-evaluation`；Nature-Paper-Skills `manuscript-optimizer` / `review-article-architecture` |
| R2 科学与引用审计 | Q3/Q4/Q6/Q7；逐项配对 Method/Result/Abstract/Discussion、数值、统计、图、原始 Run 与被引用原文；仅核既有合法证据。 | Claim–Evidence 差异及需作者补证项目 | `scientific-critical-thinking`、`stats-reporting-audit`、`citation-verifier`、`claim-source-verification`；可选 PaperQA2 |
| R3 结构与贡献修订 | Q1/Q2/Q5；**仅在已获修稿授权且 R1/R2 定位后**修改受影响段落；强化已证实贡献、修复信息结构，不能擅自改用户已批准目录。 | 可追溯局部修改；重大结构变化仅给出建议待确认 | `manuscript-optimizer`、`results-section-revision`、`anti-defensive-writing` |
| R4 英语与机械化修订 | Q5/Q8/Q9；科学主张已稳定后进行局部语言精修和重复表达处理；对修改位置做语义/数字对比。 | 修改片段与语义保持检查；若有外部查重报告则逐项解释命中 | `scientific-prose-style`、`scientific-writing`；可选 LanguageTool、Vale |
| R5 投稿预检/回归 | Q1–Q10 受影响项；复核修订后 Claim、数字、引用、图表、文章类型和期刊要求；有 Word/PDF 交付请求时导出并**实际渲染**。 | `REVIEW_READY` / `AUTHOR_ACTION_REQUIRED` / `NOT_VERIFIED`，以及真实检查范围 | `submission-audit`、`peer-review`、`docx`/`pdf`；可选 MarkItDown |

依赖顺序为 **R1→R2→R3→R4→R5**，但科研完整性检查贯穿所有轮次。新发现科学错误立即返回受影响的 R2/R3；局部修订只复核对应 Claim、上下游章节与导出页，不作无限整篇迭代。**审查请求**可停在 R1/R2，**审查并修改**可连续进行 R1–R5；没有真实文稿或无修改授权时不得以“工作流要求”为由生成稿件。

## 3. Claim Strength Calibration：强而不虚

| 类型 | 判断与措辞 |
|---|---|
| `OBSERVED` | 来自有效直接证据：陈述 `shows / increased / was higher` 等明确事实，携带具体比较、metric、样本/条件；无谓 `may potentially` 应删除。 |
| `INTERPRETATION` | 与证据相符的解释，表达意义和适用边界，不伪装直接测量。 |
| `HYPOTHESIS` | 未检验的机制/因果/预测可清晰提出，但须区别于实证观察，并指出可反驳路径。 |
| `VISION` | 综述/Perspective 可提出大胆、有条件的方向与倡议；不可当作已实现功能。 |
| `UNVERIFIED` | 找不到可信来源、近邻或证据冲突；定位并补证/缩窄/保留待办，不转换为确定性结论。 |

**双向审查**：同时找 `OVERCLAIM` 与 `UNDERCLAIM`。禁止把无统计支持的趋势称“显著”，也禁止将可信的负结果、边界规律和量化增益一律写成“可能略有帮助”。如果科学解释存在多种可能，可明确主观察、给出最合理的解释与反解释，避免空洞的免责声明。每次升降主张力度须有`原句→新句→证据状态`，并核对修改前后的比较方向、数据角色及因果语义。

## 4. 问题定位、最小修改和质量门禁

- **优先级**：`BLOCKER` = 无效/冲突/无来源的关键事实、评价泄漏、科研伦理或越权；`MAJOR` = 实质方法、结构、主张力度或引用支持问题；`MINOR` = 局部术语/语法/衔接；`STYLE` = 纯格式。不能用加权总分抵消 BLOCKER。`SOURCE_UNVERIFIED`、`NOT_MEASURED`、`USER_DECISION` 不得伪装成 PASS。
- **最小问题记录**：`ID | Q域 | 位置(章节/段落/句或图) | 严重度 | 原文/当前主张 | 真实证据指针及级别 | 建议修订 | 状态`。状态仅 `OPEN / FIXED / DEFERRED / USER_DECISION / UNVERIFIED`。报告可按需单文件 `MANUSCRIPT_QA_REPORT.md`，只记本次审核结果，**不是第三份科研记录**；重大科学新证据按原双文件规则增量更新。
- **G1 科学有效性**：所有进入确定性结论的关键 Claim 对应合法有效证据；无未处置的关键 BLOCKER；DEV/VAL/CONFIRMATION 不错置。证据不足时允许其他可信章节继续修改，但整稿不可标科学通过。
- **G2 语义回归**：修订前后核对每个改变的数字/单位/指标/分母/比较方向/数据角色/时序/因果/限定条件及图表引用。任何未经证据支持的升级或丢失限制必须回退并修复。
- **G3 投稿与交付**：只在用户要求 Word/PDF 时按 `PAPER_WORD_STYLE.md`/目标期刊模板生成，核验字体、标题、零段距、编号、图表引用及**真实渲染**；无法打开渲染则标 `RENDER_NOT_VERIFIED`，不能宣称外观通过。实际投稿还需要作者独立确认署名/贡献/伦理/利益冲突/AI 使用声明等。
- **AI/相似性**：无外部检测报告不输出“AI率/查重率”；有报告只说明检测机构、版本、日期、命中类型与实际证据，不能以单一百分比判定 AI 写作或原创性；**不得以规避检测器作为改写目标**。
- **停机**：已授权范围内的 BLOCKER/MAJOR 有实质性新修复时复查；否则停止空转。不为“完成五轮”重复读文件、运行多个等价审稿 Agent 或生成多个完整稿件版本。

## 5. 最小交付及 Skill 路由

- **必要时**输出一个 `MANUSCRIPT_QA_REPORT.md`（总体结论、BLOCKER/MAJOR、局部修订与证据、真实验证范围、作者决定项）。同一正文源原位增量修改并保留可回退版本；无需长期保存五份轮次报告。仅用户实际要求的 `.docx`/`.pdf` 才导出。
- `REVIEW_READY` **只表示在已检查范围内可交作者审阅**，不是科学独立确认、Q2 录用潜力实测或正式投稿授权；有关键未核项则 `AUTHOR_ACTION_REQUIRED`，缺少执行证据则 `NOT_VERIFIED`。
- 按需定位公开 Skill 来源：[K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)；[Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)；[PaperQA2](https://github.com/Future-House/paper-qa)；[Anthropic Skills](https://github.com/anthropics/skills)。Skill 名是**能力引用而非已安装声明**；未找到或未安装时使用本合同进行审查，不自动下载安装、不假称调用。
- 合成回归场景见 [evals/manuscript_qa_cases.json](evals/manuscript_qa_cases.json)；只是防回归的**公开参考案例**，静态合同检查不证明真实 Agent 审稿能力、科学正确性或 Token 改善。
