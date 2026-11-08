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
| Q2 | 整体结构/段落逻辑 | Introduction 是否为无多余子标题/大量条列的连续论证？蓝图要点是否误变成投稿清单？章节间论证、自然衔接及已批准目录是否一致？ |
| Q3 | 方法/可复现性 | 输入输出、合法特征、数据划分、训练/选模/测试隔离、超参、公式/变量、基线和算法实现是否足以理解/复核？ |
| Q4 | 结果/统计/负证据 | 指标、比较对象、独立统计单位、n、分母、置信区间/显著性、多重尝试、消融和失败边界是否正确？ |
| Q5 | 结论力度/算法差异与潜力 | 分别回答已经证实的优势、对最强简单基线及具名近邻的公平差别、可解释机制与有条件技术展望；同步识别 `UNDERCLAIM`/`OVERCLAIM`，不能将 DEV、关联或愿景升级为已确认事实。 |
| Q6 | 图表/公式/正文 | 实际存在的主图及 SI panel、图注、图例、符号、单位、颜色含义、数字、正文交叉引用是否对应？算法/机制图的整体可读性、创新点视觉层级、阅读路径和核心科学关系是否与 Methods/正文一致？局部图元合格但整体误导时不可判图合格。只读审图不授权绘图。 |
| Q7 | 参考文献身份/内容支持 | **逐条**核 DOI/题目/作者/年份/出版源/卷期页/版本/勘误撤稿线索，并检查正文每条重要引用的**具体论断—原文**支持；元数据存在 ≠ 全文已核。 |
| Q8 | 英文可读性 | 语法、术语、时态、连贯的学术段落、长短随内容自然变化、重复、空洞转折与论证节奏；不追求段落字数整齐。 |
| Q9 | 全稿 AI 风格自审与相似性 | 按 HARD / MAJOR / STYLE 对应的真实问题定位聊天痕迹、模板化、重复、空泛、术语漂移和机械衔接；已有风格扫描覆盖率只供定位，需与 SCIENCE 审查分开；不得当作真实 AI 创作比例，也不得将其解释成 AI 创作概率。 |
| Q10 | 投稿/文档交付 | 目标期刊稿型/格式、投稿清单、图表位置、补充材料、声明、Word 字段/样式及真实渲染。 |

## 2. 五轮执行（一个 Agent 按需连续工作，不强制五次确认）

| 轮次 | 范围与行为 | 最小产出 | 参考 Skill/工具（仅已安装且实际可用时调用） |
|---|---|---|---|
| R1 独立审稿 | Q1/Q2/Q5；**只读**，独立识别中心 Claim、问题重要性与最近邻局限、方法必要性、结果如何支撑解释及最强反论点，检查**整篇论证链是否断裂**；不先润色全文。 | 定位清楚的 BLOCKER/MAJOR 问题与受影响章节 | K-Dense `peer-review`、`scholar-evaluation`；Nature-Paper-Skills `manuscript-optimizer` / `review-article-architecture` |
| R2 科学与引用审计 | Q3/Q4/Q6/Q7；逐项配对 Method/Result/Abstract/Discussion、图与 Run；对**全部参考条目**验证身份及元数据，对正文关键引用逐一核原文支持；明确无法核验项。 | `REFERENCE_AUDIT` + Claim–Evidence 差异及需补证项目 | `scientific-critical-thinking`、`stats-reporting-audit`、`citation-verifier`、`claim-source-verification`；可选 PaperQA2 |
| R3 结构与贡献修订 | Q1/Q2/Q5；建立具名最近邻+强简单基线**可比性矩阵**，区分 OBSERVED / INTERPRETATION / HYPOTHESIS / VISION；在获修稿许可后强化可信差额及可证伪展望；重大结构改变仍须用户确认。 | 贡献差额、原句→新句→证据状态；重大结构变化待确认 | `manuscript-optimizer`、`results-section-revision`、`anti-defensive-writing` |
| R4 英语与机械化修订 | Q5/Q8/Q9；全稿风格扫描→定位句段→对问题位置精修→**复扫**；记录范围、规则、被标记词覆盖率与修改前后变化，语义回归仍必需。 | `LANGUAGE_AUDIT` + 已修位置及剩余问题；外部 AI/相似性检测另列 | `scientific-prose-style`、`scientific-writing`；可选 LanguageTool、Vale |
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
- **AI/相似性**：必须给出全稿 AI **风格问题扫描**结果（可按下述 Q9 合同自行量化），但没有外部报告不输出外部“AI率/查重率”；有报告仅记录检测器、版本、日期、命中类型及原始分数，不能将其解释为 AI 写作真实比例；**不得以规避检测器作为改写目标**。
- **停机**：已授权范围内的 BLOCKER/MAJOR 有实质性新修复时复查；否则停止空转。不为“完成五轮”重复读文件、运行多个等价审稿 Agent 或生成多个完整稿件版本。

