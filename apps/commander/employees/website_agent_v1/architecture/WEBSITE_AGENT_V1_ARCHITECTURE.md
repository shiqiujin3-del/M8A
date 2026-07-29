# Website Agent V1 架构说明

## 一、定位

Website Agent V1 是 M8A 的网站内容员工，负责把已批准或待审核的产品资料转成网站可用草稿、SEO 信息、结构化输出、QA 结果和发布前审批请求。

Website Agent V1 不默认发布内容。它只准备 Draft-only 内容和审批材料。

## 二、职责

1. 读取 Commander Mission。
2. 校验 Mission Protocol 字段完整性。
3. 读取产品资料与目标市场要求。
4. 生成客户可读内容草稿。
5. 生成 SEO、FAQ、Schema、媒体建议。
6. 执行 Website Agent QA V2。
7. QA Score 低于 90 时阻止进入发布流程。
8. 写入 Mission Log。
9. 生成标准 JSON Output。
10. 等待 CEO 审批后才能进入 n8n / WordPress Draft-only 链路。

## 三、生命周期

```text
registered
→ idle
→ mission_assigned
→ input_validating
→ drafting
→ qa_checking
→ waiting_ceo_approval
→ authorized_for_draft_only
→ handoff_to_executor
→ completed
```

异常路径：

```text
input_validating / drafting / qa_checking / handoff_to_executor
→ failed
→ retry_scheduled 或 waiting_human_review
```

## 四、输入

- Mission ID
- Priority
- Product
- Language
- Target Market
- Target Platform
- Expected Output
- Product Knowledge
- Approval Status
- Publish Status
- Retry Count
- Mission Log

## 五、输出

- Mission 摘要
- Content 草稿
- SEO 元数据
- Media 建议
- FAQ
- Schema
- Publish Info
- QA Result
- Mission Log

## 六、错误处理

所有错误必须写入 Mission Log。错误分为：

- webhook_failure
- wordpress_failure
- timeout
- validation_error
- network_error
- qa_score_below_threshold
- approval_missing
- unsafe_publish_attempt

## 七、日志规范

每个 Mission 必须记录：开始时间、结束时间、执行 Agent、耗时、Token、状态、错误、最终结果。日志只记录必要业务信息，不写入密钥、密码、Token、Cookie。

## 八、安全门

- 未经 CEO 审批，不调用 n8n。
- 未经 CEO 单独授权，不进入 WordPress Draft-only。
- 禁止 publish。
- 禁止 update_published_post。
- 禁止 delete_post。
- 禁止 send_gmail。
- 禁止 upload_youtube。
