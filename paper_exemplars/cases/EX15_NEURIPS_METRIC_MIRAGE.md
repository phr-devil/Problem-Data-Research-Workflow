# EX15 — NeurIPS 2023 / a seemingly new phenomenon can be a metric artifact

**Title:** Are Emergent Abilities of Large Language Models a Mirage?
**Source:** https://papers.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html
**Status:** NeurIPS 2023 conference paper；已核用户上传PDF全文，17 PDF页；原PDF不上传GitHub。
**PDF match:** `NeurIPS-2023-are-emergent-abilities-of-large-language-models-a-mirage-Paper-Conference.pdf`（SHA-256 前16位 `d9e32b422693044e`）
**Type:** measurement artifact / competitive explanation / cognitive correction
**H2 discovery sources:** B PAPER_CONTRADICTION; D DATA_EVALUATION_DEFECT; F ANOMALY_NEGATIVE_RESULT
**Contribution routes:** COGNITIVE_CORRECTION; SCIENTIFIC_DISCOVERY
**Locators:** PDF pp1–2 Abstract/Introduction将突变、不可预测性与离散指标联系；pp2–4 Fig.1–2简单数学模型和假设；p5 Fig.3–4相同输出下改变指标/统计的反证；pp6–8 Fig.5–6 BIG-Bench及指标关系验证；p9 Fig.7–8跨视觉架构构造类似表象，并列Limitations；p10 Discussion；其余为附录参考。

## 观察与可迁移策略
- **有限科学问题：** 原文不是“证明所有涌现不存在”，而是对具名现象提出更简单的竞争解释：评价指标的非线性/不连续可能把平滑能力变化表现为突变。
- **决定性设计：** 固定模型输出、变换评价指标；先用简单数学例子预测差异，再在不同任务和数据上检验，区分系统行为与测量函数造成的外观。
- **Results组织：** 建模解释 → 重评分/改统计验证 → 另一基准复验 → 构造可复现的表象；每部分围绕“原来看到的是什么”而不是堆算法。
- **低成本科研用法：** 对已获授权的保存预测，比较多种**科学上合理且事先定义**的评分与统计单位；若某结论仅在失真的指标下成立，核查是否有真实可复现的认识变化。
- **适用：** H2 B/D/F；H3机制反证；活动02测量、活动05认知纠正与边界讨论。

## AVOID
- 指标变化不能随意事后挑最有利的版本；应预设合理评价问题，并报告指标/组选择史，否则会形成新的数据选择泄漏。
- 原文并不排除某些真正涌现；只支持其检查过的任务与度量条件下的解释。
- 不能用新的非线性指标包装“首次发现”，也不能将LLM任务中的事实直接当作传感器或机器人数据的证据。
