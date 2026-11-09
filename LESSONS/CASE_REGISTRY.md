# 近期科研项目案例台账（2026-10 至 2026-11-09）

> **CASE_INDEX_ONLY / HISTORICAL_EVIDENCE**：这是案例记录与核查缺口，不是科研主控、自动成功评定、可直接投稿结论或额外审批。只在复盘、选题对照、工作流回放、跨项目查重时按需加载；普通科研任务不预读。**SAFE-Gait/APACE 的完整案例仍以 [SAFE_GAIT_APACE.md](SAFE_GAIT_APACE.md) 为唯一详细说明**，本表不复制造成两个权威版本。
>
> **来源与时点**：以用户在 2026-10-24～11-09 的项目执行回报、2026-11-05 的论文/项目交接文档，以及 2026-11-09 的 `NOVELTY_REFRAMING_REVIEW(1).md` v2 为线索。本仓库**没有挂载用户 Windows 的项目原始 Run/SEALED/归档**；报告声称 `VERIFIED` 只表示其作者当时核对过本机工件，并非本仓库独立复算。任何数字都应结合原始工件版本与真实独立单位复核。未在本台账发现的案例，**不等于不存在**。

## 0. 身份、状态与证据的共同口径

- `CASE_ID` 是稳定**研究线标识**，不与可能复用的“项目 N”同义；`PROJECT_NO`、真实任务、数据集、目录、时间快照均须联合定位。重名/重号标 `IDENTITY_CONFLICT`，不强行覆盖其他项目。尤其 **13 ≠ 18 ≠ 21 ≠ 25**，**24 MV-Uncertainty ≠ TacVerse ≠ PMSM**，**29/30 RCT 不等于 31 PTLG**。
- **独立成功轴**：`ALGO_DEV_POSITIVE`（在指定合法 DEV 评价下有正增益），`SCIENTIFIC_RESULT_SUPPORTED`（有受限科研发现/测量结果），`PAPER_PATH_CANDIDATE`（有可审查的论文证据路线），`CONFIRMATION_DONE_SCOPED`（限定义的确认已做）。一个项目可以同时有 `MECHANISM_NOT_SUPPORTED`、`ARCHIVED`、`UNKNOWN`；归档算法分支不取消其它已成立的科学结论。
- **证据层**：`REPOSITORY_LESSON`（仓库现有复盘，但不代表原始复算）；`SECONDARY_LOCAL_AUDIT`（WorkBuddy 报告从本地 JSON/NPZ/稿件核对，本次未直取）；`DOCUMENT_HANDOFF`（用户提供的交接/论文蓝图）；`USER_REPORTED`（聊天或用户表态）；`UNKNOWN`（关键原始证据不可得）。不可把这些升级为 `INDEPENDENTLY_RECOMPUTED_HERE`。结构 CI 只验证案例文本约束。
- **不执行**：此台账不授权下载、拟合/CPU/GPU、SEALED 访问、数据外传、项目解归档、正式论文写作、图片生成或投稿；不含真实受试者个人数据、逐样本预测、原始信号或本地完整源文件。
- **来源简称**：`S19` = 用户提供的 `NOVELTY_REFRAMING_REVIEW(1).md` v2（2026-11-09，包含 19 和 21）；`S19P` = `PROJECT19_MANUSCRIPT_EVIDENCE_ADDENDUM_2026-11-05.md`；`S23` = `Galaxy_HRGuard_论文写作阶段_AI对话重启交接_2026-11-05.md` 及后续论文蓝图；`SCARE` = `传感器算法项目_完整接力汇总_2026-10-26.md`；`STAC` = `PD-RW_Research_Round_2026-11-04.md` 及随后 TacVerse DEV 审查回报；`S24E` = `00_MASTER_HANDOFF.md`（2026-10-03 CATS-PD/TacQuad 早期研究，非最新实验）；`SNEW` = `PD-RW_01_传感器算法研究_2026-11-05.md` 及后续 WorkBuddy 状态；`CHAT` = 用户聊天报告（原始工件未在此核对）。上述交接材料不自动公开上传到本仓库，文件名用于用户环境内溯源。

