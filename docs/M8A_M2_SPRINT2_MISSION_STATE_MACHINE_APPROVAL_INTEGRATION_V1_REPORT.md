# M8A M2 Sprint 2 Mission State Machine & Approval Integration V1 Report

日期：2026-07-10
优先级：P0

## 一、验收结论
Mission State Machine & Approval Integration V1 已完成。Approval Center V1 已接入 Mission 生命周期模拟验证，审批结果可以驱动 Mission 状态变化。

本 Sprint 没有新增 Governance 模块，没有新增 Approval Center，没有新增 Queue，没有修改 Commander、Runtime DB Schema、Dashboard、Mission Queue 或 External Executor。

## 二、统一生命周期
Created → Queued → Pending Approval → Approved → Running → Completed → Failed → Retry → Cancelled

Reject 的业务语义记录为 Rejected → Stopped，在统一生命周期中落到 `Cancelled`。

## 三、状态流转验收
### Draft Mission
`Created → Queued → Running → Completed`

Draft 不需要 CEO 审批；在 Safety Gate 和 Execution Response Contract 约束下可自动执行。本 Sprint 未真实执行 Draft。

### Publish Mission
`Created → Queued → Pending Approval → Approved → Running → Completed`

Publish 必须审批。模拟中 CEO Approve 后，Mission 自动从 Pending Approval 进入 Approved，再进入 Running。

### Delete Mission
`Created → Queued → Pending Approval → Rejected → Stopped → Cancelled`

Delete 必须审批。模拟中 CEO Reject 后，Mission 被停止，并映射为统一状态 `Cancelled`。

### Re-Approve
`Rejected → Pending Approval → Approved → Running`

Re-Approve 驱动链路已在 Delete Mission 模拟中验证。因为 Delete 是高风险动作，本 Sprint 在 Running 后由安全边界取消，不执行外部删除。

## 四、新增文件
1. `apps/commander/mission_center_v1/runtime/mission_state_machine_approval_integration.v1.json`
2. `docs/M8A_M2_SPRINT2_MISSION_STATE_MACHINE_APPROVAL_INTEGRATION_V1_REPORT.md`

## 五、修改文件
1. `apps/commander/mission_center_v1/rules/global_mission_status.rules.json`
2. `apps/commander/mission_center_v1/runtime/mission_timeline.v1.json`
3. `apps/commander/mission_center_v1/history/mission_history.v1.json`
4. `apps/commander/runtime_persistence_v1/db/m8a_runtime_v1.sqlite`

Runtime DB 仅复用已有表：missions、approvals、mission_events、event_history、runtime_logs。未改 schema。

## 六、Git Diff 摘要
- 扩展现有 Mission status rules 为 M2 Sprint 2 生命周期定义。
- 新增本地模拟文件，验证 Draft / Publish / Delete / Re-Approve 流转。
- 追加 Mission Timeline / History 记录。
- 写入 Runtime DB 本地验收记录。

## 七、风险分析
- 当前是状态机和 Approval 驱动的本地模拟验证，未接入新的 Dashboard 操作按钮。后续如需 UI 操作，应复用现有 Dashboard。
- Delete 即使 Re-Approve 后进入 Running，也必须继续由 Safety Gate / External Executor 阻断真实删除，除非 CEO 明确授权。

## 八、安全确认
本 Sprint 未调用 n8n，未调用 WordPress，未发布，未删除，未修改线上内容，未调用 Gmail / YouTube / Google API。

## 九、停止点
M2 Sprint 2 已完成。按 CEO 要求，立即停止，等待 CEO Review，不继续 Sprint 3。
