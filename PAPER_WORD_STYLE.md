# PAPER_WORD_STYLE｜PD-RW 通用英文科研论文 Word 格式 v1.1

> **单一默认 Word 样式规范**：适用于算法、传感器、机器人等工程科研的论文蓝图审阅版和获授权的英文稿件工作版。**用户最新要求：所有段落（包括 `Title`）段前/段后均为 `0/0 pt`；全文字体 `Times New Roman`；一级/二级标题零缩进；正文首行缩进 `0.5 in`（`1.27 cm`）。** 本文件不改变论文六章骨架、科学证据、绘图授权或 [WRITING_GATE.md](WRITING_GATE.md) 的写作锁；目标期刊官方模板有明确冲突时以官方要求为准。

## 1. 页面和正文

| 项目 | 固定默认值 |
|---|---|
| 纸张 | A4（210 × 297 mm），纵向，单栏 |
| 页边距 | 上、下、左、右各 `2.5 cm` |
| 全文字体 | `Times New Roman`：标题、正文、图题、表题、表格、参考文献、页眉页脚和所有可控文本样式统一设置 |
| 多语言和数学字符 | Word 字体设置仍为 `Times New Roman`；若某些 CJK 字形或 Word 原生数学排版缺少该字体可用字形，允许系统**仅对缺失字形**回退，须保留文字与可编辑公式，不主动将某一段改成其他字体 |
| 文字颜色 | 黑色 `#000000` |
| 正文对齐 | 两端对齐；项目规划要点、清单可以左对齐 |
| 正文段落 | `11 pt`、`1.15 倍行距`、左缩进 `0`、**首行缩进 `0.5 in`（`1.27 cm`）**、段前 `0 pt`、段后 `0 pt`；包括标题后的首个正文段落 |
| 页眉/页码 | 无页眉；页脚居中，自动 `PAGE` 域、阿拉伯数字 |
| 分栏/分页 | 不强制一级章节换页；正文开启孤行控制，标题启用“与下段同页” |

## 2. Word 样式表（唯一默认，所有段前/段后按 pt）

> **零段距是硬约束**：全部样式**包括 `Title`**（正文、标题、图注、表注、参考文献、项目规划段落等）一律 `0/0 pt`。标题不设左缩进或首行缩进；普通正文（`Normal`）首行缩进 `0.5 in`。禁止用空段落、额外回车、手动段距、软回车或列表设置变相制造段间距。字体统一 `Times New Roman`。

| Word 样式 | 字体、字号 | 字重 / 对齐 | 段前 (pt) | 段后 (pt) | 行距 | 缩进（左 / 首行） |
|---|---|---:|---:|---|---|
| `Title` | Times New Roman 18 pt | 加粗、居中 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Heading 1` | Times New Roman 14 pt | 加粗、左对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Heading 2` | Times New Roman 12 pt | 加粗、左对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Heading 3` | Times New Roman 11 pt | 加粗斜体、左对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Normal` | Times New Roman 11 pt | 常规、两端对齐 | 0 | 0 | 1.15 倍 | 0 / 0.5 in |
| `Blueprint Meta` | Times New Roman 12 pt | 加粗、左对齐、不编号 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Blueprint Note` | Times New Roman 11 pt | 常规、左对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Unnumbered Heading` | Times New Roman 14 pt | 加粗、左对齐、不编号 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `List Paragraph` | Times New Roman 11 pt | 常规、左对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Figure Caption` | Times New Roman 10 pt | 常规、居中 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Table Caption` | Times New Roman 10 pt | 常规、左对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Table Text` | Times New Roman 10 pt | 常规、按表格语义对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Equation` | Times New Roman 11 pt（原生数学缺字形仅按上文回退） | 公式居中、编号右对齐 | 0 | 0 | 1.15 倍 | 0 / 0 |
| `Reference` | Times New Roman 10 pt | 常规、左对齐 | 0 | 0 | 单倍 | 0 / 0 |

- 不允许超过三级**论文章节标题**；需要更细层次时优先以连贯正文段落表达，不建立 Heading 4/5；仅在正式技术定义或目标期刊实际要求时使用短行内术语标记，**不得**靠粗体 `Challenge: / Solution: / Key Insight:` 等对话式标签制造伪小节。文档元信息、Abstract、Keywords、References、Acknowledgments 等使用无编号样式，不占用六章编号。
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

