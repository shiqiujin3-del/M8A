# Website Agent V1 标准员工包

状态：已完成 V1 标准架构设计；已补充可复用执行链 V1
日期：2026-07-09

本目录定义 M8A 第一位可长期工作的 AI 员工 Website Agent V1。它不是文章 Demo，而是可复用、可审计、可交接的员工运行标准。

安全边界：本包只定义标准、模板、schema、日志和流程；不调用 n8n，不调用 WordPress，不发布内容，不删除外部内容。

## 目录

- architecture/WEBSITE_AGENT_V1_ARCHITECTURE.md：员工架构、生命周期、输入输出、错误处理、日志规范
- schemas/mission_protocol.schema.json：统一 Mission Protocol
- schemas/standard_output.schema.json：标准 JSON Output
- prompts/prompt_system.templates.json：统一 Prompt System
- qa/website_agent_qa_v2.checklist.json：Website Agent QA V2
- logs/mission_log.schema.json：Mission Log Center
- retry/retry_engine.design.json：Retry Engine 设计
- dashboard/website_agent_dashboard.schema.json：Dashboard 数据结构
- templates/website_agent_product_template.json：未来产品/内容类型复用模板

## 可复用执行链 V1

Website Agent V1 已具备可复用执行链：Mission Intake → Knowledge Fetch → Draft Generation → SEO Enrichment → QA V2 Scoring → Approval Gate → Draft-only Handoff → Mission Log Writeback。

自动推进：Mission Intake、Knowledge Fetch、Draft Generation、SEO Enrichment、QA V2 Scoring、Mission Log Writeback。

必须 CEO 审批：Approval Gate、Draft-only Handoff，以及任何真实 n8n / WordPress / 发布 / 删除 / 修改外部平台动作。

新增文件：

- execution_chain/website_agent_execution_chain.v1.json：标准执行链
- state_machine/website_agent_state_machine.v1.json：状态机和状态转换规则
- dashboard/website_agent_state_dashboard_mapping.v1.json：总控台 / 员工工作台状态映射
- templates/product_content_mission.template.json：产品内容 Mission 模板
- templates/blog_article_mission.template.json：博客文章 Mission 模板
- templates/factory_solution_mission.template.json：工厂方案 Mission 模板
- templates/knowledge_page_mission.template.json：知识页 Mission 模板

## Knowledge Binding V1

Website Agent V1 已具备 Knowledge Binding 能力。Knowledge Fetch 不再依赖临时输入，而是从统一 Knowledge Center 读取产品资料绑定。

HK620 样例绑定：

- apps/commander/employees/website_agent_v1/knowledge_binding/hk620.knowledge_binding.v1.json
- knowledge/products/HK620/bindings/website_agent_hk620.knowledge_binding.v1.json

缺失检查清单：

- apps/commander/employees/website_agent_v1/knowledge_binding/product_knowledge_missing_checklist.v1.json

当前 HK620 只允许内部草稿和本地 QA 使用，不是 public approved，不得自动发布或对外执行。
