# M8A External Workflow Adapter V1 Design

Date: 2026-07-06

## Objective

External Workflow Adapter V1 defines how M8A can safely connect external workflows such as n8n workflows, Coze workflows, API workflows, local scripts, and future third-party automations.

The key rule:

```text
External workflows never control M8A directly.
```

They must enter through the M8A runtime boundary:

```text
External Workflow
  ↓
Workflow Adapter
  ↓
Capability Layer
  ↓
Worker Runner
  ↓
Mission Control
  ↓
Commander Console
```

## Non-Negotiable Safety Rules

External workflows must not:

- Bypass Mission Control.
- Bypass Worker Runner.
- Bypass Approval.
- Bypass Exception Framework.
- Write directly to Commander database tables.
- Publish directly to external platforms.
- Store credentials in workflow output, logs, reports, or artifacts.
- Trigger unapproved production changes.

## External Workflow Registration Standard

Every external workflow must be registered before M8A can call it.

Required fields:

```json
{
  "workflow_name": "banana_api_connection_workflow",
  "workflow_type": "mock | n8n | coze | api | local_script | third_party",
  "source_platform": "mock",
  "input_schema": {},
  "output_schema": {},
  "required_credentials": [],
  "allowed_actions": [],
  "forbidden_actions": [],
  "approval_required": true,
  "risk_level": "low | medium | high | critical",
  "timeout": 60,
  "retry_policy": {},
  "exception_policy": {}
}
```

## Workflow Registry Design

The Workflow Registry is the approved catalog of external workflows.

Responsibilities:

1. Register workflow metadata.
2. Validate whether a workflow is active.
3. Check allowed and forbidden actions.
4. Expose workflow input and output schemas.
5. Define timeout and retry policy.
6. Define approval and exception policy.

Supported workflow types:

- n8n workflows
- Coze workflows
- API workflows
- local scripts
- future third-party automations

Example registry entry:

```json
{
  "workflow_name": "banana_api_connection_workflow",
  "workflow_type": "mock",
  "source_platform": "M8A Mock Runtime",
  "input_schema": {
    "command_text": "string",
    "mission_id": "string",
    "task_id": "string"
  },
  "output_schema": {
    "integration_plan": "object",
    "required_credentials": "array",
    "api_endpoints": "array",
    "risk_points": "array",
    "next_steps": "array"
  },
  "required_credentials": [],
  "allowed_actions": [
    "generate_plan",
    "return_artifact"
  ],
  "forbidden_actions": [
    "publish",
    "write_external_system",
    "store_secret",
    "modify_m8a_state_directly",
    "call_external_api_in_mock_mode"
  ],
  "approval_required": true,
  "risk_level": "medium",
  "timeout": 60,
  "retry_policy": {
    "max_retries": 2,
    "retry_on": [
      "timeout",
      "temporary_failure"
    ]
  },
  "exception_policy": {
    "on_failure": "create_exception_from_failure",
    "owner": "Infrastructure Operator"
  },
  "status": "active"
}
```

## Workflow Adapter Design

The Workflow Adapter is a controlled runtime bridge.

It receives a M8A task and does seven things:

```text
1. Receive M8A Task
2. Load workflow registration
3. Convert M8A task input to external workflow input
4. Call external workflow or mock workflow
5. Wait for result
6. Save result as Artifact
7. Create Approval if required
8. Route failure into Exception Framework
```

The Adapter must return a structured result:

```json
{
  "workflow_name": "banana_api_connection_workflow",
  "status": "completed | failed | waiting_approval",
  "artifact_type": "workflow_result",
  "content_json": {},
  "approval_required": true,
  "exception": null
}
```

## Runtime Flow

```text
CEO Command
  ↓
Commander Console
  ↓
Mission Control creates Mission + Task
  ↓
Worker Runner claims Task
  ↓
Capability calls Workflow Adapter
  ↓
Workflow Adapter validates registry
  ↓
Workflow Adapter runs mock/external workflow
  ↓
Result saved as Artifact
  ↓
Approval created if needed
  ↓
Exception Framework handles failures
```

## Mock Workflow Demo

First mock workflow:

```text
workflow_name = banana_api_connection_workflow
workflow_type = mock
source_platform = M8A Mock Runtime
```

Input:

```json
{
  "command_text": "帮我接 Banana API",
  "mission_id": "mission_xxx",
  "task_id": "task_xxx"
}
```

Output:

