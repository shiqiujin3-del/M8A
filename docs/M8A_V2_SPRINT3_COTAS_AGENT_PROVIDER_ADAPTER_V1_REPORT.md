# M8A V2 Sprint 3: COTAS Agent Provider Adapter V1 Report

Date: 2026-07-06

## Scope

COTAS Agent Provider Adapter V1 defines COTAS as M8A's first real AI employee handoff path.

Important clarification:

```text
COTAS = Codex
```

In M8A, COTAS/Codex is an execution agent. It is not Commander.

This sprint does not:

- Call real COTAS/Codex API.
- Call Claude.
- Call OpenAI directly.
- Call Gemini.
- Connect Coze API.
- Connect any external platform.
- Modify production systems.
- Store credentials.
- Bypass Mission Control.
- Bypass Approval.
- Bypass Exception Framework.
- Modify Commander Console CEO Home.
- Modify M8A V1 lifecycle rules.

## Modified Files

- apps/commander/agent-dispatcher/registry.py
- apps/commander/agent-dispatcher/router.py
- apps/commander/agent-dispatcher/planner.py
- apps/commander/agent-dispatcher/dispatcher.py
- apps/commander/mission-control/mission_control_api.py

## Added Files

- apps/commander/agent-dispatcher/providers/cotas_provider.py
- apps/commander/agent-dispatcher/providers/COTAS_EXECUTION_PACKAGE.md
- docs/M8A_V2_SPRINT3_COTAS_AGENT_PROVIDER_ADAPTER_V1_REPORT.md

## Agent Definition

New Agent:

```text
name: COTAS Integration Agent
role: API / Connector / Adapter Development Agent powered by Codex/COTAS manual handoff
```

Responsibilities:

1. Research third-party API.
2. Design Connector.
3. Design Adapter implementation.
4. Draft test scripts.
5. Draft test report.
6. Return result as M8A Artifact.
7. Route failures into Exception Framework.

Forbidden:

1. Direct publishing.
2. Direct production website modification.
3. Saving secrets.
4. Bypassing CEO Approval.
5. Bypassing Mission Control.
6. Bypassing Exception Framework.
7. Deploying without approval.

## Provider Adapter

Provider file:

```text
apps/commander/agent-dispatcher/providers/cotas_provider.py
```

V1 mode:

```text
manual_handoff
```

Meaning:

M8A generates a standard task package for COTAS/Codex. A human can copy the package to COTAS/Codex for execution. No automatic external AI call happens in V1.

## COTAS Execution Package

Generated file:

```text
apps/commander/agent-dispatcher/providers/COTAS_EXECUTION_PACKAGE.md
```

Package sections:

- Mission
- Task
- Context
- Allowed Actions
- Forbidden Actions
- Expected Output
- Acceptance Criteria
- Security Rules
- Return Format

Example return format:

```json
{
  "agent": "COTAS Integration Agent",
  "status": "completed | blocked | failed",
  "integration_plan": {},
  "required_credentials": [],
  "api_endpoints": [],
  "adapter_design": {},
  "test_plan": [],
  "risk_points": [],
  "approval_points": [],
  "next_steps": [],
  "exception": null
}
```

## Agent Dispatcher Integration

For integration-type missions, Agent Dispatcher now selects:

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

Mission types include:

- integration
- connector
- API 接入
- 端口接入
- workflow 接入
- platform adapter

## Coze API Mission Test

Input:

```text
帮我接 Coze API 到 M8A
```

Observed result:

```json
{
  "mission_id": "mission_integration_1783336842051190000",
  "mission_name": "INTEGRATION_MISSION",
  "planner_version": "agent_dispatcher_integration_v1",
  "mission_type": "integration",
  "status": "waiting_approval",
  "artifact_type": "agent_plan",
  "selected_agents": [
    "Research Agent",
    "Infrastructure Agent",
    "COTAS Integration Agent",
    "QA Agent",
    "Commander Review"
  ],
  "cotas_package_path": "/Users/shiqiujing/Documents/M8A/apps/commander/agent-dispatcher/providers/COTAS_EXECUTION_PACKAGE.md",
  "cotas_api_called": false,
  "approval_actions": [
    "approve_agent_plan"
  ],
  "real_ai_called": false,
  "external_platform_called": false,
  "real_code_written": false
}
```

Validation:

| Requirement | Result |
| --- | --- |
| Mission created | PASS |
| Agent Plan generated | PASS |
| COTAS Integration Agent selected | PASS |
| COTAS_EXECUTION_PACKAGE.md generated | PASS |
| approve_agent_plan approval created | PASS |
| Real external API called | NO |
| Production system modified | NO |
| Secrets stored | NO |
| Approval bypassed | NO |
| Exception Framework bypassed | NO |
| Commander Console Home modified | NO |

## Risk Points

1. Manual handoff depends on human copy/paste discipline.
2. COTAS/Codex output must be reviewed before being applied.
3. Credentials must never be included in execution package.
4. Automatic COTAS/Codex API execution is not implemented yet.
5. Future API execution must be approval-gated and exception-routed.

## Upgrade Path: Manual Handoff to API Call

Next stage should introduce a provider contract:

```text
run_provider_task(agent, execution_package) -> provider_result
```

Required safety controls before API mode:

1. CEO approval for real COTAS/Codex execution.
2. Provider token stored only in secure environment config.
3. No secrets in prompts, logs, artifacts, or reports.
4. Execution result returned as Artifact.
5. Code changes require separate review.
6. Any provider failure routes to Exception Framework.
7. No direct production deployment.

Recommended sequence:

```text
Manual Handoff
→ Mock API Provider
→ Local sandbox execution
→ Human review
→ Controlled Codex/COTAS API execution
→ Approval-gated implementation
```

