# Problem–Data Research Workflow | PD-RW v1.12

> **独立科研工作流仓库**。不依赖原提示词库或其他章的文件。目标是从“有价值的大问题＋可信数据（或理论证据路径）”开始，在真实观察和有限实验中逐渐发现具体科研任务、算法与论文主张。更自由的探索**不等于放宽最终论文证据**，也不承诺发表或算法增益。

**v1.8 默认科研路线**：验收必需数据 → 发现可重复的真实规律或提出明确的可证伪需求 → 用简单合法参照证明信号和可纠正性 → 分开判断可靠结果与独立科研贡献 → 仅为明确瓶颈升级复杂机制 → 冻结后独立确认。已有有效 Run 直接续做，非新增门槛；简单结果不自动等于创新。

**科学贡献候选（保留资产，非自动Q2成功）**：可信、可证伪、相对具名最近邻具有实际差额的**增量贡献**，可进入科学证据候选；不预设必须全面SOTA、发明新网络、跨所有数据库或同时具备多种创新。效率/标定成本/可靠性/失效边界/已有方法的有意义组合都可成为贡献，但不能降低合法评价、公平对照、效应不确定性和与主张匹配的独立确认。详见 [PAPER_FIRST.md](PAPER_FIRST.md)。

**小发现保留与选刊（非项目成功）**：有限但真实的增量贡献可以保留为候选，但需另证其科学重要性、Q2+投稿潜力和独立确认条件。活动04–05有可信DEV证据或特定负Pilot时，先评估可收窄的科学主张与缺口，必要时参考 [VENUE_STRATEGY.md](VENUE_STRATEGY.md) 的稿件潜力 S/A/B/C（另有NONE/UNKNOWN）及期刊冲刺/主投/保守分层；二者是两根不同轴、不是JCR分区或录用概率，也不构成STOP门槛。仅在需要真实选刊时联网核最新范围、近期近邻论文、索引与费用。

**Q2科研证据优先（非自动写稿）**：默认成果是有具名近邻和独立证据支持、具有真实JCR Q2+投稿潜力的科学主张，Q1更好；小而可靠的成果先保护，但不能因普通期刊可发直接算成功。得到可信Run后先核Q2新知识/证据缺口，再决定补证据还是有界科学升级；写作依然须成果总结审查及独立用户授权。见 [PAPER_FIRST.md](PAPER_FIRST.md) 与 [VENUE_STRATEGY.md](VENUE_STRATEGY.md)。

**v1.12 可信算法工程闭环**：活动04需要新算法/复杂训练时才按需读[ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)：真实误差→预测前合法杠杆→强简单替代→一项可证伪预言/低成本正控→获授权的Agent连续实现和DEV实验→公平比较及Run保留→必要时直接转论文补证据。保留单一科研主控，不新增自动训练框架或无上限候选树；参考AIDE/autoresearch/RD-Agent/mini-swe-agent的思想，不复制其整套执行器。

**最低成功标准：可信JCR Q2+投稿潜力，优先Q1**；真实科学证据、具名最近邻与相关期刊近期同类发表先例共同支持，不要求实际录用。普通专业期刊/B-C自定义档不自动算成功。见[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)。

**Q2证据结构预检（可选，不认证成功）**：`python -m core.q2_preflight PACKET.json` 只检查引用字段是否齐全，示例见[Q2_EVIDENCE_PACKET.example.json](Q2_EVIDENCE_PACKET.example.json)；实际科学贡献、JCR分区与Q2潜力仍由证据审查决定。

**下一步Agent指令 / 用户选择分流**：[NEXT_ACTION_POLICY.md](NEXT_ACTION_POLICY.md)。已授权且可自行决定或明确值得执行的技术工作，直接给简短可执行Agent指令；需用户判断或新增授权时，先给推荐和选项，不提前给Agent指令。

**论文写作锁（强制）**：[WRITING_GATE.md](WRITING_GATE.md)。默认 `WRITING_LOCKED`：必须先有科研成果总结和用户审查，再有独立明确的写作授权；可发表性、`DRAFTABLE`、确认成功和自动路由均不会启动论文提纲/初稿。证据补齐、科研验证与普通诊断不受影响。

**完成算法后的科学增值（可选）**：[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)。复用原始Run、错误结构及具名近邻，按新证据及现有授权做一项或一组有界且有价值的证伪；无新意则保留成果并总结，写作锁继续生效。

**高价值科研决策的统一优先级**：重要知识差额/可辨识证据优先于训练难易与小论文完成性；Q2+潜力是项目成功标准，期刊录用不是必要条件。科学问题选择由PD-RW决定，RWF只建议实验动作，不反向以低成本排序覆盖选题。

**高价值科学问题设计（按需）**：[HIGH_VALUE_RESEARCH_DESIGN.md](HIGH_VALUE_RESEARCH_DESIGN.md) 支持多视角问题搜索、数据库科学辨识力、竞争假设与有界机制探索，保留阶段/授权/写作锁。

