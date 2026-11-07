# 绘图模块：按需读取（INDEX_ONLY）

**唯一绘图授权来源**是用户对指定图片的明确请求；权威门禁见 [FIGURE_POLICY.md](../../FIGURE_POLICY.md)。本索引只帮助找到规则和工具，不能触发绘图、预览或自动导出。

| 图片类型或问题 | 只加载相关规则 |
|---|---|
| 数据图（坐标轴箭头、柱状图标记、多子图对齐） | [FIGURE_POLICY §4.5](../../FIGURE_POLICY.md) |
| 算法架构图、机制示意图 | [ACADEMIC_DIAGRAM_STYLE.md](../../ACADEMIC_DIAGRAM_STYLE.md) |
| 架构图增量设计缓存 | [FIGURE_SPEC 模板](../../templates/FIGURE_SPEC.example.json) 和已存在的项目 `.drawio` |
| 数据图脚本与实际 QA | RWF `tools/figure_templates.py`、`tools/figure_qa.py`，按需参考 [RWF 绘图规范](https://github.com/phr-devil/Research-Workflow-Forge/blob/main/docs/FIGURE_STYLE_SYSTEM.md) |

同一项目优先复用已冻结配色/模板与合法数据。只修改标签或图例时不要重新读取完整历史研究；来源改变仍须核查相关真实证据，最终出版尺寸的视觉检查不可省略。RWF 是可选实现工具，不是科研主控。
