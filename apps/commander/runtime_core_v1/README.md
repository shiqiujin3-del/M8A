# M8A Runtime Core V1

Runtime Core V1 是 M8A 的统一运行核心。

它不替代现有 Commander、Mission Queue、Runtime Persistence、Event Center、External Executor、Audit，而是在它们之间建立统一运行对象、统一状态机、统一 Provider Interface、统一 Execution Contract 和统一 Runtime Event。

## 为什么需要 Runtime Core

当前 WordPress、YouTube、Gmail、Google 等平台已经能分别执行任务，但如果每个平台各自维护状态，未来会出现：

- Dashboard 需要解析不同平台响应。
- Audit 需要适配不同日志格式。
- Retry 与 Progress 无法统一。
- YouTube 等大文件上传失败后无法标准化恢复。
- 新增平台时容易改 Commander、Dashboard、Audit。

Runtime Core V1 的目标是消除这些分叉。

## 核心组成

- `runtime_core.object.v1.json`：统一 Runtime Object。
- `runtime_state_machine.v1.json`：统一状态机。
- `provider_interface.v1.json`：统一 Provider Interface。
- `execution_contract.v1.json`：统一 Execution Contract。
- `runtime_events.v1.json`：统一 Runtime Event。
- `migration/runtime_core_migration_plan.v1.json`：迁移建议。

## 统一状态

所有 Mission 与 Execution 必须使用：

- created
- queued
- running
- waiting
- retrying
- completed
- failed
- cancelled
- timeout

## Provider 规则

Provider 只允许负责：

- Execute()
- Cancel()
- Query()
- Resume()

Provider 不允许：

- 直接操作 Dashboard。
- 直接修改 Mission。
- 绕过 Approval。
- 绕过 Audit。
- 返回无法统一解析的私有状态。

## 以后必须接入 Runtime Core 的模块

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

## 新平台接入原则

以后新增任何平台，不得修改 Commander、Dashboard、Audit。

只允许：

1. 实现 Provider Interface。
2. 返回统一 Execution Contract。
3. 写入 Runtime Event。
4. 通过 Runtime Core 更新状态。

