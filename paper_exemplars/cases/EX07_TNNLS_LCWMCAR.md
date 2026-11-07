# EX07 — IEEE TNNLS / LCwmcaR for HAR

**Title:** LCwmcaR: Learning Cross-Window Cross-Modality Correlation-Aware Representation for Human Activity Recognition
**Source:** https://doi.org/10.1109/TNNLS.2025.3581226
**Status:** IEEE TNNLS 36(10), 2025；已阅读用户上传的**大学授权**PDF，15个PDF页；**不得公开转存该PDF**。
**PDF match:** LCwmcaR_Learning_Cross-Window_Cross-Modality_Correlation-Aware_Representation_for_Human_Activity_Recognition.pdf
**Type:** HAR / multivariate time series / cross-window learning
**Locators:** PDF pp1–2按问题分层的Introduction和Related Work；pp3–7 Methods；pp8–12数据、对照、消融与敏感性；p13结论。

## 观察与可迁移策略
- 将模态和时空表征挑战与跨窗口不一致性明确分离；每个Method模块应能对应前面真实提出的难题。
- Methods段落以“用途→操作→输出→下游依赖”顺序介绍网络和符号。
- 实验先给合法划分与强基线，再分主要比较、灵敏度及模块消融，避免只有逐图口述。
- **使用位置：** HAR、跨窗口时间序列和多模态算法的Introduction、Method和Ablation。

## AVOID
不可迁移该文的模型层、数据或性能。特别检查跨窗口操作是否使用推理时无法得到的未来信息或违反合法分组；不得以原文PDF的IEEE授权文件作为GitHub资产。
