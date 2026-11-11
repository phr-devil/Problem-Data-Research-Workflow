# EX10 — npj Flexible Electronics / physical-mechanism design

**Title:** Ultra-sensitive, highly linear, and hysteresis-free strain sensors enabled by gradient stiffness sliding strategy
**Source:** https://doi.org/10.1038/s41528-024-00301-7
**Status:** npj Flexible Electronics 8:14 (2024); 已核用户上传全文PDF（8页）；原PDF不上传GitHub。
**PDF match:** s41528-024-00301-7.pdf
**Type:** flexible sensor / physical mechanism / performance tradeoff
**H2 discovery sources:** A DOMAIN_BOTTLENECK; E CROSS_DOMAIN_PRINCIPLE
**Contribution routes:** MAJOR_INNOVATION; PERFORMANCE_BREAKTHROUGH
**Locators:** PDF p1摘要及灵敏度—线性度矛盾；p2 Fig.1结构机制/Results；p3 Fig.2边缘场与形状优化；p4 Fig.3主要性能；p5 Fig.4独立性能评价与Methods；p6 Fig.5应用/模拟实现。

## 观察与可迁移策略
- 将宏大问题缩成**灵敏度与线性度的物理权衡**，先明确基于感知机理的限制，再提出梯度刚度与滑移这一物理杠杆。
- 证据顺序为：结构—可观测物理机理（Fig.1）→竞争效应与设计变量（Fig.2）→传感指标/迟滞/稳定性（Fig.3–4）→限定应用（Fig.5），让性能主张对应测量因果链。
- 适合学习“参数改变为什么产生物理收益”“如何用简单模型/有限元+测量区分机制”，不依赖复杂神经网络。
- **AI选题启发：** 对传感器公开数据，先寻找可检验的物理角色、位置或非线性响应边界；没有材料/力学真值时只能做可靠测量与条件性关联，不能事后声称证实新物理机制。
- **使用位置：** A/E研究机会、物理机制型Introduction/Results/Discussion。

## AVOID
- 高GF等指标受原文器件/测量条件限制，绝不转移为其他传感器成果；未做硬件实验不能宣称改进器件性能。
- 这是材料制备/器件物理研究，实际复现成本高；算法数据型项目优先参考论证结构而非完整开发路线。
