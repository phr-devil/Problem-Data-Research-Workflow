# PD-RW v1.4：可选的最小证据层

**定位**：只管理结构化工件、可追溯事件、跨会话恢复及开发Run的记录条件可比性；不判断选题/创新价值、不自动STOP、不执行网络/拟合/训练、不授权解封。科研决策仍由 [WORKFLOW.md](../WORKFLOW.md) 负责。

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

限制：工件文件本身附SHA-256；原始预测/代码引用只核路径可达性，不替代代码、数据血缘及外部权利检查，性能结果必须由独立科研审计判断。

**并发与恢复**：写操作使用排他锁`.evidence-write.lock`，多Agent同写时会拒绝而不是覆盖。崩溃遗留锁须先核事件、工件和进程状态，再手动清理；若仅STATE滞后且证据文件均匹配，运行`recover`。缺失预算基准时Run比较返回`BUDGET_REVIEW_REQUIRED`，不能直接宣称公平增益。