## 5. 最小交付及 Skill 路由

- **必要时**输出一个 `MANUSCRIPT_QA_REPORT.md`（总体结论、BLOCKER/MAJOR、局部修订与证据、真实验证范围、作者决定项）。同一正文源原位增量修改并保留可回退版本；无需长期保存五份轮次报告。仅用户实际要求的 `.docx`/`.pdf` 才导出。
- `REVIEW_READY` **只表示在已检查范围内可交作者审阅**，不是科学独立确认、Q2 录用潜力实测或正式投稿授权；有关键未核项则 `AUTHOR_ACTION_REQUIRED`，缺少执行证据则 `NOT_VERIFIED`。
- 按需定位公开 Skill 来源：[K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)；[Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)；[PaperQA2](https://github.com/Future-House/paper-qa)；[Anthropic Skills](https://github.com/anthropics/skills)。Skill 名是**能力引用而非已安装声明**；未找到或未安装时使用本合同进行审查，不自动下载安装、不假称调用。
- 合成回归场景见 [evals/manuscript_qa_cases.json](evals/manuscript_qa_cases.json)；只是防回归的**公开参考案例**，静态合同检查不证明真实 Agent 审稿能力、科学正确性或 Token 改善。

## 6. 核心审核合同（论证链、Q9、Q7、Q5）

### Q1/Q2/Q5：整篇论证链审查（复用 R1/R2，不增加第六轮）

仅对核心 Claim 检查 `INTRODUCTION_QUESTION/GAP → METHODS_DESIGN → RESULTS_EVIDENCE → DISCUSSION_INTERPRETATION/ALTERNATIVE → CONCLUSION`：每一跳是否有合法数据或原文支持、是否存在解释越级、近邻不公平比较、遗漏负结果或章节职能错位。把“事实证据不足”与“证据已有但叙事不清”分开处理；科研证据不存在时不能通过改写补出。能力/部署/测量型论文不强制编造因果机制；可检验的未来愿景可以保留但不当成已实现。尽可能由没有直接参与本段写作的执行上下文独立复看受影响 Claim；若只能同一模型/上下文执行，明确 `INDEPENDENCE_NOT_MEASURED`，不得假称多 Agent 同意证明科学正确。问题写入同一 `MANUSCRIPT_QA_REPORT.md`，不新增审核轮次、文档或修改许可。

### Q2/Q5/Q8：连续引言、详略得当与核心贡献深度（沿用 R1/R3/R4）

- **引言的成稿检查**：对于新研究论文、Review 或 Perspective，Introduction 默认只有一个一级标题，后接自然连贯的英文段落；`1.1 Background`、`1.2 Challenges`、`1.3 Contributions` 等通常是**将内部蓝图误作论文正文**，应判 `MAJOR` 并给出原文位置和段落化改写方案；Introduction 内大面积 bullets/numbered lists、文献逐篇罗列、`Our contributions are as follows:` 后无实质推理也应审查。目标刊物、特殊文章类型或该项目用户已批准的例外不得擅自拆除；**审稿发现问题不等于获得改稿权限**，重大已批准结构变更仍先取得用户确认。
- **科学问题的递进性**：反向阅读段落主张，检查读者能否从“为何重要→已有解决方案的边界→具体未解问题→为什么采用本研究设计→实际贡献”推导出论文目标。不要把 Introduction 改成孤立的背景、挑战、贡献三张清单，也不要以文献数量或引言长度取代逻辑完整性。引言已交代的创新点应在 Methods/Results 形成充分的实质解释与支持。
- **详略分配审查**：不是检测长句率或给每段统一字数，而要核**科学价值/新颖差额/理解难度/证据支撑与实际篇幅是否相称**。逐项检查：核心机制或新能力是否只占一个概括段、普通技术和背景是否反而占多数；最强相关近邻的区别是否具体、条件是否公平；方法步骤/信息可见性/设计动机是否足够复现和理解；最重要结果是否给比较、量级、统计单位、负结果与边界；Discussion 是否解释原因和意义，而非照搬 Results。若核心贡献`UNDERDEVELOPED`、无关背景`OVEREXPANDED`、多段`REPETITIVE_TEMPLATE`，给出**位置、需要补充的具体科学内容和已有证据指针**，不能仅要求“增加字数”或捏造实验。
- **编辑深度先于机械润色**：将问题分为 `CLAIM_OR_EVIDENCE_BLOCKER`（停止对相关结论强化）／`NARRATIVE_RESTRUCTURE`（段落论证顺序）／`SUBSTANTIVE_EXPANSION`（已有证据对应的重点内容未展开）／`COMPRESSION`（冗余背景/重复）／`PROSE_ONLY`（句子清晰度）。在获局部修稿权限时先解决科学与信息结构，再润色语句；相关重要段落可以完整重写，**“最小修改”意为最小有必要的科学影响范围，不是每段只能换几个词**。改写后复核原始事实、Claim 级别和原定目录。
- **轻量机器辅助只做定位**：可选 `python -m core.manuscript_flow MANUSCRIPT_TEXT.md` 只读提示引言标题、列表及段落词数分布；机器不理解创新性，不把等长/不等长段落当 PASS/FAIL、不能替代逐段科学审查。对于 Word 使用 `.docx` 同一只读工具；无真实稿件或未授权审核时不调用。
- **按文章类型适配**：Review/Perspective 的内部小节可按范围和论证组织，目标期刊格式优先；不能一律把整篇综述的分节删掉。上述无子标题引言是各类新论文的共同默认，任何具体已批准结构仍遵守原门禁。

### Q8/Q9：全文括号与分点式正文零容忍检查（沿用 R4）

- **正式稿件叙述性正文不得分点作答**：从 Abstract 至 Conclusion（包括 Introduction、Related Work、Methods、Results、Discussion）逐章检查 `▪`、`•`、`-`、`*`、`①②③`、`1. 2. 3.` 等列表式段落，以及没有可见列表符号但仍像 AI 回答提纲一样并列堆砌的段落；发现则记录原文位置、段落之间缺失的论证关系，定为至少 `MAJOR` 写作问题。审稿报告本身可列清单，但**论文正文不可以**。算法伪代码、形式化定理/定义、公式、表格、正式参考文献清单、期刊要求的结构化声明除外。
- **减少非必要括号**：检查连续括注、嵌套括注、括号解释代替完整句子、重复引入同一缩写及高密度旁注。能融入叙述的一律改写为完整句子；不要凭括号数量设置任意阈值，也不误报 `IMU` 等术语首次释义、作者—年份文献引用、公式/函数记号、图中子图标记或必要的统计信息。关键科学限定条件不能因删括号而消失。
- **真正改写而非删符号**：修稿许可已核实后，将违规列表及可删除旁注改为**连贯的、长短由论证决定的学术段落**；必要时整段重写，保持所有来源和 Claim、结果数值、负证据及方法细节。每处问题先定位，再修复，再通读受影响相邻段落与科学语义；无改稿权限时只报告，不自行变更既有稿件。既有格式例外或目标期刊强制要求需说明适用依据。

### Q2/Q5/Q8/Q9：反模板化三层验收（复用 R1/R3/R4/R5，不新增 Agent）

以 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) 的 **HARD / MAJOR / STYLE** 合同为唯一写作规则源。**HARD 不允许进入可投稿终稿，MAJOR 依文本和来源实质审核，STYLE 只做有依据的局部改进**；不设任何禁词数量、破折号百分比、句长方差、AI 分数或改写配额。审查结论必须先区分“缺少证据”与“已有证据但表达不足”。

