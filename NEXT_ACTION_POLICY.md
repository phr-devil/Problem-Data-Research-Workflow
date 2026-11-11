# Next Action / User Decision｜Agent下一步输出规则

**双文件维护不是论文写作许可**：真实授权科研中，按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 对关键任务/Run/失败/决策及时增量更新 `RESEARCH_RECORD.md`，仅在章目或 Claim–Evidence 发生变化时增量更新 `PAPER_BLUEPRINT.md`。普通重复调试不生成固定长篇总结，旧项目不强制迁移；正式稿件继续执行 [WRITING_GATE.md](WRITING_GATE.md)。

**绘图不是自主技术默认动作**：只有用户本人明确要求绘制/重绘/修改图片时，才可给出绘图执行命令或实际作图；没有请求只用文字/表格给建议。见[FIGURE_POLICY.md](FIGURE_POLICY.md)。

> **优先级**：对所有PD-RW阶段、WorkBuddy/Codex任务交接、科研收口和Q2评估生效；不改变真实用户授权、[WRITING_GATE.md](WRITING_GATE.md)或[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)。用于**给用户的下一步输出**，不是授权Agent自动执行尚未批准的动作。

## 1. 先判断下一动作是谁能决定

- `AGENT_DECIDABLE`：已在用户真实授权、研究范围及预算内的**技术实现选择**，例如定位并修复普通Bug、复用已有Run、选最有信息量的只读诊断、重跑已授权且协议不变的受影响测试、补写非论文的科学证据摘要。Agent可自行选出**一项最佳后续动作**。
- `STRONG_RECOMMENDATION`：关键证据充分、下一技术方案明显优于备选且**无需新的用户授权或价值判断**；直接给最优执行方案，不为常规技术分歧反复要求确认。强烈建议**不覆盖权限**。
- `USER_DECISION_REQUIRED`：**深度参与模式缺少当前 H 节点的真实选择/明确委托**；**当前授权外**的新数据下载/安装/拟合/GPU、预算或成本增加、封存集开启、研究方向/主要Task更换、放弃或结束整个项目、核定主张/发表目标改变、数据外传/投稿/付费，以及**论文成果总结审查与正式写作许可**。授权范围不清、选项有无法由科学证据代替的价值取舍时也属于此类。Agent不得用自己“强烈建议”绕过用户。

### 深度参与模式中的用户科学决策（复用已有 USER_DECISION_REQUIRED）

新 PD-RW 课题默认 `USER_DEEP_PARTICIPATION`，按 [WORKFLOW.md](WORKFLOW.md) 的 H1–H10 确定哪个科学选择当前由用户负责。用户可一次明确批准多个节点或将具体节点有限委托AI；原用户消息必须可核，Agent 自评、选库表、状态字段/布尔值均非批准。旧项目已有真实选择不重新问；新证据仅重开直接受影响的节点。技术性查证、普通Bug、已有授权实验不进入新审批循环。

**待用户决策时**输出 `DECISION_ID | RECOMMENDATION+SOURCE | OPTIONS(通常2–3项)+TRADEOFFS | REQUIRED_USER_CHOICE | DEPENDENT_ACTION_HELD`。未确认节点只暂停**依赖该决定**的定稿/资源动作，仍可在既有授权范围内进行独立合法只读核查。明确委托的选题决策不授予`DOWNLOAD/TRAIN/SEALED/WRITING`权限；项目与主张事实不能由用户偏好升级成 VERIFIED。用户决定已在本轮给出时直接引用，不机械增加一次对话。

**交付前必查的遗漏**：仅针对本轮受影响决策核 `当前H_ID + 原用户选择/委托范围 + 关键证据/反证 + 依赖是否失效 + 独立执行授权`；未有真实选择时给推荐而非自称用户已批准，已确认且未变化则不重复打断。若上游H节点因数据不适配/协议更改失效，下游旧用户选择**不得被自动当作对新条件的批准**；重新核对实际影响范围并只重开必要节点。 `REVIEW:H#` 与论文标题 `HEADING:H#` 不能互换。

### 新项目统一审核卡片：相同节点、不同科学内容

