# M8A V2 Sprint 4: COTAS Result Intake V1 Report

Date: 2026-07-06

## Scope

COTAS Result Intake V1 lets COTAS/Codex return a structured result to M8A.

The result becomes:

- Artifact
- Task Event
- Approval if required
- QA Review artifact
- Exception Mission if failed or blocked

This sprint does not:

- Connect external APIs.
- Execute real Coze integration.
- Modify Commander Console CEO Home.
- Modify M8A V1 Freeze architecture.
- Store secrets.
- Publish or deploy.

## Modified Files

None of the V1 frozen runtime files were modified.

## Added Files

- apps/commander/agent-dispatcher/providers/cotas_result_intake.py
- apps/commander/agent-dispatcher/providers/COTAS_RESULT.json
- apps/commander/agent-dispatcher/providers/COTAS_RESULT_EXAMPLE.json
- docs/M8A_V2_SPRINT4_COTAS_RESULT_INTAKE_V1_REPORT.md

## COTAS_RESULT.json Standard

Required format:

```json
{
  "mission_id": "",
  "task_id": "",
  "agent_name": "COTAS Integration Agent",
  "status": "completed | failed | blocked",
  "summary": "",
  "modified_files": [],
  "new_files": [],
  "test_results": [],
  "risks": [],
  "next_steps": [],
  "requires_approval": true,
  "approval_reason": "",
  "artifacts": []
}
```

Rules:

- `mission_id` and `task_id` must reference existing Mission Control records.
- `agent_name` must be `COTAS Integration Agent`.
- `status` must be `completed`, `failed`, or `blocked`.
- No real secret values may be included.
- External API calls remain prohibited in V1.

## Result Intake Module

Module:

```text
apps/commander/agent-dispatcher/providers/cotas_result_intake.py
```

Responsibilities:

1. Read COTAS_RESULT.json.
2. Validate required fields and types.
3. Confirm referenced Mission/Task exists.
4. Save COTAS result as Artifact.
5. Write `cotas_result_received` task event.
6. If status is completed, mark referenced task completed.
7. If status is failed or blocked, call Exception Framework.
8. If `requires_approval=true`, create approval.
9. Create QA Agent Review Required artifact.

## Artifacts

Result artifact:

```text
artifact_type = json
title = COTAS Result
created_by = cotas_result_intake_v1
```

QA artifact:

```text
artifact_type = report
title = QA Agent Review Required
simulation_status = qa_review_required
```

## Approval

If approval is required:

```text
platform = M8A
action_type = approve_cotas_result
risk_level = medium
status = pending
```

Approval means:

```text
CEO allows the next controlled M8A step.
```

Approval does not mean:

```text
Call Coze API.
Deploy.
Publish.
Store credentials.
Modify production systems.
```

## Exception

If COTAS result is:

```text
failed
blocked
```

The module calls:

```text
create_exception_from_failure()
```

This creates an Exception Mission and routes the issue to Infrastructure Operator / Exception Framework.

## Example Result File

Example:

```text
apps/commander/agent-dispatcher/providers/COTAS_RESULT_EXAMPLE.json
```

Scenario:

```text
帮我接 Coze API 到 M8A
```

The example is mock-only. It does not connect Coze.

## Test 1: Completed Result Intake

Test file:

```text
/private/tmp/COTAS_RESULT_TEST_COMPLETED.json
```

Referenced Mission:

```text
mission_integration_1783336842051190000
```

Referenced Task:

```text
mission_integration_1783336842051190000_task_001
```

Observed:

| Requirement | Result |
| --- | --- |
| Format validation | PASS |
| COTAS result artifact written | PASS |
| cotas_result_received event written | PASS |
| completed status updated task | PASS |
| Approval created | PASS |
| QA Review artifact created | PASS |
| External platform connected | NO |
| Real Coze API executed | NO |
| Commander Console Home modified | NO |

Created records:

```text
result_artifact: artifact_cotas_1783337207599282000
qa_review_artifact: artifact_cotas_1783337208126801000
approval: approval_cotas_1783337207958045000
task_status: completed
```

## Test 2: Blocked Result Intake

Test file:

```text
/private/tmp/COTAS_RESULT_TEST_BLOCKED.json
```

Observed:

| Requirement | Result |
| --- | --- |
| blocked status accepted | PASS |
| Exception Framework called | PASS |
| Exception Mission created | PASS |
| Approval created | PASS |
| QA Review artifact created | PASS |

Created exception:

```text
exception_1783337225696277000
```

## QA Agent Entry

The QA Agent entry is currently represented as:

```text
QA Agent Review Required artifact
```

It contains:

- COTAS output summary
- modified_files
- new_files
- test_results
- risks
- next_steps
- QA question
- recommendation_required=true

## Risk Points

1. Result intake trusts a local JSON file; future API mode needs authentication and signature validation.
2. A result can mark a task completed only if mission_id/task_id are valid.
3. QA Agent review is an artifact in V1, not a separate queued QA task.
4. Duplicate intake of the same file can create duplicate artifacts; V2 should add idempotency key.
5. Manual handoff remains human-operated.

## Next Step: QA Agent

Recommended next sprint:

```text
COTAS Result
  ↓
QA Agent Review Task
  ↓
QA Acceptance Report
  ↓
CEO Approval
  ↓
Next Implementation Mission
```

Implementation notes:

1. Add a QA review action type.
2. Convert QA Review artifact into a queued QA task.
3. Add idempotency for COTAS result intake.
4. Keep all failures routed to Exception Framework.