| 级别 | 全文覆盖的具体检查项 | 处理与复核 |
|---|---|---|
| **HARD 格式/完整性** | 叙述正文项目符号、编号回答、粗体独立标签、`Challenge/Solution/Key Insight:` 伪小节、Markdown 原样痕迹、投稿版 `TODO/[REF]/[EQ]/[FIG]/MISSING_FIGURE`、聊天/审计/Agent 残留；Term/Claim/图表编号与有效来源不一致。 | 报位置和上下文；在授权范围内重写为自然学术叙述、补齐真实引用/工件或标 `AUTHOR_ACTION_REQUIRED`，未解决时不能 `REVIEW_READY`。工作草稿有合法证据指针的占位不得误判为已投稿件，不能因此自动画图。 |
| **HARD 科学真实性** | 假 DOI/引文、无来源的结果/统计显著性/独立确认/泛化/首创，回避负结果，将相关性冒充因果，方法/公式与代码或数据输入不一致，偷换评估条件，关键结果在 Abstract/Results/Conclusion 中不一致。 | 关联 Q1/Q3/Q4/Q5/Q7 及原始 Run/文献；`BLOCKER` 优先，不因英语流畅或自动格式扫描通过而放行。需要新实验证据则报告科学缺口，不授权自行运行。 |
| **MAJOR 论证结构** | 引言宏观空话、近邻“已有局限”不具体、Related Work 逐篇流水账/无公平比较、Methods 核心步骤和合法信息流描述不足、Results 按图号复述不说明量级与条件、Discussion 只重复结果或过度乐观、Conclusion 超出已证范围；段落间可随意交换或每段重启/总结。 | 用**反向提纲：该段的中心主张→真正提供的证据/推理→对下段的必要性**判断，不用固定段长/章节段数；定位 `UNDERDEVELOPED`、`OVEREXPANDED`、`REPETITIVE_TEMPLATE`，在修稿授权内实质扩写/压缩/重排所需局部；重大已批准目录变更仍先报用户确认。 |
| **MAJOR 信息密度/准确性** | 对核心创新只给形容词、没有和真实最近邻/简单基线的区别；论文各章不断重复同一贡献；图注含无据宣传、正文/公式/术语断链、同一模块随意换名；所有失败被包装为积极结果。 | 明确缺少的定义、公式、对照或真实结果指针；能从已有证据补写则补写，不能则收窄、保留 UNKNOWN 或提出待授权事项，不靠同义词/字数制造新内容。 |
| **STYLE 弱线索** | 高频 `delve/underscore/pivotal/intricate/holistic`、`plays a crucial role`、`It is worth noting`、`paves the way`、反复 `Moreover/By leveraging/Not only...but also...`、空洞三连词、破折号/斜杠/括注/名词化/被动句机械堆叠。 | 仅当存在重复、无信息、假因果或妨碍阅读时修；不得禁用合法专业词、结构性转折或主动/被动语态；特殊领域、数学、术语首次缩写、引用、子图等合理例外必须保留。 |

