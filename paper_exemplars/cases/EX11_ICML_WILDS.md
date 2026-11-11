# EX11 — ICML / real-world shift benchmark

**Title:** WILDS: A Benchmark of in-the-Wild Distribution Shifts
**Source:** https://proceedings.mlr.press/v139/koh21a.html
**Status:** ICML 2021, PMLR 139; 已核用户上传全文PDF（28页），含附录；原PDF不上传GitHub。
**PDF match:** koh21a.pdf
**Type:** benchmark / independent-group evaluation / distribution-shift validity
**H2 discovery sources:** C FAILURE_BOUNDARY; D DATA_EVALUATION_DEFECT; A DOMAIN_BOTTLENECK
**Contribution routes:** RESEARCH_INFRASTRUCTURE; SCIENTIFIC_DISCOVERY
**Locators:** PDF p1 Abstract/Fig.1两类真实偏移；pp2–3 Fig.2数据类型与来源；pp3–4 problem formulation；pp4–6数据集与分组设置；pp7–9 Table 1–2 ID/OOD基线和方法比较；p10 reproducibility。

## 观察与可迁移策略
- 不从“有新模型”写起，而从主流同分布测试无法回答部署偏移的问题起笔；先界定两类不同分布偏移及domain的真实单位。
- Figure 1做概念对比，Figure 2以同一输入/预测/域单位表比较多数据库；后续表格将ID与OOD、不同基线分开报告。
- 不把原始数据库规模当科学贡献：关键是**域定义、切分设计、指标适配、复用基线、可复现工具**共同消除先前评价盲区。
- **AI选题启发：** 若现有传感器数据已经包含设备/人员/位置/日期轴，先查是否能在合法独立组上定义更贴近真实部署的对照；一个可信的新评价问题也可能是窄论文贡献。
- **使用位置：** H2/C/D、H4数据库科学适配、Task评价协议、Benchmark/Results与局限。

## AVOID
- 原文建立10数据库benchmark，资源规模高；不能把“做一个新split”直接当论文新颖性，必须说明旧结论为何改变。
- OOD不等于随机抽窗测试；同源不同文件不是自动独立外部数据；不要偷读SEALED或用它调评测协议。
