# M8A WordPress Draft 正文桥接修复报告 V1

## 状态

completed_local_bridge_fix

## 问题

WordPress Draft 创建链路中，n8n WordPress 节点从 `body.content_html` 或 `body.content` 读取正文。

原桥接脚本只传递了：

- `title`
- `article_draft.summary`
- `article_draft.sections`
- SEO 字段

但没有传递完整正文 HTML 字段，导致 WordPress Draft 可能只得到标题或结构字段，而拿不到文章正文。

## 修复内容

已更新：

`apps/commander/publishing_center_v1/pipeline_bridge.py`

新增能力：

1. 将 `draft_markdown` 转换为 WordPress 可用 HTML。
2. payload 顶层新增：
   - `content_markdown`
   - `content_html`
   - `content`
3. `article_draft` 内新增：
   - `content_markdown`
   - `content_html`
   - `content`
   - `content_html_length`
4. 保持 Draft-only 安全字段：
   - `publish=false`
   - `update_published_post=false`
   - `delete_post=false`
   - `send_gmail=false`
   - `upload_youtube=false`

## 验证

验证命令：

```bash
python3 apps/commander/publishing_center_v1/pipeline_bridge.py apps/commander/content_center_v1/outputs/hk620_us_customer_article_v3_pre_publish.json
```

验证结果：

- dry_run：PASS
- payload 顶层 `content_html`：PASS
- payload 顶层 `content`：PASS
- `article_draft.content_html`：PASS
- `content_html_length`：7070
- JSON 校验：PASS

## 安全确认

本次没有：

- 执行 n8n workflow
- 创建新的 WordPress Draft
- 发布 WordPress
- 修改已发布文章
- 删除文章
- 发送 Gmail
- 上传 YouTube
- 输出任何密钥

## 关于 Post 484

Post 484 在历史结果中已被标记为 published。

因此补正文到 Post 484 属于“修改已发布文章”，本次未执行。

如需修复 Post 484 线上正文，必须由 CEO 单独授权：

“允许修改已发布 WordPress Post 484，只补正文，不改标题、不发布新文章、不删除内容。”

## 当前结论

桥接脚本已完成本地修复。

下一次走安全 Draft-only 创建链路时，n8n 将可以从 payload 中读取完整正文：

- `body.content_html`
- `body.content`

## 下一步

建议下一步先创建一个新的 WordPress Draft 验证正文是否完整写入。

不要直接修改已发布 Post 484。
