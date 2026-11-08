# PAPER_WORD_STYLE｜PD-RW 通用英文科研论文 Word 格式 v1.0

> **单一默认 Word 样式规范**：适用于算法、传感器、机器人等工程科研的论文蓝图审阅版和获授权的英文稿件工作版。**用户最新要求：除 `Title` 外，所有段落样式一律段前 `0 pt`、段后 `0 pt`；`Title` 为 `0/18 pt`。** 本文件不改变论文六章骨架、科学证据、绘图授权或 [WRITING_GATE.md](WRITING_GATE.md) 的写作锁；目标期刊官方模板有明确冲突时以官方要求为准。

## 1. 页面和正文

| 项目 | 固定默认值 |
|---|---|
| 纸张 | A4（210 × 297 mm），纵向，单栏 |
| 页边距 | 上、下、左、右各 `2.5 cm` |
| 西文字体 | `Times New Roman` |
| 中文说明字体 | `SimSun`（宋体）；缺失时使用兼容的可嵌入 CJK 字体，不依赖假定本机可用 |
| 文字颜色 | 黑色 `#000000` |
| 正文对齐 | 两端对齐；项目规划要点、清单可以左对齐 |
| 正文段落 | `11 pt`、`1.15 倍行距`、首行缩进 `0`、段前 `0 pt`、段后 `0 pt` |
| 页眉/页码 | 无页眉；页脚居中，自动 `PAGE` 域、阿拉伯数字 |
| 分栏/分页 | 不强制一级章节换页；正文开启孤行控制，标题启用“与下段同页” |

## 2. Word 样式表（唯一默认，所有段前/段后按 pt）

> **零段距是硬约束**：以下列出的所有非 `Title` 样式（含图注、表注、参考文献、编号与项目规划段落）均为 `0/0 pt`。不要用空段落、额外回车、手动段距、软回车或列表设置变相制造间距。标题的层级只靠字号、粗细、排版和语义区分。

| Word 样式 | 字体、字号 | 字重 / 对齐 | 段前 (pt) | 段后 (pt) | 行距 |
|---|---|---|---:|---:|---|
| `Title` | Times New Roman 18 pt | 加粗、居中 | 0 | 18 | 1.15 倍 |
| `Heading 1` | Times New Roman 14 pt | 加粗、左对齐 | 0 | 0 | 1.15 倍 |
| `Heading 2` | Times New Roman 12 pt | 加粗、左对齐 | 0 | 0 | 1.15 倍 |
| `Heading 3` | Times New Roman 11 pt | 加粗斜体、左对齐 | 0 | 0 | 1.15 倍 |
| `Normal` | Times New Roman 11 pt | 常规、两端对齐 | 0 | 0 | 1.15 倍 |
| `Blueprint Meta` | Times New Roman 12 pt | 加粗、左对齐、不编号 | 0 | 0 | 1.15 倍 |
| `Blueprint Note` | Times New Roman 11 pt | 常规、左对齐 | 0 | 0 | 1.15 倍 |
| `Unnumbered Heading` | Times New Roman 14 pt | 加粗、左对齐、不编号 | 0 | 0 | 1.15 倍 |
| `List Paragraph` | Times New Roman 11 pt | 常规、左对齐 | 0 | 0 | 1.15 倍 |
| `Figure Caption` | Times New Roman 10 pt | 常规、居中 | 0 | 0 | 1.15 倍 |
| `Table Caption` | Times New Roman 10 pt | 常规、左对齐 | 0 | 0 | 1.15 倍 |
| `Table Text` | Times New Roman 10 pt | 常规、按表格语义对齐 | 0 | 0 | 1.15 倍 |
| `Equation` | 数学字体 11 pt | 公式居中、编号右对齐 | 0 | 0 | 1.15 倍 |
| `Reference` | Times New Roman 10 pt | 常规、左对齐 | 0 | 0 | 单倍 |

- 不允许超过三级**论文章节标题**；需要更细层次时用正文内加粗短标签，不建立 Heading 4/5。文档元信息、Abstract、Keywords、References、Acknowledgments 等使用无编号样式，不占用六章编号。
- 空白应来自内容语义和章节编排，而不是段前/段后间距；标题在 Word 中设置 `keep_with_next`、正文 `widow_control`，必要时为完整表行设置不跨页。

## 3. 标题编号与 Markdown → Word 映射

| `PAPER_BLUEPRINT.md` 源结构 | Word 目标样式 / 编号 |
|---|---|
| `# PAPER_BLUEPRINT ...` | `Title`，不编号 |
| `## Planning Snapshot`、`## Claim–Evidence–Section Index`、`## Planning Change Notes` | `Blueprint Meta`，不编号 |
| `## 1. Introduction` 等六章 | `Heading 1`，与 Word 多级编号第1级绑定 |
| `### 3.2 Core Method and Mechanism` | `Heading 2`，与多级编号第2级绑定 |
| 按用户确认新增的 `#### 3.2.1 ...` | `Heading 3`，与多级编号第3级绑定 |
| 规划字段 `Purpose / Key Points / Evidence / Gaps / Planned Figures` | `Blueprint Note` 正文加粗字段名，不作为标题 |
| 获授权正式稿件的 `Abstract / Keywords / References / Acknowledgments` | `Unnumbered Heading`，不编号 |