**逐段与跨章检查必须抓具体证据**：至少对中心问题与最重要贡献核“问题为何重要→具名近邻真不足→设计/方法为何必要→合法可比较的主要结果/反例→结论力度与适用范围”；检查反事实或竞争解释是否被误写为已证明机制。判断局部有问题时给出原文位置、科学影响、原始证据指针、应补充或删除的**具体信息**，而不是“更像人类写作”的空泛建议。

**审查动作与通过条件**：发现 HARD 必须处理或明确阻止 `REVIEW_READY`；实质性 MAJOR 在作者批准的修订范围内解决并保留语义回归；STYLE 可保留合理用法，不必消除全部规则命中。报告仅在原有 `MANUSCRIPT_QA_REPORT.md` 加入相关定位条目，按 `HARD / MAJOR / STYLE | 位置 | 原文 | 依据/例外 | 处理/待办 | 复核结果` 记录，已修复问题无需重复输出长篇差异清单。修订后只回查受影响段落、上下游重要主张/引用/图表、相邻段衔接及最终导出；审查权限不等于修稿权限。

**边界**：只审稿时不得自动改写；修稿时不生成未经用户批准的实验、图片或非公开材料上传。AI 风格扫描仅用于**人工定位**；不允许以特定检测器得分、所谓真实 AI 率或词频阈值宣称稿件科学质量。新文件 `PAPER_BLUEPRINT` 及科研记录仍可使用内部项目符号，审稿报告也可使用表格/清单，与投稿正文格式禁止清单不矛盾。

