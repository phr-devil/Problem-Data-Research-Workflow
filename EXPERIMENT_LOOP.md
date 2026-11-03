# 活动 04｜可运行实验、信息驱动迭代与自动恢复

**执行前提**：新实证项目必须先有本轮必需数据的 `DATA_ACQUIRED_VERIFIED` 和可用开发数据，才可进入`DISCOVERY/BASELINE/IMPROVE/MECHANISM_TEST`；未完成时仅允许 `ENABLEMENT` 中的下载、文件校验和解析冒烟，不训练也不报告全库结论。理论/仿真按已声明证据路径执行。**本文件只负责怎样获得可信 Run**；“研究什么”见 [TASK_EXPLORATION.md](TASK_EXPLORATION.md)，KEEP/HOLD/PIVOT 的科研范围和授权由 [WORKFLOW.md](WORKFLOW.md) 唯一控制。首次探索不需证明新网络超过强基线或补完全部消融。优先可信`PERFORMANCE_FLOOR`与最低`PAPER_PATH_CANDIDATE`，再渐进增强科学性，见 [PAPER_FIRST.md](PAPER_FIRST.md)。具体接口、行为测试与训练故障诊断按需读 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)，不是每轮都必须加载。

## 1. 按当前问题选择模式，而不是逐一闯关

- `DISCOVERY`：合法开发数据的真实观察、残差、时间/物理/组别检查；无拟合权限时不可训练 CPU Ridge、tiny-set、聚类模型或 GPU 参数。
- `ENABLEMENT`：修数据读取、时钟/单位/同步、标签、评价器、训练稳定性；工程能力恢复可以独立验收，不用虚构增益。
- `BASELINE/IMPROVE`：准备做性能比较，先获得简单可信基线与合理调优，确保同任务、合法输入、分组、评价分母和公平资源。
- `MECHANISM_TEST`：需要机制归因时才写竞争解释、不同预测或正控；无归因需求不强迫 A/B。
- `CONFIRMATORY`：只在冻结 Claim/协议并获授权后转 [CONFIRMATION.md](CONFIRMATION.md)；不在探索内循环反复打开封存集。

## 1.5 双轨算法开发：稳妥结果 × 创新探索（按证据分配，而非双模型硬并行）

**默认最低必要复杂度，可跳过已有项**：真实数据/评价 → 复用或授权后建立简单可信同K参考 → 检查组级残差、合法预测信息 → 最小规则/校准/线性/轻量模型或正控 → 仅为明确剩余瓶颈或不同机制预言引入复杂模型。按A只读诊断、B轻量拟合、C复杂训练分配预算（不是固定GPU时长门槛）；真实时空建模需求可直接进入C，但先明确必要性和廉价判别。复杂模型失败不能覆盖简单模型和已经核验的结果。


- `RELIABLE_TRACK`：共享合法数据/评价器/基线，优先获得可复现性能、可解释的失效边界或成本—性能规律；这是研究资产，**没有独立近邻差额不能自动称论文保底**。
- `NOVELTY_TRACK`：从已核残差、真实任务约束和具名近邻缺口提出差异化机制、能力或规律；其失败只更新对应机制/Claim，不丢弃可靠结果。
- 两轨**不是两套固定预算/审批**；不要求双模型同时训练。同一Agent按`NEXT_PROBE`的信息价值和总成本选其中一轨，也可一个实验同时服务两轨。保留现有最简单可信Champion和最多一条**不同失败前提**的活跃Challenger；多分支仅在有新解释或可辨别结果时启用。旧Run、负结果与Checkpoint按既有路径复用。

## 2. Agent 一次性执行合同（跨平台交接）

ChatGPT 只传已核实的问题—数据、TASK、最大 UNKNOWN、证据指针、冻结资产与真实授权范围；WorkBuddy/Codex 应先核本地 STATE/manifest/Run及必需数据的真实下载/验收状态，不假定聊天里写的路径或权限真实存在。缺数据先返回 [DATA_DISCOVERY.md](DATA_DISCOVERY.md) 完成授权内下载与验收，禁止先写模型再等数据。不同步时以原始证据和最新用户消息为准，不重复下载或建立空目录。

