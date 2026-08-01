# M8A Report Index

Purpose: let Commander know which Missions have been completed, where the reports are, which branch/commit they belong to, and whether CEO Review is still required.

Machine-readable index:

```text
docs/M8A_REPORT_INDEX.json
```

## Update Rule

Every completed Mission must write a record into the report index.

Each record must include:

```text
Mission ID
Mission Name
Module
Branch
Commit
Report Path
Status
Tests
CEO Review Status
Next Action
```

## Safety Rule

The report index must never contain:

```text
.env values
API keys
tokens
passwords
Application Passwords
secrets
private customer data
```

## Current Review Queue

| Mission | Branch | Commit | Status | Report |
|---|---|---:|---|---|
| Recruiting Center V1 | `sprint/recruiting-center-v1` | `ceee9a0` | Waiting CEO Review | `docs/M8A_RECRUITMENT_CENTER_V1_REPORT.md` |
| AI Employee Center V1 | `sprint/ai-employee-center-v1` | `277db5a` | Waiting CEO Review | `docs/M8A_AI_EMPLOYEE_CENTER_V1_REPORT.md` |
| AI Employee Center V2 | `sprint/ai-employee-center-v2` | `daff7f4` | Waiting CEO Review | `docs/M8A_AI_EMPLOYEE_CENTER_V2_REPORT.md` |
| Commander Runtime V1 | `sprint/commander-runtime-v1` | `a62edad` | Waiting CEO Review | `docs/M8A_COMMANDER_RUNTIME_V1_REPORT.md` |
| Unified Report Index V1 | `sprint/report-index-v1` | `pending` | Waiting CEO Review | `docs/M8A_REPORT_INDEX_V1_REPORT.md` |
| CEO Review Merge Plan V1 | `sprint/report-index-v1` | `pending` | Waiting CEO Review | `docs/M8A_CEO_REVIEW_MERGE_PLAN_V1.md` |

## Merged Governance Records

| Mission | Status | Report |
|---|---|---|
| Git Safety Baseline V1 | Merged | `docs/M8A_GIT_SAFETY_BASELINE_V1_REPORT.md` |
| AI Change Control Policy | Merged | `docs/M8A_AI_CHANGE_CONTROL_POLICY.md` |
| Coze Provider Mock V1 | Merged | `docs/M8A_V2_SPRINT7_COZE_PROVIDER_MOCK_V1_REPORT.md` |
| Coze Staging Config Check | Merged | `docs/M8A_V2_SPRINT8_COZE_STAGING_CONFIG_CHECK_REPORT.md` |

## Commander Usage

Commander can read `docs/M8A_REPORT_INDEX.json` to answer:

- what has been completed
- what is waiting for CEO Review
- which branch should be reviewed next
- which report explains the work
- whether tests passed
- what the next action is

## Next Improvement

Connect Commander Runtime so every future run appends or updates a record automatically.

## Today's M8N Completion Records