### Q3/Q4/R4：证据来源绑定与修稿语义回归（原有轮次内执行）

**宣称 independent / confirmed / held-out 时必须核真实来源**：从真实稿件对核心的独立确认断言逐一追到 `claim_id → evidence_ref → split_id → source_role → selection_history → frozen_protocol`，同源开发/验证数据、用于选题/调参的切片或与开发组重叠的样本**不能**因为改名成 TEST 而充当独立确认。没有可核对的 `split_id`（或理论证明的具体假设/证明指针）就标 `SOURCE_NOT_VERIFIED`，不能声称已通过；**不能机械判断所有包含“independent”的英文句子都是统计确认**，需审阅上下文与主张类型。核验原始 Run/冻结协议/权限和实际选择史，自动脚本只能检查用户显式提供的关联元数据。

**重点句段的语义变更提示**：可按需在已授权正文精修前后运行 `python -m core.manuscript_claim_guard compare BEFORE.md AFTER.md --output guard.json`，定位变化中的数字、否定词、因果语言、数据角色及显著性表述；合法科学更正可保留但必须核原始证据与修订依据。需要核独立确认措辞时，先从合法记录准备**已经覆盖关键断言**的简短 JSON，运行 `python -m core.manuscript_claim_guard provenance CLAIM_SOURCES.json --output provenance.json`；格式见脚本文档。工具不读取 SEALED，不发送网络请求，不会证实元数据真实性、所有正文 Claim 已覆盖或科学因果正确；其 `NO_HEURISTIC_ALERT_NOT_PROOF`、`DECLARED_METADATA_NO_CONFLICT_NOT_PROOF` 均不是科学 PASS。**原有 G2 / Q7 / 十域审查保持**，新增检测仅针对有变更或确实需要验证的关键句，警报须人工核对，避免全稿重写式循环。

### Q9：全稿语言自审——定位、修复、复检

1. 对本轮实际可访问的**完整正文**执行一次有界扫描（排除 References、代码块、公式/元数据及图表源文件）；识别模板化开场、无信息修饰、重复小结、机械连接、过度保守、冗长、突然的风格跳变及缺实质主张的陈述。可使用 `python -m core.manuscript_style scan MANUSCRIPT_TEXT.md --output style_before.json`；对 Word 可读文稿也可用该工具的 `.docx` 文本提取。该工具只是**启发式风格定位器**；不可替代上下文语言审读，PDF 需先合法提取可核对文本。
2. 在 `LANGUAGE_AUDIT` 中记录：稿件版本、检查范围、扫描规则/工具版本、总词数、被标记句段/段落位置与理由、`style_flagged_word_coverage_percent`。其计算是**至少被一个规则标记的句子中词数÷被扫描正文词数**（同一词不重复计数）；**不是 AI 作者概率，也不叫作真实 AI 率**。扫描局限（如中英文混排、参考文献检测、DOCX 解析不完整）必须说明。
3. 获用户修稿许可后只优先修复确有问题的段落；给出 `位置 | 原句 | 新句 | 理由 | Claim/数字/引用是否保持`。不要为了降低数字机械替换同义词、扭曲论文特点或改写可信结果。用相同范围/规则复检，报告前后指标及仍有争议的标记；**覆盖率低不代表论文真实或专业，也不设硬性“低于x%”门槛**。
4. 如用户提供合法外部 AI/相似性报告，另外逐项解释高亮位置与来源差异；仅引用真实检测器输出，不自行捏造分数，也不假设其能识别作者身份。无外部报告标 `EXTERNAL_AI_RATE_NOT_MEASURED`，仍必须完成上述内部风格审查。

