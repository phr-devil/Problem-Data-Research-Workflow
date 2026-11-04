# Science Result Harvest & Contribution Amplification｜现有成果的科学信息挖掘与贡献充分提炼

> **现有活动04↔05及活动06/科研成果总结的按需动作，不增加阶段、权限门禁或稿件写作流程。** 目标是避免已经获得可信Run却只报告总体指标，以及已有真实创新却因未形成明确、可验证的科学主张而被低估。用户未审查科研成果总结并另行授权写稿时，保持[WRITING_GATE.md](WRITING_GATE.md)的`WRITING_LOCKED`；本文的输出是**科研证据记录**，不是论文故事、稿件图文、提纲、摘要、投稿包装或期刊录用保证。Q2+潜力按[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)另评。

## 一、两种损失必须分开识别

1. **`MISSED_SCIENTIFIC_INFORMATION`（未挖出）**：现有Run、原始逐样本预测、负结果、组级误差、不同K/设备/时间/条件与成本记录中，是否存在尚未记录的**真实、可证伪、具有重要性**的边界、能力、交互、资源权衡或失败机制线索？先找线索，不许预设一定存在新规律。
2. **`UNDERARTICULATED_CONTRIBUTION`（有证据但未充分说明）**：已有方法/结果是否相对**具名最近邻原文**增加了重要知识或能力，却只总结成总体F1、堆叠模块或“优于三种模型”？证据足够时修复科研贡献的**主张—证据映射**，不需因表述不足盲目追加GPU。
3. **`EVIDENCE_GAP`（确实证据不足）**：声称某机制/因果解释、跨域适用性、稳定规律却只有DEV单次切片/模型归因/代理真值；必须标不确定并给出**最小区分性确认**，不能靠更好语言提升论文评级。
4. **`NO_EXTRA_VALUE_FOUND`（确实没有新知识）**：真实结果有限且新近邻差额不足，保留真实工程、负证据及后续科研资产；不要编造高档创新。

## 二、恰当触发，不要求每轮重扫

**按需触发**：首个有意义且可信的Run/关键负结果、首次得到可比较的多条件预测、复杂机制与Champion差异出现、拟大规模追加实验或HOLD/结束、科研成果总结前。**若当前Run/协议/分组/原文近邻/选择史没有实质新变化，直接复用上次Harvest引用，避免循环检查。** 已有明确高价值决定性实验在运行时，不中断科研流程再做全面复盘。INVALID/泄漏/评价错误先隔离无效结果；只对其他合法工件挖掘。

### A. 既有资产“科学信息收获”——先只读

复用`BEST_VALID_RUN`、同K/同合法信息强简单基线、原始预测或可信组级指标、NEGATIVE_RUNS、任务搜索史、变量交叉/混杂、实际成本（未测则UNKNOWN）。按照**已有科学问题**挑1–2个预期重要的条件轴，不在几十/几百切片中挑出显著的幸运组。记录未支持正向Claim的反例和整个比较范围。

按需检查下列互补机会，不要强制每条都做：
- **能力与误差结构**：总体增益是否由真实独立群体/特定部署条件驱动？paired effect方向与幅度是否改变？分母、缺失/覆盖和标签是否一致？在某条件下相反的结果也是科学线索。
- **规律/失效边界**：位置、设备、人、时间、浓度、任务难度、环境或交互是否出现可反驳的条件性规律？多因素是否混杂、独立n是否足够？**相关性/模型表现差异不是因果识别**。
- **代价与能力**：合法标签预算K、计算/标定/能耗/延迟是否形成真实可复核的性能—成本权衡？不同K不能被称作同信息算法比较。
- **新机制或反解释**：真实正控/消融/误差模式是否支持某种新归纳偏置、信息路径或可靠性决策？SHAP/归因/Attention仅提供假说线索，不是因果机制证明。
- **负结果与复用价值**：失败的高难机制是否排除了某种前提，或提供新的信息不可辨识/部署下界？`NOT_RUN`不得写成负结果；一次负Pilot不否决全部Task。

**低成本工具**：可在真实用户授权的DEV/公开元数据范围内，用`python -m core.result_harvest --packet DEV_EVIDENCE.json`对**已整理、可信、同协议、同metric的成对组级观察**做纯只读描述性盘点。该工具的所有条件差异均为`EXPLORATORY`，不验来源、不评显著性、不证明因果/新颖性/Q2；对无真实Run/无法配对的任务不要伪造示例值。图像/理论研究改为相应可审核证据，无需凑输入。

### B. 横向比较候选贡献，再选主张

最多少量、通常1–3个**真正不同**的`SCIENTIFIC_CLAIM_CANDIDATE`，不是三个不同写法的同一创新。每个注明：