## 1. 已识别案例（成功、失败、边界、数据与未完成项均保留）

| CASE_ID / 号（非强制唯一编号） | 已有证据与真实结果（严格限定义） | 各成功轴 / 当前边界 | 来源 |
|---|---|---|---|
| `APACE-K0`（早期） | 无目标标签的主动校准；Oracle 理论机会约 8–10%，可部署选择策略未稳定胜简单方案 | `MECHANISM_NOT_SUPPORTED`；与 SAFE-Gait 后来改 K=1 是**不同信息条件** | 仓库 [详细案例](SAFE_GAIT_APACE.md) |
| `SAFE-GAIT-K1`（鞋垫成功） | 监督 K=1 残差校准后的跨步态条件迁移；步长在所报四个数据集/方向组合 +8.45～35.61% MAE 改善，速度混合，步时不稳 | **`ALGO_DEV_POSITIVE`**、窄范围科研贡献；非跨平台共享模型权重或全目标稳定改善 | 仓库 [详细案例](SAFE_GAIT_APACE.md)，`CHAT` |
| `CARE-TOUCH`（旧目录 4.care） | 主动触觉读取/动作预测；修正 belief-age 偏差后，“主动选择读取时机”未可靠超过周期/简单读取；触觉可预测残差的某些探针有正信号 | 原主动策略 `MECHANISM_NOT_SUPPORTED`；不是触觉感知普遍失败 | `SCARE`、`CHAT` |
| `PHYSTOK`（旧目录 5.phystok） | 触觉离散 Token/事件；早期连续表征 AUROC≈0.873，离散 Token≈0.847（当时协议）；其他接触 onset/未来预警结果受到真值、对照及同步限制 | Token 核心增量 `MECHANISM_NOT_SUPPORTED`；不能将有效事件检测与循环定义真值混为算法进步 | `SCARE`、`CHAT` |
| `HAPTILE-DATA`（两项目共用资源） | 作者邮件与采集代码澄清 Action/时间戳/单位与对齐；数据语义复核是准入工作 | `DATA_SEMANTICS_REVIEW`，**不是单独算法成功/失败**；不能把 CARE 与 PhysTok 合并 | `SCARE` |
| `CAR-IMU`（早期 IMU） | 工程测试与短片段运行有报告；跨系统同步、单位和标定独立验证不足 | `ENGINEERING_PARTIAL`、`ALGO_CLAIM_UNKNOWN` | `CHAT` |
| `REVGRAPH`（早期） | M1 与正式 MVE 运行受工程/预算阻断；未建立可信完整算法比较 | `BLOCKED` 而非算法被证伪 | `CHAT` |
| `CC-DRA`（气体漂移，历史号14） | 跨日适应 M1 相对简单 M0 约 −0.041 macro-F1（历史报告）；跨日机制/标签与可泛化性有不足 | 新对齐机制 `MECHANISM_NOT_SUPPORTED`；精确结果/协议待本机复核 | `CHAT` |
| `RISC-SENSE`（历史号15） | 简单受监督个性化 SVM/基线在合法 K 条件下有效；M1/M2 对强基线增益约 +0.005 且不显著，复杂 M3 跨人下降 | **`BASELINE_POSITIVE`**，新复杂机制 `MECHANISM_NOT_SUPPORTED`，不能全项目归零 | `CHAT` |
| `CRIA`（历史号16） | 真值邻域择优导致虚假的 GO；改正因果评价后新触发器未优于简单力阈值 | `INVALID_OLD_GO`、新算法 `MECHANISM_NOT_SUPPORTED` | `CHAT` |
| `ACRF-RCT`（历史号17） | 跨条件/跨传感器残差 ICC 较低，复杂触觉校准未证明稳定优势 | `MECHANISM_NOT_SUPPORTED`；不推断所有触觉校准不可能 | `CHAT` |
| `SRCS-IMU-P13`（项目13） | 30 人、17 佩戴位置；单 IMU/位置迁移及稀疏校准实验的结果存在不同版本，已见开发集正向分支但未建立独立泛化定论 | `DEV_FINDINGS_PRESENT`；项目13于 11-04 标记 `ARCHIVE`；不可与21/25串号 | `S19` §0、`CHAT` |
| `SINGLE-IMU-P18`（项目18） | 17位置跨人 HAR，部分位置迁移有正向结果，机制 M1/M2 未充分证明额外收益 | `SCOPED_RESULT_CANDIDATE` / `MECHANISM_UNVERIFIED`；不能与23的 GalaxyPPG 受试者接触史等同于同任务 | `CHAT` |
| `CRFW-P19`（项目19早期） | REASSEMBLE 上约3s提前失败预测，最强方案未提供稳定时间建模增益；随后另立低层技能任务 | 原 Task `MECHANISM_NOT_SUPPORTED`；**成功转向 ≠ 原 Task 复活** | `CHAT` |
| **`CRPS-P19`（项目19）** | 预测父动作后验+本体/力觉低层技能识别，主对象折 `SF=0.6717`、`GRUctx=0.7135`，segF1 **+0.0418**；算法轮 GRUctx `0.7091` 为另一构造，不能拼表 | **`ALGO_DEV_POSITIVE` / `PAPER_IN_PROGRESS`**；全 Episode 边界 F1 未改善；37 条 SEALED 跨录制确认 `NOT_RUN`，不能称部署/独立泛化成功 | `S19` §1–3，`S19P` |
| `TACTILE-DATA-P20`（项目20） | FeelingOfSuccess 与 GraspStability 数据获取和 CRC 验收报告；尚无在该项目成立的独立算法胜负结论 | `DATA_ACQUIRED`，算法 `UNKNOWN` | `CHAT` |
| **`PRELIFT-F3-P20`（项目20后期算法）** | 2026-11-08 报告的 pre-lift 四指时间中心化空间动态8维触觉特征 F3；同设备未见物体独立 SEALED（9物体/339试次）：物体均值 AURC **0.279983** vs F3-base **0.516129**（Δ−0.236145，95% CI [−0.354329,−0.118586]；8/9物体有利，p≈0.01172）；pooled AUC **0.749707** vs **0.536927** | **`ALGO_DEV_POSITIVE` / `CONFIRMATION_DONE_SCOPED` / `SCIENTIFIC_RESULT_SUPPORTED`**；排序有效不等于概率校准/Brier/ECE 有效，亦非跨设备、多中心或在线部署确认；本仓库尚未独立读取 F3 原始 Run | `CHAT`（2026-11-08本机报告，原始 Run 待导入） |
| **`DUAL-IMU-P21`（项目21）** | HARTH/HAR70+/MHEALTH/PAMAP2 线；both6 macro-F1 `0.9728`、micro `0.9880`；oracle-OR `0.9854`，净 79 窗但一人占 +92；容量置换对照 `NOT_RUN` | **`BASELINE_POSITIVE`**、协同/因果解释 `WITHDRAWN`；`AREA_DATA_PIVOT / CURRENT_PROJECT_ARCHIVED`（最新 manifest 76 文件），非 SRCS-IMU 原始线 | `S19` §0、§4–6 |
| **`GALAXY-HRGUARD-P23`（项目23）** | 16 人 DEV 24,924 参考有效窗（726 wrong、2,723 missing）；5 人同数据源确认 7,713 窗（147 wrong、1,066 missing）；确认队列的不可靠窗中 missing 约 **87.88%** | **`SCIENTIFIC_RESULT_SUPPORTED` / `CONFIRMATION_DONE_SCOPED` / `PAPER_PATH_CANDIDATE`**；强预测新算法的普遍部署收益 `NOT_SUPPORTED/ARCHIVED`；5人、跨项目接触史限制“完全独立”说法 | `S23` |
| `CATS-PD-TACQUAD-EARLY`（项目24相关早期线） | 2026-10-03 TacQuad 输入/弱序列配对 pilot：112 records / 1,896 files；B Test MRR≈0.750，shuffled 同≈0.750；sensor probe 100%、effective rank≈1.1–1.4，物理不变表征受外观 shortcut 与低秩阻断 | **`EARLY_MECHANISM_NOT_SUPPORTED`** / `FULL_LOSO_NOT_RUN`；是早期 CATS-PD 阶段，不得用它覆盖后来 MV-Uncertainty-RealData-Launch 的独立结果或用户成功判断；后续同一命题身份尚需项目原件复核 | `S24E` |
| **`MV-UNCERTAINTY-P24`（用户确认的项目24）** | `MV-Uncertainty-RealData-Launch`，已报告 17 幅图、34 份 PNG/SVG 和图件审计 PASS；用户明确认为该项目成功 | **`USER_ASSERTED_SUCCESS` / `ALGO_FINAL_METRICS_UNKNOWN`**；图件 PASS 不是算法效果或论文证据验证，待读取项目真实 RESULT/Run/冻结表 | `CHAT`（2026-11-05、11-09）；原始结果待补 |
| `PMSM-THERMAL`（曾被称“项目24”的**冲突别名**） | 电机温度线：简单 B2 OOF MAE≈4.010°C；双时间尺度/观测器候选 E2≈4.825°C（历史报告），未优于简单方案 | `MECHANISM_NOT_SUPPORTED`；**不覆盖**正式项目24 MV 的身份；项目号 `IDENTITY_CONFLICT` | `CHAT` |
| `LR-IMU-P25`（项目25） | SRCS-IMU 数据上的窗口级 HAR 因果平滑；frame/window 增益大部分可由平滑解释，历史前沿 F1≈0.8040、延迟≈1.80s（对应特定条件） | `SCOPED_MEASUREMENT_RESULT` / `NARROW`；**不同于项目21**，不能拼其 ρ、F1、归档状态 | `S19` §0、`CHAT` |
| `BATTERY-TRIAGE-P26`（项目26） | Severson LFP 电池早期 QC：协议/批次泄漏风险、前 N 周期 Task 已设计；无经证实算法结果 | `WAITING_FOR_DOWNLOAD_AUTH` / `NOT_RUN` | `CHAT` |
| `TACVERSE-Q0-P28`（项目28 或 TacVerse 独立线） | 力标签物理语义 D1/Q0 审计后，证据不足以支持原跨传感器绝对力的科学命题；数据资产可保留，最终任务 `NOT_READY` | `SCIENTIFIC_HYPOTHESIS_CLOSED` / `DATA_ASSET_PRESERVED`；**不是项目24 MV 成败**，原始 TacVerse 数据下载状态随 11-04/11-05 已发生变化，不能用早期 WAITING_FOR_DATA 覆盖后期审计 | `STAC`、`CHAT` |
| `RCT-IDEA-P29`（项目29） | RCT 材料/触觉新问题只读选题；早期官方元信息：122 材料、1,832 序列、3 DIGIT；首选后调整 | `DESIGN_ONLY`，不是算法成功或失败 | `SNEW`、`CHAT` |
| `RCT-CONTACT-P30`（项目30） | RCT 数据后续 DEV 验收与分组，所报98材料、979 DEV 序列、2个传感器；独立确认隔离；R1 未通过题目价值验证 | `DATA_READY_DEV` / `HOLDOUT_SEALED` / `RESEARCH_PIVOT`，未证算法效果 | `CHAT` |
| `SENSOR-A01-P31`（项目31早期） | 创新方向 W1 与直接原文近邻或数据可辨识性不匹配，活动01 未确认首选 | `DISCOVERY_PARTIAL` / `NO_SELECTED_TASK`，**不等于 PTLG 失败** | `CHAT` |
| `PTLG-P31`（项目31后续 RCT 方向） | 视觉—触觉—语言物理证据约束、冲突时材料属性推断和证据不足时选择性预测；复用已有 RCT 数据资产的只读科学适配/创新审查 | `QUESTION_CANDIDATE` / `REFRAME`；没有合规的新训练/SEALED/论文级算法结果，不把 E0/E1 方案当已执行 | `CHAT`（2026-11-09） |
| `MCS-HEMO-AURICLE`（未锁定编号） | Auricle 头部20通道心电/血流采集数据；后续报告 56 DEV / 14 SEALED、文件完整性检查、重复记录与噪声发现 | `DATA_QA_DONE_REPORTED`，算法 `NOT_RUN/UNKNOWN`；初期“未下载”的早期快照已不是最新状态 | `CHAT` |
| `OPENPACK-RELATED`（历史比较） | 动态策略的输入可辨识性和简单参照饱和曾被讨论；缺本机当前完整 Task/Run/分组索引 | `EVIDENCE_INCOMPLETE`，不能凭提及就判算法失败 | `CHAT` |
| `REALDISP-SHIFTSYM-BEAM`（历史线索） | REALDISP / ShiftSym-HAR / BEAM-HAR 只见讨论名称，缺逐项目最新工件与终判 | `IDENTITY_OR_EVIDENCE_UNKNOWN`，**仅登记线索** | `CHAT` |
| `RASS-EXATHLON-SAFESELECT`（历史线索） | RASS/Exathlon / SafeSelect 等只见方案或负结果片段，缺同一协议的可核比较与终判 | `EVIDENCE_INCOMPLETE`，不计入成功/失败统计 | `CHAT` |

