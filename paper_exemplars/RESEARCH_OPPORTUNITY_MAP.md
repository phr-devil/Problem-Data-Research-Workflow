# H2 研究机会图谱｜六类问题来源 × 五类论文贡献路线

> **READ_ONLY_OPTIONAL / NOT_AN_APPROVAL_GATE。** 本图谱用于教 AI 从具名文献、公开数据、合法 DEV 与历史可靠 Run 中寻找**范围有限、可证伪且有投稿潜力**的科学问题。它不是选题配额或机械的论文生成公式；论文范例不认证科学创新或期刊录用，也不替代 H1–H10 决策、下载/训练/SEALED/绘图/写稿授权。
>
> **两个正交维度**：`QUESTION_SOURCES` 六类 = *如何发现问题*；`CONTRIBUTION_ROUTES` 五类 = *最后获得了哪种新知识、能力或可靠评价*。同一论文可能对应多项；不用每个项目都遍历六类或都达成五类。

## 一、六类科研问题来源：每类都给可执行的论文例子

| H2问题来源 | 学会识别的“小而真”的问题 | 最适配的已核全文案例 | AI 在合法数据/既有Run上的最低动作 |
|---|---|---|---|
| **A DOMAIN_BOTTLENECK** 领域瓶颈 | 哪项实际时间、设备、物理或预测能力限制还未解决？ | [EX13 DLinear](cases/EX13_AAAI_DLINEAR.md)、[EX10 物理传感](cases/EX10_NPJ_GSS_SENSOR.md)、[EX09 软手](cases/EX09_NATCOMM_TACPALM.md) | 先选一个有科学后果的瓶颈和适用指标；无需默认做大型器件/机器人系统 |
| **B PAPER_CONTRADICTION** 论文矛盾 | 同一主张为何因模型、统计、协议或条件产生不同结论？ | [EX13 DLinear](cases/EX13_AAAI_DLINEAR.md)、[EX15 指标伪象](cases/EX15_NEURIPS_METRIC_MIRAGE.md)、[EX08 欠约束](cases/EX08_JMLR_UNDERSPEC.md) | 对齐同一合法输入/评价对象，先识别至少一种竞争解释；不同协议的分数不直接当真冲突 |
| **C FAILURE_BOUNDARY** 失效边界 | 哪些人、设备、环境、信息预算或分布使模型收益失效？ | [EX08](cases/EX08_JMLR_UNDERSPEC.md)、[EX11 WILDS](cases/EX11_ICML_WILDS.md)、旧[EX02 rPPG](cases/EX02_NPJ_RPPG.md) | 独立组和固定条件下测量有限范围的风险；不根据独立确认集挑最有利切片 |
| **D DATA_EVALUATION_DEFECT** 数据/评价缺陷 | 真值、重复采集、未来信息、group、选模和指标是否使旧优势失真？ | [EX14 DomainBed](cases/EX14_ICLR_DOMAINBED.md)、[EX16 泄漏复现](cases/EX16_PATTERNS_LEAKAGE.md)、[EX15](cases/EX15_NEURIPS_METRIC_MIRAGE.md)、[EX11](cases/EX11_ICML_WILDS.md) | 一个具名协议缺陷 + 公平纠正前后对比 + 报告对原主张的实质性影响；普通Bug修复不是自动论文 |
| **E CROSS_DOMAIN_PRINCIPLE** 跨领域原理 | 哪项统计/力学/信息假设在新任务成立，能产生新的有效能力或边界？ | [EX12 Conformal](cases/EX12_NEURIPS_CONFORMAL_SHIFT.md)、[EX10](cases/EX10_NPJ_GSS_SENSOR.md)、[EX09](cases/EX09_NATCOMM_TACPALM.md) | 先列适用前提及最强近邻，比较简单替代；跨领域搬运旧方法不等于原创 |
| **F ANOMALY_NEGATIVE_RESULT** 异常与负结果 | 简单方法强于复杂方法、虚假收益、评价翻转、类似分数但不同部署行为？ | [EX13](cases/EX13_AAAI_DLINEAR.md)、[EX14](cases/EX14_ICLR_DOMAINBED.md)、[EX15](cases/EX15_NEURIPS_METRIC_MIRAGE.md)、[EX16](cases/EX16_PATTERNS_LEAKAGE.md)、[EX08](cases/EX08_JMLR_UNDERSPEC.md) | 复用真实且合法的负结果，先排除程序错误/选择泄漏，再做一个判别性实验；不能把失败强包装为发现 |

