# MANUSCRIPT_WRITING｜证据驱动的论文正文写作与审校

> **专题执行规范，非科研第七阶段、非新增人工审批。** 仅在 [WRITING_GATE.md](WRITING_GATE.md) 的「科研成果总结经用户审查 + 独立明确正文写作授权」同时可核实后，才允许生成投稿式标题、摘要、章节正文或初稿。纯蓝图规划继续按 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md)；科研权限与数据来源以 [WORKFLOW.md](WORKFLOW.md) 及真实源工件为准；本文件不能授权 SEALED/CONFIRMATION 访问、训练、绘图、下载、外传或投稿。

## 1. 原则与最小输入

- **单一科学事实源**：优先复用项目已存在的 \`RESEARCH_RECORD.md\` 当前快照、\`PAPER_BLUEPRINT.md\` 相关 SEC_ID、合法 Run/冻结协议/研究成果总结、真实 Methods、图表源数据和用户批准的结构。摘要、旧图、AI 记忆、项目内部结论标签都不能代替原始证据；冲突时标 \`SOURCE_CONFLICT\` 并追查，不自行选有利版本。
- **证据不等于表达**：写作只能清楚呈现已经成立的结果，不能把 DEV、探索性观察、负结果、统计不显著、内部确认或无效 Run 提升为新的科学主张；研究数据角色、独立单位、分母、筛选史、统计范围和限制随 Claim 保留。
- **唯一可编辑正文源**：获授权后使用现有稿件，或建立 \`MANUSCRIPT_TEXT.md\`；不允许不同 Agent 维护互相竞争的完整论文版本。可选 \`MANUSCRIPT_OPEN_ITEMS.md\` 只记录未决引用、公式、证据或作者决定，是稿件待办，不是第三份科研记录。Word/LaTeX/PDF 从正文源按请求生成，不反向成为科学依据。
- **尊重已批准目录**：实证算法稿默认六章，Critical Review / Perspective 按文章类型与目标期刊选用专用规划结构；既有项目已获用户确认的 \`Methodology\` 等例外照旧。合并、重排、更名一级章节或重大二级结构调整，依 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) 先给必要性/依据/影响并获用户确认；本写作流程不授予自行改章权。
- **强表达原则**：科学正确性 > 推理逻辑 > 信息结构 > 清晰度 > 简练度 > 风格。已证实的观察直接写、精确量化；需要保留的不确定性只在适用主张处限定，不以大量 may/might 稀释真实结果，也不以强语气制造因果、机制、泛化或算法优势。

### 高水平论文范例学习：写正文前必须匹配案例

1. **R1 必查 [Paper Exemplar Library](paper_exemplars/README.md)**，按照研究贡献类型、当前章节论证职责和目标读者选择1–3张策略卡；仅阅读匹配卡片。无适配者记 **EXEMPLAR_NONE + reason**，不强行套用顶刊结构，也不因案例缺失阻断有证据的写作。
2. 在既有 Section Contract 或临时写作备忘中记录 **EXEMPLAR_IDS | why_match | ADOPT | AVOID**；仅保留可迁移的写作决策、段落功能与语言力度，**不导入案例的实验数据、模型、参考文献结论或独特措辞**。这一记录不进入投稿正文，也不是第三份长期科研文件。
3. **R2** 在Methodology/Results写作时参考案例的“定义→方法→证据”与“问题→结果→解释”组织策略；**R3** 在Related Work/Discussion/Introduction/Abstract写作时参考问题收窄、贡献表达、段落过渡和真实局限；**R4** 只在科学审核后参考语言清晰度，并核对精修前后科学主张是否一致。
4. **不重复读取全文**：研究类型/中心Claim没有变化时复用先前选择；局部段落修改只用已选策略卡与受影响章节。案例已有基于用户PDF的来源页码，但PDF未随GitHub发布；需要原文细节时仅在合法可访问的范围按需回查。只有策略卡可读时不得声称本轮重新核验了全文。
5. **权威边界**：科研结果、Claim–Evidence、已批准目录和 [WRITING_GATE.md](WRITING_GATE.md) 权限高于所有范例；后置Methods、七章结构、SOTA叙述不授予改章、运行新实验、下载、绘图或SEALED访问。案例用来学习写法，不自动成为本项目Related Work的证据，原文支持仍需单独核查。

## 2. 六个功能模块（按需组合，非六个 Agent）

| 模块 | 输入与工作 | 交付/核查 |
|---|---|---|
| M1 Evidence Contract | 复用可信 Claim–EXP/Run–协议–数据/图表映射；记录 metric、unit、denominator、independent_unit、cohort/split、CI、selection_history、confirmatory/descriptive/exploratory、负证据及作废版本。只查看已有合法数据，不重跑科研/SEALED。 | **精简证据快照**；未验证项标 \`UNVERIFIED\` / \`SOURCE_CONFLICT\` / \`NOT_RUN\`，不进入确定性陈述。 |
| M2 Argument Architecture | 用一行写清研究问题、主 Claim、贡献类型、3个以内关键支持证据、最强反解释和适用边界；为相关 SEC_ID 设定 section contract。 | **North Star + Claim hierarchy + 段落职责**；主结果与图片对应，非贡献信息可移到 SI/省略，但不得删负证据。 |
| M3 Evidence-to-Prose | 先固定决定结果含义的测量/评价定义，再将对应主要 Results 写成自然英文；补齐 Methods/Results 后处理 Related Work、Discussion、Introduction、Conclusion、Abstract、Title。 | **可直接修改的正文**；先事实后诠释，不写实验流水账，不为凑字数重复背景或结果。 |
| M4 Source & Placeholder | 需要外部文献时核实「原文具体段落是否支持该句」及 DOI/版本/条件；用户自行补文献时仅保留可追溯的具体引用需求。公式、图表只占位，不伪造公式或图。 | \`[REF:R01 — claim requiring source]\`、\`[EQ:E01 — exact definition]\`、\`[FIG:F01 — intended panel]\`；不使用虚构 [1]/DOI 或占位文献推导确定性近邻结论。 |
| M5 Scientific Audit | 核 Method ↔ Result ↔ figure/table ↔ Discussion ↔ Abstract 的数值、口径和定义；查证据强度、统计单位、因果措辞、失效/负结果、最近邻原文。 | 分级问题：\`BLOCKER\`（无证据/无效/冲突），\`MAJOR\`（口径/论证改变），\`MINOR\`（术语/衔接），\`STYLE\`；仅修复受影响位置。 |
| M6 Prose & Delivery | 科学主线稳定后再去机械化、审计口吻和过度防御；段落连接、重复、语气及刊物格式按需精修。精修后再次核查所有改变了的数值、限制、Claim、图/引用与公式占位。 | **最终可审阅纯文字稿 + 未解决事项**；完成文字 ≠ 科学确认、正式投稿准备或作者审批。 |

### Section Contract：每节只需六项

\`Question | Main message | Evidence IDs & status | Paragraph roles | Figures/Tables | Boundary\`

按论证需要设段落，不固定段数或字数。段落只承担一项主要任务；图呈现数据，正文陈述推断。相同核心数值可在 Results、Abstract、Conclusion 按各自功能有限重复，但禁止各章重复整段解释。若现有 \`PAPER_BLUEPRINT.md\` 已含这些字段，复用而不另造计划文件。

### Claim Strength Calibration：强而不虚

**科研表达不等于保守写作**：`OBSERVED` 有直接证据；`INTERPRETATION` 要符合观测并容许反解释；`HYPOTHESIS` 可提出有科学意义的机制与可证伪预言，但不能称已证明因果；`VISION/ADVOCACY` 可明确提出原创概念框架、技术愿景、标准化或跨学科倡议，讲清实现条件、障碍及可检验里程碑。未来构想无需已被全面实验验证，但不可写成既成事实。不要用大量 may/might 和免责声明消除作者立场。综述/Perspective 的学术贡献可来自高质量证据综合、争议澄清和研究议程，而不必提供算法得分。


| 支持程度 | 用词策略 |
|---|---|
| 真实直接观察/已确认效应 | \`shows\`、\`accounted for\`、\`was observed\` 等直陈，并就近给出条件、数值或范围。 |
| 描述性/探索性差异 | \`was higher\`、\`differed\`、\`was associated with\`；明确研究范围，但不自动加 may/might。 |
| 未直接检验的机制/因果解释 | \`is consistent with\`、\`may reflect\`；仅作为可能解释，不写成证明。 |
| 阴性、不确定、矛盾结果 | 准确给出实际比较及 CI/统计边界；不把未显著写成等效、不把失败试验包装成成功，也不自我贬低。 |
| 没有证据 | 不写成事实；保留明确待查标记，或删除/缩窄主张。 |

**防止润色升级 Claim**：例如 \`highest observed AUROC under evaluated conditions\` 不得被改成 \`consistently outperformed competing methods\`。必要的样本量、独立性、输入合法性和研究范围是科学信息，不属于应删除的“防御式写作”；冗余内部 Run ID、Bug 追踪、测试通过数和审计措辞一般不应出现在稿件正文，除非直接决定可复现性或结果解释。

## 3. 四轮自主执行（依赖而非固定人工确认）

| 轮次 | 执行顺序与技能借鉴 | 最小产出 |
|---|---|---|
| R1 证据与论证 | **M1→M2**。先核合法科研快照及最强最近邻；定义 North Star、Claim 层级、现有结构与各节职责。复用既有快照，资料没变化不得重复通读全库。 | 临时证据/段落合同；科学冲突的受影响节标 BLOCKER。 |
| R2 核心正文 | **M3+M4+增量 M5**。实证稿先配对 Method/Measurement definition 与主要 Result；综述先综合原始文献与争议，Perspective 先组织核心论点与最强反解释；不强造不存在的方法/实验。 | 两章关键正文及待补公式/图表/文献位置。 |
| R3 其余正文 | **M3+M4+增量 M5**。实证稿据已有 Results 完成 Discussion、Related Work、Introduction 与 Conclusion；综述/Perspective 从核实的文献证据、原创框架及条件性展望组织剩余章节；最后 Abstract、Title、Keywords。 | 六章完整稿件；无证据文献论断仍待查，不能假完成。 |
| R4 科学与文字闭环 | **M5→M6→针对修改的回归 M5**。先科学/跨章与引用审查，再段落逻辑、语气与格式；按 BLOCKER/MAJOR/MINOR 优先局部修订，不反复整稿重生。 | \`MANUSCRIPT_TEXT.md\` + 必要时 \`MANUSCRIPT_OPEN_ITEMS.md\`。 |

R2 重点是**方法定义与结果一对一对应**，不是一次性写完 Methods 再机械填所有实验。R3 的执行顺序与最终论文阅读顺序不同；最终顺序遵循已批准的目录。四轮可以在同一次已授权 WorkBuddy 任务中连续完成，不额外要求四次用户确认。必要重大结构/科研范围/数据权限变化，仍遵守原有用户决策门禁。

## 4. 核心质量核验与失败处理

1. **科学事实**：所有重要数字、效应、比较与方法必须有原始证据指针；同一指标检查样本、窗口、事件、受试者、分母及 CI 是否匹配；不得用 AI 总结、截图、美化图代替冻结数据源。
2. **验证边界**：明确 DEV、VAL、封存确认、外部验证及其他项目的既有接触史；不可把同源 held-out 说成全独立外部验证，不能由图片或论文生成流程读取 SEALED。
3. **方法—结果双向**：每项 Results 都能找到对应 Method/指标定义；每个声称已执行的重要方法能找到结果、目的或“没有结果”的明确状态；模型版本、训练合法输入、基线和时间方向不得漂移。
4. **外部文献**：验证的是“原文支持具体 Claim”，而不只是 DOI 真实；无法取得全文时标 \`SOURCE_UNVERIFIED\`，不自动写确定性首创/最优/研究空白或比较数值。
5. **论证与语言**：段落与主 Claim 有关，负结果与最强反解释不遗漏；既不能把论文写成审计记录，也不能删掉决定方法含义的限制与声明。
6. **结果改变时的局部影响追踪**：仅更新相关 Results、对应 Method/figure/caption、Discussion、Introduction、Abstract、Conclusion 和引用位置；标明变更原因，不覆盖旧有效 Run，不全篇盲目改写。
7. **检查分层**：程序只可确定性检查明确列出的数字、标识、占位符、重复编号和结构引用；科学解释与原文支持须人/Agent逐项核真实来源。静态测试 PASS 不等于稿件科学正确、Q2潜力或投稿授权。
8. **停机与升级**：\`BLOCKER\` 只阻断依赖它的确定性陈述；其他可信章节继续。需要额外实验、重新确认、访问付费/受限材料、外传或改动已批准结构时报告授权/作者决定，不擅自执行。只有有实质问题才做下一轮修订；不得靠固定轮数或多个 Agent 相互重复审稿。

## 5. 最小交付与适用 Skill

- 默认输出**英文纯文本/Markdown**；数学先保留语义完整的 \`[EQ:...]\`，不提前硬编码最终公式编号；引用由用户补充时保留有具体 Claim 的 \`[REF:...]\`；图表只占位（无绘图授权不得出图）。如用户明确要求 Word，才使用 [PAPER_WORD_STYLE.md](PAPER_WORD_STYLE.md) 排版并真实渲染检查。
- 正文中不保留 \`SEC_ID\`、历史 Run 路径、开发审计备注等项目管理用语；这些仅在内部证据映射和未决事项中。涉及方法复现的必要协议、参数、限制与数据获取声明必须保留。
- 只报告关键成果、真实验证范围、BLOCKER 和需作者处理的事项；不要创建冗余长期文档、单独 Agent 日志、多个“最终稿”或无意义的全文反复润色。

**按需借鉴的公开原始项目（不强制安装全部、不得声称已调用）：**

- [K-Dense Scientific Writing](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-writing)：证据绑定、数值/Methods–Results 一致性、引用及作者责任。
- [Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)：\`manuscript-optimizer\`（Claim Architecture）、\`stats-reporting-audit\`、\`claim-source-verification\`、\`anti-defensive-writing\`。
- [Academic-Paper-Skills](https://github.com/DELONG-L/Academic-Paper-Skills)：\`paper-writing\`（正文生成）、\`paper-review\`（局部审查与闭环）。
- [latex-paper-skills](https://github.com/yunshenwuchuxun/latex-paper-skills)：\`empirical-paper-writer\` 的证据/占位状态思想；不导入全套 LaTeX/issue 系统。
- [PaperQA2](https://github.com/Future-House/paper-qa)：可选的原文检索辅助；检索命中不自动证明 Claim 正确。

**核心原则：以可追溯证据支撑清晰、有力度的科学论证；只有事实变化才更新依据，只有实际缺陷才重写正文。**
