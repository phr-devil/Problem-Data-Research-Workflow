# PD-RW 仓库轻度分层维护说明（INDEX_ONLY）

## 1. 本次边界：先增导航，不迁权威

- 唯一 Agent 默认入口：[`AGENTS.md`](../AGENTS.md)。
- 唯一科研决策主控：[`WORKFLOW.md`](../WORKFLOW.md)；原有三循环/六活动和授权门禁不修改。
- [`policies/README.md`](../policies/README.md) 与 [`modules/README.md`](../modules/README.md) 及其研究、论文、绘图专题索引只是轻量**路径清单**（INDEX_ONLY），无新增规则或审批。旧路径与脚本全部保留，无双份规范。
- 研究项目内的 `RESEARCH_RECORD.md` / `PAPER_BLUEPRINT.md`、Run/STATE 和所有原始证据位置不变；原测试仍可直接访问根目录权威文档。
- **历史科研案例统一归属**：[LESSONS/CASE_REGISTRY.md](../LESSONS/CASE_REGISTRY.md) 是项目成功/失败/证据缺口的按需单一索引；细节与最终事实仍以用户项目原始 Run/归档为准。RWF 仅链接此索引，不复制，不纳入 AGENTS 默认预读。
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

**六活动合同的权威边界**：`WORKFLOW.md` 决定研发活动/权限的科研语义，`contracts/research_activity_protocol.v1.json` 只提供可测试的交接结构；`contracts/human_review_protocol.v1.json` 另管 H1–H10。任何更新须同步唯一 owner/结构镜像与定向回归，不能在专题另造“活动07”、自动审批器、第二科研日志或固定研究方法。

## 4. 规则演进：优先替换，不累积指令（维护任务才读）

- **单一权威**：`AGENTS.md` 只承载冷启动、版本核验、最小权限和专题路由；`WORKFLOW.md` 只承载科研决策循环、状态/止损、跨专题边界；技术/科研细则归现有专题；`modules/` 与 `policies/` 索引只存链接，不复制条款。RWF 只负责实现与证据复核，不复制 PD-RW 科研政策。
- **先诊断再改规则**：发现问题先区分 `NOT_LOADED / STALE_RULE_SOURCE / CONFLICT / MISAPPLIED / MISSING_CAPABILITY`。前四类先修版本、路由、冲突或示例；仅确有新能力缺失且无法复用现有专题时新增规则或工具。
- **新增规则的归属**：先选唯一 owner 文件，优先替换冗余段落；只有独立、稳定且确有增量职责时才新建专题，并在入口加**一条短路由**。不建立空占位、第二权限表、固定多Agent、强制读遍所有文件或新的研究关卡。
- **可复现版本**：跨会话/外部 Agent 应能说明 `RULE_REPO | RULE_COMMIT | LOADED_FILES`；本地非 Git 复制件无法验证远端 HEAD 时标 `RULE_VERSION_UNVERIFIED`，不得自称已同步。离线工作允许继续按已知版本及用户授权执行，不强制联网，不把 Markdown 中写的 SHA 当成实时 HEAD。
- **变更验收**：记录受影响的任务行为、原规则去向、适用授权；运行受影响的离线结构/语义回归，关键安全门禁不得退化。需要宣称科研质量或 Token 改善时依 [REPLAY_PROTOCOL.md](../REPLAY_PROTOCOL.md) 另行真实同预算评测；未实测一律 `NOT_MEASURED`。不为提交文档重跑科研模型。
- **上下文预算**：以 `AGENTS.md` 精简入口与按需专题为默认；大块理论、图件、Word 格式、历史经验只在对应任务加载。Token 预算是维护提示而不是科学正确性的上限；必要的安全和证据要求不得因缩短入口而被删除。


## 5. 本次规则收敛的保护合同（维护者按需读，不加入Agent默认上下文）

