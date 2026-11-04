# Venue Strategy｜JCR Q2+ 科研潜力与期刊适配（活动03、05–06按需）

**科研目标与优先级**：以[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)为统一成功口径：**有证据支持的JCR Q2或更高期刊投稿潜力**即达到论文导向项目科研目标，优先争取Q1；**实际录用不是必要条件，也不可保证**。这是研究判断而非写作授权；[WRITING_GATE.md](WRITING_GATE.md)继续禁止未经“科研成果总结→用户审查→独立明确写作许可”的初稿/摘要/章节生成。本文件仅评估主张和期刊匹配，不新增阶段/CLI事件或自动投稿。

## 0. 何时查期刊：早期找先例，后期核实分区

- **选题阶段**：在明确方向时，轻量对比1–3篇该领域**真实已发表**的Q1/Q2相似研究，检查问题重要性、核心贡献与决定性实验；未查清类别/年度标`VENUE_ANALOGS_UNKNOWN`，**不因未知而放弃探索**。
- **可信结果/重要Claim变化/准备收束**：读具名最近邻原文，核最相关的1–3本真实期刊及近期同类型论文，判断科学主张是否具备Q2竞争力，指出最重要的1–3项证据差距。
- **具体投稿前（经用户授权）**：重新核索引、最新JCR、文章类型、官方Aims & Scope、投稿要求与费用；不需每轮重复检索。

## 1. JCR Q2+ 核验口径（不等于“IF固定阈值”）

每个具体期刊按下列字段留证：`JOURNAL | JCR_EDITION | JCR_SUBJECT_CATEGORY | QUARTILE(Q1/Q2/OTHER/UNKNOWN) | INDEX(SCIE/ESCI/other) | VERIFICATION_SOURCE+DATE | ACCEPTED_ARTICLE_TYPE | RECENT_ANALOGS`。

1. **JCR分区与影响因子不同**：Q1/Q2按指定JCR年度、学科类别确定，分区可能随年份或学科而异；影响因子不可以直接换算Q2。与中科院分区、Scimago/SJR等级分别记录，不得混同。
2. **具名真实来源**：优先可核实的Clarivate/JCR记录、期刊/出版商官方范围与近年实际同类论文。第三方分区表可做线索，但无法核实即`QUARTILE_UNVERIFIED`，不凭猜测给出已核实Q2。优先SCIE，如用户明确要求SCIE才将其列为额外硬约束；不要默认混淆ESCI和SCIE。
3. **论文适配胜于IF**：至少解释一项主张如何与目标期刊近期真实同类型工作在问题价值、证据规模、比较强度和读者群上可比。不能凭刊名相似、几个关键词或“某刊是Q2”断言论文达到Q2。
4. **不预测录用率**：JCR是期刊层面的分类，不是单篇论文质量证书；没有官方可信录用概率标`UNKNOWN`。没有可靠当前来源时不编造JIF、类别、分区和费用。

## 2. 两根独立坐标轴

**A. `MANUSCRIPT_POTENTIAL`（旧S/A/B/C启发式）**：S/A/B/C继续仅表示科学主张的潜在广度、增量与成熟路线；**一律不得直接映射JCR分区**。B/C可以是真实可信的研究成果，但**并非自动Q2项目成功**；S/A同样不会自动达成Q2。科学证据不足但已有线索标`UNKNOWN`，不要早期乱判失败。

**B. `Q2_COMPETITIVENESS`（科研成功轴）**，遵循[Q2_PUBLICATION_GOAL.md](Q2_PUBLICATION_GOAL.md)：

| 判决 | 能作出的结论 | 下一步 |
|---|---|---|
| `Q2_POTENTIAL_SUPPORTED` | 有真实科学证据、具名近邻原创差额、有效公平对照/必要确认，以及可核实的相关Q1/Q2期刊与近期同类发表先例，足以支持“具有Q2+投稿竞争力”的判断 | **科研成功**；成果总结、交用户审查，写作须另获授权 |
| `Q2_UPGRADE_POSSIBLE` | 当前贡献或证据不足，但有可信、可证伪、成本合理的机制/能力/规律升级 | 按需科学升级或补决定性证据；Q1优先，但不为影响因子无界堆模型 |
| `Q2_UNCERTAIN` | 近邻原文、评价可信度、独立确认或最新期刊依据不足 | 补最小缺失事实；暂不宣布成功或失败 |
| `BELOW_Q2_TARGET` | 真实差额/重要性/验证不足，且有依据的升级路线已不可行或不值得 | 保留资产，建议转向或项目级失败收束；项目结束按用户权限执行 |

`PAPER_PATH_CANDIDATE`、`DRAFTABLE`、开发集显著提升、普通专业期刊可发**不等于**`Q2_POTENTIAL_SUPPORTED`；未收到期刊录用也**不阻止**证据充分时判科研成功。

## 3. 同一Q2+标准内尽可能投更高水平

对目标研究提出少量有证据的期刊梯队（通常`STRETCH / TARGET / FALLBACK`各0–2本）：`STRETCH`优先真实适配Q1或更有影响力的专业刊，`TARGET`为可信且匹配的Q1/Q2，`FALLBACK`只能是**仍在Q1/Q2最低目标内**的可行去处。若没有真实适配的Q2+期刊，输出`VENUE_FIT_UNKNOWN/BELOW_Q2_TARGET`并说明证据，**不能拿Q3/Q4作为项目成功退路**。

科研判断优先比较**问题重要性、主张实际增量、最强同条件参照、关键机制反解释、独立证据/组级不确定性与真实适用边界**；不要求所有项目必须全新网络、跨多个数据库、最高F1或理论证明。选定最有价值的1–3项证据缺口；如升级确实有机会提升Q2→Q1竞争力，且成本合理，可继续一组有界实验，不受“已有B/C小稿就直接结束”的旧规则约束。

## 4. 正确止损与输出

- 只得到一个正向DEV切片/后验挑组：`EXPLORATORY / Q2_UNCERTAIN`，不是已确认新规律。
- 算法输给强简单基线但揭示可信边界/部署成本规律：保护Run，核独立价值与确认资格，仍可研究Q2路径。
- 具名最近邻已覆盖全部贡献、没有新的合法区分性问题：`BELOW_Q2_TARGET`候选，并建议HOLD/PIVOT；不能只因一次负Pilot就判整个项目失败。
- 结果达到Q2潜力且未获用户写作许可：**只形成科研成果总结，不写论文**；实际接收和发表视为外部事件，不改变此写作规则。

**最短输出（只有真正触发时）**：
`CLAIM+RUN | NEW_KNOWLEDGE+NEAREST_ORIGINAL | Q2_DECISION+REASONS | Q1/Q2_VENUE+JCR_YEAR/CATEGORY/SOURCE_OR_UNKNOWN | MAIN_EVIDENCE_GAPS(1..3) | NEXT+AUTH/COST`。
省略与本轮决定无关的APC、几十本刊和装饰图。

## 5. 工具来源（概念参考，非自动认证）

- [journal-recommender](https://github.com/zero565656/journal-recommender)：按范围、稿型与费用筛目标。
- [journal-finder-skill](https://github.com/utkugrhn-source/journal-finder-skill)：提醒检查官方索引、类别与JCR年份。
- [Journal Suggestor](https://github.com/harshvardhaniimi/journalsuggestor)：使用相似已发表论文作为期刊范围线索。
- [Journal Fit Engine](https://github.com/WENSHAO521/journal-fit-engine)：重视贡献实质与读者群匹配。

这些工具不提供可靠的录用概率，也不会替代主张证据、期刊官方核验和用户科研决定。
