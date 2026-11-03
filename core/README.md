# PD-RW v1.5：可选的最小证据层

**定位**：管理只读TaskSpec资格预检、Probe候选合同、结构化证据/工件指纹、跨会话恢复、开发Run的记录条件可比性以及显式调用的文献元数据查询；不判断选题/创新价值、不自动STOP、默认不联网、不执行拟合/训练（仅显式`literature-search`会发起元数据网络请求）、不授权解封。科研决策仍由 [WORKFLOW.md](../WORKFLOW.md) 负责。

## 最小使用

```bash
python -m core.cli init --root research --project-id example
python -m core.cli record --root research --kind run --artifact runs/r1.json
python -m core.cli record --root research --kind claim --artifact claims/c1.json
python -m core.cli record --root research --kind note --note "待核实的假设；不升级证据"
python -m core.cli status --root research
python -m core.cli compare --champion research/runs/r1.json --challenger research/runs/r2.json --metric macro_f1
python -m unittest discover -s tests -v
```

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
