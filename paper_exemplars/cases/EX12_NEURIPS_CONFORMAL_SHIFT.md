# EX12 — NeurIPS / bounded theory under covariate shift

**Title:** Conformal Prediction Under Covariate Shift
**Source:** https://proceedings.neurips.cc/paper/2019/hash/8fb21ee7a2207526da55a679f0332de2-Abstract.html
**Status:** NeurIPS 2019; 已核用户上传全文PDF（11页）；原PDF不上传GitHub。
**PDF match:** NeurIPS-2019-conformal-prediction-under-covariate-shift-Paper.pdf
**Type:** theoretical guarantee / distribution shift / uncertainty
**H2 discovery sources:** E CROSS_DOMAIN_PRINCIPLE; C FAILURE_BOUNDARY
**Contribution routes:** MAJOR_INNOVATION; SCIENTIFIC_DISCOVERY
**Locators:** PDF pp1–2 Introduction与交换性基线；pp3–4 covariate shift假设/加权方法与Corollary；pp5–6实验设置及Fig.1 coverage；pp7–8 weighted exchangeability与Theorem 2；p8 Discussion，后续为拓展/应用。

## 观察与可迁移策略
- Introduction先写明确目标（预测区间覆盖）与现有方法的前提（交换性），再只改变一类条件：训练与测试的covariate分布可以不同、条件输出分布保持不变。
- 方法与理论结论一一对应：声明可证明的假设、密度比可用性/估计误差，再给出加权构造、定理与经验覆盖率对照，最后讨论范围外情况。
- 核心不是“比某模型分数高”，而是**在清楚的假设下拓展已知保证可适用的范围**；Fig.1检验覆盖而非随便展示预测曲线。
- **AI选题启发：** 跨传感器/人群适配中的方法移植，先标明哪些不变性假设无法由当前数据库确认；可做有界预测区间/拒答评价，但不借用其理论保证。
- **使用位置：** E跨领域原理、理论研究/保证型Methods、假设与局限对齐。

## AVOID
- 该理论的保证依赖特定分布条件和权重假设；未知概念漂移或标签机制改变时不能声称distribution-free部署保证。
- 不能仅因在公开数据上应用conformal方法就宣称数学创新；需新假设、真实有效的能力差额或明确的失效测量。