- **正式稿件引言/结论的样式映射**：新实证稿 `Introduction` 为一个 `Heading 1`，默认后续直接使用 `Normal` 连续英文段落，**不从蓝图的 `SEC-INTRO-01/02` 或内部标签产生 `Heading 2`、数字 `1.1/1.2`、`List Paragraph` 或贡献清单**；`Conclusion` 通常也直接用 `Normal`，不为唯一段落强造 `6.1`。正式排版时用真实 Heading 样式检查，而不是只看段落字体；期刊规范、文章类型及项目已批准结构需要例外时遵守其约束及用户确认。段落篇幅随科学信息量变化，不为段距 `0/0 pt` 规定统一字数或插入人为换行。
- 使用 Word 的**真实标题样式与多级列表**生成 `1.` / `3.2` / `3.2.1`；源 Markdown 若自带 `1.` / `3.2` 等编号，导出前剥离显示编号，禁止出现 `1. 1. Introduction`。保留原 `SEC_ID`/Claim–Evidence 映射，不把 ID 当打印标题。
- Markdown H1/H2/H3 与 Word Title/Heading 1/Heading 2 **并非同级直映**；导出流程必须显式转换，不能只用默认的 Pandoc heading 映射并宣称准确。
- Word 蓝图是现有 `PAPER_BLUEPRINT.md` 的**按需可再生导出件**，不是新增第三份长期科研记忆；无用户明确 Word 导出请求不自动输出 `.docx`。纯框架审阅版仅含提纲/规划字段，不产生投稿式标题、摘要或正文。

## 4. 图片、表格、公式和引用

- **图的唯一默认位置**：正式论文工作稿中的所有图片（多子图作为一张整体图片）都排在**全部正文文字、Conclusion、Acknowledgments/Declarations、References 之后**的末尾 `Figures` 区域；正文中只保留 `Fig.1`、`Fig.1(a)` 等交叉引用，不在正文段落中内嵌图片或图注。图片居中、不超版心宽度，**图题紧跟对应图片下方**，使用 `Figure Caption` 样式。此规则只约束正文撰写及 Word 导出，不作为 `MANUSCRIPT_QA.md` 的事后修改指令。
- **图题显示格式（精确）**：单幅单面板为 `Fig.1 Overall description.`；真实多面板为 `Fig.1 Overall description. (a) Panel a description. (b) Panel b description.`，其余面板按 `(c)`、`(d)` 依次排列。严格 `Fig.` 紧贴自动数字、数字后一个空格接标题；**不使用** `Fig. 1.`、`Fig.1.`、`Figure 1`；**只有一个面板时不得写 `(a)`**。首句概括整图，每个子图说明独立对应真实面板；无面板时不生成 `(a)` 标签。
- **Word 字段实现**：用 `Fig.` + 紧贴的 `SEQ Figure` 字段 + 单个空格 + 图题文本构造显示，数字后的句点只属于图题内容而**不是编号格式**；为数字建立书签，并为正文 `Fig.1` / `Fig.1(a)` 等绑定可更新交叉引用。导出后刷新/物化字段显示并检查源文本、Word 字段与真实渲染，禁止错号、漏号或多余句点。
- **表**：优先三线表，表题在上方、`Table Caption` 样式、`Table 1. ...` 自动序号；单元格 `Table Text`，不人为增加段距。
- **公式**：居中，公式编号右对齐 `(1)`；变量、上下标、单位按通行数学/物理规范处理，使用 Word 原生公式而非用图片代替。
- **交叉引用**：正文对图、表、公式使用可更新的 Word 域/书签，避免人工输入易漂移的编号。
- **图源缺失时**：正文仅提供必要的图号引用；末尾 `Figures` 处保留 `MISSING_FIGURE` 文字占位（图题可标 DRAFT），不伪装为真实插图，也不自动创建图片。允许使用的既有图片直接后置，不改变 [FIGURE_POLICY.md](FIGURE_POLICY.md) 绘图授权边界。
- **参考文献**：审阅默认编号引用 `[1]`、`[2]`；`Reference` 样式 `10 pt`、单倍行距、**段前段后 `0/0 pt`**。实际文献条目与引用必须有真实来源，投稿时遵守期刊指定样式。
- Word 框架中的图表仅记录文字规划，不因 Word 导出而绘图；实际出图须 [FIGURE_POLICY.md](FIGURE_POLICY.md) 的用户请求。

## 5. 执行与最小验收

1. 确认当前请求是**蓝图 Word 审阅版**还是**正式稿件 Word 工作版**；蓝图可在 `WRITING_LOCKED` 期间按用户的 Word 导出要求生成，正式稿件须先通过科研总结审查及独立写作授权。不得把格式需求当作写作授权。
2. 复用同一已核实的 `PAPER_BLUEPRINT.md`（或获授权正式稿件）作为内容源；只在确有 Word 导出需求时使用现有 Word/Pandoc/python-docx 工具，不要求为普通科研项目预装全套工具。
3. 实际 `.docx` 导出后检查：**图片是否全部在最后一段文字/References 之后、每张图是否紧随图题、单面板图题无 (a)、多面板图题 (a)(b) 与真实面板一致、可见图号是否严格为 `Fig.1` 而非 `Fig. 1.`，并核对正文交叉引用**；同时检查：A4/页边距、`Times New Roman`/字号、全部非 Title 的 `0/0 pt`、Title `0/18 pt`、真实 Heading 1–3、无双重编号、无空段伪装间距、页码域和图表公式编号；显示效果须渲染复核，不得用单纯文件校验冒充视觉 QA。
4. 用户未请求 Word 导出时只维护 Markdown 蓝图。目标期刊官方 Word/LaTeX 模板与图像后置/图题格式有明确冲突时，应**先说明差异并经用户确认**，再生成**另一个投稿格式版本（投稿专用版）**；不擅自改变本工作稿规范、科研事实、既有蓝图或原始证据。
