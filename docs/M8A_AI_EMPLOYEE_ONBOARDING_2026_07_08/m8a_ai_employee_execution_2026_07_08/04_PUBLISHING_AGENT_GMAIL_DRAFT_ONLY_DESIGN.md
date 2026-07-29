# Publishing Agent 今日交付：Gmail Draft Only 工作流设计 V1

日期：2026-07-08

## 目标

设计一个只创建邮件草稿、不发送邮件的工作流。

## 工作流定位

Gmail 只作为营销执行工具，不是员工，不是总控。

Publishing Agent 负责准备邮件内容和草稿，是否发送必须由 CEO 审批。

## 流程设计

1. Commander 创建邮件任务。
2. Publishing Agent 生成邮件主题和正文。
3. QA Agent 检查邮件内容。
4. n8n 创建 Gmail Draft。
5. Commander 返回 Draft 信息给 CEO。
6. CEO 决定是否发送。

## 当前允许

- Gmail 连接健康检查。
- 设计 Draft Only 流程。
- 准备邮件草稿方案。

## 当前禁止

- 发送邮件。
- 删除邮件。
- 读取邮件正文。
- 修改邮箱标签。
- 批量群发。

## CEO 审批点

必须审批：

- 邮件主题。
- 收件人名单。
- 邮件正文。
- 是否发送。

## 验收标准

- 草稿创建后不得自动发送。
- CEO 能看到邮件内容。
- 每封邮件都有任务编号。
- 发送动作必须独立审批。

## 下一步

等待 CEO 批准后，创建 Gmail Draft Only n8n 工作流。
