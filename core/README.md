# PD-RW v1.5：可选的最小证据层

**定位**：管理只读TaskSpec资格预检、Probe候选合同、结构化证据/工件指纹、跨会话恢复、开发Run的记录条件可比性以及显式调用的文献元数据查询；不判断选题/创新价值、不自动STOP、默认不联网、不执行拟合/训练（仅显式`literature-search`会发起元数据网络请求）、不授权解封。科研决策仍由 [WORKFLOW.md](../WORKFLOW.md) 负责。

**可选只读Q2预检与Agent输出决策**：`python -m core.q2_preflight PACKET.json` 对已有科学/期刊证据包做结构检查，**不会**证明新颖性或JCR真实性；`core.action_output.output_mode` 返回“可给Agent指令/需要用户选择”的输出限制，但其参数本身不能证明真实授权。详见 [Q2成功规则](../Q2_PUBLICATION_GOAL.md)与[下一步输出规则](../NEXT_ACTION_POLICY.md)。

**高价值研究辅助（只读、非自动科学认证）**：

- `python -m core.scientific_discriminability --metadata DEV_METADATA.json --factor-a device --factor-b class --group subject --role DEV`：在**已获合法读取许可**的DEV或公开元数据上检查交叉/稀疏独立组；不读封存集、不拟合；输入角色为自述，不能证明因果、训练/下载授权或有效确认。
- `python -m core.science_choice_replay --cases evals/science_choice_cases.synthetic.json --blind`：输出无专家参考的构造场景；`--responses RESPONSES.json` 审计选择、关键风险及授权/Q2误判。合成测试不是实测科研成功率。真实历史时点需独立冻结和评审。

**PD-RW→RWF 科学决策交接（可选）**：RWF 的 `python -m adapters.science_handoff --project PROJECT --packet PROJECT/SCIENCE_HANDOFF.json` 接受研究问题、重要性、具名原文近邻、竞争解释、区别性预测、数据混杂、独立组、合法信息、下一决定性实验及1–8个已许可 DEV/公开元数据 SHA-256来源；详见 [SCIENTIFIC_HANDOFF.example.json](../SCIENTIFIC_HANDOFF.example.json)。其哈希PASS不代表科学事实、数据合法性、Q2或用户授权；RWF的便宜Probe顺序不能反向覆盖PD-RW的科学方向选择。

**已有Run科学信息挖掘（只读、非科研认证）**：`python -m core.result_harvest --packet DEV_EVIDENCE.json` 对已合法整理的同任务、同K、同协议和同metric的DEV配对组级指标输出条件差异、组间异质性与实测资源权衡线索。输入来源、独立组和数据许可来自调用者声明，不重算指标、不提供p值、不证明因果或期刊水平。带上次`previous_packet_sha256`可在同内容下返回`UNCHANGED_INPUT_REUSE`，减少重复审查。见[SCIENCE_RESULT_HARVEST.md](../SCIENCE_RESULT_HARVEST.md)。

**活动01选题反早停（可选，只读）**：`python -m core.search_choice_review --packet SEARCH_DECISION.json` 对最多3个已发现的科研候选、不同失败前提的竞争搜索、原文反证、官方元数据D1科学可评价性进行**结构性核查**。示例`evals/search_choice.synthetic.json`是虚构数据、**非真实文献或研究价值证据**；`STRUCTURALLY_READY_FOR_D1_PLANNING_ONLY`不等于有科学新颖性、Q2潜力或用户下载授权。该检查不联网、不读数据、不训练，也不增加审批门。

## 最小使用

```bash
python -m core.cli init --root research --project-id example
python -m core.cli record --root research --kind run --artifact runs/r1.json
python -m core.cli record --root research --kind claim --artifact claims/c1.json
python -m core.cli record --root research --kind note --note "待核实的假设；不升级证据"
python -m core.cli status --root research
python -m core.cli compare --champion research/runs/r1.json --challenger research/runs/r2.json --metric macro_f1 --higher-is-better
python -m unittest discover -s tests -v
```

`compare` 不再默认指标越大越好：两份 Run 同时声明相同 `metric_direction=max|min` 时按该方向计算；否则需要显式 `--higher-is-better` / `--lower-is-better`。未声明则 `improvement=null`、`METRIC_DIRECTION_REVIEW_REQUIRED`（预算不匹配仍优先报告预算复核）；方向及 Run 声明都不是独立科学核验，需比对 TaskSpec 的真实评价定义。封存 Run 永远不能用来迭代比较。

