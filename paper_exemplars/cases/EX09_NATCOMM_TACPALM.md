# EX09 — Nature Communications / tactile palm–finger system

**Title:** Soft robotic hand with tactile palm-finger coordination
**Source:** https://doi.org/10.1038/s41467-025-57741-6
**Status:** Nature Communications 16:2395 (2025); 已核用户上传全文PDF（14页）；原PDF不上传GitHub。
**PDF match:** s41467-025-57741-6.pdf
**Type:** soft robotics / tactile sensing / coordinated system capability
**H2 discovery sources:** A DOMAIN_BOTTLENECK; E CROSS_DOMAIN_PRINCIPLE
**Contribution routes:** MAJOR_INNOVATION; PERFORMANCE_BREAKTHROUGH (scope-limited)
**Locators:** PDF p1摘要、系统限制；p2 Fig.1系统构图与能力定位；pp3–4 Fig.2机械/触觉机制；pp5–6 Fig.4抓取能力；pp7–9 Fig.5–6感知、闭环操作；pp10–11 Discussion/Methods与Fig.7演示。

## 观察与可迁移策略
- Introduction先定位当前软手的**手掌触觉覆盖不足**，不是泛称所有机器人都缺感知；Fig.1同时解释系统结构、接触作用以及不同软手的能力坐标。
- Results按层级证明：触觉掌/软指能力 → 识别/重建 → 触觉反馈支持的实际动态操作；以任务能力为中心，而不是以传感器硬件零件为中心堆图片。
- 系统主张要求证明新能力与 palm–finger cooperation 的关系；区分“系统搭建成功”和“相对无协同/简单控制的增量”。
- **AI选题启发：** 对公开机器人数据，优先寻找“某个可观测接触条件下新增什么能力”的限定问题；可只借鉴模块证据组织，**不必重建机器人手或达到原文系统规模**。
- **使用位置：** A领域瓶颈、E跨域结构；机器人/触觉系统的Figure 1叙事与Results能力链。

## AVOID
- 该论文依赖专门硬件、多项设备研发和真实演示，**不是低成本公开数据论文的优先工作量模板**。
- 不把论文的触觉密度、机械性能和动作演示迁移到自己数据集的证据；算法仿真不自动等同真实触觉闭环能力。
- 未获绘图/硬件/训练/写作授权不复制图、实验和文本。
