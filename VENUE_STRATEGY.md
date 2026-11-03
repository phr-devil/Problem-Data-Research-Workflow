# Venue Strategy｜稿件潜力与期刊匹配（活动05–06按需）

**唯一目的**：保护“小而真实”的论文机会，为一项具体Claim选适合的期刊；不预测录用概率、不决定是否停止算法。新科研任务仍按[WORKFLOW.md](WORKFLOW.md)执行；增量贡献与证据见[PAPER_FIRST.md](PAPER_FIRST.md)，确认按[CONFIRMATION.md](CONFIRMATION.md)。**这不是第七步/新自动审批/新的状态Schema**。

## 0. 提前进行轻量论文参照（不要求初期完整期刊评级）

**选题/任务阶段**：在`USER_SCOPE`已明确、有可检验任务族时，可低成本查同方向近期1–3篇真实已发表论文及其期刊/文章类型，记录最小可发表贡献类型、关键实验与论文篇幅；不需要先给S/A/B/C，不以IF筛选/淘汰问题，也不要求全面期刊检索。无联网/无充分证据时标`VENUE_ANALOGS_UNKNOWN`，不阻止科学探索或合法数据获取。**结果阶段**：有可信Run且需要决定是补论文还是继续算法时，根据近期类似稿件建立2–3本参考池；**投稿准备阶段**才严格检查索引、APC、作者指南和最新政策。避免每轮重复搜刊。

## 1. 什么时候触发

- 已有可信DEV现象或合法正/负Pilot，且可提出一项可证伪的新规律、局部改进、资源/标定成本权衡、失效边界或有意义的组件组合：**先进入最小Claim路线**，不需要新架构或全面SOTA。
- 只有假说/无可信Run：只可做“题材与可能期刊”探索，档次记`UNKNOWN`，不得将想象中较低的档次作为Task淘汰理由。
- 在`PAPER_PATH_CANDIDATE`、重要Claim变化或用户要求选刊时，按需估计一次；普通调参不反复分档或全网搜期刊。真实投稿前刷新现行期刊规则。

## 2. 稿件潜力四档（**自定义启发式，不是官方JCR/CAS分区**）

| `MANUSCRIPT_POTENTIAL` | 研究贡献的典型范围 | 最合适的下一证据；不是固定强制实验数量 |
| --- | --- | --- |
| **S：领域影响型** | 对广泛的重要问题提供可迁移的新方法/机制/认识 | 展示较广影响、具名强近邻比较与跨场景或理论支持（按主张） |
| **A：有力专业贡献** | 对一个重要专业问题有明确且可信的实质改善/解释 | 相关强参照、关键消融/反解释、独立单位及适当稳健性 |
| **B：完整增量贡献** | 一项有意义的局部收益、标定/资源效率提升、可信规律或组合方法 | 同合法信息的直接强基线、实际代价/不利指标、有效独立确认 |
| **C：聚焦窄贡献** | 适用条件明确的较小新发现、技术改进或短篇贡献 | 与窄Claim匹配的关键对照、误差/不确定性和独立证据 |
| **NONE / UNKNOWN** | 仅已知复现、无独立差额 / 证据尚不可判断 | NONE先保留资产再找别的问题；UNKNOWN做廉价判别；均非项目自动STOP |

**B/C档不是失败**；S/A也不等于必然接收。分档依据问题重要性、对已有知识的新增程度、适用范围与可收集证据，而非固定F1阈值、GPU用量、网络深度或IF；一项重要小改进即使未达全球SOTA仍可具备论文价值。区分`MANUSCRIPT_POTENTIAL`（稿件可发展广度）与现有证据成熟度（`PAPER_PATH_CANDIDATE/CLAIM_WITH_GAPS/CONFIRMED`），不可互相代替。分档可以随着新证据调整，**不得用于自动STOP、自动投稿或宣称质量认证**。

## 3. 第二轴：具体期刊的相对适配梯队

针对**同一篇稿件**给出`STRETCH / TARGET / FALLBACK`，不是S/A/B/C的固定映射；小贡献也可能非常匹配某个专业期刊。使用真实`title/abstract + Claim + 实验/验证范围 + 文章类型 + 作者费用/时间/索引要求`：

