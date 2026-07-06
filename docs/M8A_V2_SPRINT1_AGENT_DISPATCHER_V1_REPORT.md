# M8A V2 Sprint 1: Agent Dispatcher V1 Report

Date: 2026-07-06

## Scope

M8A V2 Sprint 1 establishes Agent Dispatcher Runtime V1.

V1 Architecture Freeze was respected:

- Commander Console was not modified.
- Mission Control was not modified.
- Worker Runner was not modified.
- Exception Framework was not modified.
- Approval was not modified.
- Mission lifecycle was not modified.
- Task lifecycle was not modified.

This sprint does not call Claude, Codex, ChatGPT, OpenAI, Gemini, or any external platform.

## Architecture

```text
Commander
  ↓
Agent Dispatcher
  ↓
Agent Registry
  ↓
Router
  ↓
Planner
  ↓
Mock Agent Runtime
  ↓
Agent Execution Plan
  ↓
Commander Review
```

## Files Added

- apps/commander/agent-dispatcher/registry.py
- apps/commander/agent-dispatcher/router.py
- apps/commander/agent-dispatcher/planner.py
- apps/commander/agent-dispatcher/dispatcher.py
- apps/commander/agent-dispatcher/agent_runtime.py
- apps/commander/agent-dispatcher/demo_banana_api.py
- docs/M8A_V2_SPRINT1_AGENT_DISPATCHER_V1_REPORT.md

## Agent Registry

Registered mock Agents:

| Agent | Role |
| --- | --- |
| Research Agent | Researches API docs, platform constraints, and integration risks |
| Code Agent | Plans implementation and test tasks |
| QA Agent | Reviews safety, acceptance criteria, and regressions |
| Website Agent | Plans website-side draft and content operations |
| Infrastructure Agent | Plans credentials, API auth, DNS, webhooks, and security |
| Business Analyst Agent | Maps business goal, ROI, and CEO summary |
| Content Agent | Plans content assets and messaging |

Each Agent includes:

- name
- role
- capabilities
- priority
- estimated_runtime
- cost
- approval_policy
- exception_policy
- status

## Router

Router input:

```text
Mission
```

Router output:

```text
Agent Execution Route
```

For:

```text
帮我接 Banana API
```

Router selected:

```text
Research Agent
↓
Infrastructure Agent
↓
Code Agent
↓
QA Agent
```

Reason:

```text
Mission asks to connect Banana API, so the safest route is research,
infrastructure/auth planning, implementation planning, and QA review.
```

## Planner

Planner generates:

- Agent Plan
- Task Sequence
- Dependencies
- Expected Outputs
- Approval Points

Banana API plan:

| Step | Agent | Task | Depends On |
| --- | --- | --- | --- |
| 1 | Research Agent | Research Banana API requirements | None |
| 2 | Infrastructure Agent | Plan Banana API credentials and network access | Research Agent |
| 3 | Code Agent | Plan Banana API connector implementation | Infrastructure Agent |
| 4 | QA Agent | Validate Banana API integration plan | Code Agent |

## Dispatcher Runtime

Dispatcher responsibilities:

1. Select Agent.
2. Arrange execution order.
3. Produce plan.
4. Collect mock result.
5. Return plan to Commander.
6. Document Exception Framework policy for future runtime failures.

Dispatcher V1 does not execute real tasks.

## Mock Agent Runtime

All Agent output is mock:

```json
{
  "external_ai_called": false,
  "external_platform_called": false
}
```

## Banana API Demo Mission

Demo command:

```text
帮我接 Banana API
```

Demo file:

```text
apps/commander/agent-dispatcher/demo_banana_api.py
```

Observed result:

| Check | Result |
| --- | --- |
| Mission accepted | PASS |
| Agent Plan generated | PASS |
| Research Agent selected | PASS |
| Infrastructure Agent selected | PASS |
| Code Agent selected | PASS |
| QA Agent selected | PASS |
| Execution order generated | PASS |
| Dependencies generated | PASS |
| Approval points generated | PASS |
| Final plan generated | PASS |
| Real Claude call | NO |
| Real Codex call | NO |
| Real ChatGPT/OpenAI call | NO |
| Real Gemini call | NO |
| External platform connection | NO |

## Next Stage: Real AI Provider Design

### Claude

Recommended role:

- Research Agent
- Business Analyst Agent
- Content Agent

Integration rule:

```text
Agent Dispatcher
→ Provider Adapter
→ Claude
→ Artifact
→ Approval if public/customer-facing
→ Exception Framework on failure
```

### Codex

Recommended role:

- Code Agent
- QA Agent

Integration rule:

```text
Agent Dispatcher
→ Codex Adapter
→ Local coding plan / patch proposal
→ Human review
→ Mission Control task result
```

Codex must not directly publish or connect external platforms.

### OpenAI

Recommended role:

- Content Agent
- Research summarization
- Structured planning

Integration rule:

```text
Agent Dispatcher
→ OpenAI Adapter
→ Structured JSON output
→ Artifact
→ Approval if public-facing
```

### Provider Adapter Contract

Future real providers must implement:

```text
run(agent, task, context) -> AgentResult
```

Result must include:

- agent_name
- task_title
- status
- output
- artifact_type
- cost_estimate
- model_used
- safety_notes
- exception if failed

Any failure must route into:

```text
Exception Framework
```

## Recommendation

Agent Dispatcher V1 is ready as a mock runtime.

Next sprint should integrate Agent Dispatcher with Mission Control as a planning layer only, without allowing real AI execution yet.

