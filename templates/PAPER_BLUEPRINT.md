# PAPER_BLUEPRINT｜论文结构与证据规划（非正文）

> 一个文档 H1；**论文一级章节 = H2，必要二级小节 = H3；**Introduction 和通常较短的 Conclusion 默认无 H3**，内部论证规划标签不是投稿正文的小标题**。以下六章适用于**新实证算法/机器学习论文的优先默认框架**；新综述/Perspective 可按 [双文档规则](../DUAL_DOCUMENT_WORKFLOW.md) 选相应蓝图。不因 Agent 偏好或参照论文自行改变六章顺序、数量、名称。只有特殊研究或目标期刊官方要求确有必要时，先提出具体变更、依据及影响，**取得用户明确确认后**才能合并、改名、增删或调序一级章节，以及重大重排二级小节。SEC_ID 保持稳定。仅规划章节要点、证据与缺口，不自动生成正式投稿标题、摘要、正文、图注或图片。

**Word 审阅版格式**：仅在用户要求导出 Word 框架时，按 [PAPER_WORD_STYLE.md](../PAPER_WORD_STYLE.md) 使用 `Title → Heading 1/2/3` 的转换和所有非 Title `0/0 pt` 段距；本 Markdown 仍是唯一框架内容源。

## Planning Snapshot（非论文章节）
- 当前科学问题/工作主题（不是正式投稿标题）：
- 论文类型与目标读者/候选期刊（未核实写 UNKNOWN）：
- 论文结构：新 EMPIRICAL_RESEARCH 默认六章；已批准目录重大变更提案（无/待用户确认/已确认）、必要性与影响：
- 结构例外用户确认原始消息指针（无则 NONE；未经确认禁止应用变更）：
- 目标期刊最新格式/近 1–2 篇同类论文的核实来源（未核实写 UNKNOWN；不得凭范文强制固定目录）：
- **中心论证句（WORKING_THESIS，科学规划而非投稿正文）**：用一句可修订的话写明“重要问题/真实约束 → 我们相对最强近邻新增的知识或能力 → 最重要的有效证据及其边界”；可为机制、能力、测量、负结果或规律，**不强制因果句式**，尚未成立填 `TENTATIVE/UNKNOWN`，不得成为写作授权门槛：
- 中心论证的最强替代解释/反例及下一项能改变判断的证据（指向已有 Claim/Run/文献，避免重复）：
- 主要科学 Claim（C01/CLM-001 等，保持项目已有 ID；不得高估 DEV）：
- 最强最近邻与反解释、重要不利结果：
- 最重要的 1–3 项证据缺口及下一步（重要跨节缺口可选引用 RESEARCH_RECORD.md 中 GAP-001，不复制事实）：
- 科研事实入口：RESEARCH_RECORD.md（最新 EXP/Run 指针）：
- 最后有实质内容变化的来源/事件/日期（未知则 UNKNOWN）：
- 图表/参考文献需求：仅文字说明，不触发任何生成。

**主张层级而非填空式故事（复用下方 Claim–Evidence 索引）**：在 `WORKING_THESIS` 下从合法证据中选一条中心主张，通常只保留 1–3 条直接支持的次级主张（按实际数量，不凑数）。对每条使用下方同一表的 `Claim ID → EXP/Run/真实文献 → 最强反例/负证据 → Section ID`；未支持的写 `TENTATIVE/UNKNOWN`。主要章节围绕中心主张分配必要的读者问题和证据功能，**不把 Run 日志、QA 合格项和检查过程写成论文故事**。新的合法证据可修订或撤回中心主张；不改变已获用户批准的重大章节结构，也不新增 `Claim Lattice` 第二套账本。

## Claim–Evidence–Section Index（非论文章节）
| Claim ID | Section ID（稳定） | 原 EXP/Run/文献来源 | 支持状态 | 反证/局限/下一实验 |
|---|---|---|---|---|
| C01 (TENTATIVE) | SEC-INTRO-02 | NOT_RUN | UNKNOWN | UNKNOWN |

## 1. Introduction
- **投稿正文呈现**：只有一个 `Introduction` 一级标题，其下是衔接自然的连续英文段落；**不输出 1.1/1.2 小节标题，也不把以下内部要点逐项复制为正文 bullet/numbered list**。段落数量与长度依论证需要决定，不套统一配额。
- **内部逻辑路径（仅蓝图规划，不打印为正文小标题）**：研究问题及真实重要性 → 最相关研究及其已解决部分 → 实质性知识缺口与最强替代解释 → 本研究目标/方法的必要性 → 具有真实证据边界的具体贡献。按文献和科学问题合并、拆分或调整顺序；不要求每点恰好一段。
- SEC_ID: SEC-INTRO-01
- 内部规划片段：背景与最近邻论证；**非输出小节**。
- 拟写要点：必要背景、真正相关的近邻原文、现有能力及不足；无原文写 UNKNOWN。
- SEC_ID: SEC-INTRO-02
- 内部规划片段：缺口与研究目标；**非输出小节**。
- 拟写要点：关键未解决问题、方法为何针对该缺口、中心创新/优势和与之对应的 Claim/Run；不足与反证保留 TENTATIVE。
- **重点展开**：核心创新在 Introduction 中说清科学动机、差别与意义；技术实现/公式与全部对照细节放入 Methods/Results，不在引言堆实验日志、硬凑三条 contributions 或重复摘要。
- **篇幅依据**：背景与泛泛应用简写，决定性近邻差额和问题定义详写；不强行让各段等长。