工件路径相对`--root`。Run/Claim的JSON字段见`contracts.py`；机器索引使用`STATE.json`和append-only `EVENTS.jsonl`。发生断电导致状态与事件尾部不一致时，`status`报警，可在检查日志与工件后显式调用`recover`。仅核验JSON和相对路径存在不能证明原始实验真实、公平或可复现。

**字段（最低限度）**：

- Run: `run_id, task_id, protocol_id, dataset_version, evaluator_version, group_split, sample_ids_hash, legal_inputs[], status, split, metrics{}`；VALID另需`artifact_refs:{metrics,predictions,code}`；sealed另需`frozen_protocol_ref, authorization_ref`。后两者只是人工可核的指针，绝非自动授权。
- Claim: `claim_id, task_id, claim_text, status`；SUPPORTED另需`evidence_run_ids[], artifact_refs[], strongest_alternative`；CONFIRMED还需`confirmation_run_ids[], confirmation_protocol_ref`。机器只能检查引用关联，不能自动认证科学确认。
- 旧`STATE.md / RUNS.tsv / CLAIMS.md`继续使用，不强制迁移或覆盖。建议只有在产生可信Run或重要Claim时建立机器索引，探索草稿无需每次格式化。

限制：Run/Claim工件文件附SHA-256；v1.5新增记录时对有效Run的原始预测/指标/代码生成SHA-256指纹（默认status不重复全量哈希，--deep才复核），不替代代码、数据血缘及外部权利检查，性能结果必须由独立科研审计判断。

**并发与恢复**：写操作使用排他锁`.evidence-write.lock`，多Agent同写时会拒绝而不是覆盖。崩溃遗留锁须先核事件、工件和进程状态，再手动清理；若仅STATE滞后且证据文件均匹配，运行`recover`。缺失预算基准时Run比较返回`BUDGET_REVIEW_REQUIRED`，不能直接宣称公平增益。

## v1.5：执行前后只读检查

```bash
python -m core.cli task-check --root research --spec task.json
python -m core.cli task-pin --root research --spec task.json --output task-pinned-v1.json
python -m core.cli probe-check --file probe.json
python -m core.cli run-check --root research --run runs/r1.json
python -m core.cli status --root research --deep
python -m core.cli literature-search --query "sensor calibration transfer" --limit 5 --output search-evidence.json
```

`task-check`要求`task.json`至少含：`task_id, protocol_id, dataset_version, target_definition, label_provenance, prediction_time, legal_inputs[], group_key, independent_unit, metric, metric_direction(max/min), evaluator_version, editable_paths[], protected_paths[], references{data_manifest,split_manifest,evaluator}, correctness_checks[]`。已存在的开发split清单可附`train_ids/dev_ids`和`train_groups/dev_groups`做**实际不重叠检查**；缺字段标UNKNOWN而非假PASS；若新Run绑定已固定TaskSpec，必须有非空且不交叠的train/dev样本ID与独立group清单，否则拒绝声称该快照下的Run通过最小结构核查。`task-pin`会新建包含完整`expected_sha256`的TaskSpec快照；新Run若携带`task_spec_ref/task_spec_sha256`，系统要求快照与实际数据/划分/评价器哈希一致，拒绝静默替换。既有Run可不绑定，不能倒推其已锁定。只读资格检查不执行评价器，不访问sealed标签。

`probe-check`只检查一条候选的失败前提、竞争解释、明确区别性预测、最廉价测试、正/负/无效三类结果的后续含义及授权成本。不生成科学创新、不自动授权GPU、也不能仅凭结构推断物理可学性。`run-check`审计命令、Git commit、Python版本、seed、环境文件、任务快照与预算元数据；缺字段标`PROVENANCE_PARTIAL`，并不自动否定既有科学结果。

`literature-search`**只有显式执行才联网**；最多返回有限的OpenAlex/Crossref论文元数据（原始DOI、标题和时间），失败标记且不覆盖已有输出。返回的元数据不是论文方法复核，不得凭搜索为空声称创新。无法联网时保持原有手工检索/NEIGHBOR_UNVERIFIED路径。

**兼容性**：旧v1.4`STATE.json/EVENTS.jsonl`继续可读；新增Run推荐携带`task_spec_ref/task_spec_sha256`与`execution{command,git_commit,python_version,seed,environment_ref}`，但不反向要求迁移历史Run。deep核验大型预测文件可能产生额外I/O，仅在有科学结论变化、恢复或正式确认前调用。程序不判定论文价值、时间因果、确认集资格或授权。