在 `USER_DEEP_PARTICIPATION` 下，人工节点定义来自 [`contracts/human_review_protocol.v1.json`](contracts/human_review_protocol.v1.json) 的 `required_dimensions`，科研语义仍归 [WORKFLOW.md](WORKFLOW.md)。每轮只有**当前需要用户决定**的H节点成为主卡片，按 `PROTOCOL_VERSION | H1–H5_PROGRESS | CURRENT_REVIEW(ID+固定名称) | AI_RECOMMENDATION+SOURCE | RISKS/UNKNOWN | OPTIONS+TRADEOFFS | REQUIRED_DIMENSIONS/CHOICE_OR_DELEGATION | NEXT_DEPENDENT_ACTION` 给出内容。选项因领域不同而不同，但H1研究目标、H2来源+贡献路线、H3问题、H4证据资源、H5最终题目永不互换定义。允许用户一条消息明确完成多个节点、逐项委托或暂缓；已决定且未变化的内容不再询问。当前节点只涉及一个合理候选也可如实说明，不凑假选项。

**两种结果不可混淆**：`can_present_review_declarations_only` 表示所声明的前置审核齐备，**可以提出当前节点问题**；`can_advance_declarations_only` 才表示所声明的当前节点决策及维度齐备，可以考虑依赖工作；两者都必须先核原用户消息及真实证据，**都不是下载/拟合/SEALED/绘图/正式写作权限**。重要维度只选择部分时维持待决并仅补缺项，不能重新索要已答项。旧项目无 `protocol_version` 允许兼容读取，但不能以同名节点自动假定满足新版本。

## 2. 对用户的输出格式（互斥）

### A. 无需用户决策 → **必须直接给简洁可复制的下一步Agent指令（NEXT_AGENT_INSTRUCTION）**

先给一句`DECISION+EVIDENCE`，然后给一个短的、可交给Codex/WorkBuddy/研究Agent执行的**Agent指令**，包含：当前已证据锚点、目标、允许动的文件/数据/协议范围、关键保护（如sealed/预算/写作锁）、完成判据和最少结果反馈。自主处理关联小修与最小必要测试，不规定无意义的固定批次，不要求重复读取所有文件、不生成装饰图与冗长日志。若本次任务已完成且无需后续工作，直接报告`NO_NEXT_ACTION`，不编造指令。

### B. 必须用户决策 → **先明确推荐及依据，再给可选方案；禁止预先输出Agent执行指令**

简洁输出`RECOMMENDATION+WHY | OPTIONS(通常2–3个，说明投入/收益/风险) | REQUIRED_USER_CHOICE`。可以提供事实、方案、费用估算和授权边界，但**不输出下一阶段的Codex/WorkBuddy执行提示词或自动执行命令**。用户作出明确选择并确认相应权限后，在**下一回合**按A给可执行Agent指令或继续相应工作。

## 3. 判定示例与边界

| 情形 | 输出规则 |
|---|---|
| 已授权DEV算法内部修复；现有日志显示明确Bug | A：给直接可运行的修复与定向验证Agent指令 |
| 已有可信Run、候选主张Q2评估需只读查文献/组级残差 | A：给低成本核查Agent指令；不得冒称Q2成功 |
| 证据提示一次新GPU实验能显著提高Q2竞争力，但GPU授权尚无 | B：推荐并列成本/选项，**不发训练Agent指令** |
| 复杂机制失败，建议更换整个主要Task或归档项目 | B：先给推荐和转向/保持/结束选项；不自动转向或STOP |
| 科研总结已完成，需要用户审查或用户尚未允许论文写作 | B：只给成果判定/选择，不发论文撰写Agent指令 |
| 写作已获项目范围内明确用户许可 | A：在真实许可范围内给写作Agent指令；不能由Q2判决代替许可 |

**次序固定**：科学正确性/原始证据 → 法定与用户授权 → 是否用户决策 → 输出形式。信息未知时优先最便宜合法查证；不能代替用户作决定。避免对每个普通实施细节提问，也不要把禁行的“Agent指令”偷偷放到建议选项里。