## 2. Related Work
### 2.1 Closest Approaches and Differences
- SEC_ID: SEC-RELATED-01
- 拟写内容：按实质方法分类、比较最直接的研究对象，不堆砌引用。
- 科研/文献依据与缺口：原文/DOI/版本（仅摘要标 UNVERIFIED）；状态 PLANNED。

## 3. Proposed Method
### 3.1 Task and Problem Formulation
- SEC_ID: SEC-METHOD-01
- 拟写内容：任务、预测前合法输入、符号/约束与评估设定。
- 科研/文献依据与缺口：真实 TaskSpec/协议/数据版本；状态 PLANNED。

### 3.2 Core Method and Mechanism
- SEC_ID: SEC-METHOD-02
- 拟写内容：算法框架、核心步骤/公式、关键机制和与最强可比方法的可检验差异。
- 科研/文献依据与缺口：实际代码/协议/消融指针；未验证机制解释标 EXPLORATORY。

### 3.3 Implementation and Reproducibility（按需）
- SEC_ID: SEC-METHOD-03
- 拟写内容：仅规划复现核心方法所必需的实现、训练、复杂度或资源信息；不强制新增实验。
- 科研/文献依据与缺口：代码版本、配置、资源记录及尚未证实的细节；状态 PLANNED。

## 4. Experiments
### 4.1 Evaluation Protocol
- SEC_ID: SEC-RESULT-01
- 拟写内容：数据拆分、独立单位、评估指标、基线、公平对照及不确定性。
- 科研/文献依据与缺口：有效协议与原始 Run；状态 PLANNED。

### 4.2 Main Results and Baseline Comparisons
- SEC_ID: SEC-RESULT-02
- 拟写内容：与核心科学主张匹配的主要结果、公平基线、效应量与不确定性及图表文字需求；不重复讨论段落。
- 科研/文献依据与缺口：EXP/Run 与负结果；未运行部分标 NOT_RUN。

### 4.3 Ablation, Robustness and Boundary Analyses（按主张需要）
- SEC_ID: SEC-RESULT-03
- 拟写内容：决定性消融、竞争解释、限制及重要失败类别。
- 科研/文献依据与缺口：有效实验/待补实验；状态 TENTATIVE。

## 5. Discussion
### 5.1 Interpretation and Limitations
- SEC_ID: SEC-DISCUSSION-01
- 拟写内容：解释主要结果为何出现、竞争性机制与应用意义、不能支持的结论、失败案例和局限；不复写第4章数据。
- 科研/文献依据与缺口：真实 Claim–Evidence、近邻原文；状态 PLANNED。

## 6. Conclusion
- **投稿正文呈现**：通常只有一个 `Conclusion` 一级标题，使用紧凑连贯的正文段落，不为单一小节强加 `6.1`，不罗列空泛贡献清单；特定期刊或已批准结构另按其要求。
- SEC_ID: SEC-CONCLUSION-01
- 内部规划片段：总结与边界；非输出小节。
- 拟写内容：回答研究问题、归纳证据支持的独立贡献与适用边界，适当给出明确后续条件；不引入新结果或新主张。
- 科研/文献依据与缺口：最终可靠的 Claim 与独立证据；状态 PLANNED。

## Planning Change Notes（非论文章节）
- **例外必须先提案、后确认**：确需将 Related Work 并入 Introduction、合并 Experiments 与 Discussion、增设理论章节、调整 Method 的名称，或依期刊强制格式采用 Results → Discussion → Methods 等结构时，先列明「当前结构→建议结构、必要性、官方/科学依据、影响」，获得本项目用户明确确认后才能修改；未确认只在 Planning Snapshot 记录提案，不替换六章。六章内非结构性小节要点和证据可随科研增量更新；重要二级小节删除、合并、跨章搬移或叙事整体重排也须确认，不为填模板而编造证据。
- 仅记录新/失效 EXP/Run/Claim 导致哪些 SEC_ID 的规划改变、理由与来源；不复制实验历史。
- SEC_ID 不随显示章节序号或名称变动而重用；旧项目已有章节编号可继续沿用，不强制迁移。
- 写作锁：严格遵守 [WRITING_GATE.md](../WRITING_GATE.md)；科研成果总结须经用户审查，随后还需明确授权正式写稿；图片另外需要明确绘图请求。`WORKING_THESIS` 是可修改的科学规划，不是写稿许可或已证实结论。
