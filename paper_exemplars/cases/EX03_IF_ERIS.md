# EX03 — Information Fusion / ERIS OOD time series

**Title:** ERIS: An energy-guided feature disentanglement framework for out-of-distribution time series classification
**Source:** https://doi.org/10.1016/j.inffus.2026.104407
**Status:** Information Fusion 135 (2026), 104407；已阅读用户上传全文，13个PDF页。
**PDF match:** 1-s2.0-S1566253526002861-main.pdf
**Type:** algorithm / OOD time-series classification
**Locators:** PDF pp1–2问题动机；pp2–3 Related Work；pp3–5机制/模型；pp5–7实验设置及主结果；pp8–11按RQ的消融/敏感性；p12结论。

## 观察与可迁移策略
- 以具体失效机制提出可检验问题，设计模块逐项回应问题，而不是先罗列网络层。
- Methods依赖顺序为预备定义→核心机制→辅助机制→完整模型；定义和符号与下游实证对应。
- 实验先固定数据、强基线、指标和公平性，再报告主要比较，最后按RQ检验消融、容量、鲁棒性和超参数。
- **使用位置：** 算法型HAR/OOD论文的Proposed Method、Experiments、Ablation；按真实结果组织而非模仿胜利叙事。

## AVOID
不能从本论文复制能量先验、损失函数、网络或SOTA结果。对测量型或描述性论文，不得强塞多模块新算法和消融。