> **GOAL**：当前 TASK_ID 的最有信息价值 `NEXT_PROBE`，说明可能结果会怎样改变决策及总预算。
>
> **EXECUTE**：复用 `BEST_VALID_RUN` → 真实开发数据读取与最小受影响检查 → 必要实现/局部修复 → 公平简单基线或判别试验 → 留存代码/协议/预测/原始指标/负结果 → 定向回归；已批准范围内连续处理关联小问题。
>
> **PROTECTED**：标签及原始血缘、合法 group/split、评价器、未接触确认集和用户冻结内容。**EDITABLE**：当前批准范围内模型、特征、Loss、普通调参。变更时间/标签/协议需要新版本，只重算受影响 Run，不能静默覆盖历史。
>
> **OUTPUT**：实际新增 Run/观察、原始路径、相对公平基线的效应及独立组不确定性（不具备则 UNKNOWN）、修复及验证结果、成本与唯一下一探针；没执行写 NOT_RUN，崩溃记 PARTIAL/CRASH。

### 新机制设计前的最小假设（不额外开审批门）

对真正改变机制/信息/任务能力的Challenger，附一行`ALGORITHM_HYPOTHESIS = ERROR_PATTERN | MECHANISM_LEVER | STRONG_SIMPLE_ALTERNATIVE | DISCRIMINATING_SIGNATURE | PROBE(+POS/NEG/INVALID决策) | COST_CAP`。假说可由数据、物理或文献驱动；初始仅标`HYPOTHESIZED`，不要求预先证明正收益。纯工程修复、超参调优或基线复现不必造“新机制”。

优先检查该方法**凭什么有新增能力**：`EXTRA_INFORMATION`（部署前合法信息）、`INDUCTIVE_BIAS`（物理/结构约束）、`OPTIMIZATION`（同一目标更可训练）、`CAPACITY`（模型表达力），或明确的新成本/可靠性规律。若四者均无差异，可能只是换名。先给出区别于公平简单替代的合法、可观察预测；不强制每次设计全套消融。

**论文驱动的实验选择**：当已有一项可信增量贡献候选时，优先执行能证明该Claim的最小公平比较、分组稳健性、速度/标定成本测量或关键消融；不因未达全局SOTA而默认扩网络/多库。允许真实成本—性能权衡（部分指标下降），但必须报告负面指标、相同合法输入/预算和适用范围。RWF按需复核可信Run，PD-RW决定论文主张。

## 2.5 任务阶梯的实验复用与公平条件

当实际 TASK 属于 [TASK_LADDER.md](TASK_LADDER.md) 的某层时，**一次运行只服务一个明确协议与层级**：保存 `level_id / task_id / K_target_labels / inference_visible_info / group_split / protocol_id`（旧Run已有等价信息可用路径引用）。跨层共享L0数据血缘、评价器实现与简单基线代码；若L2允许K-shot而L3不允许，必须**分别**训练/评价并公平比较各自合法对照。不能把增加标签后的指标涨幅归因于新算法本身，也不能把目标标定样本同时当无偏测试样本。

**最低成本的级间探针**：先找本层是否有真实剩余误差/可纠正干预→核本层可用信息与简单参照→再考虑模型复杂度。若 L3 无标签机制无法利用合法信息，可在已批准的开发池尝试 `DOWN` 到L2的少标签标定（此时**新TASK/协议/Claim**），并和同K强简单基线比较；若失败原因只是短训欠收敛，先修当前机制而不是自动降级。层级转换时旧 Run 成为共享观察/基线资产，**不得无条件继承其科学效应或确认资格**。必要时用正控与短/长锚点，但不是固定强制实验。

## 2.7 固定评价下的 Champion–Challenger（只在真正比较方法时使用）

借鉴 autoresearch 的**稳定评价＋完整尝试日志**，但不复制其无限运行或只用单一最佳分数KEEP的准则。

