# M8A AI 员工上岗同步计划 V1

生成日期：2026-07-08

## 目标

把第一批 AI 员工从“已登记”推进到“已上岗，可分配任务”。

## 当前已完成

已生成上岗包：

- `ai_employee_onboarding_v1.json`
- `employee_status_patch_v1.json`
- `n8n_workflow_bindings_patch_v1.json`
- `employee_missions_2026_07_08.json`
- `M8A_AI_EMPLOYEE_ONBOARDING_REPORT_V1.md`

## 第一批上岗员工

- Website Agent
- SEO Agent
- Data Agent
- Publishing Agent
- Video Agent

## 同步到 Commander 后的效果

CEO 在总控页面应看到：

- 5 名 AI 员工状态为“正式上岗”
- 每名员工有明确岗位
- 每名员工有明确可用平台
- 每名员工有禁止动作
- 每名员工有今天第一项任务

## 建议同步文件

需要同步到 M8A 主项目：

- `apps/commander/employees/registry/ai_employee_registry.json`
- `apps/commander/employees/runtime/employee_status.json`
- `apps/commander/integrations/n8n_workflow_bindings.json`
- `apps/dashboard/employee_workbench_data.json`

## 当前环境说明

当前可写目录是：

- `/Users/shiqiujing/Documents/n8n`

M8A 主项目目录当前不是可写目录，因此本次先生成可同步上岗包。

## 下一步

1. 将上岗包同步到 Commander。
2. 打开 AI 员工工作台确认显示。
3. 分派 Website Agent 的下一篇 WordPress Draft。
4. 分派 SEO Agent 的 HK620 页面 SEO 检查。
5. 分派 Data Agent 的数据日报模板。

## CEO 需要知道的事

这一步不会触发任何外部发布。

这一步不会发邮件。

这一步不会上传视频。

这一步不会改 Google、WordPress、YouTube 设置。

它只是让 AI 员工正式进入岗位，并准备执行下一批任务。
