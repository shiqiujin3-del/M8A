# M8A Runtime Persistence Architecture V1

状态：A 类 Build，本地建设，不调用外部平台。

## 目标

为 Mission Center 与 Event Center 建立本地长期运行数据层。现有 JSON 继续可读，SQLite 作为 V1 runtime store，未来可升级 PostgreSQL。

## 存储边界

- Mission：任务主数据、负责人、优先级、状态、依赖、运行状态。
- Event：append-only 事件流，不覆盖历史事件。
- Employee Queue：员工当前任务、待办、失败、阻断、QA 指标。
- Timeline：Mission 与 Event 的时间线视图。
- History：永久保留 Mission / Event / QA / Approval / Error 记录。
- Runtime Log：健康检查、导入、迁移、重试记录。

## 原则

1. JSON 是兼容输入和配置层。
2. SQLite 是本地运行数据层。
3. Event Store append-only，不直接覆盖事件。
4. Dashboard 先读兼容 JSON，未来可切换到 SQLite 视图。
5. 不调用 n8n / WordPress / Gmail / YouTube / 外部 API。
