# EX14 — ICLR 2021 / model selection is part of the scientific problem

**Title:** In Search of Lost Domain Generalization
**Source:** https://arxiv.org/abs/2007.01434
**Status:** ICLR 2021 peer-reviewed conference paper；已核用户上传PDF全文（29 PDF页，含附录）；原PDF不上传GitHub。
**PDF match:** `1580_in_search_of_lost_domain_gener.pdf`（SHA-256 前16位 `41431d2a09d0a28f`）
**Type:** evaluation-protocol correction / simple ERM baseline / benchmark methodology
**H2 discovery sources:** D DATA_EVALUATION_DEFECT; F ANOMALY_NEGATIVE_RESULT; B PAPER_CONTRADICTION
**Contribution routes:** RESEARCH_INFRASTRUCTURE; COGNITIVE_CORRECTION
**Locators:** PDF pp1–2 Abstract、Table 1公平ERM对比及三项贡献；pp3–4 model selection as part of learning problem / Table 2；p5 DomainBed实现（七数据集、十四算法、三种选模）；pp6–7实验设计、Table 3不同选择规则结果；p8 Table 4 ERM消融、Discussion及负结果限制；p9 Conclusion；pp10–29参考文献/附录及详细设置。

## 观察与可迁移策略
- **真正的问题：** 某算法宣称的OOD泛化进展是否受不同网络、数据、调参预算或选模规则驱动？把“模型选择标准”视为研究问题本身，而不是无关实现细节。
- **结果证据链：** 先用公平统一设置验证强ERM基线，然后按不同模型选择方式呈现DG算法的表现；再用数据增强和模型容量消融解释基线为何强。
- **结构：** 引言限定比较不可解释的原因 → 明确可见训练域和测试域/选模信息 → DomainBed评测接口 → 主要比较与消融 → Discussion承认负结果受算法集合和算力范围限制。
- **低成本科研用法：** 沿用已有合法DEV上的预测与训练日志，检查强简单基线是否存在、组间切分与超参选择是否对齐；选择足以改变已有文献结论的一项重点协议差异，不需要复制大规模Benchmark。
- **适用：** H2 D/F/B；H4/H6评测可识别性；活动04公平基线审查、活动05认知纠正/Benchmark讨论。

## AVOID
- 原文总计大规模模型训练（论文报告约58,000次模型训练）；**不是**默认研究预算要求。
- 原文算法集合与模型搜索策略下的平均结果，不证明所有领域泛化方法都失效；测试域oracle选择的对照不等于可部署的合法模型选择。
- 不能使用SEALED/独立test集调整超参数，或在修订协议后用同一测试集报告无偏改进。
- “重跑一次ERM”不是自动的论文贡献；应说明纠正了什么可信但错误的旧结论。
