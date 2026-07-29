# M8A Employee Mission Queue V1 报告

日期：2026-07-09

## 结论

已建立 Employee Mission Queue V1，并把 Product Knowledge Gap Task Center V1 的 HK620 资料缺口任务派入 AI 员工队列。

本次属于 A 类 Build，本地建设任务，不需要 CEO 审批。未调用 n8n，未调用 WordPress，未生成新文章，未发布、未删除、未修改任何外部平台。

## 队列状态

Employee Mission Queue V1 支持以下状态：

- queued
- in_progress
- blocked
- qa_pending
- completed
- failed

## 每个员工分到几件任务

Knowledge Agent：6 件

- 公开技术规格
- 产品图片
- 产品视频
- 客户案例
- 服务 FAQ
- 交付 / 保修 / 价格政策

Website Agent：2 件

- 外部参考链接
- 内部链接

QA Agent：10 件

- 公开使用审批记录
- 公开宣传边界
- 以及对其他 8 个缺口任务的验收队列

## 哪些任务阻断公开发布

阻断公开发布的原始缺口任务共 8 个：

- 公开技术规格
- 产品图片
- 产品视频
- 客户案例
- 服务 FAQ
- 交付 / 保修 / 价格政策
- 公开使用审批记录
- 公开宣传边界

员工队列中包含 QA 验收项，因此阻断公开发布的队列项数量会高于原始缺口任务数量。

## 新增文件

- `apps/commander/employees/mission_queue_v1/employee_mission_queue.schema.json`
- `apps/commander/employees/mission_queue_v1/hk620_employee_mission_queue.v1.json`
- `apps/commander/employees/mission_queue_v1/knowledge_agent.hk620.queue.v1.json`
- `apps/commander/employees/mission_queue_v1/website_agent.hk620.queue.v1.json`
- `apps/commander/employees/mission_queue_v1/qa_agent.hk620.queue.v1.json`

## 更新文件

- `apps/commander/employees/runtime/employee_queue.json`
- `apps/dashboard/index.html`
- `apps/dashboard/employee_workbench.html`
- `apps/dashboard/employee_workbench_data.json`
- `apps/commander/employees/profiles/website_agent.json`
- `apps/commander/employees/profiles/knowledge_agent.json`
- `apps/commander/employees/profiles/qa_agent.json`
- `apps/commander/employees/runtime/employee_status.json`
- `apps/commander/employees/reports/employee_dashboard.json`

## 是否需要 CEO 授权

本次不需要 CEO 授权。

未来如果要调用 n8n、WordPress、创建真实 Draft、发布、删除、修改外部平台、发送 Gmail 或上传 YouTube，仍必须 CEO 单独授权。

## 如何验证

1. 打开 `apps/dashboard/index.html`，确认显示“HK620 资料缺口已进入员工队列”。
2. 打开 `apps/dashboard/employee_workbench.html`，查看员工卡片中的待办数量、QA 待验收数量、阻断公开发布数量。
3. 查看 `apps/commander/employees/mission_queue_v1/hk620_employee_mission_queue.v1.json`，确认三位员工队列已生成。
4. 查看 `apps/commander/employees/runtime/employee_queue.json`，确认 HK620 缺口任务已进入 pending_missions。
5. 确认所有 JSON 可解析，页面没有调用任何外部平台。