| Mission | Owner | Status | Report |
|---|---|---|---|
| Commander Runtime V2 Local Scheduling Bridge | Research Agent | Completed | `docs/M8A_COMMANDER_RUNTIME_V2_REPORT.md` |
| M8N Commander Console Runtime Data Connection | Website Agent | Completed | `apps/dashboard/index.html` |
| AI Employee Workbench V1 | Website Agent | Completed | `docs/M8N_AI_EMPLOYEE_WORKBENCH_V1_REPORT.md` |
| Platform Connector Console V1 | Website Agent | Completed | `docs/M8N_PLATFORM_CONNECTOR_CONSOLE_V1_REPORT.md` |
| AI Employee Registry V2 Missing Roles | Knowledge Agent | Completed | `docs/M8N_AI_EMPLOYEE_REGISTRY_V2_REPORT.md` |
| M8N Daily General Manager Brief V1 | Research Agent | Completed | `docs/M8N_TODAY_GENERAL_MANAGER_REPORT.md` |
| M8N CEO Review List V1 | Commander Reporting Agent | Completed | `docs/M8N_CEO_REVIEW_LIST_V1.md` |
| M8N Manager Directive Execution | Commander Reporting Agent | Completed | `docs/M8N_MANAGER_DIRECTIVE_EXECUTION_REPORT.md` |
| Worker Runner Local Integration V1 | Automation Agent | Completed | `docs/M8N_WORKER_RUNNER_LOCAL_INTEGRATION_V1_REPORT.md` |
| n8n 本地接入 | Automation Agent | Completed | `docs/M8N_N8N_LOCAL_CONNECTION_V1_REPORT.md` |
| n8n 工作流绑定 AI 员工 | Automation Agent | Completed | `docs/M8N_N8N_WORKFLOW_BINDING_V1_REPORT.md` |
| 外部平台 API 接入准备 | Automation Agent | Waiting Credentials | `docs/M8N_EXTERNAL_API_CONNECTION_READINESS_V1_REPORT.md` |
| M8A 组织架构 V1.0 冻结落地 | Commander Reporting Agent | Completed | `docs/M8A_ORGANIZATION_ARCHITECTURE_V1_0.md` |
| 今日外部平台授权收尾 | Automation Agent | Waiting CEO Browser Authorization | `docs/M8A_PLATFORM_AUTHORIZATION_TODAY_V1.md` |
- wordpress_draft_creation_test_v1：WordPress 草稿创建实测，结果 blocked，报告 docs/M8A_WORDPRESS_DRAFT_CREATION_TEST_V1.md。
- external_execution_n8n_only_policy_v1：外部平台统一 n8n 执行路线政策，状态 completed，报告 docs/M8A_EXTERNAL_EXECUTION_N8N_ONLY_POLICY_V1.md。
- wordpress_n8n_auth_diagnosis_v1：WordPress n8n 授权失败诊断，状态 blocked，报告 docs/M8A_WORDPRESS_N8N_AUTH_DIAGNOSIS_V1.md。
- wordpress_draft_verification_v1：WordPress Draft 验证成功，状态 completed，报告 docs/M8A_WORDPRESS_DRAFT_VERIFICATION_REPORT_V1.md。
- website_agent_hk620_first_business_draft_v1：Website Agent 首次真实业务 WordPress Draft，状态 completed，报告 docs/M8A_HK620_WEBSITE_AGENT_EXECUTION_REPORT_V1.md。
- qa_agent_hk620_wordpress_draft_review_v1：QA Agent HK620 Draft 检查，状态 completed，报告 docs/M8A_HK620_QA_CHECK_REPORT_V1.md。
| M8A Pending Work Audit V1 | Commander Reporting Agent | Completed | `docs/M8A_PENDING_WORK_AUDIT_V1_REPORT.md` |
| WordPress Draft 正文桥接修复 V1 | Website Agent / Publishing Center | Completed Local Bridge Fix | `docs/M8A_WORDPRESS_DRAFT_CONTENT_HTML_BRIDGE_FIX_V1_REPORT.md` |
| 平台授权收尾任务关闭 V1 | Automation Agent / Mission Center | Completed | `docs/M8A_PLATFORM_AUTHORIZATION_CLOSURE_V1_REPORT.md` |
| Publishing Employee 设计 V1 | Publishing Agent / Publishing Center | Completed Design | `docs/M8A_PUBLISHING_EMPLOYEE_DESIGN_V1.md` |
| WordPress Draft 正文完整性验证 V1 | Website Agent / Publishing Center | Completed | `docs/M8A_WORDPRESS_DRAFT_BODY_COMPLETENESS_VERIFICATION_V1_REPORT.md` |
| HK620 产品视频缺口 gap_003 补齐 V1 | Content Center / Knowledge Center | Completed | `docs/M8A_HK620_PRODUCT_VIDEO_GAP_003_COMPLETION_REPORT.md` |