## 唯一入口与最短路径

- **AI 首次进入**：只读 [START.md](START.md)，再按用户意图读 [WORKFLOW.md](WORKFLOW.md) 的对应活动；只在需要时读一份专题。已有项目优先读其最新 STATE、原始 Run/数据版本；**无需预读所有章节、24条旧Prompt或全部来源**。
- **每次用户会指定研究方向**（如视觉、NLP、机器人、传感器或明确「方向不限」）：AI仅在本轮范围内筛1–3个问题—资源组合；**优先核实可评价主库D1，再按科学主张与成本扩展外部复现/备用数据库**（可多库联合开发，但不凑数量），标明标签/分组兼容性与来源。**方向确定后立即自主选库并进入数据获取：有真实下载授权即由Agent连续下载及验收；无授权则给官方来源、成本与授权方案（**不提前给下载Agent执行指令**）并停在等待数据状态，不先进入实证任务/算法开发**。无需再次让用户选择数据库，也不要求先证明增益。
- **用户已有具体研究机制或旧项目**：可以直接进入对应活动（通常03/04），复用真实 STATE 和 Run；不强制重新选题，不未经确认迁移旧项目。

## 六项研究活动（可跳跃，不是六道审批门）

| 编号 | 任务与入口 | 最小交付 | 主要执行环境 |
|---|---|---|---|
| 01 | 自适应科研机会搜索、选库与优先获取：[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) / [DATA_DISCOVERY.md](DATA_DISCOVERY.md) | SEARCH_HANDOFF→DATA_PORTFOLIO→获授权下载/验收或待下载清单；理论题用PROOF_PATH |
| 02 | 数据获取验收后，审计与真实科研现象：[DATA_DISCOVERY.md](DATA_DISCOVERY.md) / [DATA_INSIGHT.md](DATA_INSIGHT.md) | DATA_MANIFEST（DATA_ACQUIRED_VERIFIED）＋DATA_INSIGHT_CARD；封存确认资源 | 获授权的 WorkBuddy/Codex/本地环境 |
| 03 | 从现象/文献生成、比较任务并按需分层：[TASK_EXPLORATION.md](TASK_EXPLORATION.md) / [TASK_LADDER.md](TASK_LADDER.md) | PRIMARY_TASK＋NEXT_DISCRIMINATING_PROBE、备选任务按需，不提前承诺增益 | ChatGPT＋可访问真实数据的 Agent |
| 04 | 双轨算法开发与工程循环：[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) / [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md)（按需） | 有效Run、ALGORITHM_HYPOTHESIS及下一最有价值实验 | 获授权的代码/实验 Agent |
| 05 | 与活动04并行收敛最小可发表科研证据：[PAPER_FIRST.md](PAPER_FIRST.md) / [VENUE_STRATEGY.md](VENUE_STRATEGY.md)（按需） | CLAIM_EVIDENCE_MAP＋科研结果证据表、补证据计划/按需期刊参考（非初稿） | ChatGPT＋代码 Agent |
| 06 | 严格科学确认：[CONFIRMATION.md](CONFIRMATION.md) | 有效独立证据或 CONFIRMATION_UNAVAILABLE，论文声明边界 | 独立核验与获授权正式实验 |

**实证执行前提（非额外科研审核）**：本轮确定为必需的D1及其他必需库，应先获取选定版本的完整必需原始文件、核文件完整性和本地可达性，再进行数据画像、正式TASK冻结、基线或算法实验；已有可信本地副本直接验收复用。下载未获授权或未完成，停在 `WAITING_FOR_DOWNLOAD_AUTH` / `WAITING_FOR_DATA`，仅允许公开资料调查、下载准备和不依赖数据的假说草拟；不能以示例数据/模拟运行假冒完整实证。备用库按需获取，理论/无需静态库的仿真按证据路径处理，见 [DATA_DISCOVERY.md](DATA_DISCOVERY.md) §4。

**唯一主线：三个决策循环贯穿六项活动**——A 研究机会（先定宽方向→多数据库角色配置→授权后真实观察→任务）→ B 算法实证（可信L0基线、判别探针→有效 Run）→ C 科研价值（L1/L2/L3上探、下探、收窄或横向备用→严格确认）。阶段可以跳转，**不是六道强制关卡**。Task Ladder 是按数据条件启用的研究机会结构，非四级必做、非难度越高论文价值必高；L0/L1也不自动构成保底论文。下探换标签预算/部署信息时更换TASK和协议，封存holdout仍须重新核任务适配。科学止损统一见 [WORKFLOW.md](WORKFLOW.md)。

## 五条不可放宽的边界

