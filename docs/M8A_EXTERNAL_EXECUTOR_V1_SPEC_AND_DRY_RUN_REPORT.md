# M8A_EXTERNAL_EXECUTOR_V1_SPEC_AND_DRY_RUN_REPORT

日期：2026-07-10

## 一、Sprint 结果
External Executor V1 规格与 Draft-only Dry-run 链路已完成。当前只完成本地规格、payload contract、Dry-run validator、readiness state、Dashboard 数据和 Runtime / Audit 写入，没有真实调用 n8n、WordPress 或任何外部平台。

## 二、Executor 架构
External Executor V1 位于 Production Safety Gate 之后，只接受安全闸门批准后的 action。核心字段包括 executor_id、platform、action_type、mission_id、authorization_id、payload、dry_run_result、execution_status、audit_log_id。

## 三、n8n Draft-only 规格
- 平台：n8n
- workflow path：m8a-hk620-draft-only
- 允许动作：create_wordpress_draft_only
- 禁止旧 workflow：CWbGujhdNKFpa5JZ
- 禁止动作：publish、update_published_post、delete_post、send_gmail、upload_youtube

## 四、WordPress Draft Result 标准
真实 Draft-only 执行未来必须返回 ok、execution_id、post_id、draft_url、title、status=draft、created_at、source_mission_id、safety_gate_result。Dry-run 阶段 post_id 和 draft_url 不允许伪造。

## 五、Payload Contract
Payload 必须包含 mission_id、product、market、language、article_draft、qa_report、qa_score、action=create_wordpress_draft_only、dry_run、publish=false、update_published_post=false、delete_post=false、send_gmail=false、upload_youtube=false。

## 六、Dry-run Validator
本次 Dry-run 校验结果：dry_run_passed。

校验内容：字段完整性、禁止动作全部为 false、QA Score >= 90、授权状态满足 Dry-run、action 只允许 Draft-only。

## 七、Readiness State
状态机已建立：waiting_safety_gate、waiting_ceo_authorization、ready_for_dry_run、dry_run_passed、ready_for_real_execution、executed_draft_only、execution_failed、blocked。

当前模拟链路状态：ready_for_real_execution。

## 八、Dashboard 接入
总控台新增“外部执行器 V1”状态卡，显示当前模式、可执行动作、禁止动作、Dry-run 通过数量、待真实执行数量、最近执行器事件。

## 九、Audit Log 验证
已写入本地 External Executor audit log，并写入 Runtime Persistence V1 的 runtime_logs。写入内容包括：规格创建、payload contract 校验、Dry-run 通过、readiness state 更新。

## 十、风险与下一步建议
风险：当前还没有进行真实外部执行。下一步如果要调用 n8n Draft-only，必须 CEO 单独授权，并使用一次性授权、idempotency key、payload preview 和执行结果回写。

建议下一步：建立 CEO 授权后的真实调用适配器，但默认仍应保持 Draft-only，禁止 publish/delete/update/send/upload。

## 十一、是否具备下一步真实调用条件
具备前置条件，但还不能自动真实调用。当前状态只表示 Dry-run passed 与 ready_for_real_execution；真实调用必须另行 CEO 单独授权。