### Q7：参考文献逐条双层验证 + 论断支持

1. **完整性与数量边界**：从真实稿件提取文末参考文献和正文引用，检查总数、连续编号/author-year、双向一致性、重复条目及未消解的 `[REF:...]` 占位；提取/排序不完整则 `REFERENCE_SET_INCOMPLETE`，不能声称逐条通过。按 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) 的**约30篇软目标**记录已验证真实条目数量、未核/占位数量和关键来源缺口；**篇数少不等于审核 FAIL，绝不为补数量生成不存在或无关文献**。综述/Perspective 及期刊要求按实际适配。
2. **每条身份和书目信息**：对所有参考条目逐一验证存在性与题名、作者/顺序、年份、出版物、卷期、页码/文章号、DOI（若适用）、正式发表/预印本版本。优先 Crossref、DataCite、出版商或官方数据库做精确匹配；可按需复用 `core.literature.verify_reference_metadata` 与 `python -m core.reference_audit refs.json --output refs_check.json --allow-network` 的**只查 DOI 元数据**能力。输入 JSON 为 `{"expected_count": N, "references": [{"ref_id":"R1","doi":"10...","title":"...","year":2026,"first_author":"..."}]}`；`expected_count` 须来自稿件独立计数。`--allow-network` 只能在本轮获准做公开 DOI 查询时使用，仅发送 DOI，不发送未公开正文。查不到 DOI 不能推断文献不存在；没有 DOI 应从官方书目来源人工核验。检测到撤稿、勘误或版本异常应复核原出版商记录；服务未返回警报 **≠** 确认不存在撤稿。
3. **每个关键引文的内容支持**：对于创新/首创、具名近邻差额、方法依据、关键数字、机制和重要争议，定位原文相关位置并判断 `SUPPORTS / PARTIAL / CONTRADICTS / SOURCE_ACCESS_LIMITED / NOT_CHECKED`。即便返回 `METADATA_MATCH` 也仅意味着**给定的书目信息字段与 DOI 元数据匹配**；`METADATA_PARTIAL` 必须查缺项，`METADATA_MISMATCH` 必须修正，二者不能冒充逐条完成。批量核验的 `DOI_METADATA_AUDITED_NOT_CLAIMS` 不等于所有条目通过；须查看 `metadata_integrity`、`duplicate_doi_count`、`duplicate_ref_id_count` 和各条 `status`。出现 `ISSUES_REQUIRE_MANUAL_REVIEW` 必须追查重复条目或匹配缺失；即使 `ALL_MATCHED_NOT_CLAIM_VERIFIED` 也没有核验论文对引文的使用。**元数据校验通过不得自动标 `SUPPORTS`**；只有摘要时只能支持摘要明确表达的有限结论，不得声称核验全文。
4. 最小记录 `REF_ID | identity+metadata status | DOI/official source+date | corrections/retractions check | citing Claim/section | source passage/location+support status | action`；元数据错必须更正，来源不支持时须更换可信来源或修改主张。所有条目要求**被逐条审查**，不是强迫每条都核验成功；无法访问时如实留 `UNVERIFIED`，不得让关键引用带着未解决的错误进入 `REVIEW_READY`。
5. 使用网络检索仅在真实授权和合法来源范围内进行；不外传未公开稿件、原始数据或受许可限制的全文。不要用自动生成的 DOI/[1] 填补空缺，优先复用已有已核证据。

