# Dispatcher

Version: V1  
Status: design initialized  
Date: 2026-07-06

## Function

Dispatcher converts Commander Missions into employee tasks.

```text
Read Commander Mission
↓
Validate protocol fields
↓
Split mission into tasks
↓
Assign target employee
↓
Set task status
↓
Write mission log
↓
Return result to Commander
```

## Target Employees

| Employee | Responsibility |
|---|---|
| Content Operator | Generate content drafts from approved knowledge |
| Knowledge Manager | Check knowledge coverage and review queues |
| Website Operator | Prepare website draft/publish tasks after approval |
| Distribution Operator | Prepare social/video distribution tasks |
| Sales Assistant | Prepare customer reply drafts |
| Business Analyst | Analyze performance, gaps, and priorities |

## Dispatch Rules

1. If task action is content_generation, assign Content Operator.
2. If task action is knowledge_check, assign Knowledge Manager.
3. If task action is website_draft or website_publish_prepare, assign Website Operator.
4. If task action is social_distribution_prepare, assign Distribution Operator.
5. If task action is customer_reply_draft, assign Sales Assistant.
6. If task action is analytics_summary, assign Business Analyst.

## Guardrails

1. Do not connect external platforms from Dispatcher V1.
2. Do not publish without human approval.
3. Do not approve product knowledge automatically.
4. Do not write credentials into mission files.
5. Do not create new agent frameworks.
