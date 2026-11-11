# EX16 — Patterns 2023 / reproducible correction of ML-based scientific claims

**Title:** Leakage and the reproducibility crisis in machine-learning-based science
**Source:** https://doi.org/10.1016/j.patter.2023.100804
**Status:** Patterns 4 (2023), article 100804；已核用户上传PDF全文（13 PDF页）；原PDF不上传GitHub。
**PDF match:** `1-s2.0-S2666389923001599-main.pdf`（SHA-256 前16位 `8efbd99a03b368b7`）
**Type:** leakage taxonomy / measurement-validity audit / reproducible cognitive correction
**H2 discovery sources:** D DATA_EVALUATION_DEFECT; F ANOMALY_NEGATIVE_RESULT; B PAPER_CONTRADICTION
**Contribution routes:** COGNITIVE_CORRECTION; RESEARCH_INFRASTRUCTURE
**Locators:** PDF pp1–2 Highlights/Summary/研究范围；p3 Fig.1跨领域既有综述与受影响论文；pp4–6八类泄漏分类与不同合法预测信息的问题；pp6–7 model info sheets及局限；pp8–9 Fig.2–3 civil-war-prediction复核与修正结果及Discussion；p10 Conclusion/Experimental Procedure；pp11–13细节与参考。

## 观察与可迁移策略
- **首先区分研究声明与可用信息：** 不是看模型分数高不高，而是检查预测当时是否非法使用了未来信息、全数据预处理、重复样本或训练/测试选择交叉。
- **多级证据：** 文献中已核出的泄漏案例 → 可复用的错误分类与披露清单 → 一个有代表性的具体领域复现实验，显示修正后复杂方法可能不再占优势。
- **图表组织：** Fig.1呈现分类覆盖和受影响研究，不误读成全部被独立复现；Fig.3将原报告与修正结果对照，突出对既有科学结论的改变。
- **AI可做的小论文切口：** 找一个具名、使用广泛且结论受泄漏影响的评测前提，在合法DEV中先复现、区分错误来源，再以按独立单位冻结的新协议验证结论变化；复现困难、源代码不可得或无未污染确认时坦诚降低主张。
- **适用：** H2 D/F/B；H4真值/独立性；活动02 QA、活动03评估合法性、活动05认知修正论文论证。

## AVOID
- 论文报告的“294篇/17学科”是**通过先前审查研究汇总**的范围，不意味着作者逐一独立复现294篇论文。
- 不能因为某种常见泄漏风险存在，就直接指控任何具名论文已经泄漏；需要原始协议、可验证证据和公平修正后的效应。
- 单纯修复自己数据处理Bug/重做split通常只是科研正确性义务；要形成独立论文贡献必须证明原结论受到实质性改变。
- 审核不代表授权读取SEALED、回填测试标签、自动运行大量算法或正式论文写作。
