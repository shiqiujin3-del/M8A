# Video Agent 今日交付：YouTube Private/Draft Only 工作流设计 V1

日期：2026-07-08

## 目标

设计一个只允许私有或草稿阶段的视频工作流，不公开视频。

## 工作流定位

YouTube 是执行工具，不是 AI 员工。

Video Agent 负责视频脚本、视频资料准备、上传方案设计。

公开发布必须 CEO 审批。

## 流程设计

1. Commander 创建视频任务。
2. Video Agent 生成视频脚本。
3. QA Agent 检查脚本和合规风险。
4. Video Agent 准备标题、描述、标签、缩略图需求。
5. n8n 执行 Private/Draft Only 上传。
6. Commander 返回视频私有链接或状态。
7. CEO 决定是否公开发布。

## 当前允许

- YouTube 只读连接检查。
- 设计 Private/Draft Only 流程。
- 准备视频标题、描述、标签方案。

## 当前禁止

- 上传公开视频。
- 发布视频。
- 删除视频。
- 修改频道设置。
- 自动公开视频。

## CEO 审批点

必须审批：

- 视频标题。
- 视频脚本。
- 视频描述。
- 是否上传。
- 是否公开发布。

## 验收标准

- 默认状态必须是 Private 或 Draft。
- 不允许自动公开。
- 每个视频任务必须有任务编号。
- 发布动作必须独立审批。

## 下一步

等待 CEO 批准后，创建 YouTube Private/Draft Only n8n 工作流。
