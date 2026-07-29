# M8A Product Knowledge Gap Task Center V1 报告

日期：2026-07-09

## 结论

已基于 Website Agent Knowledge Binding V1 建立“产品资料缺口任务中心”。HK620 从 approved_internal 推进到 future public approved 的路径已经拆成可跟踪任务，包含负责人、状态和验收标准。

本次属于 A 类 Build，本地建设任务，不需要 CEO 审批。未调用 n8n，未调用 WordPress，未生成新文章，未发布、未删除、未修改任何外部平台。

## HK620 当前缺哪些资料

已建立 10 个缺口任务：

1. 公开技术规格
2. 产品图片
3. 产品视频
4. 客户案例
5. 外部参考链接
6. 内部链接
7. 服务 FAQ
8. 交付 / 保修 / 价格政策
9. 公开使用审批记录
10. 公开宣传边界

## 哪些缺口阻止公开发布

当前 8 个任务会阻止公开发布：

- 公开技术规格
- 产品图片
- 产品视频
- 客户案例
- 服务 FAQ
- 交付 / 保修 / 价格政策
- 公开使用审批记录
- 公开宣传边界

外部参考链接和内部链接不一定阻止本地草稿，但会影响 SEO、可信度和 QA 分。

当前本地概念草稿仍可推进，但必须带 QA 扣分和安全提示；不得把 HK620 当作 public approved 使用。

## 哪些 AI 员工负责

Website Agent：

- 负责内容结构
- 负责内部链接和外部参考占位
- 负责发布准备
- 不负责凭空补产品事实

Knowledge Agent：

- 负责资料整理
- 负责知识库补全
- 负责来源文件登记
- 负责推动规格、图片、视频、客户案例、服务 FAQ、政策资料补齐

QA Agent：

- 负责验收
- 负责 QA Score
- 负责公开声明边界
- 负责判断是否阻止发布流程

## 新增文件

- `apps/commander/product_knowledge_gap_task_center/product_knowledge_gap_task_center.schema.json`
- `apps/commander/product_knowledge_gap_task_center/product_knowledge_gap_task_center.index.json`
- `apps/commander/product_knowledge_gap_task_center/hk620_product_knowledge_gap_tasks.v1.json`
- `knowledge/products/HK620/gap_tasks/hk620_product_knowledge_gap_tasks.v1.json`

## 更新文件

- `apps/dashboard/index.html`
- `apps/dashboard/employee_workbench.html`
- `apps/dashboard/employee_workbench_data.json`
- `apps/commander/employees/profiles/website_agent.json`
- `apps/commander/employees/profiles/knowledge_agent.json`
- `apps/commander/employees/profiles/qa_agent.json`
- `apps/commander/employees/runtime/employee_status.json`
- `apps/commander/employees/reports/employee_dashboard.json`

## 是否需要 CEO 授权

本次不需要 CEO 授权，因为这是 A 类 Build，本地建设任务。

未来如果要执行以下动作，仍必须 CEO 授权：

- 调用 n8n
- 调用 WordPress
- 创建或更新真实 WordPress Draft
- 发布
- 删除
- 修改已发布文章
- 发送 Gmail
- 上传 YouTube

## 如何验证

1. 打开 `apps/dashboard/index.html`，确认显示“HK620 资料缺口任务中心已建立”。
2. 打开 `apps/dashboard/employee_workbench.html`，确认 Website Agent V1 区域显示 Product Knowledge Gap Task Center V1。
3. 检查 `apps/commander/product_knowledge_gap_task_center/hk620_product_knowledge_gap_tasks.v1.json`，确认 10 个任务包含 gap_id、owner_agent、acceptance_criteria、blocks_public_publish 等字段。
4. 检查 `knowledge/products/HK620/gap_tasks/hk620_product_knowledge_gap_tasks.v1.json`，确认统一知识中心也有副本。
5. 确认所有 JSON 可解析，页面没有调用任何外部平台。