1. **确定研究方向/多库组合 ≠ 授权下载/安装 ≠ 授权CPU拟合或GPU训练 ≠ 授权正式确认/付费/外传/投稿**；只有可核实的真实用户授权及既有已批准范围才能执行对应动作。理论分析、只读检索不自动扩展权限。
2. **可以下载完整原始数据，不等于可以开放使用确认集内容**。独立确认数据在任务发现、切片筛选、调参、机制选择阶段应保持封存。不能以反复切分同一已选测试集重新制造独立确认。
3. **算法可运行 ≠ 任务可学 ≠ 科学增量 ≠ 可发表论文**。代理目标、合成正控、内部重采样须注明支持的主张范围。
4. **早期只排已证实的关键不可替代阻断**；未知机制/未运行强基线不自动拒绝探索。正式论文确认必须严格核真值、独立单位、时间因果、公平基线、置信区间/效应和具名最近邻。
5. **输出证据优先**：默认短文本/指标/路径；图表只为判别科学问题或验证证据，01–05不自动做精美图片、长报告或PPT/PDF。避免重复读取、无效多Agent与重绘；不为省Token跳过科学验证。见[WORKFLOW.md](WORKFLOW.md) §5。

## 相关材料
- **真实成功与失败一体案例**：[APACE → SAFE-Gait](LESSONS/SAFE_GAIT_APACE.md)；包含 Oracle/可辨识性差距、K=0→K=1 合法信息变化、目标级异质性与论文边界。
- **可重复只读工具**：`python -m core.cli information-check --file LESSONS/SAFE_GAIT_INFO_PROBE.json`，核 K/信息时点/support-query/成本与共同失败前提；不拟合、不可替代科学判决。
- **历史盲回放设计**：[SAFE_GAIT_REPLAY.json](LESSONS/SAFE_GAIT_REPLAY.json)，当前为事后重构案例，未宣称已执行真正盲回放。


- [WORKFLOW.md](WORKFLOW.md)：总控、状态路由、权限和跨活动续做
- [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)：按本轮范围动态扩缩、多源检索、热点/研究空白与反向近邻检查
- [DATA_DISCOVERY.md](DATA_DISCOVERY.md)：数据/基准组合、独立评价、下载与封存合同
- [DATA_INSIGHT.md](DATA_INSIGHT.md)：活动02开发池画像、数据类型分析、混杂与现象验证、DATA_INSIGHT_CARD
- [TASK_EXPLORATION.md](TASK_EXPLORATION.md)：任务科学价值×可行性比较、主/备选任务与 Claim 收敛
- [POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)：已完成算法的小修改科学性审查、最低成本判别与退出
- [Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)：JCR Q2+潜力成功目标与Q1优先策略（不要求实际录用）
- [PAPER_FIRST.md](PAPER_FIRST.md)：可信性能、独立贡献与增强科学性分账，活动04↔05按需反馈
- [TASK_LADDER.md](TASK_LADDER.md)：L0–L3任务阶梯、共享资产、UP/DOWN/NARROW/LATERAL/HOLD与两类传感器示例
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)：任务到代码、基线、测试不变量与训练诊断（编码时按需读）
- [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)：真实实验、按症状探针、分层公平对照、可复现 Run 与修复；故障按需参考本库 [IMPLEMENTATION_GUIDE](IMPLEMENTATION_GUIDE.md) 的定位与恢复流程
- [CONFIRMATION.md](CONFIRMATION.md)：从开放探索到严格论文确认
- [EXAMPLE_SENSOR.md](EXAMPLE_SENSOR.md)：传感器跨平台迁移的假想执行实例（明确非实测）
- [templates/STATE.md](templates/STATE.md)：兼容旧项目的人类可读续做索引；有效Run/Claim应保留可核验证据
- [REFERENCES.md](REFERENCES.md)：高星 GitHub 项目的具体借鉴点、限制与原始链接
- [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md)：真实项目冻结点的盲回放和人工配对评审
- [SCENARIOS.json](SCENARIOS.json)：57个PD-RW专属的**合成**反例/风险场景；CI只校验结构和关键词，不调用模型

**工作流质量评价**：结构回归并非科研成功率。[WORKFLOW.md 的评测协议](WORKFLOW.md) 要求使用信息隔离的历史盲回放和前瞻性项目审计，在相同预算下比较任务发现、有效科研证据、过早止损、无效循环与总资源成本；**目前尚未运行真实模型对照，效果未测量**。评测按需开展，不成为每个科研项目的强制阶段。

**状态以真实项目文件和工具运行结果为准**；本文只提供指导，不能自动访问本地数据或替用户训练。

## 独立项目说明

此仓库是从 [Research-Prompt-Library](https://github.com/phr-devil/Research-Prompt-Library) 的原第十章整理的独立版本：工作流文档在仓库根目录，配有最短 AI 入口 `AGENTS.md`、结构回归测试及盲回放检查脚本。无需载入旧仓库的 08/09 章，也不绑定第三方算法 Agent。实验、运行记录及数据应放在各自项目目录，勿提交敏感数据或大型原始数据。

**离线验证**：`python -m unittest discover -s tests -v`；`python -m json.tool SCENARIOS.json > /dev/null`；盲回放：`python chapter10_replay.py responses.json`（仅校验结构，不代替科研盲审）。

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