- **Champion** = 当前`BEST_VALID_RUN`中的最简单可信参照，保留其预测/指标/代码/协议作为`VERIFIED_REFERENCE`（DEV证据，并非独立论文确认）；**Challenger** = 本轮唯一有明确科学差异的候选。固定`task_id / level_id / K_unit / legal_inputs / support_query_policy / group_split / evaluator_version / budget_basis`；若某字段不同，标`NOT_COMPARABLE`，可以研究成本—性能曲线，但不能写同等信息条件下的算法提升。
- **执行前一句话**：`HYPOTHESIS | WHAT_CHANGES_ONLY | EXPECTED_OBSERVATION | DECISION_IF_POS/NEG/INVALID | COST_CAP`。少量参数共同调整可以属于同一机制假设，不要求一次只改一行代码；但关键因果解释必须能排除简单竞争因素。
- **执行后证据**：配对group差异/合理不确定性、完整训练收敛或必要正控、代码与配置版本、真实独立单位数、额外标签/算力成本、失败结果及可重现原始路径。小收益不能靠挑最优seed升级为论文主张；负Pilot不自动判全部机制不可学。
- **不同状态有不同动作**：`INVALID`（数据/评价失效）只隔离并定向修复；`NOT_COMPARABLE`先明确预算/输入差别；`INCONCLUSIVE`按是否存在廉价辨别选择继续或HOLD；`COMPARABLE_POS/NEG`仅更新当前机制证据，若触发不同科学任务的研究则交 [TASK_LADDER.md](TASK_LADDER.md)。
- **预算策略**：不强制每个任务短/长和多seed；当欠收敛、容量或数据尺度可能改变科学结论时才成对扩容。升级实验需要说明“若结果A/B出现，将改变哪个决定”；连续试验无新信息时停止**本分支**，保留有价值的开发观察与失败证据。

### 公平调参与计算投入的触发条件（按需）

区分`scientific`（研究机制变量）、`nuisance`（各法合理调优的学习率、正则、epoch）、`fixed`（任务/标签/合法输入/group/evaluator）。记录各法搜索范围、次数、预算；基线欠调参而候选充分搜索不能证明创新，联合改动也不能声称单模块因果归因。

扩大GPU只在可能改变决定时：末尾checkpoint还在改善→成对延长；容量不足有证据→成对小/大；独立组不确定→优先更多合法group而非无限seed；标签/梯度/评价错误→先修复。不得以GPU占用率作为目标，仍受真实授权上限约束。

### 多数据库实验结果的边界（仅跨库执行时读）

沿用`DATA_PORTFOLIO`中D1–D4的`DEV_SHARED/PIVOT_RESERVE/SEALED_CONFIRM`用途角色；可同时在多库开展开发，开发集发现问题与选模，外部库按预定的**任务映射、合法标签预算、独立group和确认用途**评估。可分别训练/适应，但必须报告跨库哪部分共享机制、哪个新条件被测试；不把不同库的原始分类F1直接相加，也不把D2用于调参后仍称未触碰独立确认。单库正结果先标`SINGLE_DATASET_EVIDENCE`，多库独立增益必须靠真实可比数据与对照支持。

### 结果反馈：一次迭代要回答一个决策问题

**负Pilot归因记录**：沿用本文件现有INVALID/UNDERTRAINED/COMPARABLE_NEG/MIXED分类，优先排代码与评价错误、基线不公平、欠收敛，再考虑机制假说；仅查相关项。按需更新既有Run/STATE中的BRANCH_ID、FAILED_PREMISE、NEXT_DISTINCT_PROBE和CUMULATIVE_COST。预算阈值触发复盘，不能自动扩写为项目STOP。

`INVALID`（泄漏/真值/评价/代码缺陷）→定向修复与受影响回归，不作科学否定；`UNDERTRAINED`→必要时公平成对延长/调优；`COMPARABLE_NEG`→定位是否假说/信息前提未成立，考虑更简单方案或不同机制；`MIXED`→查独立group、成本与切片选择历史；`COMPARABLE_POS`→核强简单替代及对应`CLAIM_EVIDENCE_MAP`；`INCONCLUSIVE`→只追加可能改变决定的有界探针。保留失败Run；如无新增信息且成本不值得，HOLD**当前分支**而非AREA_DATA。

采用AIDE/MLEvolve式**有界经验复用**：在现有`RUNS.tsv/STATE`中记录`parent_run / failed_premise_or_signal / reusable_asset / next_distinct_lever`（可用既有字段则不扩列）；分支融合只有在信息预算、机制前提及评价协议兼容时才试，不默认树搜索、向量数据库或多Agent。失败的解释只限本次有效证据，欠训练不等于证明机制不可学。

### 从诊断到一个新机制的最短循环（AIDE/R&D-Agent式经验复用）

