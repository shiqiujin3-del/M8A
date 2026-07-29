# M8A M2 Sprint 1 Approval Center V1 Report

日期：2026-07-10
优先级：P0

## 一、验收结论
Approval Center V1 已完成。

本 Sprint 没有新增顶层模块，没有新增数据库，没有修改 Runtime DB Schema，没有修改 Commander、Mission Queue、Dashboard 数据结构、External Executor、Execution Response Contract 或 WordPress Draft Workflow。

## 二、完成能力
- Approve：支持 `approved` 状态。
- Reject：支持 `rejected` 状态。
- Pending：支持 `pending` 状态。
- Re-Approve：支持 `re_approved` 状态。
- Approval History：已建立 `approval_history.v1.json`。
- Approval Audit：已建立 `approval_audit.v1.json`，并写入 Runtime Log。

## 三、核心规则
- Draft 可自动执行：`create_wordpress_draft_only` 在 Safety Gate 通过后可自动执行。
- Publish 必须审批：任何 `publish` 动作必须 CEO 审批。
- Delete 必须审批：任何 `delete` 动作必须 CEO 审批。
- 修改已发布内容必须审批。
- Gmail Send / YouTube Upload 或 Publish 必须审批。

## 四、新增文件
1. `apps/commander/governance/approval_center_v1/rules/approval_policy.v1.json`
2. `apps/commander/governance/approval_center_v1/queue/approval_queue.v1.json`
3. `apps/commander/governance/approval_center_v1/history/approval_history.v1.json`
4. `apps/commander/governance/approval_center_v1/audit/approval_audit.v1.json`
5. `apps/commander/governance/approval_center_v1/runtime/approval_center_runtime_mapping.v1.json`
6. `docs/M8A_M2_SPRINT1_APPROVAL_CENTER_V1_REPORT.md`

## 五、修改文件
- `apps/commander/runtime_persistence_v1/db/m8a_runtime_v1.sqlite`：复用现有 `approvals`、`runtime_logs`、`mission_events`、`event_history` 表写入 Sprint 1 验收记录。未改表结构。

## 六、Git Diff 摘要
本 Sprint 仅新增 Approval Center V1 子目录和中文报告，并向现有 Runtime DB 写入本地记录。未修改已验收链路代码。

## 七、验收结果
- JSON 文件全部可解析。
- Runtime DB `approvals` 写入 3 条 Sprint 1 记录：2 条 pending 示例、1 条 Draft-only approved 记录。
- Runtime DB `runtime_logs` 写入 Approval Center V1 审计日志。
- Event Store 写入 `Approval Center V1 Completed` 事件。

## 八、风险分析
- 当前是本地规则与记录中心，不是新 UI，不改变现有 Dashboard。后续 Sprint 如需可视化，应在已有 Dashboard 内接入，不新增 Dashboard。
- Publish / Delete 仍只是被审批规则阻断；真实外部动作继续依赖 Production Safety Gate 与 CEO 授权。

## 九、安全确认
本 Sprint 未调用 n8n，未调用 WordPress，未创建 Draft，未发布，未删除，未修改线上内容，未调用 Gmail / YouTube / Google API。

## 十、停止点
M2 Sprint 1 已完成。按 CEO 要求，立即停止，等待 CEO Review，不继续 Sprint 2。
