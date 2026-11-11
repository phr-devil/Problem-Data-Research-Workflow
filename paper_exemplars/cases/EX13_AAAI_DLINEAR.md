# EX13 — AAAI 2023 / strong simple baseline as a scientific challenge

**Title:** Are Transformers Effective for Time Series Forecasting?
**Source:** https://doi.org/10.1609/aaai.v37i9.26317
**Status:** AAAI 2023 peer-reviewed conference paper; 已核用户上传PDF全文，8 PDF页；原PDF不上传GitHub。
**PDF match:** `02124-AAAI23.ZengA.pdf`（SHA-256 前16位 `365a43dc42b12b28`）
**Type:** baseline challenge / temporal-mechanism falsification / low-complexity empirical correction
**H2 discovery sources:** A DOMAIN_BOTTLENECK; B PAPER_CONTRADICTION; F ANOMALY_NEGATIVE_RESULT
**Contribution routes:** COGNITIVE_CORRECTION; SCIENTIFIC_DISCOVERY（主）；PERFORMANCE_BREAKTHROUGH（仅严格限定任务）
**Locators:** PDF p1 Abstract/Introduction提出对long-term time series forecasting中Transformer有效性的质疑；pp2–3 LTSF-Linear/Linear、NLinear、DLinear的定义及 Fig.1–2；p4 Table 1数据集与 Table 2主要公平性能比较；p5 Fig.3定性预测与 Table 3输入序列长度；pp6–7 Fig.4、Tables 4–8模型组成、输入乱序、embedding、训练量及资源效率反证；p7 Conclusion；p8参考文献。

## 观察与可迁移策略
- **问题发现：** 不是再提出一套热门架构，而是挑战“复杂的时序注意力是否真正利用了时间顺序”这个可证伪前提。
- **最低可判别实验：** 使用直接多步预测的简单线性模型，与既有复杂模型在任务、输入窗口、预测跨度、指标上公平比较。简单基线能否保持竞争力是关键，而不是线性网络名字本身。
- **机制证据：** 在主要结果后专门改变序列顺序、embedding、输入长度、模块配置等，检验模型是否真正利用作者声称的重要结构；对照与假设同构。
- **图表组织：** 先以Table 2建立主差异，再用Fig.3和后续机制/效率对照解释差异及代价，最后把“存在的评价盲区”作为讨论核心。
- **AI可移植的小论文思路：** 在合法公开传感器数据上，先有合适的朴素基线（统计模型、直接回归、固定规则），再调查具名复杂方法相对公平基线的增量与条件边界；无需默认开发新大模型。
- **适用：** H2 A/B/F；H3竞争性反证；活动03强简单基线、活动04机制对照、活动05认知纠正Results。

## AVOID
- 原文研究的是**长时序预测**且依据特定的九个数据集/预测跨度，不能泛化为“所有Transformer或所有HAR任务都无效”。
- 与过往论文比必须对齐直接/迭代预测方式、窗口长度、超参数搜索、预处理、计算预算和数据切分；不能用现成表格值替代自己的有效实验。
- “简单方法获胜”只意味着限定条件下的比较结论；没有真实近邻差额、重复验证或解释则不自动构成独立发表贡献。
- 不复制原文图/表/数据，不提前训练、读取SEALED、绘图或解锁论文写作。
