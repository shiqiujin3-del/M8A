# M8A Publishing Center V1 报告

日期：2026-07-10

## 一、结论

Publishing Center V1 已建立。

本次只完成统一发布调度架构与数据模型，没有修改 Runtime Core，没有修改 Commander，没有继续上传 HK680，没有修改 WordPress Provider 或 YouTube Provider，也没有连接任何生产平台。

状态：READY FOR NEXT PROVIDER

## 二、为什么需要 Publishing Center

M8A Runtime Core V1 已经建立统一运行机制。

但是如果 Commander 继续直接面对 WordPress、YouTube、Facebook、LinkedIn、TikTok 等 Provider，平台越多，Commander 越复杂。

Publishing Center V1 的作用是把所有“内容发布任务”集中到一个统一入口：

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

以后 Commander 不直接调用 WordPress、YouTube 等 Provider。

## 三、V1 已完成能力

### 1. Publishing Mission

统一发布任务对象已定义，支持：

- Publish Product
- Publish Article
- Publish Video
- Publish Social Post

核心字段包括：

- publishing_mission_id
- mission_id
- publishing_type
- priority
- target_platform
- target_provider
- content_ref
- approval_status
- runtime_status

### 2. Publishing Queue

统一发布队列已定义，V1 支持状态：

- queued
- running
- completed
- failed

队列只负责发布任务排队与状态记录，不直接调用外部平台。

### 3. Publishing Dispatcher

调度规则已定义：

- Publish Article → WordPress Provider
- Publish Product → WordPress Provider
- Publish Video → YouTube Provider
- Publish Social Post → Facebook / LinkedIn / TikTok Provider

V1 只完成调度设计，不真实执行上传或发布。

### 4. Publishing Result

统一返回对象已定义，包含：

- mission_id
- execution_id
- provider
- resource_type
- status
- resource_id
- resource_url
- started_at
- finished_at
- error

Publishing Result 已明确兼容 Runtime Core Execution Contract。

### 5. Publishing Dashboard Model

未来 Dashboard 数据模型已定义，包括：

- 今天待发布
- 发布中
- 成功
- 失败
- 等待审批

本次没有开发前端页面。

## 四、与 Runtime Core 的兼容性

Publishing Center 不替代 Runtime Core。

Publishing Center 只负责：

- 接收发布任务
- 进入发布队列
- 根据任务类型选择 Provider
- 生成 Publishing Result

Runtime Core 继续负责：

- Mission 生命周期
- Execution 生命周期
- Retry 生命周期
- Progress 生命周期
- Audit 生命周期
- Event Store

Publishing Result 必须兼容 Runtime Core Execution Contract。

## 五、验收问题回答

### 1. Commander 是否已经可以把发布任务交给 Publishing Center？

原则上可以。

V1 已定义 Commander 需要写入的 Publishing Mission 对象。下一阶段只需要让 Commander 创建发布类 Mission 时写入 Publishing Center，不需要 Commander 直接选择 WordPress 或 YouTube Provider。

### 2. Publishing Center 是否已经能够根据任务类型选择对应 Provider？

可以。

V1 已定义 Dispatcher 规则：

- publish_article → wordpress_provider
- publish_product → wordpress_provider
- publish_video → youtube_provider
- publish_social_post → facebook_provider / linkedin_provider / tiktok_provider

### 3. 新增平台是否原则上只需新增 Provider，而不需要修改 Commander？

是。

新增 Facebook、LinkedIn、TikTok 等平台时，原则上只新增：

- Provider
- dispatch rule

不需要修改 Commander、Dashboard、Audit 的核心逻辑。

### 4. Publishing Center 是否完全兼容 Runtime Core？

是。

Publishing Result 已对齐 Runtime Core Execution Contract，核心字段包括 execution_id、mission_id、provider、resource_id、resource_url、status、started_at、finished_at、retry_count、error。

## 六、新增文件

- apps/commander/publishing_center_v1/README.md
- apps/commander/publishing_center_v1/publishing_center.schema.json
- apps/commander/publishing_center_v1/publishing_queue.v1.json
- apps/commander/publishing_center_v1/publishing_dispatcher.v1.json
- apps/commander/publishing_center_v1/publishing_result.v1.json
- apps/commander/publishing_center_v1/publishing_dashboard_model.v1.json
- apps/commander/publishing_center_v1/publishing_migration_plan.v1.json
- docs/M8A_PUBLISHING_CENTER_V1_REPORT.md

## 七、本次未做事项

- 没有修改 Runtime Core。
- 没有修改 Commander。
- 没有继续上传 HK680。
- 没有修改 WordPress Provider。
- 没有修改 YouTube Provider。
- 没有开发 Facebook、LinkedIn、TikTok。
- 没有连接任何生产平台。
- 没有发布、删除、修改任何生产内容。

## 八、下一步建议

下一步可以进入“Next Provider”阶段：

1. 先把 WordPress Draft Provider 映射为 Publishing Center 的 publish_article 默认 Provider。
2. YouTube Provider 在可靠上传层完成后，再接入 publish_video。
3. Facebook、LinkedIn、TikTok 后续只作为新增 Provider 接入，不再改 Commander。

最终状态：READY FOR NEXT PROVIDER

