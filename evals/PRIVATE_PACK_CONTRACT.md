# Private Evaluation Pack Contract｜按需评估，不新增科研阶段

**公开 `evals/cases/` 及 `operational.py` 仅为 `REGRESSION_ONLY`。** 本文件规定私有评估包的最小格式，但仓库不保存私有题目、参考答案、真实研究数据或评分密钥。

## 私有包与外部隔离

在仓库外且不可被受测Agent读取的位置保留 JSON：

```json
{"format":"pdrw-private-pack-v1","visibility":"EXTERNAL_PRIVATE","pack_id":"your-private-001","cases":[{"case_id":"HIDDEN-01","agent_task":{"prompt":"Synthetic question","allowed_effects":["READ_FILE"],"budget_id":"B1"},"reference":{"rubric_version":"rev1","review_criteria":["Scientific evidence and competing hypotheses"]}}]}
```

`python -m evals.private_pack validate --pack /protected/pack.json` 仅核格式；`python -m evals.private_pack export --pack /protected/pack.json --output /isolated/tasks.json` 导出剔除 `reference` 的任务，不得回写本仓库；已有目标不覆盖。文件格式校验、SHA256、外部目录都**不能保证盲测**。真正能力评估要求外部执行器隔离 Agent 的文件与网络（包括对公开 GitHub/历史的访问），参考答案不可通过工具、记忆或搜索获得。

## 独立行为证据的最低要求

外部执行器记录实际的 `event_id | timestamp | operation | resource/path | decision`，附捕获范围、模型/工具清单、任务与预算指纹、真实 input/output tokens、调用次数和耗时；日志必须处于 Agent 不可写空间。声明 `capture_source=EXTERNAL_INSTRUMENTED` 或附一段示意 trace，仍然只表示 `TRACE_DECLARATIVE_ONLY`；**签名不能代替检查捕获完整性**。没有可验证的隔离/完整捕获和独立审稿时，权限及科研质量为 `NOT_CERTIFIED`，效率改善为 `NOT_MEASURED`。

## Token 友好的分层评估

日常 CI 仅标准库合成回归；影响论文论证、科研选择或权限语义时按需使用相应操作型测试；重大变更才执行配对 A/B。可复用冻结基线，但须复核模型配置、任务、工具、授权和预算等条件一致。科学创新与前瞻性由独立评审根据实际内容和版本锁定 Rubric 判断，不以命中某个标准答案代替。

本模块不授予下载、SEALED、训练、绘图或正式论文写作权限，不要求固定多 Agent 或额外人工审批。
