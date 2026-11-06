# PAPER_BLUEPRINT｜论文结构与证据规划（非正文）

> 一个文档 H1；**论文一级章节 = H2，二级小节 = H3**。仅规划各节准备写什么、对应何种证据和缺口，不自动写正式论文段落、标题、摘要或图注，不自动画图。章节可随科学发展调整，SEC_ID 保持稳定。

## Planning Snapshot（非论文章节）
- 当前科学问题/工作主题（不是正式投稿标题）：
- 论文类型与目标读者/候选期刊（未核实写 UNKNOWN）：
- 主要科学 Claim（C01/CLM-001 等，保持项目已有 ID；不得高估 DEV）：
- 最强最近邻与反解释、重要不利结果：
- 最重要的 1–3 项证据缺口及下一步：
- 科研事实入口：RESEARCH_RECORD.md（最新 EXP/Run 指针）：
- 最后有实质内容变化的来源/事件/日期（未知则 UNKNOWN）：
- 图表/参考文献需求：仅文字说明，不触发任何生成。

## Claim–Evidence–Section Index（非论文章节）
| Claim ID | Section ID（稳定） | 原 EXP/Run/文献来源 | 支持状态 | 反证/局限/下一实验 |
|---|---|---|---|---|
| C01 (TENTATIVE) | SEC-INTRO-02 | NOT_RUN | UNKNOWN | UNKNOWN |

## 1. Introduction
### 1.1 Research Context and Motivation
- SEC_ID: SEC-INTRO-01
- 拟写内容：研究背景、真实重要性、应用问题（要点，不是稿件段落）。
- 科研/文献依据与缺口：具名原文或 UNKNOWN；状态 TENTATIVE。

### 1.2 Gap and Planned Contributions
- SEC_ID: SEC-INTRO-02
- 拟写内容：最近邻的真实局限、关键问题、计划主张的有限贡献。
- 科研/文献依据与缺口：C01 → EXP/Run；最强替代解释与未完成证据；状态 TENTATIVE。

## 2. Related Work
### 2.1 Closest Approaches and Differences
- SEC_ID: SEC-RELATED-01
- 拟写内容：按实质方法分类、比较最直接的研究对象，不堆砌引用。
- 科研/文献依据与缺口：原文/DOI/版本（仅摘要标 UNVERIFIED）；状态 PLANNED。

## 3. Proposed Method or Research Design
### 3.1 Task and Problem Formulation
- SEC_ID: SEC-METHOD-01
- 拟写内容：任务、预测前合法输入、符号/约束与评估设定。
- 科研/文献依据与缺口：真实 TaskSpec/协议/数据版本；状态 PLANNED。

### 3.2 Core Method and Mechanism
- SEC_ID: SEC-METHOD-02
- 拟写内容：算法步骤、关键公式所在位置、与强简单备选的不同可测预言。
- 科研/文献依据与缺口：代码与实际消融指针；未验证解释标 EXPLORATORY。

## 4. Experiments and Results
### 4.1 Evaluation Protocol
- SEC_ID: SEC-RESULT-01
- 拟写内容：数据拆分、独立单位、评估指标、基线、公平对照及不确定性。
- 科研/文献依据与缺口：有效协议与原始 Run；状态 PLANNED。

### 4.2 Main Results
- SEC_ID: SEC-RESULT-02
- 拟写内容：主要科学问题对应的比较、需要的表格与数值证据（仅文字计划）。
- 科研/文献依据与缺口：EXP/Run 与负结果；未运行部分标 NOT_RUN。

### 4.3 Ablation, Boundary or Mechanism Analysis
- SEC_ID: SEC-RESULT-03
- 拟写内容：决定性消融、竞争解释、限制及重要失败类别。
- 科研/文献依据与缺口：有效实验/待补实验；状态 TENTATIVE。

## 5. Discussion
### 5.1 Interpretation and Limitations
- SEC_ID: SEC-DISCUSSION-01
- 拟写内容：证据能支持什么、不能支持什么，适用范围、负结果。
- 科研/文献依据与缺口：真实 Claim–Evidence、近邻原文；状态 PLANNED。

## 6. Conclusion
### 6.1 Supported Takeaways
- SEC_ID: SEC-CONCLUSION-01
- 拟写内容：归纳已受证据支持的贡献及边界，不引入新主张。
- 科研/文献依据与缺口：最终可靠的 Claim 与独立证据；状态 PLANNED。

## Planning Change Notes（非论文章节）
- 仅记录新/失效 EXP/Run/Claim 导致哪些 SEC_ID 的规划改变、理由与来源；不复制实验历史。
- SEC_ID 不随显示章节序号或名称变动而重用；旧项目已有章节编号可继续沿用，不强制迁移。
- 写作锁：成果总结须经用户审查，随后还需明确授权正式写稿；图片另外需要明确绘图请求。
