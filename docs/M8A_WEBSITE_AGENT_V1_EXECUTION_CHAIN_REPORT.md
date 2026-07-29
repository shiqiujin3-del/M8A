# Website Agent V1 可复用执行链报告

日期：2026-07-09

## 结论

Website Agent V1 已从“已上岗员工”推进到“具备可复用执行链”的正式员工。

以后 HK690、HK680、六面钻、CNC、Factory Solution、Blog、Knowledge 不需要重新开发流程，只需要替换产品资料、市场资料和内容任务输入。

本次任务属于 A 类 Build，本地建设任务，不需要 CEO 审批。未调用 n8n，未调用 WordPress，未发布、未删除、未修改任何外部平台。

## 标准执行链

Website Agent Execution Chain V1：

1. Mission Intake
2. Knowledge Fetch
3. Draft Generation
4. SEO Enrichment
5. QA V2 Scoring
6. Approval Gate
7. Draft-only Handoff
8. Mission Log Writeback

## 可自动推进步骤

以下步骤属于本地 Build / 本地验证，可自动推进，无需 CEO 审批：

- Mission Intake
- Knowledge Fetch
- Draft Generation
- SEO Enrichment
- QA V2 Scoring
- Mission Log Writeback

## 必须 CEO 审批步骤

以下步骤必须 CEO 审批或单独授权：

- Approval Gate
- Draft-only Handoff
- 任何真实 n8n 调用
- 任何真实 WordPress 调用
- 发布、删除、修改已发布文章
- Gmail / YouTube 等外部平台动作

## 状态机

Website Agent V1 状态机：

- idle
- intake_received
- knowledge_loaded
- draft_generated
- qa_completed
- waiting_approval
- approved_for_draft
- handed_off_to_n8n
- completed
- failed

状态转换规则已写入：`apps/commander/employees/website_agent_v1/state_machine/website_agent_state_machine.v1.json`

## 新增模板

- `product_content_mission.template.json`：产品内容 Mission 模板
- `blog_article_mission.template.json`：博客文章 Mission 模板
- `factory_solution_mission.template.json`：工厂方案 Mission 模板
- `knowledge_page_mission.template.json`：知识页 Mission 模板

## Dashboard 映射

每个状态如何显示到总控台和员工工作台，已写入：

`apps/commander/employees/website_agent_v1/dashboard/website_agent_state_dashboard_mapping.v1.json`

总控台现在显示 Website Agent V1 已具备可复用执行链。

员工工作台现在显示执行链、状态机、CEO Gate 和可复用模板。

## 复用规则

新增产品或内容类型时，只替换：

- product_profile
- market_profile
- content_brief
- approved_facts
- forbidden_claims
- SEO keywords
- CTA direction

不得重做 Mission Intake、Draft Generation、QA V2、Approval Gate、Draft-only Handoff、Mission Log Writeback 流程。

## 安全边界

本次只做本地文件、规则、模板和页面数据接入。

未执行：

- n8n
- WordPress
- publish
- update_published_post
- delete_post
- send_gmail
- upload_youtube

## 验证方式

1. 打开 `apps/dashboard/index.html`，查看 Website Agent V1 员工状态，确认显示“具备可复用执行链”。
2. 打开 `apps/dashboard/employee_workbench.html`，查看 Website Agent V1 正式员工区，确认显示 Execution Chain V1、状态机、可复用模板。
3. 检查四个模板 JSON 是否存在并可解析。
4. 检查 `website_agent_state_machine.v1.json` 是否包含 10 个状态和 CEO Gate 规则。
5. 确认页面没有触发 n8n / WordPress 外部动作。