### Q5：算法差别与潜力表达

1. 复用现有 `CLAIM_EVIDENCE_MAP`，对**最相关 1–3 项具名近邻**及一个有意义的强简单基线建立轻量比较：`TASK | INPUT/LABEL/INFORMATION_BUDGET | SPLIT/PROTOCOL | METHOD_DIFFERENCE | METRIC/EFFECT+UNCERTAINTY | DEPLOYMENT_COST | FAIRNESS_STATUS | SOURCE`。比较标 `DIRECT_COMPARABLE / CONTEXT_ONLY / NOT_COMPARABLE`；后两者不得用数字并排冒充直接胜利。
2. 对中心贡献明确写出 `已观测结果（OBSERVED）→ 合理解释（INTERPRETATION）→ 可证伪机制/假设（HYPOTHESIS）→ 有条件的未来能力/应用（VISION）`，不要求每篇都具备全部层次。可在 Discussion 展开真实技术潜力，说明促成它的已知机制/能力及必要的新测试；**愿景无需伪造实验，但不得宣称已经完成部署或验证**。
3. 审查 `UNDERCLAIM`（真实增益、负结果蕴含的边界、资源/在线条件下的新能力被弱化）与 `OVERCLAIM`（不可比 SOTA、因果推断、独立确认或跨域泛化被夸大）。凡增强力度记录 `原句→新句→数据/文献指针→证据层级`；若缺公平对照或关键独立证据，标 `EVIDENCE_GAP`，不靠修辞补证。
4. 综述/Perspective 按“已有证据综合—争议和反解释—研究框架—可检验议程”处理，不强制套算法性能表；适用范围应由论文类型决定。

**对照文献覆盖按科学主张扩展，不按 Q1/Q2 强制固定方法数量**：上面的 1–3 项是初次最近邻可比性矩阵的**起点**，不是整篇 Related Work 或投稿审稿的引用上限。若已有不同范式的实质竞争者、任务定义或评价标准冲突，必须覆盖**所有会改变核心新意/公平性判断的相关重要路线**，可多于 3 项；不能因目标 Q1 而硬凑 5 个无意义或不可比方法，也不能因 Q2 就漏掉第 4 个真正关键近邻。比较缺乏原文或相同协议时标 `CONTEXT_ONLY/NOT_COMPARABLE`，不能制造 SOTA 优势。参考文献数量仍依 [MANUSCRIPT_WRITING.md](MANUSCRIPT_WRITING.md) **约30篇软目标、宁少勿假**，与直接方法比较数量是不同概念。

**QA 深度跟随作者实际任务**：用户要求审读未完成的章节/初稿时，优先运行 R1 的核心科学论证与受影响 Q2/Q5/Q7，必要时 R2 核实验/引用；**完整稿件投稿前**再执行适用的全部十域和最终版式审核。已有完整稿且用户明确要求完整审核时不得以“初稿”名义逃避关键科学错误、数据/引用真实性检查。无改稿授权时只报告问题，不自动重写、重排或生成新图。

### R5 最终闭环与可接受状态

- `LANGUAGE_AUDIT`：全稿扫描范围与覆盖率、重点段落改前/改后、复扫、残余问题；对长句与语言流畅度保留人工判断。
- `REFERENCE_AUDIT`：所有条目核对覆盖情况、错误/缺失、关键 Claim 的原文支持与待核列表；**不能以 Crossref 返回条目数量代替文献通过率**。
- `CLAIM_CONTRIBUTION_AUDIT`：中心主张、最近邻可比性、已证实优势、强弱表述修订、明确的前瞻性路线及未验证条件。
- 三者合并到**一个** `MANUSCRIPT_QA_REPORT.md`，不额外生成三个长期文档。先 G1 科学和引文、再 G2 语义回归、最后 G3 格式与交付；关键引文冲突或科学漂移仍是 BLOCKER。若确实无法获取原文，显式 `AUTHOR_ACTION_REQUIRED` 而非虚假 PASS。