1. 从具名最近邻论文的实际发表期刊、近年真正收录的同类文章、出版商Journal Finder或OpenAlex等来源生成小名单；关键词/摘要相似度仅是线索。
2. 先排除**不接收该文章类型、明确范围不符、不符授权费用/许可证等硬约束**的期刊。对每个候选说明近期2–3篇可核查的同方向文章（不足就如实标UNKNOWN）。
3. 查**期刊官方**Aims & Scope、投稿格式、当前索引和费用政策；JCR分区须写年份+学科类别，CAS另列，SCIE/ESCI与SJR不能混写；hybrid期刊须区别可选OA APC与订阅路线。审稿时长和录用率没有可靠来源标`UNKNOWN`，不捏造百分比。
4. 结合Claim成熟度、差距、读者群与篇幅输出一组有证据的`STRETCH/TARGET/FALLBACK`（通常各1–2本、没有合适则少列），并写每一本**最值得补的1项证据**。`FALLBACK`也不保证录用；作者最后决定是否投稿。

**受控输出（只有触发时附加一行，复用CLAIM_EVIDENCE_MAP或STATE索引，不强制新JSON）**：
`CLAIM+RUN | POTENTIAL(S/A/B/C/NONE/UNKNOWN)+WHY+UNCERTAINTY | EVIDENCE_GAPS | VENUES(STRETCH/TARGET/FALLBACK, verified source+date) | NEXT_CHEAP_TEST | AUTH`。
无期刊检索权限、无最新数据或用户尚未要求具体期刊时，`VENUES=NOT_CHECKED`，不猜IF/APC、也不默认联网搜几十本刊。

## 3.5 以稿件完成难度决定下一步

先分别判断：`CLAIM_EVIDENCE` 是否足够，`MANUSCRIPT_COMPLETENESS` 是否有基本结构与必要对照，`VENUE_FIT` 是否存在真实同方向投稿去处。可有B/C档潜力但论文未完成；可写初稿也不等于完成确认。若距离一个匹配专业期刊的最小完整稿件仅剩1–3项有限补证据任务，则先完成它们，不因缺新网络/全面SOTA而扩大研发；期刊层级及IF不作为研究项目生死门槛。缺关键真值/组独立性/近邻新意时明示缺口，不借选低档期刊跳过科学诚信。用户不要求具体选刊时`VENUES=NOT_CHECKED`。

## 4. 失败与论文出口

- 新模型输给简单基线：保留可靠Run；如果发现此前未解释的边界/成本/可靠性规律，继续B/C窄Claim候选，而不强制UP或直接`NO_INDEPENDENT_CLAIM`。
- 仅观察到某个DEV切片正结果：标`EXPLORATORY`、保存切片选择史，必要时用真正独立组验证，不能制造“显著小发现”。
- 最近邻已覆盖所有差额或任务不具备合法真值：当前Claim`NO_INDEPENDENT_CLAIM`或`HOLD`；并非证伪所有数据、任务和研究方向。
- 已有可支持B/C的Claim：优先补直接强基线、关键消融、真实成本测量或独立确认；**不为了追求S/A而自动启动大规模GPU训练**。

## 5. 可借鉴的公开工具（概念参考，不安装、不视为认证）

- [journal-recommender](https://github.com/zero565656/journal-recommender)：按主题、期刊范围和投稿约束做冲刺/目标/保守分层。
- [journal-finder-skill](https://github.com/utkugrhn-source/journal-finder-skill)：检查官方索引、费用、JCR类别、投稿范围，避免混淆分区。
- [Journal Suggestor](https://github.com/harshvardhaniimi/journalsuggestor)：以OpenAlex相近文章作期刊匹配证据。
- [Journal Fit Engine](https://github.com/WENSHAO521/journal-fit-engine)：重视论文学术贡献、目标读者与期刊实际文章类型的匹配。

所有工具均不提供可信的稿件接收概率；此处仅迁移可解释的选刊思路，具体期刊数据必须在当次检索时核实。