> **项目编号防污染**：本表中的“项目 N”反映用户在不同时点的命名，不是全局唯一主键。特别是旧消息中 `Galaxy-HRGuard` 曾被误说成18、`PMSM-CausalThermal` 曾被说成24；本台账保留历史别名但**不修改已建立的19/21/23/24/25目录事实**。没有目录/manifest证据的编号只做可疑别名，不作最终注册。

## 2. 最应保留的跨案例教训（用于提出问题，不作为完成证据）

| 比较 | 有效信息 | 不应得出的结论 |
|---|---|---|
| APACE → SAFE-Gait | **信息条件变化**（决策前 K=0→合法 K=1 残差）比再加网络更能解释成功转向 | 把 K=1 的收益说成零标签主动策略成功 |
| CRFW → CRPS | 同数据中的失败预测 Task 与9类低层技能 Task 是不同科学问题；后者有正向 DEV 算法增益 | 因早期 Task 失败判整条数据/机器人研究无价值 |
| RISC-Sense / 双 IMU21 | 简单/多输入的强基线可能有效，但复杂模块附加科学贡献不成立 | 总体准确率高即自有新算法成功，或某个机制负结果即整个项目失败 |
| CRPS19 / Galaxy23 | **算法指标正向**与**连续部署/评价合约**并非同一主张；三状态测量结果可以独立有论文价值 | 把 segF1 增益说成跨录制确认，或把 HR 强预测路线 ARCHIVE 说成全项目失败 |
| 项目24 MV / TacVerse / PMSM | 编号相似或被历史误用时，必须用任务+目录+原始 Run 锁定身份；图件通过、标签审计、拟合结果是不同对象 | 混合三个项目的成功、失败、数据或封存状态 |
| 项目13 / 18 / 21 / 25 | SRCS-IMU 是数据集名，双IMU-HARTH和窗口平滑是不同 Task/冻结切分；独立单位通常是人而非窗口 | 将不同项目的数值、受试者ID、结论拼成一个“最新性能” |
| 项目20 数据准备 → F3 独立确认 | F3 在固定同设备/未见物体范围给出可重复的排序改进，必须保留确认指标和校准未完成的界限 | 将较早数据验收快照当成项目最终结论，或从 AURC/AUC 直接宣称 Brier/ECE、跨设备可靠性 |\n| TacVerse / RCT / Auricle / Battery | 数据验收或理论可行性是科研资产，尚未建立算法胜负 | 下载 CRC PASS、合成测试 PASS 或论文路线图即算法成功 |
| 旧负结果重释 | 事后重要问题可以生成新假说，但应保留强反解释、真实最近邻和缺少的判别证据 | 将 `EX_POST_REFRAMING` 误写成事前假设或已确认原创新 |

