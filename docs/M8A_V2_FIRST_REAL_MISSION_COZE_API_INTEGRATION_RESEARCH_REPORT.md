# M8A V2 First Real Mission: Coze API Integration Research & Design

Date: 2026-07-06

## Mission

Mission:

```text
Coze API Integration Research
```

Mission ID:

```text
mission_integration_1783337975814152000
```

Original COTAS task:

```text
mission_integration_1783337975814152000_task_001
```

## Scope

This mission validates the full M8A loop:

```text
CEO target
  ↓
Agent Dispatcher
  ↓
COTAS/Codex execution package
  ↓
COTAS_RESULT.json
  ↓
Result Intake
  ↓
QA Agent queued task
  ↓
QA_RESULT artifact
  ↓
CEO Approval
```

This mission did not:

- Call real Coze API.
- Connect external platforms.
- Save credentials.
- Modify Commander Console CEO Home.
- Break M8A V1 Freeze architecture.
- Write production Coze adapter code.

## Sources Reviewed

Official Coze documentation pages reviewed for research:

- https://www.coze.com/open/docs/developer_guides/coze_api_overview
- https://www.coze.com/open/docs/developer_guides/authentication
- https://www.coze.com/open/docs/developer_guides/pat
- https://www.coze.com/open/docs/developer_guides/oauth_jwt
- https://www.coze.com/open/docs/developer_guides/workflow_run

## Agent Plan Summary

Selected agents:

```text
Research Agent
↓
Infrastructure Agent
↓
COTAS Integration Agent
↓
QA Agent
↓
Commander Review
```

Agent Plan artifact:

```text
artifact_agent_plan_1783337976108510000
```

## COTAS Execution Package

Path:

```text
apps/commander/agent-dispatcher/providers/COTAS_EXECUTION_PACKAGE.md
```

Absolute path:

```text
/Users/shiqiujing/Documents/M8A/apps/commander/agent-dispatcher/providers/COTAS_EXECUTION_PACKAGE.md
```

The package defined COTAS/Codex as an execution agent only. It does not allow COTAS to become Commander or bypass Mission Control, Approval, or Exception Framework.

## COTAS_RESULT.json

Path:

```text
apps/commander/agent-dispatcher/providers/COTAS_RESULT.json
```

Absolute path:

```text
/Users/shiqiujing/Documents/M8A/apps/commander/agent-dispatcher/providers/COTAS_RESULT.json
```

COTAS_RESULT status:

```text
completed
```

COTAS result artifact:

```text
artifact_cotas_1783338031370586000
```

Result summary:

```text
COTAS/Codex completed Coze API integration research and designed Coze Agent Provider Adapter V1 for M8A. This is research and architecture design only. No real Coze API was called, no external platform connection was made, no production code was written, and no secrets were saved.
```

## Coze API Integration Research

### Coze API 接入方式

Coze should be evaluated as an Agent Provider behind M8A Agent Dispatcher.

Recommended integration modes:

1. Mock-first provider adapter inside M8A.
2. Manual credential preparation after CEO approval.
3. Future controlled API call through provider adapter only.
4. Workflow execution result returned as M8A Artifact.

### 认证方式

Research notes:

- Personal Access Token can be evaluated for controlled server-side testing after approval.
- OAuth / JWT style authorization should be evaluated for production-grade app integration after security review.

M8A policy:

- Credentials must come from secure environment/config only.
- Credential values must never be written to code, prompts, logs, artifacts, or reports.
- Approval is required before any real credential is used.
- Credential failure must route to Exception Framework.

### 可用能力

Candidate capabilities:

- Run Coze workflow from M8A task input.
- Receive workflow result as structured JSON.
- Convert workflow result into M8A Artifact.
- Create Approval if result is public, customer-facing, or external-action related.
- Route failure into Exception Framework.

Not allowed in V1:

- Direct publishing.
- Direct customer reply.
- Direct database mutation outside Mission Control.
- Direct production workflow execution.

### 限制与风险

Main risks:

1. Coze authentication must be confirmed before live use.
2. Workflow output schemas may differ by workflow design.
3. Rate limits, timeout behavior, workspace permissions, and bot/workflow publishing state must be verified.
4. Coze-generated content or tool actions must not bypass M8A Approval.
5. API failure, authentication failure, timeout, or schema mismatch must enter Exception Framework.

### Coze 在 M8A 中的定位

Coze should be positioned as:

```text
Agent Provider / Workflow Provider
```

Coze should not be:

```text
Commander
Mission Control
Approval authority
Direct publisher
Direct database writer
```

## Coze Agent Provider Adapter V1 Design

Proposed module:

```text
apps/commander/agent-dispatcher/providers/coze_provider_adapter_v1.py
```

Mode:

```text
mock_first
```

Input contract:

```json
{
  "mission_id": "string",
  "task_id": "string",
  "agent_name": "string",
  "workflow_name": "string",
  "input_json": {},
  "approval_context": {}
}
```

Output contract:

```json
{
  "provider": "coze",
  "mode": "mock | staging | production",
  "status": "completed | failed | blocked",
  "result_json": {},
  "artifact_type": "json",
  "requires_approval": true,
  "exception": null
}
```

Runtime flow:

```text
Agent Dispatcher selects Coze Provider Adapter
  ↓
Worker Runner calls provider adapter task
  ↓
Adapter validates input schema
  ↓
Adapter runs mock response in V1
  ↓
Adapter saves Artifact
  ↓
Adapter creates Approval when needed
  ↓
Adapter routes failure to Exception Framework
```

## QA Result

QA task:

```text
mission_integration_1783337975814152000_qa_002_1783338032203649000
```

QA task final status:

```text
waiting_approval
```

QA_RESULT artifact:

```text
artifact_1783338132064846000
```

QA status:

```text
passed
```

QA checks:

```text
9
```

QA approval:

```text
approval_1783338132284260000
```

Approval action:

```text
approve_qa_result
```

## Task Events

Mission task event count after QA:

```text
22
```

Important events:

- Mission created.
- Agent Plan artifact created.
- COTAS result received.
- QA review required.
- QA Agent task queued.
- QA task claimed.
- QA_RESULT artifact created.
- approve_qa_result approval created.

Exception path was also verified during QA rule tuning. A false-positive QA failure entered Exception Framework, then QA rule was corrected and the task was re-run successfully.

## Acceptance Results

| Requirement | Result |
| --- | --- |
| Mission created | PASS |
| Agent Plan created | PASS |
| COTAS Execution Package created | PASS |
| COTAS_RESULT.json intake completed | PASS |
| QA Agent task created | PASS |
| QA_RESULT artifact created | PASS |
| approve_qa_result approval created | PASS |
| No real Coze API connection | PASS |
| No secrets saved | PASS |
| Commander Console Home unchanged | PASS |
| Task events recorded | PASS |
| Failure path enters Exception Framework | PASS |

## Recommendation

Should M8A enter Coze Provider Adapter V1 development?

```text
YES
```

Reason:

Coze appears suitable as a controlled Agent Provider candidate for M8A if implemented behind Mission Control, Worker Runner, Approval, and Exception Framework.

Recommended first development scope:

1. Create `coze_provider_adapter_v1.py` in mock mode.
2. Define strict input/output schemas.
3. Add tests for schema validation, timeout, authentication failure, blocked result, and exception routing.
4. Add credential placeholders only; do not store real credentials.
5. Do not call real Coze API until CEO approves staging verification.