**历史要求对照索引**：涉及旧版大幅精简、用户决策与科研门禁的调整，按需核 [RULE_INHERITANCE_AUDIT.md](RULE_INHERITANCE_AUDIT.md) 的旧要求归宿和明确替代；该表是维护证据而非第二套执行规范，普通科研任务不预读。变更只更新受影响 ID 及反例，不每次重审整张表。

**先恢复语义，再考虑压缩或移动**：从 Git 历史比对变更前后受影响的关键义务，按 `PRESERVED / MOVED / MERGED / REPLACED / RETIRED / UNKNOWN` 逐项判定；单纯缩短文字或关键词测试变绿不等于保真。`UNKNOWN` 不擅自删规则。历史代码/协议/冻结Run和用户原消息依然分别决定工程事实、科研真值与用户许可；不得靠文档为旧项目补写虚假授权。

| 稳定追踪 ID（仅维护定位，不增CLI状态或审批） | 规则的唯一权威与适用触发 | 反例验证重点 |
|---|---|---|
| `AUTH-EXEC` | [WORKFLOW.md](../WORKFLOW.md) 权限边界 + [NEXT_ACTION_POLICY.md](../NEXT_ACTION_POLICY.md) 用户原指令/下一动作；实际下载、拟合、成本、外传之前 | 未获许可时不能执行；选择课题不等于资源许可 |
| `AUTH-SEALED` | [CONFIRMATION.md](../CONFIRMATION.md)；访问/复核独立池之前 | SEALED不能替代DEV选模或自动开启 |
| `AUTH-WRITE` | [WRITING_GATE.md](../WRITING_GATE.md)；正式标题/摘要/正文之前 | 蓝图或科研成功不自动解锁 |
| `AUTH-FIGURE` | [FIGURE_POLICY.md](../FIGURE_POLICY.md)；生成/重绘图片之前 | 未明确要求不得主动出图 |
| `EVIDENCE-VALIDITY` | [WORKFLOW.md](../WORKFLOW.md) 科研总控 + [EXPERIMENT_LOOP.md](../EXPERIMENT_LOOP.md) 实验有效性；形成Claim/决定下一Probe时 | INVALID/NOT_RUN不升格成成功或负科学结论 |
| `RULE-RELOAD` | [AGENTS.md](../AGENTS.md) 入口/版本和 [DUAL_DOCUMENT_WORKFLOW.md](../DUAL_DOCUMENT_WORKFLOW.md) 恢复；会话/Task/规则变化及敏感操作前 | 不因读过一次就假设永久生效，版本/授权不明不自我许可 |

**变更前核归属**：新的科研限制先标 `HARD_GATE`（必须满足）、`CONDITIONAL`（在具体场景触发）、`HEURISTIC`（可按任务调整）；每项只有一个详细定义的owner，其他文件只保留导航或最小禁令提醒。只有真正新增独立职责才新建专题。对运行工具可控的场景，应在执行层实施权限检查；Markdown和静态CI不能证明真实拦截，未验证的机制必须如实标明。

**每个涉及规则的PR描述最短覆盖**：`OLD_REQUIREMENT+COMMIT/PR → PRESERVED/MOVED/MERGED/REPLACED/RETIRED(+WHY) → OWNER+TRIGGER → AFFECTED_CALLERS → NEGATIVE_CASES/TESTS → UNMEASURED_RISKS`。仅分析受影响的要求，不强制全仓长篇审计；更新机器可读镜像时检查与文字owner一致，旧路径/调用方保持兼容。一次重要规则修改若丢失原要求或未解除相互矛盾，不因CI绿灯直接合并。

**取消机械字符上限**：`AGENTS.md`、`WORKFLOW.md` 及索引均不因字符数超过阈值而测试失败；以导航职责、完整引用、实际加载路径和关键条件覆盖检查为准。必要内容可以变长，重复或未用内容应删除/移至其owner，但保留可追溯的旧要求映射。Token下降、Agent真实理解与门禁合规必须由 [REPLAY_PROTOCOL.md](../REPLAY_PROTOCOL.md) 的同条件捕获验证，未测记 `NOT_MEASURED`。
