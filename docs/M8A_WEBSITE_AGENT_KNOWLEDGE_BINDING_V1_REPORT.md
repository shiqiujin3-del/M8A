# M8A Website Agent Knowledge Binding V1 报告

日期：2026-07-09

## 结论

Website Agent V1 已具备 Knowledge Binding 能力。执行链中的 Knowledge Fetch 不再依赖临时输入，而是从统一 Knowledge Center 读取产品资料绑定。

本次属于 A 类 Build，本地建设任务，不需要 CEO 审批。未调用 n8n，未调用 WordPress，未生成新文章，未发布、未删除、未修改任何外部平台。

## 本次新增能力

- Website Agent Knowledge Binding V1 标准。
- HK620 产品知识绑定样例。
- 产品资料缺失检查清单。
- Knowledge Fetch 执行链说明更新。
- 总控台与员工工作台展示更新。

## HK620 知识绑定包含什么

HK620 绑定字段包括：

- product_id：product_hk620
- product_name：HK620
- product_category：骨骼门线条专用封边 / 开槽 / 切断连续加工设备
- target_market：美国
- buyer_persona：美国门厂、家具厂、装饰线条加工客户
- features：先封边、再开槽、最后切断、连续工艺路线
- specs：当前多项技术规格缺失，不能虚构
- applications：骨骼门线条加工、门厂新工艺探索、连续加工场景
- pain_points：短料加工稳定性、人工/分段加工一致性、门厂差异化工艺需求
- differentiators：工艺顺序本身，但不得写行业唯一、绝对第一、量化优势
- FAQ：内部可用基础问答
- media_requirements：产品图、细节图、应用图、demo 视频仍缺失
- internal_links：HK620 Source Library、Golden Knowledge V3、Knowledge Gap Report
- external_references：官方外部页面仍未验证
- source_files：统一知识中心和 HK620 cards
- freshness_status：fresh_for_internal_draft_only / not_public_approved

## 哪些资料缺失会卡住任务

会阻止本地草稿：

- product_id / product_name 缺失
- product_category 缺失
- target_market 缺失
- buyer_persona 或 applications 缺失
- 没有任何 approved_internal source_file
- forbidden_claims / public_use_boundary 缺失

会阻止发布或外部交接：

- CEO approval 缺失
- QA Score 低于 90
- public approval status 缺失
- Draft-only 单独授权缺失

## 哪些资料缺失只降低 QA 分

以下不阻止本地概念草稿，但会降低 QA 分：

- 完整技术规格缺失
- 产品图片 / 细节图 / 应用图缺失
- 产品 demo 视频缺失
- 外部参考链接缺失
- 内部链接目标缺失
- 客户案例 / 公开证据缺失
- 服务 FAQ / 故障排除缺失
- 精确交付、保修、价格政策缺失

## 哪些步骤可自动做

可自动做，且不需要 CEO 审批：

- 读取本地 Knowledge Binding JSON
- 检查必填字段
- 检查 source_files 是否存在
- 检查 freshness_status
- 检查 public_use_boundary
- 生成缺失项摘要
- 将缺失项写入 Mission Log
- 本地草稿前的知识准备与 QA 扣分判断

## 是否需要 CEO 授权

本次 Knowledge Binding 建设不需要 CEO 授权。

未来以下动作仍必须 CEO 授权：

- 调用 n8n
- 调用 WordPress
- 创建或更新真实 WordPress Draft
- 发布
- 删除
- 修改已发布文章
- 发送 Gmail
- 上传 YouTube

## 新增文件

- `apps/commander/employees/website_agent_v1/knowledge_binding/website_agent_knowledge_binding.schema.json`
- `apps/commander/employees/website_agent_v1/knowledge_binding/hk620.knowledge_binding.v1.json`
- `apps/commander/employees/website_agent_v1/knowledge_binding/product_knowledge_missing_checklist.v1.json`
- `knowledge/products/HK620/bindings/website_agent_hk620.knowledge_binding.v1.json`

## 更新文件

- `apps/commander/employees/website_agent_v1/execution_chain/website_agent_execution_chain.v1.json`
- `apps/commander/employees/website_agent_v1/dashboard/website_agent_dashboard.schema.json`
- `apps/commander/employees/website_agent_v1/README.md`
- `apps/dashboard/index.html`
- `apps/dashboard/employee_workbench.html`
- `apps/dashboard/employee_workbench_data.json`
- `apps/commander/employees/profiles/website_agent.json`
- `apps/commander/employees/runtime/employee_status.json`
- `apps/commander/employees/reports/employee_dashboard.json`

## 验证方式

1. 打开 `apps/dashboard/index.html`，确认显示 Website Agent 已具备 Knowledge Binding。
2. 打开 `apps/dashboard/employee_workbench.html`，确认 Website Agent V1 区域显示 Knowledge Binding V1 和 HK620 绑定路径。
3. 检查 `apps/commander/employees/website_agent_v1/knowledge_binding/hk620.knowledge_binding.v1.json`，确认字段完整。
4. 检查 `apps/commander/employees/website_agent_v1/knowledge_binding/product_knowledge_missing_checklist.v1.json`，确认阻断项和 QA 扣分项已分开。
5. 确认页面没有调用 n8n / WordPress，也没有生成或发布新文章。
