# 本轮上传 PDF 来源清单｜2026-11-11

> **仅保存元数据与 SHA-256，不提交 PDF 或其中的原文图表。** PDF 仅通过用户当前聊天附件获得；GitHub/WorkBuddy 的新会话不自动继承附件权限、字节或本地路径。以下哈希是对本轮已上传文件**实际字节**的校验值，用于未来识别相同全文、定位合法持有的个人副本、避免重复建卡；不表示自动授权下载/再分发。

本轮共 **10 份上传 PDF / 9 个不同 SHA-256 / 9 篇不同论文**。其中 EX08–EX12 已在此前完成策略卡，本轮通过内容哈希核对后复用；EX13–EX16 为这次根据新上传全文增加的策略卡。EX12 的两个不同文件名完全相同，**只计一次**。不对EX01–EX07（未在本轮上传）声称完成文件哈希复核。

| 本轮论文 ID | PDF页 | 本轮上传文件名 | SHA-256（完整） | 处理 |
|---|---:|---|---|---|
| [EX08](cases/EX08_JMLR_UNDERSPEC.md) | 61 | `20-1335(2).pdf` | `0bfceedec5f0a29ca74466785d2f3785e52509e6cd683ffe33318820e9b17eaf` | 既有全文卡；复用 |
| [EX09](cases/EX09_NATCOMM_TACPALM.md) | 14 | `s41467-025-57741-6(1).pdf` | `f3facf08d6ee69018dd5c330db87ec0360fed5d2a0926668d3e51840db1b71da` | 既有全文卡；复用 |
| [EX10](cases/EX10_NPJ_GSS_SENSOR.md) | 8 | `s41528-024-00301-7(1).pdf` | `d3469d78bfe56311cbe619789cfbc4a8fb214be335724cef8ae23d25b4650849` | 既有全文卡；复用 |
| [EX11](cases/EX11_ICML_WILDS.md) | 28 | `koh21a(1).pdf` | `ce963a0ae9567d43ce852c014b2f7f2860cfc5e86ad497ef8d4f1ffe42cb3677` | 既有全文卡；复用 |
| [EX12](cases/EX12_NEURIPS_CONFORMAL_SHIFT.md) | 11 | `NeurIPS-2019-conformal-prediction-under-covariate-shift-Paper(1).pdf` | `15234a15fc04d6f3d332870c49676327bb0af4352652df3ad7f6ca61b883b905` | 既有全文卡；复用 |
| [EX12](cases/EX12_NEURIPS_CONFORMAL_SHIFT.md) | 11 | `NeurIPS-2019-conformal-prediction-under-covariate-shift-Paper (1).pdf` | `15234a15fc04d6f3d332870c49676327bb0af4352652df3ad7f6ca61b883b905` | **完全相同文件，去重** |
| [EX13](cases/EX13_AAAI_DLINEAR.md) | 8 | `02124-AAAI23.ZengA.pdf` | `365a43dc42b12b28ab9f30d16a5e6900f3970bd3640fab8cc1a2df96d6e6f2dc` | 新增全文卡 |
| [EX14](cases/EX14_ICLR_DOMAINBED.md) | 29 | `1580_in_search_of_lost_domain_gener.pdf` | `41431d2a09d0a28f62c616b8e90d17e71faf72b1cb75d3cba77a47752284a67b` | 新增全文卡 |
| [EX15](cases/EX15_NEURIPS_METRIC_MIRAGE.md) | 17 | `NeurIPS-2023-are-emergent-abilities-of-large-language-models-a-mirage-Paper-Conference.pdf` | `d9e32b422693044e5f5f0714e7758e4abc6f8f8db763de59ecf25a9b7893207d` | 新增全文卡 |
| [EX16](cases/EX16_PATTERNS_LEAKAGE.md) | 13 | `1-s2.0-S2666389923001599-main.pdf` | `8efbd99a03b368b719bc3b9c876c195400dce857968f2dfe043939ebb7af11ec` | 新增全文卡 |

**后续 Agent 处理规则：**

1. 先按 DOI/精确题名 + SHA-256 排重；文件重命名但哈希相同不新建案例；不同版本要先审差异、不要机械覆盖旧策略卡。
2. 原全文仍需合法来源才能回看；读取策略卡不等于读取过原论文全文；每个案例仍需注明页码、适用范围与 AVOID。
3. 此清单只管理**范例来源与原创分析**，不保存科研任务的训练结果；不能转成项目实验记录、科学证实或用户授权。
4. 此批文件没有 SelectiveNet PDF：它仍为 [图谱](RESEARCH_OPPORTUNITY_MAP.md) 中的 `C05 FULLTEXT_NOT_REVIEWED`，**不计入16张全文策略卡**。