**探针预算（可选）**：`probe.json`可加入`cost_estimate:{"gpu_hours":0.4,"tokens":5000}`；`probe-check --file probe.json --remaining-budget-file budget.json`会在给定JSON预算内提示`BUDGET_REVIEW_REQUIRED`，绝不自动STOP或将预算文件视为用户训练授权。

**按需信息条件核对（无训练）**：`python -m core.cli information-check --file info-shift.json`。输入 `root_problem`、`before/after`（task_id、protocol_id、每单位 K、合法决策前可见信息）、`new_information`（标签/反馈是否预测前可见、support-query 是否独立、成本及同 K 简单基线）、可选 `evidence`（Oracle/实际策略与参照结果及来源）。输出只标记信息条件候选和风险，不判断科学成功、不自动转题、不批准训练。案例见 [LESSONS/SAFE_GAIT_APACE.md](../LESSONS/SAFE_GAIT_APACE.md)。


**v1.6可选失败原因分诊（纯建议）**：`python -m core.cli failure-check --file failure.json`；输入示例：`{"task_id":"T","protocol_id":"P","findings":[{"kind":"EVALUATION_INVALID","evidence_level":"OBSERVED","evidence_ref":"runs/audit.json"}]}`。kind可为`EVALUATION_INVALID/TRAINING_INADEQUATE/LEGAL_INFORMATION_GAP/SIMPLE_BASELINE_DOMINATES/CLAIM_NOT_DISTINCT/STATISTICAL_UNCERTAINTY/MECHANISM_NEGATIVE/EXPLORATORY_OBSERVATION`。输出的路线与范围不是Run事实复核；原始证据须由Agent读取，程序不会自动训练、STOP或改变授权。

**按需可行性结果判读：** `python -m core.cli feasibility-check --file PROJECT/FEASIBILITY_ENVELOPE.json` 仅对 Forge 生成的候选/参照差值提出下一个实验方向，不重新打开数据、不拟合、不把传入 JSON 自报内容当独立验证。原始数据和运行工件仍应先在 Forge 用 `tools.feasibility_probe` 核验。任务集分层与具体用法见 [FEASIBILITY_ENVELOPE.md](../FEASIBILITY_ENVELOPE.md)。


## 稿件语义与独立确认标注的离线警报（仅按需）

```bash
python -m core.manuscript_claim_guard compare before.md after.md --output alerts.json
python -m core.manuscript_claim_guard provenance claims.json --output provenance.json
```

第二个命令读取明确提供的 JSON `{"claims":[{"claim_id":"C01","text_anchor":"independently confirmed","asserted_role":"INDEPENDENT_CONFIRMATION","source_role":"CONFIRMATION","split_id":"CONFIRM-01","development_split_ids":["DEV-01"],"selected_on_source":false,"protocol_frozen":true,"evidence_ref":"runs/confirm-01"}]}`，仅核声明的 split/角色是否存在**明显矛盾或缺项**。第一命令对修改前后已变化文本做词法警报（数值、否定、因果、显著性、DEV/VAL/TEST 等角色），不替代语言理解、来源核对或合法的科学修改。支持 `.md/.txt/.docx` 的文本抽取，未提供完整证据映射、修改范围过大、原始证据不可用时均须人工审阅；无警报不代表语义不变。**不会读 SEALED、联网、画图或自动改论文**。稿件授权和审核由 [MANUSCRIPT_WRITING.md](../MANUSCRIPT_WRITING.md) / [MANUSCRIPT_QA.md](../MANUSCRIPT_QA.md) 决定。

## 可选跨仓库独立指标复算

本地有最新 RWF checkout 时，可运行 `python -m core.cli forge-verify --root PD_PROJECT --run runs/R.json --forge-repo RWF_REPO --forge-project FORGE_PROJECT --forge-run runs/R/RUN.json --metric MAE`。PD Run与RWF Run的原始预测文件需字节相同，RWF在自己的工作目录和Python进程内核真实DEV标签/组/指标；避免两个仓库同名 `core` 包发生导入冲突。输出仅为 `METRIC_VERIFIED_DEV_ONLY`，旧Run无验证证据时保留`REPORTED`，不修改原Run/STATE或封存数据。若相对路径参数，`--run` 相对于 PD_PROJECT，`--forge-run` 相对于 FORGE_PROJECT。
