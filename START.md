# PD-RW v1.11｜AI 最短入口

仅在用户明确选择PD-RW时启用。**默认科研目标是形成可信、可发表的科学证据，而不是直接撰写论文。**本轮研究范围以当前用户指令为准；[WORKFLOW.md](WORKFLOW.md) 是科研决策与权限的唯一总控，**无需预读所有专题**。

1. **已有项目**：先核真实STATE/Run、manifest和用户授权。若使用 `STATE.json/EVENTS.jsonl`，先查事件一致性；缺工件不冒充有效结果。仅按当前阻碍读对应专题。
2. **新课题**：机会搜索→自主定D1及必需外部库→核官方版本/必要文件/许可/容量→**优先下载并核验数据**。已有完整副本直接复用；有下载授权的Agent连续完成获取，不再为选库/下载反复请示；无下载授权则给直链/保存路径/可执行命令，标 `WAITING_FOR_DOWNLOAD_AUTH`，不进入数据实证。详见 [DATA_DISCOVERY.md](DATA_DISCOVERY.md)。
3. **数据就绪后**：必须先有 `DATA_MANIFEST` 中本轮必需库的 `DATA_ACQUIRED_VERIFIED`（文件完整与可读，不代表科学有效）；否则只做下载/恢复与非实证准备。就绪后按 [DATA_INSIGHT.md](DATA_INSIGHT.md) 观察真实现象，再到 [TASK_EXPLORATION.md](TASK_EXPLORATION.md) 选任务；Task Ladder按需读。理论/仿真按明确证据路径例外处理。
4. **已有任务/运行**：按 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) 获取有效Run、诊断负Pilot；**需要设计新算法或连续编码/GPU实验**时，按需读 [ALGORITHM_ENGINEERING.md](ALGORITHM_ENGINEERING.md) 的误差→杠杆→廉价正控→有界执行闭环，实际接口和保护规则读 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)。机制失败先分辨可用信息/公平基线/欠训练，再决定转向或补论文。论文贡献读 [PAPER_FIRST.md](PAPER_FIRST.md)，正式独立确认读 [CONFIRMATION.md](CONFIRMATION.md)。

**Q2科研目标**：按[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)，最低成功标准是有证据支持的JCR Q2+投稿潜力（Q1更好），**不要求实际发表**；Q3/Q4或仅小发现不等于项目成功，但未知/负Pilot不自动失败。

**写作锁**：阅读 [WRITING_GATE.md](WRITING_GATE.md)；在用户审查科研成果总结且明确授权写作之前，禁止自动生成论文提纲/章节/初稿。论文潜力判断、DRAFTABLE、可信Run、确认完成都不解除锁定；继续科研与补证据不受影响。

**完成算法后（按需）**：稳定可信Run且拟HOLD/结束/再堆模型时，参考[POST_ALGORITHM_SCIENCE_AUDIT.md](POST_ALGORITHM_SCIENCE_AUDIT.md)判断一次小规模科学升级是否值得；不新增必经阶段，不自动拟合或写稿。

**论文证据优先触发**：新Task形成时可按需读 [VENUE_STRATEGY.md](VENUE_STRATEGY.md) §0 的真实类似论文，不先做正式期刊评级。首个可信Run、关键负Pilot、拟新建高成本模型或HOLD/PIVOT时，应按需读 [PAPER_FIRST.md](PAPER_FIRST.md) §0，先判断能否完成一篇窄主张的论文；如果最低必要证据可补齐，优先补主张的科研证据，不默认为升级算法或启动论文写作。稿件确认仍须读 [CONFIRMATION.md](CONFIRMATION.md)；无需每次重载这三个文件。

**证据索引**：新项目出现首个有效Run且有Python环境时按 [core/README.md](core/README.md) 初始化和记录工件；既有项目不强制迁移，无法执行则保留真实原始路径并标`INDEX_PENDING`。

**统一输出**：`NEW_EVIDENCE+PATH | DECISION_CHANGE/UNKNOWN | NEXT_PROBE+可能结果 | AUTH/COST`。不编造运行或检索，不使用封存集调参。新规则不代表额外审批门，现有合法授权范围内可连续执行。

**出现 Oracle 有收益、可部署策略却无增益的症状时**：按需读[SAFE-Gait/APACE 复盘](LESSONS/SAFE_GAIT_APACE.md)并选择 `information-check` 的只读核对；平常项目不要预读此案例或新增审批步骤。

**关键DEV结果独立复算（按需）**：若已有适配RWF的同一原始预测工件，在正式基线/明显增益/异常评审时使用 `core.cli forge-verify`，只得到指标算术验证；旧Run无条件不升级、没有RWF也不阻断探索。先读 [core/README.md](core/README.md) 对应说明，不预加载RWF源码。
