# FEASIBILITY_ENVELOPE｜真实信号—简单基线—剩余空间（按需）

**触发时机**：已有可信 DEV Run，准备开发较昂贵或复杂的机制；或出现“Oracle 有空间但策略无收益”“简单方法很强”“新机制多次没有增益”。**不是新的必经关卡**。已有足够证据可跳过，缺实验授权只能只读分析。

## 最短检查（不虚构可学性）

1. **DATA/TRUTH**：评价标签、独立组、预测前合法输入与封存资格是否真实支持任务？数据不适配，先修真实任务/评价，而不是训练大模型。
2. **SIGNAL**：无信息/简单参照是否来自训练组且与候选同合法输入、同协议？缺可靠参照记 `UNKNOWN`，不能用 DEV 全体标签算无信息策略，再把它当合法预测的成绩。观察到差值不等于可学的稳定规律。
3. **BASELINE/ERROR**：复用可信的基线、逐样本预测和分组残差；只看当前科学问题相关的 1–2 个条件。高 F1 不等于零科研空间，残差大也**不等于可实现的性能上限**；欠训练/标签冲突/组级样本过少应先排查。
4. **LEVER**：新算法具体利用**哪些新增合法信息、先验、优化结构或资源限制**？给出与最强简单替代不同的可观测预言，再做最小、可否证、成本可控实验。Oracle 仅为理想参考；动态门控还需要决策前可辨识性。
5. **DECISION**：有可信组级机制线索→有界实验；没有公平参照→补参照；相同失败前提多次无新增证据→暂停该分支或合法 DOWN/NARROW/LATERAL；没有合理数据/真值→换 Task 或库。始终保留负结果，**不自动 STOP 整个项目**。

## 可执行复用（Forge 已有验证 Run 时）

在 Forge 仓库的环境中，运行：

```bash
python -m tools.feasibility_probe --project PROJECT --candidate PROJECT/runs/C/RUN.json --reference PROJECT/runs/B/RUN.json --metric macro_F1 --out PROJECT/FEASIBILITY_ENVELOPE.json
```

- `--reference` 可省略：只描述既有 DEV 误差，`SIGNAL=UNKNOWN`；若两个 Run 有多项共同指标，需以 Task 预冻结的指标指定 `--metric`。
- 参考 Run 只是**经过可信标签复算的参考模型**，并不能证明其是无信息、强或公平调优的简单基线。比较期间的真实模型训练与选择历史应另行检查。
- 分类输出按组错误率、回归输出按组绝对误差；事件定位仅返回已核实的主要指标，不虚构可比的逐组 Oracle。
- 该命令**不训练模型**；读取 DEV 会按既有规则写入审计记录；`--out` 为明确要求时创建一份新 JSON，绝不覆盖。无文件时直接打印 JSON。

可将生成的 JSON 交给 PD-RW 的**只读建议器**：

```bash
python -m core.cli feasibility-check --file PROJECT/FEASIBILITY_ENVELOPE.json
```

它不重新验证传入 JSON，因此需核其 `evidence_ref` 所指真实 Run。结果只给**下一项有意义的实验方向**，不授予训练/封存确认权限，也不把开发集差值当论文创新。

## 最小输出与研究边界

`DATA_VALIDITY | SIGNAL_EVIDENCE | SIMPLE_REFERENCE_STATUS | GROUP_RESIDUALS | PAIRED_DEV_DELTA | DISTINCT_LEVER | NEXT_PROBE`。

未知标 UNKNOWN；不造单一“可学性评分”、不强制 P 值/三种随机种子、不默认新可视化或长报告。科学成功仍需具名近邻差额、相同合法信息的公平对照、组级稳健性及独立确认；对经过反复任务选择的 DEV 切片标 **EXPLORATORY**。允许减少复杂度和调整合法信息条件，但必须更新 Task/协议/Claim，不能将 APACE 的 K=1 结果解释为 K=0 原任务成功。
