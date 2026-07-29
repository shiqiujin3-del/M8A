# M8A Publishing Center V1

Publishing Center V1 是 M8A 所有内容发布任务的统一调度中心。

它位于 Commander 与 Provider 之间：

```text
Commander
  ↓
Publishing Center
  ↓
Runtime Core
  ↓
External Executor
  ↓
Provider
```

## V1 边界

本版本只完成最小可运行架构：

- Publishing Mission
- Publishing Queue
- Publishing Dispatcher
- Publishing Result
- Publishing Dashboard Model
- Publishing Migration Plan

V1 不真实调用任何平台，不上传 YouTube，不修改 WordPress，不开发 Facebook、LinkedIn、TikTok。

## 核心原则

以后 Commander 不直接调用 WordPress、YouTube、Facebook、LinkedIn 等 Provider。

所有内容发布任务必须先进入 Publishing Center，再由 Publishing Center 根据任务类型选择 Provider。

新增平台时，原则上只新增 Provider 和 Dispatcher 映射，不修改 Commander、Dashboard、Audit。

## 与 Runtime Core 的关系

Publishing Center 负责任务分类与 Provider 选择。

Runtime Core 负责统一运行对象、状态机、Execution Contract、Event 与 Audit 生命周期。

Publishing Result 必须兼容 Runtime Core Execution Contract。

