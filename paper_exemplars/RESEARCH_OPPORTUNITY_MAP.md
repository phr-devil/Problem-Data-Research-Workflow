# 研究机会匹配图谱｜六类问题来源 × 五类论文贡献

> **USE_IN_ACTIVITY_01_ONLY_WHEN_HELPFUL / NOT_AN_APPROVAL_GATE**：本图谱帮助AI理解如何从一个**范围有限、能合法检验、具有可投稿增量**的科学问题出发。不是题目生成公式、不是文献创新审计、不是用户H2选择或写作授权。优先公开数据、合法已有DEV/Run、小的决定性实验；绝不伪造指标、拆分重复成果或以图表包装代替真实贡献。
>
> **两层正交轴（来自 [SEARCH_DISCOVERY.md](../SEARCH_DISCOVERY.md) 和 [HIGH_VALUE_RESEARCH_DESIGN.md](../HIGH_VALUE_RESEARCH_DESIGN.md)）**：六类 **`QUESTION_SOURCES`** = 去哪里发现问题；五类 **`CONTRIBUTION_ROUTES`** = 最终凭什么形成独立学术贡献。一个案例可以命中多类；无须六类逐条检索、五类同时实现。

## 一、六类问题来源：优先学可负担的“论文切口”

| 问题来源（稳定H2语义） | AI应主动寻找的**有限且可检验**问题 | 重点论证案例 | 成本策略 |
|---|---|---|---|
| **A DOMAIN_BOTTLENECK** 领域瓶颈 | 已发论文仍未解决的具体条件、资源或时间约束；先读limitations而非想象宏大应用 | [EX09](cases/EX09_NATCOMM_TACPALM.md) 触觉掌协同；[EX10](cases/EX10_NPJ_GSS_SENSOR.md) 灵敏度/线性度权衡；下方候选 **C01** | EX09/10依赖硬件与系统，**只学习问题—证据构图**；算法数据型优先C01的简明实证对比 |
| **B PAPER_CONTRADICTION** 研究矛盾 | 同一问题不同论文结论冲突？先对齐指标、合法输入与协议，再找真正的不同预测 | [EX08](cases/EX08_JMLR_UNDERSPEC.md) 同IID表现≠同应力行为；候选 **C03** | 单个可重复的争议 + 一个合理指标/条件反证可以是有价值的研究 |
| **C FAILURE_BOUNDARY** 失效边界 | 在什么设备/人/时间/噪声/部署信息下结果可靠或失败？ | 原有 [EX02](cases/EX02_NPJ_RPPG.md)；[EX08](cases/EX08_JMLR_UNDERSPEC.md)；[EX11](cases/EX11_ICML_WILDS.md) | 低成本先做合法分组/条件评估，避免在同一确认集上反复挑切片 |
| **D DATA_EVALUATION_DEFECT** 数据或评测缺陷 | 真值从何而来、是否重复、是否代理标签、是否泄漏、强基线是否公平？ | [EX11](cases/EX11_ICML_WILDS.md)；候选 **C02**、**C04** | 若纠错足以**改变原结论**，可形成评价/认知修正稿；普通Bug修复不是自动创新 |
| **E CROSS_DOMAIN_PRINCIPLE** 跨学科原理 | 某种物理/统计/信息约束能否合法转移到当前任务，并产生可区分的收益或新边界？ | [EX12](cases/EX12_NEURIPS_CONFORMAL_SHIFT.md)；[EX10](cases/EX10_NPJ_GSS_SENSOR.md) | 不强制理论推导；先核迁移前提是否成立，单纯套用旧方法通常不够 |
| **F ANOMALY_NEGATIVE_RESULT** 异常和负结果 | 强方法不如简单法？相同分数不同失败？旧增益是否来自评价/标签？ | [EX08](cases/EX08_JMLR_UNDERSPEC.md)；候选 **C01**、**C02**、**C03** | **已有合法Run的负证据优先复用**，认真做一项判别性实验；不能把失败硬说成新规律 |

**AI要学到的主要动作**：`具名近邻/已有主张 → 未解释的实际差异 → 一个强基线/竞争解释 → 便宜且合法的判别试验 → 范围有限的科学Claim → 明示失败条件和投稿贡献类别`。不是“找一个热门大模型加上去”；也不把预算低等同于科研价值低。

## 二、五类论文贡献路线：与六来源分开判断