```json
{
  "integration_plan": {
    "summary": "Plan a safe Banana API connection through M8A Capability Layer.",
    "phases": [
      "Research Banana API documentation",
      "Confirm authentication and credentials",
      "Design connector contract",
      "Create mock adapter",
      "Run QA and exception tests",
      "Request CEO approval before real integration"
    ]
  },
  "required_credentials": [
    "BANANA_API_BASE_URL",
    "BANANA_API_KEY",
    "BANANA_WEBHOOK_SECRET"
  ],
  "api_endpoints": [
    "GET /status",
    "POST /jobs",
    "GET /jobs/{id}",
    "POST /webhooks"
  ],
  "risk_points": [
    "Credential storage must not be written to code or artifacts.",
    "External write actions require approval.",
    "Webhook failures must enter Exception Framework.",
    "Rate limit and timeout behavior must be defined before production."
  ],
  "next_steps": [
    "CEO reviews Agent Plan.",
    "Infrastructure Operator confirms credentials policy.",
    "Code Agent designs connector interface.",
    "QA Agent defines mock and failure tests."
  ]
}
```

## Artifact Rule

Workflow Adapter output must be saved as:

```text
artifact_type = workflow_result
```

Artifact content must include:

- workflow_name
- workflow_type
- source_platform
- input_summary
- output
- safety_notes
- approval_required
- external_action_executed=false for mock mode

## Approval Rule

If workflow output involves any of the following, approval is required:

- writing code
- modifying M8A system behavior
- connecting API
- configuring credentials
- deployment
- external platform action
- customer-facing output
- public publishing

Approval record:

```json
{
  "platform": "M8A",
  "action_type": "approve_external_workflow_result",
  "risk_level": "medium",
  "status": "pending"
}
```

Approve means:

```text
Allowed to proceed to the next controlled M8A step.
```

Approve does not mean:

```text
Run external workflow in production.
Publish.
Deploy.
Store credentials.
```

## Exception Rule

Any failure must call:

```text
create_exception_from_failure()
```

Exception sources:

- workflow registry validation failure
- input schema mismatch
- output schema mismatch
- timeout
- retry exhausted
- authentication failure
- webhook failure
- external API failure
- local script error

Failure flow:

```text
Workflow Failure
  ↓
Exception Framework
  ↓
Exception Mission
  ↓
Infrastructure Operator
  ↓
Recovery Plan
  ↓
CEO Approval if needed
```

## How It Avoids Bypassing M8A

| Risk | Control |
| --- | --- |
| External workflow directly controls M8A | Not allowed. Adapter receives Worker Task only. |
| External workflow bypasses Mission Control | Not allowed. Every call starts from Mission Task. |
| External workflow bypasses Approval | Adapter creates approval for risky outputs. |
| External workflow bypasses Exception Framework | Adapter routes all failures to Exception Framework. |
| External workflow writes secrets to artifacts | Forbidden action. Credential values must be masked. |
| External workflow publishes directly | Forbidden unless a future approved publish capability exists. |

## V1 Acceptance Design

V1 should pass:

1. Register mock workflow `banana_api_connection_workflow`.
2. Worker Runner calls Capability.
3. Capability calls Workflow Adapter.
4. Workflow Adapter returns mock result.
5. Result is saved as artifact.
6. Approval is created.
7. Failure enters Exception Framework.
8. Mission Control remains the state source.
9. Commander Console remains the CEO surface.
10. No real external platform is connected.

## Next Stage: n8n

n8n integration should be added only after mock adapter passes.

Rules:

```text
M8A Task
  ↓
Workflow Adapter
  ↓
n8n Webhook / API
  ↓
n8n Result
  ↓
Artifact
  ↓
Approval
  ↓
Exception Framework if failed
```

n8n may execute internal workflow logic, but it must not directly mutate M8A state.

## Next Stage: Coze

Coze should be treated as a workflow provider, not a Commander authority.

Rules:

- Coze receives structured input from Adapter.
- Coze returns structured output.
- M8A validates output schema.
- Public/customer-facing output requires approval.
- Failures route to Exception Framework.

## Next Stage: Third-Party API Workflow

Third-party workflow must define:

- API auth method
- rate limits
- timeout
- retry policy
- allowed methods
- forbidden methods
- data retention policy
- exception policy

Production write actions require separate approval.

## Main Risks

1. External workflows may produce untrusted output.
2. Credentials may leak if schema is not strict.
3. n8n or Coze may execute side effects outside M8A if not locked down.
4. Retry can duplicate actions unless idempotency is required.
5. Approval boundaries must remain strict.
6. Exception Framework must be mandatory for all adapter failures.

## Recommendation

Build V1 implementation in this order:

1. Workflow Registry local file/module.
2. Mock Workflow Adapter.
3. Capability wrapper.
4. Worker Runner handler.
5. Artifact + Approval integration.
6. Exception Framework failure test.
7. Only then connect n8n or Coze in a separate sprint.

