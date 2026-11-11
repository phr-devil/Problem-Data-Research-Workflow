# EX08 — JMLR / underspecification and scientific correction

**Title:** Underspecification Presents Challenges for Credibility in Modern Machine Learning
**Source:** https://www.jmlr.org/papers/v23/20-1335.html
**Status:** JMLR 23 (2022); 已核用户上传全文PDF（61页），非预印本；原PDF不上传GitHub。
**PDF match:** 20-1335(1).pdf
**Type:** scientific discovery / failure boundary / cognitive correction
**H2 discovery sources:** B PAPER_CONTRADICTION; C FAILURE_BOUNDARY; F ANOMALY_NEGATIVE_RESULT
**Contribution routes:** SCIENTIFIC_DISCOVERY; COGNITIVE_CORRECTION
**Locators:** PDF pp2–3 Abstract/Introduction与两条核心主张；pp4–7概念、结构缺陷与欠约束的区分；pp7–12简单模型/理论示例；pp14–30跨领域stress-test证据（Fig.4–14）；pp31–32结论/讨论。

## 观察与可迁移策略
- 从一个可验证的反常现象提出问题：训练域验证性能几乎相同的模型，部署域的行为却不同。先定义这不等于已知的简单域偏移/结构缺陷，再提出可区分的“欠约束”解释。
- 先用小型、可分析模型证明“为何可能”，再以不同场景的复现实证证明“实际存在”；在结果组织中始终围绕同一科学问题，而不是按模型种类逐项报分。
- 科学证据核心不是更高的指标，而是**固定正常性能的同时改变随机种子等无关因素，观察应力测试结果的变化**；这类正交干预能形成独立的测量型/纠错型主张。
- **AI选题启发：** 在已有合法DEV结果中找“同一评测分数、不同条件表现”的矛盾；优先一个数据集、一种可复验的关键条件、一个强反解释和清晰边界，不强制复刻原文大型多领域研究。
- **使用位置：** H2/B、C、F问题发现；H3反证；活动05的Result/Discussion/负结果论证。

## AVOID
- 原文是61页跨多个领域的大型研究，不是Q2窄贡献稿件的章节数量或实验规模模板。
- 不从同分数模型的差异直接推出部署“不可靠”的普遍定理；必须区分随机波动、选择偏差、真值问题和真正独立应力条件。
- 不复制原文推导、数据、图或措辞；没有授权不自动训练多seed模型或读取SEALED。
