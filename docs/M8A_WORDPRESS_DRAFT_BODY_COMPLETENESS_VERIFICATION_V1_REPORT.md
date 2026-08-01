# M8A WordPress Draft 正文完整性验证报告 V1

## 状态

completed

## 目标

验证修复后的 `content_html` 桥接 payload 是否能让 n8n / WordPress Draft-only 链路写入完整正文，而不是只写标题。

## 执行内容

使用修复后的桥接脚本：

`apps/commander/publishing_center_v1/pipeline_bridge.py`

执行 Draft-only：

```bash
python3 apps/commander/publishing_center_v1/pipeline_bridge.py apps/commander/content_center_v1/outputs/hk620_us_customer_article_v3_pre_publish.json --execute
```

## 新建 Draft

| 字段 | 结果 |
|---|---|
| WordPress Post ID | 486 |
| WordPress Status | draft |
| Title | HK620 Skeleton Line Edge Banding Machine for Door, Furniture, and Decorative Strip Production |
| Draft URL | https://woodmachinerynetwork.com/?p=486 |
| Edit URL | https://woodmachinerynetwork.com/wp-admin/post.php?post=486&action=edit |
| n8n Execution ID | 291 |
| Workflow | m8a_hk620_draft_20260708 |

## 正文验证

只读检查 WordPress REST API 后确认：

| 检查项 | 结果 |
|---|---|
| HTTP Status | 200 |
| Post ID | 486 |
| Status | draft |
| Content Length | 7070 |
| 包含标题结构 H1/H2 | PASS |
| 包含 HK620 | PASS |
| 包含 Overview | PASS |
| 包含 FAQ | PASS |

## 安全确认

本次没有：

- 发布 WordPress
- 修改已发布 Post 484
- 删除文章
- 发送 Gmail
- 上传 YouTube
- 调用旧高风险 workflow `CWbGujhdNKFpa5JZ`

本次只创建新的 WordPress Draft：

- Post ID：486
- 状态：draft

## 结论

PASS。

桥接修复有效。

新的 WordPress Draft 已成功写入完整正文，不再只有标题。

## 下一步

建议由 CEO 在 WordPress 后台打开 Draft 486 检查页面排版。

如果内容、格式、事实边界通过，再进入单独的 CEO 发布审批。

发布仍不能自动执行。