已有负Pilot分类保留；若不是评价无效、训练不足或基线不公，才用`error_evidence_refs → failed_premise → competing_explanation → mechanism/lever → distinct_prediction → minimum_test → if_positive/if_negative/if_invalid → estimated_cost/authorization_scope`形成**一条**`PROBE_CANDIDATE`（按需记JSON，不强制所有Run产出）。`python -m core.cli probe-check --file probe.json`仅检查假设是否有可分辨的实验承诺，不会训练，也不会证明机制创新。对已失败的同一前提优先复盘/寻找新杠杆，而非换网络名字续命；保留旧Run与parent关系。预算阈值只触发复盘/授权检查，不做项目自动STOP。一个有效实验可同时服务可靠性能与机制诊断，不必强制双轨GPU并行。

## 3. 正负 Pilot 后的按症状实验选择

**APACE → SAFE-Gait 型故障的最短实验（必要时才触发）**：`ORACLE_GAIN>0` 且真实动态策略不胜固定/随机参照时，先确认训练/协议有效，再在 DEV 上检查最佳动作**在决策前是否可预测**；可见输入近似但最优动作不同，应怀疑隐藏信息或不可辨识性（不凭少量样本证明不可能）。若实际应用可合法获得一次目标残差或历史反馈，提出 `K=1` 新 Task，核标定发生于 query 前、support/query 无交叉、同 K 简单残差修正/收缩、标签成本及独立组；不要继续仅靠大模型调参追回 Oracle。若结果按目标/方向不均匀，转为条件特定的机制/边界检验，不能事后把最好切片包装成普适成功。[案例](LESSONS/SAFE_GAIT_APACE.md)。


| 当前证据 | 优先最小动作 | 不能推出 |
|---|---|---|
| **负 Pilot** 且欠收敛 | 核评价/梯度/正控/合理超参，必要时合法短/长训练锚点 | 一次负结果意味着机制或项目 STOP |
| 简单基线饱和、新模型无增益 | 开发组配对残差、简单替代、可用新信息与任务价值 | 特权 Oracle 差值是可达收益 |
| 训练好但跨人/设备/日变差 | 核 train-only 归一化、时序和合法 group；简单校准 | 随机帧高分代表外部泛化 |
| 模态互补但动态选择不好 | 可纠正性、激活前可辨识性、同成本固定策略 | Oracle 互补意味着可学习门控 |
| 微弱正收益或简单模型更好 | 同协议组级效应与异质性、强简单解释、近邻差额 | 幸运 seed 证明独立论文贡献 |
| 熵下降但真实指标下降 | 已知扰动正控、干预单位和独立标签指标 | 置信度改善等于校准成功 |

**继续/扩大训练的条件**：先验证结果有效，再试最便宜的竞争解释，并遵循 §2.7 的公平 Champion–Challenger 合同；只有规模/时长可能改变判断、授权允许且成本合理，才运行成对小/大、短/长锚点或更大 GPU。`INCONCLUSIVE` ≠ REFUTED，不要求无限追加 seed；小增益同样需要核公平性。实验结果应对应新信息或恢复必要能力，而不是为了占满显存。真正科学止损由总控按证据范围处理。

## 4. 自动纠错复用第八章

`CRITICAL`（已证实泄漏、假真值、越权、关键平台不可用）只阻断受影响动作/Claim；`REPAIRABLE` 在原授权内定向复现→最小修复→相关回归→恢复；`MINOR` 记录或顺手处理，不中断。科学负结果不作为 Bug 强行“修正”。真实故障时按 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) 做定向诊断与最小恢复，不改变PD-RW路由与授权。

修复后原失败测试实际通过才能报已修复；未验证标 NOT_RUN。**Run 证据与负结果不得被回退丢失**：代码即使回退仍保留原 Run 的 commit、数据/协议版本、合法逐样本预测和负证据。已污染或失效的指标只标 INVALID，不用于科学判决。

**证据交接**：有效Run保留task_id、protocol_id、dataset_version、evaluator_version、group_split、sample_ids_hash、legal_inputs及原始指标/逐样本预测/代码配置路径；使用机器索引时参见[core/README.md](core/README.md)，校验器只核结构和记录的可比性，不认证科学因果。

## 5. 可恢复证据和 Token 预算

复用现有 STATE/RUNS，记录 `run_id | task_id | parent_run | data_version | protocol_id/evaluator_version | code_commit | seed | auth | cost | status | metrics_or_observations | raw_paths | decision_scope`，只读最近有效 Run 和当前相关代码；不重复训练已验证结果。`KEEP/IMPROVE/REPAIR/INCONCLUSIVE/DISCARD` 先限定 RUN/机制，不能因单次结果把 AREA_DATA 判失败。