**最推荐AI记住的选题模板不是固定实验结构，而是判断链：** `已发表/普遍接受的具体主张 → 一个可能改变该主张的可观察差异 → 最强公平简单对照或竞争解释 → 最便宜的合法判别性分析 → 独立组与证据边界 → 一个真实且不重复的Claim`。

## 二、五类论文贡献（与发现路线分开判断）

| H2贡献取向 | 最有教学价值的全文论文 | 可负担研究目标 |
|---|---|---|
| **MAJOR_INNOVATION** | [EX09](cases/EX09_NATCOMM_TACPALM.md)、[EX10](cases/EX10_NPJ_GSS_SENSOR.md)、[EX12](cases/EX12_NEURIPS_CONFORMAL_SHIFT.md) | 真有新系统能力、物理机制或证明时才采用；不是低成本项目默认 |
| **PERFORMANCE_BREAKTHROUGH** | [EX13](cases/EX13_AAAI_DLINEAR.md)、[EX10](cases/EX10_NPJ_GSS_SENSOR.md)、旧EX03/EX07 | 与强简单基线公平比较并报告资源/方差/独立单位；不能用单一最佳seed宣称突破 |
| **SCIENTIFIC_DISCOVERY** | [EX08](cases/EX08_JMLR_UNDERSPEC.md)、[EX15](cases/EX15_NEURIPS_METRIC_MIRAGE.md)、[EX11](cases/EX11_ICML_WILDS.md) | 找受限规律、条件异质性与真正的可解释反例；保留混杂不确定性 |
| **RESEARCH_INFRASTRUCTURE** | [EX14](cases/EX14_ICLR_DOMAINBED.md)、[EX11](cases/EX11_ICML_WILDS.md)、[EX16](cases/EX16_PATTERNS_LEAKAGE.md) | 提供别人确实可复用的评测协议/核查清单/基准，而不必复制大型Benchmark规模 |
| **COGNITIVE_CORRECTION** | [EX13](cases/EX13_AAAI_DLINEAR.md)、[EX14](cases/EX14_ICLR_DOMAINBED.md)、[EX15](cases/EX15_NEURIPS_METRIC_MIRAGE.md)、[EX16](cases/EX16_PATTERNS_LEAKAGE.md) | **默认重点考虑**：在可核来源和公平对照下修正“复杂模型必优、指标突变、无泄漏、泛化成立”等具体结论 |

**发表务实原则：** 更推荐用现有公开数据和强基线验证**一项有学术意义的小差额**，不是按热度复现大型顶会工程。若实证支持不了新贡献，止损并保留负证据，不能拆分同一数据/主张制造重复稿、编造创新或保证Q2录用。

## 三、来源可信状态及全文去重

- **EX01–EX16**：均有已整理的原创全文策略卡；其中 **EX08–EX12** 对应本轮再次上传的5篇既有全文，**EX13–EX16** 对应4篇新上传全文。详见 [PDF SHA-256 来源清单](PDF_SOURCE_MANIFEST.md)。不在GitHub存放PDF字节。
- **C05**： [Geifman & El-Yaniv, *SelectiveNet*, ICML 2019](https://proceedings.mlr.press/v97/geifman19a.html)，仍是 **FULLTEXT_NOT_REVIEWED** 的公开候选：属于 C/E 类失效边界和选择性预测相关方法；本轮没有相应PDF，不应假装已经审阅，也**不计入16篇**。
- 当前案例库解决“怎么提出和论证问题”，不是当前项目的最新Related Work，必须独立检查最强具名近邻和研究新颖性。全文缺失时不伪造页码或准确数据。

## 四、在工作流中的最短调用方式

1. **活动01/H2**：仅在需要帮助生成/区分研究方向时按问题源查 1–3 张最适配策略卡；引用示例中的**研究动作**，不是照搬具体研究题目、模型和规模。
2. **活动01/H3–H5**：用最新相关原始文献、数据真值和真实授权验证科学主张；案例不能替用户确认 H3/H4/H5。
3. **活动03–05**：如已有可信Run，优先做公平基线、真实负证据、条件边界和旧结论修正；仅在新科学差额值得投资时再加实验。
4. **正式论文撰写 R1**：仅在原 `WRITING_GATE` 和人工科研审核通过后，按当前Claim匹配1–3篇全文论证卡；不强制凑数量或改既定章节。案例本身不批准下载、训练、SEALED、出图或撰稿。
