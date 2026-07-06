# M8A V2 Sprint 5: QA Agent Review Task V1 Report

Date: 2026-07-06

## Scope

QA Agent Review Task V1 upgrades the COTAS Result Intake QA Review artifact into a formal queued QA Agent task.

This sprint does not:

- Connect real Coze API.
- Connect external platforms.
- Modify Commander Console CEO Home.
- Break M8A V1 Freeze architecture.
- Publish, deploy, or store credentials.

## Modified Files

- apps/commander/agent-dispatcher/providers/cotas_result_intake.py
- apps/commander/mission-control/worker_runner.py

## Added Files

- apps/commander/mission-control/migrations/007_qa_agent_review_task_v1.sql
- apps/commander/agent-dispatcher/providers/QA_RESULT_EXAMPLE.json
- docs/M8A_V2_SPRINT5_QA_AGENT_REVIEW_TASK_V1_REPORT.md

## Migration

Migration:

```text
apps/commander/mission-control/migrations/007_qa_agent_review_task_v1.sql
```

It:

1. Extends `commander_artifacts.artifact_type` to include:

```text
qa_review_result
```

2. Registers `QA Agent` in `commander_workers`.

No new table was added.

## QA Task Creation

When COTAS Result Intake receives:

```text
status = completed
```

it now creates a new `commander_tasks` record:

```text
worker_name = QA Agent
action = qa_review_cotas_result
status = queued
```

The task input includes:

- mission_id
- original_cotas_task_id
- cotas_result_artifact_id
- modified_files
- new_files
- test_results
- risks
- next_steps
- summary
- artifacts

## QA Agent Mock Handler

Worker Runner now supports:

```text
qa_review_cotas_result
```

V1 is rule-based only. It does not call a real AI provider.

Checks:

1. COTAS result artifact and summary are present.
2. modified_files / new_files exist.
3. test_results exist.
4. risks are explicit.
5. next_steps are explicit.
6. No forbidden action is reported.
7. No secret-like value is present.
8. No external platform was modified.
9. The result declares mock/no external connection.

## QA_RESULT.json

Example file:

```text
apps/commander/agent-dispatcher/providers/QA_RESULT_EXAMPLE.json
```

Schema:

```json
{
  "qa_status": "passed | failed | needs_human_review",
  "summary": "",
  "checks": [],
  "risks": [],
  "recommendation": "",
  "requires_ceo_approval": true
}
```

## Artifact

QA completion saves:

```text
artifact_type = qa_review_result
title = QA_RESULT
simulation_status = qa_review_completed
```

## Approval

If `requires_ceo_approval=true`, Worker Runner creates:

```text
platform = M8A
action_type = approve_qa_result
risk_level = medium
status = pending
```

Approval means CEO allows the next controlled step. It does not execute real Coze, deploy, publish, or use credentials.

## Exception

Severe QA issues raise an error and route through Worker Runner into Exception Framework.

Severe examples:

- forbidden action
- secret leaked
- external platform modified
- missing test evidence

## Test 1: Completed COTAS Result Creates QA Task

Input:

```text
COTAS completed result for "帮我接 Coze API 到 M8A"
```

Observed:

```json
{
  "qa_task_initial_status": "queued"
}
```

Result:

```text
QA Agent task created successfully.
```

## Test 2: QA Agent Handler Executes

Mission:

```text
mission_integration_1783337681312752000
```

QA task:

```text
mission_integration_1783337681312752000_qa_002_1783337682781290000
```

Observed:

```json
{
  "runner_message": "Task executed locally.",
  "qa_task_final_status": "waiting_approval",
  "qa_artifact_types": [
    "qa_review_result"
  ],
  "qa_action_types": [
    "approve_qa_result"
  ],
  "qa_result_status": "passed",
  "check_count": 9
}
```

Validation:

| Requirement | Result |
| --- | --- |
| QA task status queued | PASS |
| QA Agent handler executes | PASS |
| QA_RESULT artifact created | PASS |
| QA checks complete | PASS |
| approve_qa_result approval created | PASS |
| COTAS original result preserved | PASS |
| Commander Console Home unchanged | PASS |
| External platform connected | NO |
| Real Coze API executed | NO |

## Test 3: Severe Issue Routes to Exception Framework

Severe test:

```text
Secret-like value in COTAS result summary.
```

Observed:

```json
{
  "mission_id": "mission_integration_1783337758830896000",
  "qa_task_id": "mission_integration_1783337758830896000_qa_002_1783337760240849000",
  "runner_error": "QA Agent found severe COTAS result issue",
  "qa_task_status": "failed",
  "exception_count": 1
}
```

Validation:

| Requirement | Result |
| --- | --- |
| Severe issue detected | PASS |
| QA task failed | PASS |
| Exception Framework called | PASS |
| Exception Mission created | PASS |

## Risk Points

1. QA Agent V1 uses local rules only, not a real AI provider.
2. Duplicate COTAS intake can create multiple QA tasks.
3. QA task idempotency should be added in V2.
4. Secret detection uses simple keyword rules.
5. A future AI QA provider must still route failures to Exception Framework.

## Next Step: Real AI Provider QA

Recommended next sprint:

```text
QA Agent Review Task
  ↓
QA Provider Adapter
  ↓
Mock AI QA
  ↓
Human approval
  ↓
Real AI provider only after approval
```

Provider requirements:

1. Structured input only.
2. No secrets in prompt.
3. No external platform calls.
4. Output as QA_RESULT.
5. Severe issues route to Exception Framework.
6. CEO approval before implementation proceeds.

