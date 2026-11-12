# 执行保障：事件检查与权限边界

本文件仅在原有六活动/H1–H10内描述执行保障，不增加用户审批、科研阶段或长期文档。唯一科学规则仍在 WORKFLOW.md。

## 三级执行机制

1. **权限硬边界**：新数据下载、SEALED、独立确认、付费、外传、危险安装、正式绘图、正式写稿、投稿、项目整体STOP及超H5变更，必须由实际工具宿主核真实用户授权、对象和范围。最好通过文件系统ACL、独立工具代理、审计日志阻断非法行为，而不是相信Agent声明。当前本仓库未提供这样的可信运行时工具包装器或OS级SEALED隔离。
2. **科研检查点**：H6、新算法设计、重要Run/负面结果、H8与主张升级时，使用可复用的结构预检。缺必要字段不得宣称完成科学交接；检查通过仍不证明真值、创新性、独立确认或Q2+潜力。探索阶段允许UNKNOWN/NOT_RUN，不能逼迫无效实验。
3. **自主研发**：H5内的安全非付费DEV编码、训练、评价、修复、机制变化和H6–H8决定无需重复人工确认。只有相关证据/权限/任务发生实质变化时重新核查，不在每一轮调参生成报告。

## 离线预检接口

- python -m core.execution_preflight action ACTION.json
- python -m core.execution_preflight science CHECKPOINT.json

Action接受 READ_PUBLIC、ANALYZE_EXISTING_METADATA、REVIEW_RULES；DEV_CODE/DEV_TRAIN/DEV_EVALUATE/DEV_FIX；以及 DOWNLOAD/READ_SEALED/RUN_CONFIRMATION/DRAW_IMAGE/WRITE_MANUSCRIPT/SUBMIT/PAY/EXTERNAL_UPLOAD/UNSAFE_INSTALL/PROJECT_SCOPE_CHANGE/PROJECT_STOP。

Action结果为 ALLOW/BLOCK/UNKNOWN。没有受限副作用的公开只读操作可返回ALLOW；DEV需已确认H5、DEV合法、H5范围内、安全非付费、无项目特别禁令；任何受限操作的JSON自填授权都不会构成真实授权，CLI默认UNKNOWN。宿主必须独立认证授权、调用 action_preflight(packet, independently_authorized=True)，并在动作入口独立实施工具/文件权限控制。此参数不是密码，必须由不受Agent控制的宿主代码传递；Agent能够自行调用Python时不能把该返回值当成可信许可。**没有运行时宿主接入时标 ENFORCEMENT_NOT_CONNECTED，不得声称硬性拦截已实现。**

Science触发器：H6_TASK（C01–C12主贡献、R1–R6路线、问题、近邻或UNKNOWN）；NEW_ALGORITHM（真实瓶颈、简单替代、判别预言）；SIGNIFICANT_RUN/NEGATIVE_RESULT（Run或NOT_RUN、负结果或NONE、竞争解释和下一证据行动）；H8_CLAIM/CLAIM_PROMOTION（主贡献及证据核查，升级时注明独立来源或UNAVAILABLE）。READY_FOR_SCIENTIFIC_REVIEW仅代表结构齐全；BLOCK_HANDOFF仅阻断将不完整交接宣称为完成，不阻断安全合法的自主研究。

## 与研究主张相结合

先按 CONTRIBUTION_TAXONOMY.md 判断主贡献及可选辅助贡献，再选择相匹配的强对照、真实验证、证明、审计、系统测试或失效分析。理论、评价、负面结果等可无算法H7。不要求全部六条研究路线都做，不将H2旧五类合同枚举迁移或作废。

利用现有 RESEARCH_RECORD.md 记录重要检查结果和来源指针，已有同规则版本、同Task、同证据哈希的检查可复用。无第三份常驻日志；真实Agent轨迹必须由宿主独立捕获，尚未实测标NOT_MEASURED。静态CI只证明对应代码测试通过，不证明科学正确性或真实Agent遵从。