## 3. 实际缺口清单（按价值排序，原始文件不在仓库时不得造值）

1. **P20-F3 确认补录**：取 11-08 一次性 SEALED 对应真实评价协议、9物体/339试次结果表、F3-base/F0 参照、代码及选择史；核对独立单位。Brier/ECE 尚未确认，**不能仍把整个项目20记为只完成数据下载**。
2. **P24-MV 最紧缺**：核项目实际 `PROJECT_SPEC/STATE`、最新算法 Run/冻结协议、最强基线配对指标、原始科研成果总结及确认结果、论文状态。用户成功认定保留 `USER_ASSERTED_SUCCESS`；不能由17图 PASS 推断算法胜利，也不能因缺证据判失败。早期 CATS-PD/TacQuad 负结果单独保存，是否同一最终 Task 待核。
3. **P19-CRPS**：对象折父动作预测精度未持久化；readout 保留帧特征对照 `NOT_RUN`；37 SEALED 跨录制确认 `NOT_RUN`；v2/旧日志不同 Run 不能混数。其合法 DEV 算法成功保持有效，不自动开展推理/训练。
4. **P23-Galaxy**：强预测在线增益未被证实；已成立的窄测量结果与5人同源确认单列；图/稿件是否完成以本机最新版本为准，不宣称外部多中心验证；正式写作权限仍须独立核实。
5. **P21-HARTH**：容量匹配置换对照 `NOT_RUN`；未拟合的 `N2dc/N2dp` 不得视作负结果；归档只读；缺历史源码不可冒充全部实验可复现。采用 `S19` v2 的76文件而非早期74文件。
6. **项目身份冲突**：P24 MV vs PMSM/TacVerse；13/18/21/25；项目31 W1 vs PTLG；必须由真实 `PROJECT_PATH/Task/PRIMARY_DATA/ARCHIVE_MANIFEST` 唯一定位。
7. **早期案例及未完成选题**：CARE、PhysTok、CC-DRA、RISC、CRIA、ACRF、CAR-IMU、RevGraph、P18/P25/P26/P28/P29/P30/P31/Auricle 尚缺跨版本 Run ledger 或本仓库可独立验证的终判；只保留真实可追溯快照，不造结果。
8. **仅有名称的候选**：不能拿来算项目总量、总成功率或“所有算法失败”；因项目多 Task 与编号复用，**全时期真正独立项目总数 UNKNOWN**。
9. **GitHub 无法补齐的原始信息**：用户 Windows 私有项目工件未全部同步。本仓库只能记录来源和缺口；将来能访问本机且获相应授权时，优先只读核对，不进行拟合、SEALED 或归档修改。

## 4. 轻量维护、使用与验证

- 只在出现**新项目、真实状态/证据改变、身份冲突修正或新增经核对来源**时增量编辑受影响 CASE 行；每个案例先保留 **正结果+负结果+来源+独立单位/确认状态**，不删除旧负结果、也不为补齐状态编数值。不要求每个真实项目生成新的长文档、JSON或第二份案例。
- 项目自己的 `RESEARCH_RECORD.md`、`PAPER_BLUEPRINT.md`、`STATE/Run/ARCHIVE_MANIFEST` 仍是**实际权威**；此表只是跨项目索引，不覆盖本机归档，且不取代写作权限。真实可回放案例需另依 [REPLAY_PROTOCOL.md](../REPLAY_PROTOCOL.md) 冻结**当时**可见信息，禁止把事后案例卡当成已盲法测试。
- RWF 只引用这一份 PD-RW 案例台账，用于选择可复算的案例或审查无效实验；不在 RWF 再复制科研结论。按 [docs/STRUCTURE.md](../docs/STRUCTURE.md) 的“单一权威+替换优先+按需加载”维护，避免再次造成 Agent 上下文膨胀。
