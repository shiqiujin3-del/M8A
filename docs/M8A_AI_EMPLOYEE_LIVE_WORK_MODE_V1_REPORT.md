# M8A AI Employee Live Work Mode V1 报告

日期：2026-07-10

## 结论

本次没有重新创建 AI 员工，也没有重做员工中心。

本次目标是把已经存在的员工推进到“可领取本地任务、产出结果、写入审计”的 Live Work Mode。

## 本次接入员工

- Knowledge Agent
- Website Agent
- QA Agent
- Publishing Agent

## 执行链路

Knowledge Agent → Website Agent → QA Agent → Publishing Agent

## 验收结果

1. Knowledge Agent 正确识别 HK620 公开技术规格任务需要真实资料来源，状态进入 `waiting_source_material`。
2. Website Agent 完成两个本地结构化任务：
   - HK620 外部参考链接计划
   - HK620 内部链接计划
3. QA Agent 完成两个本地 QA：
   - 外部参考链接计划：88 分，需人工确认 URL，不允许发布
   - 内部链接计划：91 分，通过本地 QA，不允许发布
4. Publishing Agent 完成发布准备检查，状态进入 `waiting_ceo_authorization`。

本次共处理 6 个工作项：1 个 Knowledge 等待资料、2 个 Website 输出、2 个 QA 检查、1 个 Publishing 发布准备。

## 安全确认

本次没有调用 n8n。

本次没有调用 WordPress。

本次没有调用 YouTube。

本次没有调用 Gmail。

本次没有发布、删除或修改任何外部平台内容。

## 生成文件

- `apps/commander/employees/live_work_mode_v1/live_work_config.v1.json`
- `apps/commander/employees/live_work_mode_v1/live_work_runner.py`
- `apps/commander/employees/live_work_mode_v1/live_work_run_result.v1.json`
- `apps/commander/employees/live_work_mode_v1/live_work_audit_log.v1.json`
- `apps/commander/employees/live_work_mode_v1/live_employee_status.v1.json`

## 当前真实状态

Website Agent 与 QA Agent 已经具备可重复本地工作能力。

Knowledge Agent 不是没启动，而是卡在真实资料缺口，不能虚构规格、图片、视频、客户案例、价格或保修承诺。

Publishing Agent 已经能做发布准备检查，但未获 CEO 授权前不能调用外部平台。

## 下一步

下一步应把 Live Work Mode 接到更稳定的“队列循环”：

1. 定时扫描本地 Mission Queue。
2. 只自动执行 A 类 Build / 本地任务。
3. 遇到资料缺口、CEO 审批、外部动作立即停止并写明原因。

## 状态

READY FOR LOCAL EMPLOYEE LOOP
