# M8A V2 Sprint 2: Agent Dispatcher Integration V1 Report

Date: 2026-07-06

## Scope

Agent Dispatcher Integration V1 connects the Agent Dispatcher planning layer into Mission Control.

This sprint keeps M8A V1 Architecture Freeze intact:

- Commander Console CEO Home was not restructured.
- Worker Runner execution model was not changed.
- Exception Framework lifecycle was not changed.
- Approval lifecycle was not changed.
- Mission lifecycle was not changed.
- Task lifecycle was not changed.
- No real Claude, Codex, OpenAI, Gemini, or external platform was connected.
- No real development task was executed.

## Modified Files

- apps/commander/mission-control/mission_control_api.py
- apps/dashboard/index.html
- apps/commander/agent-dispatcher/planner.py

## Added Files

- apps/commander/mission-control/migrations/006_agent_dispatcher_integration_v1.sql
- docs/M8A_V2_SPRINT2_AGENT_DISPATCHER_INTEGRATION_V1_REPORT.md

## Migration

The migration extends `commander_artifacts.artifact_type` to allow:

```text
agent_plan
```

No new database table was added.

## Mission Type Detection

Mission Control now recognizes integration-type commands when input contains:

- 接 API
- 接通 API
- integration
- connector
- 接软件
- 接平台
- Banana API

Detected mission type:

```text
mission_type = integration
```

HK620 USA market commands continue to use the existing HK620 rule planner.

## Integration Runtime

For integration missions, Mission Control calls:

```text
apps/commander/agent-dispatcher/
```

It creates:

1. Mission record.
2. One review task.
3. Agent Plan artifact.
4. CEO approval.

It does not execute real AI, code changes, credentials, deployment, or external platform actions.

## Agent Plan Artifact

Saved as:

```text
artifact_type = agent_plan
```

Content includes:

- mission_type
- selected_agents
- task_sequence
- dependencies
- expected_outputs
- approval_points
- mock_runtime_result
- real_ai_called=false
- external_platform_called=false
- real_code_written=false

## Approval

Created approval:

```text
platform = M8A
action_type = approve_agent_plan
risk_level = medium
status = pending
```

Approval means:

```text
CEO allows the next planning/execution sprint to proceed.
```

Approval does not mean:

```text
Call real AI.
Write code.
Connect API.
Deploy.
Use credentials.
Call external platform.
```

## Dashboard

Commander Console CEO Home was not restructured.

Mission Detail display was extended so Artifacts / Approvals can show:

- Agent Dispatcher Plan
- Selected Agents
- approve_agent_plan approval

## Test 1: Banana API Mission

Input:

```text
帮我接 Banana API
```

Result:

```json
{
  "mission_id": "mission_integration_1783334679293769000",
  "mission_name": "CONNECT_BANANA_API",
  "planner_version": "agent_dispatcher_integration_v1",
  "mission_type": "integration",
  "status": "waiting_approval",
  "artifact_types": ["agent_plan"],
  "selected_agents": [
    "Research Agent",
    "Infrastructure Agent",
    "Code Agent",
    "QA Agent",
    "Commander Review"
  ],
  "approval_actions": ["approve_agent_plan"],
  "real_ai_called": false,
  "external_platform_called": false,
  "real_code_written": false
}
```

Validation:

| Requirement | Result |
| --- | --- |
| Mission created | PASS |
| mission_type = integration | PASS |
| Agent Dispatcher called | PASS |
| agent_plan artifact created | PASS |
| Research Agent selected | PASS |
| Infrastructure Agent selected | PASS |
| Code Agent selected | PASS |
| QA Agent selected | PASS |
| Commander Review included | PASS |
| approve_agent_plan approval created | PASS |
| Real Claude/Codex/OpenAI called | NO |
| External platform connected | NO |
| Real code written | NO |
| Commander Console Home restructured | NO |

## Test 2: HK620 Regression

Input:

```text
今天重点做 HK620，美国市场。
```

Result:

```json
{
  "mission_id": "mission_hk620_us_growth_1783334679889870000",
  "mission_name": "HK620_US_GROWTH",
  "planner_version": "rule_planner_v1",
  "mission_type": null,
  "task_count": 7,
  "task_actions": [
    "read_hk620_product_knowledge",
    "generate_us_market_direction",
    "generate_english_landing_page_structure",
    "simulate_wordpress_draft",
    "generate_social_distribution_drafts",
    "generate_whatsapp_inquiry_reply",
    "generate_mission_summary"
  ]
}
```

Validation:

| Requirement | Result |
| --- | --- |
| Existing HK620 flow used | PASS |
| Not misclassified as integration | PASS |
| 7 original tasks generated | PASS |
| Worker / Website Capability unaffected | PASS |

## Risk Points

1. Integration missions currently create a planning approval only; they do not create executable Worker tasks beyond review.
2. Agent Dispatcher is still mock-only.
3. Provider adapters for Claude, Codex, OpenAI, and Gemini are not connected.
4. Dashboard display is lightweight and only shows Agent Plan summary in Mission Detail.
5. Future execution must continue to route failures into Exception Framework.

## Next Stage Recommendation

V2 Sprint 3 should add an Agent Provider Adapter interface, still in mock mode first:

```text
Agent Dispatcher
  ↓
Provider Adapter
  ↓
Mock Claude / Mock Codex / Mock OpenAI
  ↓
Artifact
  ↓
Approval
  ↓
Exception Framework on failure
```

Do not connect real providers until mock provider contract and approval boundaries pass.

