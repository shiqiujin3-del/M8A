# M8A Publishing Center → WordPress Provider 接入 V1 报告

日期：2026-07-10

## 目标

把 Publishing Center V1 从架构标准推进到第一条真实 Provider 接入：

```text
Commander
  ↓
Publishing Center
  ↓
Runtime Core compatible result
  ↓
External Executor
  ↓
WordPress Draft-only Provider
```

## 接入范围

本次只接入：

- publishing_type：publish_article
- target_platform：wordpress
- provider：wordpress_provider
- action：create_wordpress_draft_only

## 安全边界

本次禁止：

- Publish
- Delete
- Update Published Post
- Gmail
- YouTube
- 旧 workflow：CWbGujhdNKFpa5JZ

## 新增文件

- apps/commander/publishing_center_v1/publishing_center_runner.py
- apps/commander/publishing_center_v1/publishing_queue.runtime.v1.json
- apps/commander/publishing_center_v1/last_publishing_wordpress_draft_result.v1.json
- apps/commander/publishing_center_v1/publishing_audit_log.v1.json
- apps/commander/external_executor_v1/real_execution/last_publishing_center_wp_draft_result.v1.json

## 验收方式

运行：

```bash
python3 apps/commander/publishing_center_v1/publishing_center_runner.py --execute
```

成功标准：

- Publishing Mission 创建成功。
- Publishing Queue 写入成功。
- Dispatcher 选择 wordpress_provider。
- n8n Draft-only webhook 返回 success=true。
- 返回 execution_id。
- 返回 WordPress Draft resource_id / resource_url。
- requires_execution_lookup=false。

## 最终结论

真实执行已通过。

- Publishing Mission ID：pub_article_wp_draft_1783690334345
- Mission ID：mission_publish_article_wp_draft_1783690334345
- n8n Execution ID：86
- WordPress Draft ID：449
- Draft URL：https://woodmachinerynetwork.com/?p=449
- Status：completed
- requires_execution_lookup：false
- Runtime Core compatible：true

安全确认：

- 未 Publish。
- 未 Delete。
- 未 Update Published Post。
- 未调用 Gmail。
- 未调用 YouTube。
- 未调用旧 workflow：CWbGujhdNKFpa5JZ。

最终状态：READY FOR NEXT PROVIDER