`CLAIM_TYPE(capability/mechanism/boundary/cost/measurement/negative) | REAL_WORLD_IMPORTANCE | OBSERVED_RUN+NEGATIVE_EVIDENCE | NAMED_NEAREST_ORIGINAL+ACTUAL_GAP/UNKNOWN | STRONGEST_ALTERNATIVE | EXPLORATORY_OR_CONFIRMED | GROUP_N+SELECTION_HISTORY | KEY_MISSING_EVIDENCE | DECISIVE_TEST+COST/AUTH`

优先比较真正**新增知识、在该数据上能否区分主张、已完成证据、未污染独立确认及新增成本**。科研主控PD-RW选择最值得继续的主张，不让RWF最便宜的下一Probe决定科学问题；不机械给分，不因小发现就停止寻找更有价值的证据。若多个贡献**相互独立且真实**，保留附属Claim索引，不自动拼成一篇更“大”的论文。用户拥有重大Task改变/项目级停止等决策权。

### C. 科学贡献充分性审查——先辨“没说清”还是“没证明”

对一个主要候选做**非论文**的`CONTRIBUTION_EVIDENCE_BRIEF`：

`IMPORTANT_PROBLEM | WHY_EXISTING_WORK_INSUFFICIENT | ACTUAL_NEW_KNOWLEDGE_OR_CAPABILITY | EVIDENCE_RUNS+FAIR_COMPARISON | SUPPORTING_AND_CONTRADICTORY_RESULTS | STRONGEST_ALTERNATIVE | SCOPE+INDEPENDENCE | ARTICULATION_GAP/EVIDENCE_GAP/BOTH/NONE | DECISIVE_NEXT_ACTION+AUTH`

判别规则：
- **`ARTICULATION_GAP`**：关键科学证据已经存在，但成果总结遗漏了问题重要性、与近邻的*真正差异*、能力/机制的正确限定、负结果或最直接的实验对应关系。→ 用已有证据修正**科研成果总结/Claim–Evidence表**（允许诊断图与结果表），**不擅自写标题、摘要、引言、讨论、论文大纲或投稿图版**。
- **`EVIDENCE_GAP`**：机制解释/泛化/成本/效应大小依赖未完成或无效验证。→ 标明“尚不能主张”，仅在原授权内选最小决定性实验；新资源/SEALED按[NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)先请用户决策。
- **`BOTH`**：既有证据没有被准确提炼，且关键实验未完成。→ 先明确现有合法证据到底支持什么，再设计一项最有价值的补证据实验。
- **`NONE`**：已有科研价值表达清楚，证据也充分到当前限定范围。→ 复用结果，别重复撰写“包装稿”，按Q2与权限规则决定后续。

**重要原则**：创新性 ≠ 修辞强度；没有新证据不能说“证实物理机制”，没有独立组不能说“普遍适用”，不得以结果图更漂亮代替因果/统计支持。既有真实算法工作的意义可以通过更准确的科学分类和证据映射得到体现，但**不许伪造结果或改变原始主张边界**。

## 三、既有实验与开源项目的最小融合

| 参考项目 | 可吸收的机制 | 不借用的错误推断 |
|---|---|---|
| [MLflow](https://github.com/mlflow/mlflow) + [DVC](https://github.com/treeverse/dvc) | 同协议Run/预测/配置/负结果可追溯，防止只拿最佳表格 | 记录完整 ≠ 独立创新 |
| [Cleanlab](https://github.com/cleanlab/cleanlab) + [Evidently](https://github.com/evidentlyai/evidently) | 疑似错标/漂移/异质性线索，避免遗漏科学异常 | 怀疑数据问题 ≠ 真值确认或机制解释 |
| [SHAP](https://github.com/shap/shap) + [DoWhy](https://github.com/py-why/dowhy) | 解释→竞争解释→不同预测→受控证据 | 特征归因 ≠ 因果效应，工具不能自动认证机理 |
| [RD-Agent](https://github.com/microsoft/RD-Agent) | 已有实验结果反推最有信息量的下一个科学问题 | 反复调参/自动生成稿件 ≠ 科研升级 |

不自动安装开源框架，不创建额外Agent或综合期刊评分器。仅将与研究问题有关的现有分析工具按需复用。

## 四、最短交接和止损

同一`TASK+PROTOCOL+RUN_HASH+GROUP_SCHEMA+METRIC+SEARCH_HISTORY`已有Harvest且没有新科学信息时标`HARVEST_REUSED`，别重复查论文、画图或跑训练。只更新真正新增的证据、候选贡献及唯一下一决定性实验；`SCIENCE_RESULT_HARVEST`只作为`STATE.md`中的**可选引用**，不是强制机器事件/新审核门。

最终科研成果总结前，确认**是否有未盘点的重要已有结果**以及是否存在`ARTICULATION_GAP`；不得因此强制进行新实验、无界切片搜索或额外论文式写作。结果总结交用户审查；**只有用户审查成果总结并单独授权**后才可撰写论文。可在当前许可下自主完成的只读诊断或普通修复，按[NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)直接给下一Agent指令；新下载/训练/封存/主张范围变更/结束项目需用户决定时只给推荐和选项，不提前给执行指令。
