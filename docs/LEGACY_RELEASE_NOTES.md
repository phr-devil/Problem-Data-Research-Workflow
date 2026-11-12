# 历史版本执行层说明（非现行规则）

> 本文仅存档早期版本的功能演进与原始示例。当前执行必须以 [WORKFLOW.md](../WORKFLOW.md)、[AGENTS.md](../AGENTS.md) 和现行契约为准。旧版内容不提供当前授权、阶段或审核职责；涉及 H6/H8 等变化须适用当前 v1.3 规则。

## v1.5 轻量执行层

- 科学判断、授权与止损仍由 [WORKFLOW.md](WORKFLOW.md) 负责；[core/README.md](core/README.md) 的程序只负责记录证据、恢复状态和检查开发Run的可比性，不自动推进固定科研阶段。
- 旧 `STATE.md/RUNS.tsv/CLAIMS.md` 可继续复用，无需迁移；新项目首次获得有效Run时，如可执行Python，使用 `python -m core.cli init --root research --project-id demo` 建立机器索引。已启用后，应为新增有效Run和已支持Claim关联真实工件。
- 运行 `python -m unittest discover -s tests -v` 验证代码与结构约束，**不代表科研质量或成功率已验证**；真实效能需按 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) 盲回放。

### 新增：从 Task 到可执行证据（按需，不是新关卡）

- 当研究任务已需要实际编码/拟合时，先编写最小 TaskSpec（合法输入、独立单位、固定评价器、开发分组、受保护文件、可观察正确性检查）。`python -m core.cli task-check --root research --spec task.json` 只做只读结构和数据划分预检；新Run绑定已通过`task-pin`固定受保护文件哈希的任务快照，不跑评价器，更不批准训练。
- 负Pilot后可用`probe-check`审查一个机制候选的竞争解释、区别性预测、正负结果含义及成本；AI仍负责提出科学假设、调用前复核真实权限。
- 有效Run可运行`run-check`检查环境/复现信息缺口，`status --deep`复核关联的预测/指标/代码文件指纹；旧v1.4记录继续可读。
- 仅明确调用`literature-search`时联网获取OpenAlex/Crossref元数据与检索时间、来源；元数据不是全文创新性核查。具体调用见[core/README.md](core/README.md)。
- 论文路线允许`NO_WINNER`后转为真实失效边界/规律或`NO_INDEPENDENT_CLAIM`，不凭零增益自动包装成论文。**科研成功率仍NOT_MEASURED**，须按[REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md)执行真实历史盲回放。


**v1.6重点**：在原数据→任务→算法双轨中增加按真实负证据的原因路由；失败优先修评价、辨别欠训练/信息不足、核同K简单基线与论文贡献，允许合法信息条件PIVOT但不自动STOP。只读`python -m core.cli failure-check --file failure.json`供重大负结果按需使用，具体见[WORKFLOW.md](WORKFLOW.md)；既有 v1.5 状态/Run保持兼容。未做真实历史盲回放，不宣称成功率提高。

- **可学性与剩余空间诊断**：[FEASIBILITY_ENVELOPE.md](FEASIBILITY_ENVELOPE.md)。已有真实 Run 时先看可核对的 DEV 误差、简单方法与信息条件，再决定新机制或转向；不默认训练、评审或画图。


## v1.7 · 可信DEV指标交接（可选）

关键 DEV Run 可用本地安装的 RWF 独立复算原始标签、样本和指标；不复制第二套状态系统、不强制旧Run迁移：

```bash
python -m core.cli forge-verify --root PD_PROJECT --run runs/R.json --forge-repo RWF_REPO --forge-project FORGE_PROJECT --forge-run runs/R/RUN.json --metric macro_F1
```

需将**相同字节的原始预测 JSON**保存在PD-RW Run与RWF Run引用路径下，Task/协议/数据版本/独立组/样本ID/合法输入/信息层级需相符；若旧项目仅有CSV或不同样本编号，先在DEV合法地生成等价的标准预测工件并核对，不得靠复制F1制造验证。接口输出仅为 `METRIC_VERIFIED_DEV_ONLY`，不能证明训练执行来源、时间因果合法性、算法增益公平性、论文贡献或封存确认。详情见[FEASIBILITY_ENVELOPE.md](FEASIBILITY_ENVELOPE.md)。

**可选双文档只读核查**：在 PD-RW 源码环境使用 `python -m core.doc_integrity --project PROJECT_DIR`；只检查文档结构、重复 ID 和显式 EXP/SEC_ID 交叉引用，缺失的旧文件不要求迁移。支持 `--record/--blueprint` 自定义相对路径。详见 [双文档规则 §7](DUAL_DOCUMENT_WORKFLOW.md)。它不验证科学结果、不读取 SEALED、不生成图片或改写文件；无相关问题时不需要运行。