**默认按[WORKFLOW.md](WORKFLOW.md) §5最短输出**：Run、代码、失败证据与必要诊断图保留路径，只报两轨判断变化和NEXT_PROBE；不贴全部日志、反复渲染曲线或制作论文级图片。`无限循环`和流水账都不是目标。

**轻量成本预检（只在实际分支需要时）**：Probe可选填GPU/CPU/人工时和Token数值预算；用`probe-check --remaining-budget-file`与当前可核实剩余预算比较。超额只触发重新规划或真实授权，不默认否决科学命题。

## v1.6｜负Pilot原因优先，非通用再调参

只在有真实新证据的分叉点执行：

- `INVALID`（真值邻域取峰、未来特征、支持/查询交叉、聚合错位）：隔离受影响结果，修最早错误并定向回归；**不在坏评价器上继续调参**。
- `UNDERTRAINED`：以有预算上限的成对小/大训练或梯度/收敛诊断鉴别，不要求完整重训全库。
- `INFORMATION_LIMITED`：核可纠正性与决策前可预测性；若K或可见信息真实改变，按Task Ladder生成新Task/协议/Claim，旧零标签Claim保持失败边界。
- `BASELINE_DOMINATED`：保留简单Champion及负Run，暂停同前提复杂模块；比较不同可检验机制、任务边界或新规律。
- `CLAIM_UNSUPPORTED`：核具名近邻及实际独立价值，允许NO_INDEPENDENT_CLAIM；工程资产可复用。
- `INCONCLUSIVE`：用独立组效应量与不确定性决定下一廉价实验，不能把CI包含0直接写成机制已证伪。

以上是诊断标签不是额外必填清单或自动STOP。若有已记录且可靠的评价与数据证据，直接续用，不重复做全套正控/训练。可选`failure-check`只分类Agent提供的证据指针，真实动作仍由原`WORKFLOW.md`与授权决定。

### 由剩余误差提出真正的新机制（只在机制开发时执行）

读取最近**可信、同 Task/同合法信息**的 Run 与可行性画像：对已有可靠残差提出 `ERROR_PATTERN → REASON_EXISTING_BASELINE_MISSES_IT → LEVER → DISTINCT_PREDICTION → MINIMAL_TEST`。新机制必须比简单参照多利用某种*可检测*信号、归纳偏置、优化能力或实际资源限制；若只是更复杂的模型名称，先不要投入昂贵 GPU。若 DEV 结果无增益：先排评价失效/欠训练/不公调优，再检查信息缺口或换机制，**不把任务自动 STOP**。一个有界实验可同时更新性能和机制证据，不自动生成额外报告；细节见 [FEASIBILITY_ENVELOPE.md](FEASIBILITY_ENVELOPE.md)。


## v1.7 · 关键结果的可信证据分级与最小新机制

- `REPORTED`：Agent自报指标或原始工件仅做哈希记录；可探索，不可称独立核实增益。
- `METRIC_VERIFIED_DEV_ONLY`：按需借 RWF `forge-verify` 用原始DEV标签独立复算，匹配同一批预测、任务、样本、合法输入和K/level；只证明**算术与工件一致**。
- `INDEPENDENTLY_CONFIRMED`：冻结协议与主张后，经独立未污染确认和必要科研审核支持，不由DEV工具自动升级。

最低可发表路线与强基线公平性由 [PAPER_FIRST.md](PAPER_FIRST.md) / [CONFIRMATION.md](CONFIRMATION.md) 判定；被核实的 F1 不能单独证明机制、在线因果执行或学术新颖性。旧Run仍兼容。关键结果的可执行验证见[README.md](README.md)；不强制每个小Pilot都构造一份RWF工程。

**最高信息价值的新机制选择**：取现有可信DEV Run的一项可重复错误→明确简单方法错在哪里→提出合法新杠杆(信息/归纳偏置/优化/成本)→写能与强替代区分的预测→做最便宜有界试验。若缺数据真值/现成强基线，先修或补齐，不用换网络名假装新机制；负结果保留，按Run/机制/Task/Claim分层处理。一次实验可同时服务可靠性能与创新探索。
