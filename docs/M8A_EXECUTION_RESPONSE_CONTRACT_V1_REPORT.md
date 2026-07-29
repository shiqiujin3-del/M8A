# M8A Execution Response Contract V1 Report

日期：2026-07-10
优先级：P0

## 一、Sprint 目标
本 Sprint 只建立统一 Execution Response Contract，不新增执行器，不连接新平台，不修改 Commander、Mission Queue、Runtime DB Schema、Dashboard 数据结构，也不修改已经验收的 WordPress Draft-only workflow 业务逻辑。

## 二、当前问题
P0 Incident Response 已验收，真实链路已经跑通：Commander → External Executor → n8n → WordPress Draft → Runtime DB → Audit → Dashboard。

但是当前 webhook 直接返回仍是旧格式：

```json
{"message":"Workflow was started"}
```

External Executor 不能仅凭 webhook response 立即获得 execution_id、WordPress Draft ID、Draft URL、执行耗时和错误信息。当前 Draft ID 443 是从 n8n execution #33 中补查得到的。

## 三、最终 JSON Schema
已新增：

`apps/commander/external_executor_v1/contracts/execution_response_contract.v1.schema.json`

核心成功结构：

```json
{
  "success": true,
  "mission_id": "mission_real_wp_draft_hk620_20260710_1783648705",
  "trace_id": "trace_real_wp_draft_20260710T015825",
  "execution_id": 33,
  "executor": "n8n",
  "workflow_id": "aTVbw0a7MId3NCBH",
  "workflow_name": "m8a_hk620_draft_20260708",
  "action_type": "create_wordpress_draft_only",
  "status": "completed",
  "started_at": "2026-07-10T02:57:21.037Z",
  "finished_at": "2026-07-10T02:57:23.610Z",
  "duration_ms": 2573,
  "retry_count": 1,
  "result": {
    "type": "wordpress_draft",
    "post_id": 443,
    "post_status": "draft",
    "draft_url": "https://woodmachinerynetwork.com/?p=443",
    "edit_url": "https://woodmachinerynetwork.com/wp-admin/post.php?post=443&action=edit",
    "title": "HK620 Draft Test from M8A",
    "slug": "hk620-draft-test-from-m8a",
    "external_id": 443,
    "external_url": "https://woodmachinerynetwork.com/?p=443",
    "platform_status": "draft"
  },
  "error": null,
  "safety": {
    "draft_only": true,
    "publish": false,
    "delete_post": false,
    "update_published_post": false,
    "send_gmail": false,
    "upload_youtube": false,
    "old_workflow_called": false,
    "prohibited_workflow": "CWbGujhdNKFpa5JZ"
  },
  "compatibility": {
    "contract_version": "execution_response_contract_v1",
    "legacy_webhook_response": {
      "message": "Workflow was started"
    },
    "requires_execution_lookup": true,
    "normalization_source": "n8n_execution_lookup"
  }
}
```

核心失败结构：

```json
{
  "success": false,
  "mission_id": "mission_example_failed",
  "trace_id": "trace_example_failed",
  "execution_id": null,
  "executor": "n8n",
  "workflow_id": "aTVbw0a7MId3NCBH",
  "workflow_name": "m8a_hk620_draft_20260708",
  "action_type": "create_wordpress_draft_only",
  "status": "failed",
  "started_at": "2026-07-10T00:00:00Z",
  "finished_at": "2026-07-10T00:00:02Z",
  "duration_ms": 2000,
  "retry_count": 1,
  "result": null,
  "error": {
    "error_code": "N8N_WEBHOOK_EXECUTION_FAILED",
    "error_message": "n8n workflow did not return a WordPress Draft result.",
    "retryable": true,
    "retry_count": 1,
    "http_status": 502,
    "failed_node": null,
    "details": null
  },
  "safety": {
    "draft_only": true,
    "publish": false,
    "delete_post": false,
    "update_published_post": false,
    "send_gmail": false,
    "upload_youtube": false,
    "old_workflow_called": false,
    "prohibited_workflow": "CWbGujhdNKFpa5JZ"
  },
  "compatibility": {
    "contract_version": "execution_response_contract_v1",
    "legacy_webhook_response": null,
    "requires_execution_lookup": false,
    "normalization_source": "direct_webhook_response"
  }
}
```

## 四、新增文件
1. `apps/commander/external_executor_v1/contracts/execution_response_contract.v1.schema.json`
2. `apps/commander/external_executor_v1/contracts/execution_response_contract.v1.example.success.json`
3. `apps/commander/external_executor_v1/contracts/execution_response_contract.v1.example.error.json`
4. `docs/M8A_EXECUTION_RESPONSE_CONTRACT_V1_REPORT.md`

## 五、修改文件
无既有业务文件修改。未修改 Commander、Mission Queue、Runtime DB Schema、Dashboard 数据结构、n8n workflow、WordPress 内容。

## 六、为什么这样设计
1. 顶层 `success/status/error` 让 External Executor 可以统一判断完成、失败、是否可重试。
2. 顶层 `executor/workflow_id/workflow_name/action_type` 让结果可追踪到具体执行系统。
3. `result.type` 让 WordPress、Gmail、YouTube、Facebook、LinkedIn、AIToEarn、Google API 都能复用同一外壳，只替换 result 内部字段。
4. `safety` 固定记录禁止动作，避免 Draft-only 结果和 publish/delete/update/send/upload 混淆。
5. `compatibility` 保留旧 webhook response，保证旧接口继续可用。

## 七、未来平台兼容方式
- WordPress：`result.type=wordpress_draft`，使用 post_id、post_status、draft_url、slug。
- Gmail：`result.type=gmail_draft`，可使用 external_id、external_url、platform_status。
- YouTube：`result.type=youtube_upload`，可使用 external_id、external_url、platform_status，并继续由 safety 禁止自动 publish。
- Facebook / LinkedIn：使用 generic external result 或后续枚举扩展，不改变顶层结构。
- AIToEarn：使用 `result.type=aitoearn_task`，保留 mission_id / trace_id / execution_id。
- Google API：使用 `result.type=google_api_result`，把具体对象 ID 放入 external_id。

## 八、本次 HK620 Draft Workflow 验证结论
当前 HK620 Draft workflow 尚不能直接返回完整 Execution Response Contract。

已确认事实：
- n8n execution：#33
- workflow_id：aTVbw0a7MId3NCBH
- workflow_name：m8a_hk620_draft_20260708
- WordPress Draft ID：443
- Draft URL：https://woodmachinerynetwork.com/?p=443
- 状态：draft
- 当前 webhook 直接 response：`{"message":"Workflow was started"}`

因此当前仍需要查询 n8n execution 才能获得 Draft ID / Draft URL。

## 九、后续建议
如 CEO 后续批准修改 n8n workflow 响应层，可只增加 response mapping / respond-to-webhook 输出节点，让 workflow 在完成 WordPress Draft 创建后直接返回本 Contract。该动作不应改变 Create Draft 业务逻辑，不应增加 publish/delete/update/send/upload。

## 十、安全确认
本 Sprint 未调用 n8n，未调用 WordPress，未发布，未删除，未修改线上内容，未调用 Gmail / YouTube / Google API。
