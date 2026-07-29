# M8A Runtime Core V1 报告

日期：2026-07-10

## 一、结论

Runtime Core V1 已建立为 M8A 的统一运行核心标准。

本次没有继续上传 HK680，没有继续调试 YouTube，没有修改 WordPress、Gmail、Facebook 或其它外部平台。交付内容只包含 Runtime Core 设计、状态机、Provider Interface、Execution Contract、Runtime Event、目录结构建议与迁移建议。

## 二、为什么现在必须建立 Runtime Core

M8A 已完成 Commander、Mission、Dashboard、Runtime、Audit、WordPress Draft、YouTube Upload 验证。

YouTube 上传过程中暴露出一个长期架构问题：如果 WordPress、YouTube、Gmail、Facebook、LinkedIn 未来各自维护状态，Dashboard、Audit、Retry、Progress 都会被迫适配不同平台格式。

Runtime Core V1 用统一运行对象把这些状态收回 M8A 中央。

## 三、Runtime Core 设计

Runtime Core V1 包含：

- Mission：任务身份、类型、优先级、负责人、状态。
- Execution：执行身份、Provider、动作、开始结束时间、耗时。
- State：统一状态机当前状态与状态变更原因。
- Provider：外部平台能力声明。
- Resource：外部资源 ID、URL、类型、状态。
- Progress：执行进度，支持大文件上传。
- Retry：重试次数、策略、下一次重试时间。
- Error：错误码、错误信息、是否可重试。
- Result：统一执行结果。
- Event：最后事件 ID、Event Store 与 Audit 要求。

## 四、统一状态机

统一状态：

- created
- queued
- running
- waiting
- retrying
- completed
- failed
- cancelled
- timeout

关键规则：

- Draft-only 与 Read-only 可在安全授权范围内自动从 queued 进入 running。
- Publish、Delete、Update Published Content 等 B 类动作必须进入 waiting，等待 CEO 授权。
- retrying 只能回到 queued 或进入 failed。
- completed、failed、cancelled、timeout 是终态。

## 五、Provider Interface

所有 Provider 只允许实现：

- Execute()
- Cancel()
- Query()
- Resume()

Provider 不允许：

- 直接操作 Dashboard。
- 直接修改 Mission。
- 绕过 Approval Center。
- 绕过 Production Safety Gate。
- 绕过 Audit。

新增平台时，只能新增 Provider 实现，不能让 Commander、Dashboard、Audit 为新平台改私有逻辑。

## 六、统一 Execution Contract

所有 Provider 必须返回：

- execution_id
- mission_id
- provider
- resource_id
- resource_url
- status
- started_at
- finished_at
- retry_count
- error

Dashboard 与 Audit 只读取这些统一字段，不再解析 WordPress、YouTube、Gmail 等平台私有响应。

## 七、Runtime Event

Runtime Core V1 要求所有事件进入 Event Store：

- Mission Created
- Mission Started
- Execution Started
- Execution Progress
- Execution Retry
- Execution Failed
- Execution Completed
- Mission Completed

这保证 Mission 生命周期、Execution 生命周期、Retry 生命周期、Progress 生命周期、Audit 生命周期都能被统一追踪。

## 八、目录结构建议

建议目标目录：

```text
apps/commander/runtime_core_v1/
  README.md
  runtime_core.object.v1.json
  runtime_state_machine.v1.json
  provider_interface.v1.json
  execution_contract.v1.json
  runtime_events.v1.json
  migration/
    runtime_core_migration_plan.v1.json
docs/
  M8A_RUNTIME_CORE_V1_REPORT.md
```

## 九、迁移建议

第一阶段：冻结 Runtime Core 标准。

第二阶段：把已验证 Provider 映射到 Runtime Core：

- WordPress Draft Executor
- Gmail Draft Executor
- Google Search Console Executor
- GA4 Executor

第三阶段：把大文件上传 Provider 接入 Progress、Retry、Resume：

- YouTube Upload Executor
- 未来 Vimeo、Google Drive、Dropbox、S3、OSS

第四阶段：Dashboard 与 Audit 收敛为只读 Runtime Core 字段。

## 十、以后必须运行在 Runtime Core 的模块

- WordPress Draft Executor
- YouTube Upload Executor
- Gmail Draft Executor
- Google Search Console Executor
- GA4 Executor
- Facebook Executor
- LinkedIn Executor
- Vimeo / Google Drive / Dropbox / S3 / OSS 上传 Executor
- Mission Queue Live Integration
- Approval Center 到 External Executor 的交接
- Production Safety Gate 到 External Executor 的交接

## 十一、对未来平台的约束

Runtime Core 建立后，新增任何平台不得修改：

- Commander
- Dashboard
- Audit

新增平台只允许：

1. 实现 Provider Interface。
2. 返回统一 Execution Contract。
3. 写入 Runtime Event。
4. 通过 Runtime Core 更新状态。

## 十二、安全确认

本次没有执行以下动作：

- 没有继续上传 HK680。
- 没有继续调试 YouTube。
- 没有调用 n8n。
- 没有修改 WordPress。
- 没有修改 Gmail。
- 没有开发 Facebook。
- 没有发布、删除、修改任何生产内容。

Runtime Core V1 到此完成，等待 CEO Review。