- **编号标题的实际缩进**：`Heading 1`、`Heading 2` 连同自动多级编号的段落均要求左缩进 `0`、首行缩进 `0`，不得因编号模板悄悄带入 `w:ind` 或额外制表位导致正文标题整体右移。`Normal` 的每个正文自然段（含标题后首段）使用真实首行缩进 `0.5 in`，**不是添加空格或 Tab**；图题、表题、公式、参考文献、图表单元格等非正文样式不继承正文首行缩进。
- **正式稿件引言/结论的样式映射**：新稿件 `Introduction` 默认只有一个 `Heading 1`，默认后续直接使用 `Normal` 连续英文段落，**不从蓝图的 `SEC-INTRO-01/02` 或内部标签产生 `Heading 2`、数字 `1.1/1.2`、`List Paragraph` 或贡献清单**；`Conclusion` 通常也直接用 `Normal`，不为唯一段落强造 `6.1`。正式排版时用真实 Heading 样式检查，而不是只看段落字体；期刊规范、文章类型及项目已批准结构需要例外时遵守其约束及用户确认。段落篇幅随科学信息量变化，不为段距 `0/0 pt` 规定统一字数或插入人为换行。
- **叙述性正文不得排成列表**：正式投稿正文的 `Normal` 段落不得使用 `List Paragraph`、Word 自动项目符号/自动编号，或以 `▪ / • / ①②③` 开头把多个自然段写成分点作答。一级/二级学术章节的 Heading 自动编号不属于正文分点，算法伪代码、表格、形式化定义、公式或期刊强制声明除外。正式稿件中非必要圆括号应改写为流畅句子，保留专业术语首次缩写、文献引用、数学与图号等必要括号。`List Paragraph` 样式继续保留供**内部蓝图或明确允许的非叙述材料**，不能因为样式表存在就默认在论文正文使用。
- **防止对话/提纲格式进入 Word 成稿**：在正式投稿稿件导出时核对叙述性正文没有以 `Challenge:`、`Solution:`、`Key Insight:`、`Our Advantages:` 等冒充段内标题；没有纯装饰性粗体、Markdown 残留或带 `TODO/[REF]/[EQ]/[FIG]` 的未消解占位。蓝图 Word 审阅版不同于投稿正文，可保留规划标签与待补证据标记；真实算法伪代码、正式定理、方程、图题、引用和期刊规定的声明保留原有格式，不能因正文风格规则误删。
- 使用 Word 的**真实标题样式与多级列表**生成 `1.` / `3.2` / `3.2.1`；源 Markdown 若自带 `1.` / `3.2` 等编号，导出前剥离显示编号，禁止出现 `1. 1. Introduction`。保留原 `SEC_ID`/Claim–Evidence 映射，不把 ID 当打印标题。
- Markdown H1/H2/H3 与 Word Title/Heading 1/Heading 2 **并非同级直映**；导出流程必须显式转换，不能只用默认的 Pandoc heading 映射并宣称准确。
- Word 详细论文框架审阅版必须忠实呈现现有 `PAPER_BLUEPRINT.md` 的科学叙事、逐节具体论证、结果与边界（详见 [DUAL_DOCUMENT_WORKFLOW.md](DUAL_DOCUMENT_WORKFLOW.md) §1A）；不得把详细内容压缩为机械字段清单。它是现有 `PAPER_BLUEPRINT.md` 的**按需可再生导出件**，不是新增第三份长期科研记忆；无用户明确 Word 导出请求不自动输出 `.docx`。纯框架审阅版仅含提纲/规划字段，不产生投稿式标题、摘要或正文。

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
3. 实际 `.docx` 导出后检查：**图片是否全部在最后一段文字/References 之后、每张图是否紧随图题、单面板图题无 (a)、多面板图题 (a)(b) 与真实面板一致、可见图号是否严格为 `Fig.1` 而非 `Fig. 1.`，并核对正文交叉引用**；同时检查：A4/页边距、**所有可控文字的 `Times New Roman`**/字号、**所有段落（含 Title）段前/段后 `0/0 pt`**、`Heading 1/2` 左缩进及首行缩进均 `0`、`Normal` 首行缩进 `0.5 in`（`1.27 cm`）、真实 Heading 1–3、无双重编号、无空段伪装间距、页码域和图表公式编号；显示效果须渲染复核，不得用单纯文件校验冒充视觉 QA。
4. 用户未请求 Word 导出时只维护 Markdown 蓝图。目标期刊官方 Word/LaTeX 模板与图像后置/图题格式有明确冲突时，应**先说明差异并经用户确认**，再生成**另一个投稿格式版本（投稿专用版）**；不擅自改变本工作稿规范、科研事实、既有蓝图或原始证据。
