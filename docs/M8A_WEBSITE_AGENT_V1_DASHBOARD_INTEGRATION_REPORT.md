# M8A Website Agent V1 接入总控与员工工作台报告

日期：2026-07-09

## 结论

Website Agent V1 已接入总控台和 AI 员工工作台。CEO 可以在页面中看到 Website Agent 是正式上岗员工，而不是只存在于文档中。

本次只做本地 UI 与本地数据接入，未调用 n8n，未调用 WordPress，未发布、未删除、未修改任何外部平台内容。

## 已确认已完成能力

- Commander Mission 输入入口：已存在，未重复开发。
- CEO Approval 审批链路：已存在，未重复开发。
- Website Agent Draft Generation：已存在本地链路，未重复开发。
- QA Checklist：已升级到 Website Agent QA V2 标准。
- n8n Webhook：已记录为 Draft-only 入口能力，本次未调用。
- Commander 到 n8n 调用：已通过安全门保留，本次未触发。
- WordPress Draft 创建：已有验收记录，本次未创建新草稿。
- HK620 Draft 测试：已有验收记录，本次未重复执行。
- Workflow 正式命名：仍需 CEO 在 n8n 外部平台手动确认。
- Mission Log 与长期记录：已接入 Website Agent V1 标准日志规范。

## 本次接入内容

- 总控台新增 Website Agent V1 员工状态卡片。
- 员工工作台新增 Website Agent V1 正式员工展示区。
- 员工数据补充 Employee ID、部门、状态、当前任务、Mission Queue、QA Score Gate、Draft Count、Waiting Approval、Logs / History 入口、可复用模板说明。
- Website Agent 本地档案补充 Mission Protocol、Prompt System、QA V2、Retry Engine、Mission Log 能力。

## Mission 分类规则 V1

A 类：Build（建设）

AI 可以自动完成，无需 CEO 审批。包括：写代码、建 Dashboard、建 Agent、建模板、建文档、建知识库、写测试、本地验证。

外部平台动作仍不得自动执行，仍需 CEO 审批。包括：调用 n8n、调用 WordPress、发布、删除、修改已发布文章、发送 Gmail、上传 YouTube。

## 验证方式

1. 打开总控台 `apps/dashboard/index.html`，查看“Website Agent V1 员工状态”。
2. 打开 AI 员工工作台 `apps/dashboard/employee_workbench.html`，查看“Website Agent V1 正式员工”。
3. 确认页面显示 QA Score Gate：90、Mission Queue、Draft Count、Waiting Approval、Logs / History、可复用模板说明。
4. 确认页面显示 Build 类无需 CEO 审批，外部平台动作仍需 CEO 审批。

## 是否需要 CEO 授权

本次本地建设接入属于 A 类 Build，不需要 CEO 审批。

任何未来 n8n、WordPress、发布、删除、修改外部平台内容的动作，仍必须 CEO 单独授权。
