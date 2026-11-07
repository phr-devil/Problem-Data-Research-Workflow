# Paper Exemplar Library｜论文案例库

> 本库根据用户提供的7篇论文全文PDF提炼**原创的论证结构和语言策略**，供PD-RW获授权的论文写作参考。每张卡带 DOI/原文链接、PDF页码、适用范围与禁用边界。**不在GitHub公开PDF、原文段落、图或表**；IEEE学校授权件和Elsevier版权全文尤其不得镜像。原始PDF位于用户本次上传的会话，并不意味着WorkBuddy本地自动拥有同名文件。核对日期：2026-11-07。

## 七篇论文与单篇策略卡

| ID | 研究类型 / 优先用途 | 来源 | 策略卡 |
|---|---|---|---|
| EX01 | 生理监测、真实场景系统验证；摘要与宏观叙事 | [Nature · Passive heart-rate monitoring (2026)](https://doi.org/10.1038/s41586-026-10507-6) | [EX01](cases/EX01_NATURE_PHRM.md) |
| EX02 | 测量可靠性、异质条件与负结果 | [npj Digital Medicine · rPPG reliability (2025)](https://doi.org/10.1038/s41746-025-02192-y) | [EX02](cases/EX02_NPJ_RPPG.md) |
| EX03 | 分布外时间序列分类、机制与消融 | [Information Fusion · ERIS (2026)](https://doi.org/10.1016/j.inffus.2026.104407) | [EX03](cases/EX03_IF_ERIS.md) |
| EX04 | 视觉—触觉机器人、系统与条件性收益 | [Robotics and Autonomous Systems · SPOTS (2026)](https://doi.org/10.1016/j.robot.2026.105512) | [EX04](cases/EX04_RAS_SPOTS.md) |
| EX05 | HAR、IMU物理角色与复杂方法组织；**预印本** | [arXiv 2605.02743v1 · Triple Spectral Fusion (2026)](https://arxiv.org/abs/2605.02743) | [EX05](cases/EX05_ARXIV_TSF.md) |
| EX06 | 传感器域泛化、分阶段方法、独立Discussion | [Expert Systems with Applications · ASAM (2026)](https://doi.org/10.1016/j.eswa.2026.131585) | [EX06](cases/EX06_ESWA_ASAM.md) |
| EX07 | IEEE HAR、跨窗口/模态机制与消融 | [IEEE TNNLS · LCwmcaR (2025)](https://doi.org/10.1109/TNNLS.2025.3581226) | [EX07](cases/EX07_TNNLS_LCWMCAR.md) |

## WorkBuddy 使用合同（M2 / R1 必查索引，非额外审批）

1. 已经具备科研成果审查与正文写作授权时，在写作 R1 按**研究贡献类型→目标小节职责→期刊读者**选1–3篇；单凭期刊名气不可优先。主张没有变化时重用已有选择，不重复下载、重新通读7篇。没有适合者记录 **EXEMPLAR_NONE + reason**，不得硬套。
2. **只读入选的策略卡**，内部 Section Contract 暂记 **EXEMPLAR_IDS / why_match / ADOPT / AVOID**，不向投稿正文写入这些元信息。R2参考Methods/Results的论证顺序，R3参考引言与讨论的段落职责，R4仅在科学审核后参考语言清晰度。
3. **学习写作决策，不复制原文**。不从范例直接迁移数据、模型机制、统计显著性、实验规模、声称首创的结论或独特句式；案例不自动成为本项目Related Work引用。科学事实仍要经单独的Claim–Source核验。
4. 需要原文细节时用卡中PDF页码定位，在合法可访问情况下有界回看；原PDF不可得时可以使用经本轮提炼的策略卡，但**不得声称本轮重读原文**，也不得由DOI或摘要推测全文句法。
5. 范例中有 Nature/npj 的正文后置Methods和SPOTS七章结构，**不能因此修改用户已经确认的六章或二级目录**。不因阅读范例触发受控数据读取、实验训练、生成图片、付费下载、外传或投稿。
6. 完稿前检查：结构借鉴是否真的提升当前Claim的清晰度；是否删除不利结果、削弱必要边界或把条件性观察写成因果；不合适就不采用该案例技巧。

## 默认选择

- **测量/腕式心率可靠性（如Galaxy-HRGuard）**：EX02为主，EX01辅助；负结果和部署条件可借EX04的“何时有效”论证。
- **算法/HAR/IMU/跨域**：在EX03、EX05、EX06、EX07中按真实任务问题选1–3个，避免把所有算法写成SOTA+消融模板。
- **机器人/触觉/具身**：EX04为主；有合法跨窗口多模态任务再参考EX07。
- **置信不足或缺失近邻原文**：不让案例填充科学证据缺口；继续支持已经核实的正文，针对缺口留标记。

源PDF没有提交，策略卡只是原创分析。特别说明：EX05是**上传的arXiv v1预印本**，其正式发表状态没有从该文件得到确认。见 [正式写作规范](../MANUSCRIPT_WRITING.md)。