| `CONTRIBUTION_ROUTES` | 对应范例 | 对公开数据、低算力项目的现实定位 |
|---|---|---|
| **MAJOR_INNOVATION** 重大创新 | [EX09](cases/EX09_NATCOMM_TACPALM.md)、[EX10](cases/EX10_NPJ_GSS_SENSOR.md)、[EX12](cases/EX12_NEURIPS_CONFORMAL_SHIFT.md) | 仅当确有新系统能力/物理机制/理论保证及证据时选择；**不是默认路线** |
| **PERFORMANCE_BREAKTHROUGH** 性能突破 | [EX10](cases/EX10_NPJ_GSS_SENSOR.md)、旧EX03/EX07、候选 **C05** | 同合法输入与预算的强基线、公平效应量和独立单位；不能仅靠随机seed差异宣称突破 |
| **SCIENTIFIC_DISCOVERY** 科学发现 | [EX08](cases/EX08_JMLR_UNDERSPEC.md)、旧[EX02](cases/EX02_NPJ_RPPG.md)、[EX11](cases/EX11_ICML_WILDS.md) | 适合一个真实规律/受限边界，但必须排除关键混杂 |
| **RESEARCH_INFRASTRUCTURE** 基础设施 | [EX11](cases/EX11_ICML_WILDS.md)、候选 **C02** | 可做有独立效用的新评价协议/测量与开放可复用工具，不必做十个数据库 |
| **COGNITIVE_CORRECTION** 认知纠正 | [EX08](cases/EX08_JMLR_UNDERSPEC.md)、候选 **C01**、**C03**、**C04** | **优先考虑**：纠正广泛使用的代理标签、泄漏、失真指标或复杂模型优势；必须真正改变科学结论 |

## 三、五篇论文全文卡和公开核验的低成本范例候选，必须分清

- **EX08–EX12**：本次从用户上传的五份PDF逐页核对了论文结构及关键Fig/Table，已有卡片与PDF页码；用户PDF**不上传GitHub**。
- **C01–C05**：仅核对公开出版/会议资料，**未在本次生成全文策略卡**；不得记为`FULLTEXT_REVIEWED`，需要时才合法读取原文。

| 候选 | 公开论文原始来源（已核验出版信息） | 强映射 | AI应学习的可负担研究动作 |
|---|---|---|---|
| **C01** | [Zeng et al., *Are Transformers Effective for Time Series Forecasting?*, AAAI 2023](https://doi.org/10.1609/aaai.v37i9.26317) | A/B/F → COGNITIVE_CORRECTION | 简单线性基线挑战复杂模型；对齐多步预测协议与信息预算。不泛化为“Transformer均无效” |
| **C02** | [Gulrajani & Lopez-Paz, *In Search of Lost Domain Generalization*, ICLR 2021](https://mlanthology.org/iclr/2021/gulrajani2021iclr-search/) | D/F → RESEARCH_INFRASTRUCTURE、COGNITIVE_CORRECTION | 统一模型选型和公平预算，检查强ERM是否已足够；原文大型DomainBed不是必需规模 |
| **C03** | [Schaeffer et al., *Are Emergent Abilities of Large Language Models a Mirage?*, NeurIPS 2023](https://papers.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html) | B/D/F → COGNITIVE_CORRECTION | 用可观察的指标形式差异区分“现象真的突变”与“评价制造突变”，有假设与反解释 |
| **C04** | [Kapoor & Narayanan, *Leakage and the reproducibility crisis in machine-learning-based science*, Patterns 2023](https://doi.org/10.1016/j.patter.2023.100804) | D/F → COGNITIVE_CORRECTION | 沿泄漏类型与评测协议重算原结论，不能把一般数据泄漏排查自动写成独立论文 |
| **C05** | [Geifman & El-Yaniv, *SelectiveNet*, ICML 2019](https://proceedings.mlr.press/v97/geifman19a.html) | C/E → PERFORMANCE_BREAKTHROUGH | 把拒答、覆盖率和风险曲线构成独立Task；不默认需要重训练多头网络，先与强简单置信阈值比较 |

## 四、默认取舍策略（非固定路线）

- **已有公开数据库+旧Run**：优先审查 **D/F/C/B** 中真正影响结论的条件性机会；用最少合法分析验证，选不与最近邻重复的1个主Claim，最多2个备选。
- **有真正新物理条件/硬件验证**：再重视 **A/E**；没有物理真值就不能把相关性包装成已证明的新机制。
- **有投稿目标**：优先一种能够由现有数据、强简单比较、独立组和明确局限支撑的贡献；期刊分区/审稿成功率需要另行核验，**不能承诺Q2录用**。
- 用户选择H2来源及贡献倾向，AI可提具体推荐；文献卡只帮助研究构思和获准写作时的论证，不批准H3/H4/H5、下载、训练、SEALED、出图或撰稿。避免拆分同一数据和同一核心主张制造重复稿。
