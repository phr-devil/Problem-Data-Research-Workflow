# PD-RW 仓库轻度分层维护说明（INDEX_ONLY）

## 1. 本次边界：先增导航，不迁权威

- 唯一 Agent 默认入口：[`AGENTS.md`](../AGENTS.md)。
- 唯一科研决策主控：[`WORKFLOW.md`](../WORKFLOW.md)；原有三循环/六活动和授权门禁不修改。
- [`policies/README.md`](../policies/README.md) 与 [`modules/README.md`](../modules/README.md) 及其研究、论文、绘图专题索引只是轻量**路径清单**（INDEX_ONLY），无新增规则或审批。旧路径与脚本全部保留，无双份规范。
- 研究项目内的 `RESEARCH_RECORD.md` / `PAPER_BLUEPRINT.md`、Run/STATE 和所有原始证据位置不变；原测试仍可直接访问根目录权威文档。
- RWF 保持独立仓库：PD-RW 设科研问题、科学主张、论文及图像授权；RWF 可选地实现真实指标复算、图型模板和静态 QA。PD-RW 不复制其实现代码。
- 论文正文写作的稳定执行规范放在根目录 [MANUSCRIPT_WRITING.md](../MANUSCRIPT_WRITING.md)；
- 完整稿件**生成之后**的独立审核与局部修订验收由根目录 [MANUSCRIPT_QA.md](../MANUSCRIPT_QA.md) 主责；不复制写作流程或新增授权机制。[WRITING_GATE.md](../WRITING_GATE.md) 继续唯一负责写作授权，模块索引只提供路径指针，不出现第二套权限。

## 2. 按任务的最小读取

1. 先读 **用户当前目标和真实授权**；若知道原项目直接定位其 STATE、`RESEARCH_RECORD.md` 首页及相关 `PAPER_BLUEPRINT.md` 章节，不通读历史。
2. 用 `AGENTS.md` 的现成直接路由选一个相关权威文件；若分类仍不明确，**才**查模块索引。不得把“入口 → 索引 → 所有模块”当成必经步骤。
3. 分清原始来源、权限、方法与样式：科学事实由真实合法 Run/Methods 支持；权限由用户实际请求和原权威文件控制；索引和主题文件不能授权操作。
4. 仅按变更影响范围更新当前科研/论文文件并执行必要测试；图片任务始终保持明确出图许可，正式稿件保持独立写作门禁。
5. 输出新增证据、判断、未解决项和下一合法行动；不产生第三份科研日志，不自动画图、写稿或训练。

## 3. 后续增量维护

- 新专题**先归属现有权威文件**；只有长期稳定且确有独立职责时再新增规范。目录 README 只加指针，不复制强制科学要求。
- 迁移权威文件（若日后确有需要）应单独授权/评估，先更新全部引用和调用方，保留兼容层，通过 Linux/Windows CI 和旧项目回归测试后再考虑删除旧路径；**本轮不做迁移**。
- 每次结构变动运行 `python -m unittest discover -s tests -v`；新增的 `tests/test_structure_routing.py` 只做本地路径/入口/权威存在性检查，不下载、不训练、不渲染图像，也不能证明 AI Token 已下降。

## 4. 规则演进：优先替换，不累积指令（维护任务才读）

- **单一权威**：`AGENTS.md` 只承载冷启动、版本核验、最小权限和专题路由；`WORKFLOW.md` 只承载科研决策循环、状态/止损、跨专题边界；技术/科研细则归现有专题；`modules/` 与 `policies/` 索引只存链接，不复制条款。RWF 只负责实现与证据复核，不复制 PD-RW 科研政策。
- **先诊断再改规则**：发现问题先区分 `NOT_LOADED / STALE_RULE_SOURCE / CONFLICT / MISAPPLIED / MISSING_CAPABILITY`。前四类先修版本、路由、冲突或示例；仅确有新能力缺失且无法复用现有专题时新增规则或工具。
- **新增规则的归属**：先选唯一 owner 文件，优先替换冗余段落；只有独立、稳定且确有增量职责时才新建专题，并在入口加**一条短路由**。不建立空占位、第二权限表、固定多Agent、强制读遍所有文件或新的研究关卡。
- **可复现版本**：跨会话/外部 Agent 应能说明 `RULE_REPO | RULE_COMMIT | LOADED_FILES`；本地非 Git 复制件无法验证远端 HEAD 时标 `RULE_VERSION_UNVERIFIED`，不得自称已同步。离线工作允许继续按已知版本及用户授权执行，不强制联网，不把 Markdown 中写的 SHA 当成实时 HEAD。
- **变更验收**：记录受影响的任务行为、原规则去向、适用授权；运行受影响的离线结构/语义回归，关键安全门禁不得退化。需要宣称科研质量或 Token 改善时依 [REPLAY_PROTOCOL.md](../REPLAY_PROTOCOL.md) 另行真实同预算评测；未实测一律 `NOT_MEASURED`。不为提交文档重跑科研模型。
- **上下文预算**：以 `AGENTS.md` 精简入口与按需专题为默认；大块理论、图件、Word 格式、历史经验只在对应任务加载。Token 预算是维护提示而不是科学正确性的上限；必要的安全和证据要求不得因缩短入口而被删除。
