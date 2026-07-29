# M8A 总控数据校准 V1 报告

生成时间：2026-07-12T01:48:34Z

## 一、结论

总控数据校准 V1 已完成。员工工作台原来显示“外部 API 未连接”，原因是页面写死了该字段，没有读取真实平台状态。现在已改为读取平台连接状态，并显示已同步数量。

## 二、已修正问题

1. 员工工作台“外部 API：未连接”改为真实状态。
2. 总控台旧提示“仅 Dry-run、没有调用外部 API”已更新为当前真实状态。
3. 平台/API 状态已统一写回 platform_connector_status.json。
4. AI 员工工作台增加平台同步摘要。

## 三、当前平台状态

### 已可用或已接入

- WordPress：可创建 Draft
- n8n：唯一正式外部执行层，可执行 Draft-only
- Gmail：可 Draft
- YouTube：可上传视频
- Google Search Console：可读数据
- GA4：可读数据
- LinkedIn：可发，发布前审批
- Medium：可发布 / 可草稿，发布前审批
- Quora：可发，发布前审批
- Substack：可草稿

### 待授权或冻结

- Google Business Profile：待授权
- Facebook：待 Meta 权限
- Instagram：待 Meta 权限
- TikTok：待 Developer App / Content Posting API 授权

## 四、AI 员工分工

- Website Agent：WordPress Draft 与网站内容
- Publishing Agent：Gmail、LinkedIn、Medium、Quora、Substack
- Video Agent：YouTube 与 TikTok 视频链路
- SEO Agent：GSC 与搜索数据
- Data Agent：GA4 与日报数据
- Automation Agent：n8n、平台连接、授权状态
- QA Agent：所有内容 QA，低于 90 分不进入发布
- Commander Reporting Agent：总控台状态同步

## 五、安全确认

本次只做本地数据校准，没有调用 n8n、WordPress、Gmail、YouTube、Google API，没有发布、删除或修改外部内容。

公开发布、删除、修改已发布文章、发送 Gmail、公开视频上传，仍必须 CEO 单独审批。
