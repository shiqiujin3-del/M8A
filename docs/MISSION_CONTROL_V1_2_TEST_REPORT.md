# M8A Mission Control V1.2 Test Report

Date: 2026-07-06

## Scope

Mission Control V1.2 adds three local-only capabilities:

1. Failed task retry.
2. Approval audit.
3. WordPress draft simulator.

No real WordPress, n8n, or external platform connection was added.

## Modified Files

- `/Users/shiqiujing/Documents/M8A/apps/commander/mission-control/mission_control_api.py`
- `/Users/shiqiujing/Documents/M8A/apps/commander/mission-control/README.md`
- `/Users/shiqiujing/Documents/M8A/apps/dashboard/index.html`

## New Files

- `/Users/shiqiujing/Documents/M8A/apps/commander/mission-control/migrations/003_mission_control_v1_2.sql`
- `/Users/shiqiujing/Documents/M8A/docs/MISSION_CONTROL_V1_2_TEST_REPORT.md`

## Database Migration

Migration file:

`/Users/shiqiujing/Documents/M8A/apps/commander/mission-control/migrations/003_mission_control_v1_2.sql`

Added fields:

- `commander_tasks.retry_count`
- `commander_artifacts.simulation_status`
- `commander_artifacts.payload_snapshot`
- `commander_approvals.decision_reason`
- `commander_approvals.decided_by`
- `commander_approvals.payload_snapshot`

Migration result: PASS

## API Changes

### Retry Failed Task

`POST /api/tasks/:id/retry`

Behavior:

- Only failed tasks can be retried.
- Retry changes task status from `failed` to `queued`.
- `retry_count` increases by 1.
- A `task_retry` event is written.
- If `retry_count >= 2`, retry is rejected and `task_retry_rejected` is written.

### Approval Audit

`GET /api/approvals`

`GET /api/approvals/:id`

Approval decision payload now supports:

```json
{
  "decision": "approved",
  "decision_reason": "CEO reviewed local draft payload.",
  "decided_by": "石总"
}
```

Decision data stored:

- `decision_reason`
- `decided_by`
- `decided_at`
- `payload_snapshot`

### WordPress Draft Simulator

Mock action:

`simulate_wordpress_draft`

Behavior:

- Generates a local WordPress draft payload.
- Saves it as a `draft_payload` artifact.
- Creates a CEO approval record.
- On approval, marks artifact `simulation_status = simulated_ready`.
- Does not publish.
- Does not connect to WordPress.

## Dashboard Changes

Added or updated areas:

- Failed Tasks
- Retry button
- Approval Audit
- Approval Detail fields
- WordPress Draft Simulator

WordPress draft simulator displays:

- Draft title
- Slug
- Meta title
- Meta description
- Content preview
- Approval status
- Simulation status

## Acceptance Test

Input:

`今天重点做 HK620，美国市场。`

Test mission:

`HK620_US_GROWTH`

Result:

| Check | Result |
|---|---|
| Mission created | PASS |
| 7 tasks generated | PASS |
| Website Operator generated WordPress draft payload | PASS |
| WordPress draft entered approval | PASS |
| Approve changed draft to `simulated_ready` | PASS |
| Reject changed approval to `rejected` | PASS |
| Failed task can retry | PASS |
| Retry limit blocks third retry | PASS |
| Retry events written | PASS |
| Approve/reject events written | PASS |
| No real WordPress connection | PASS |
| No n8n connection | PASS |
| No external platform connection | PASS |

## Test Evidence

Mission ID:

`mission_hk620_us_growth_1783318708513`

Generated task count:

`7`

Retry counts:

`1`, `2`

Third retry response:

`400 Retry limit exceeded. Maximum retry_count is 2.`

Approvals before decision:

`3`

WordPress approval:

`approval_1783318713272`

Social approval:

`approval_1783318714226`

WordPress approval result:

`approved`

Social approval result:

`rejected`

WordPress draft:

```json
{
  "title": "HK620 Skeleton Door Strip Processing for the USA Market",
  "slug": "hk620-skeleton-door-strip-processing-usa",
  "simulation_status": "simulated_ready",
  "publish": false
}
```

Event counts:

```json
{
  "task_retry": 2,
  "task_retry_rejected": 1,
  "approval_decision": 2,
  "wordpress_draft_simulated_ready": 1
}
```

Failed task items visible to Dashboard:

`1`

## Local Start Command

Set token:

```text
export M8A_COMMANDER_API_TOKEN="change-this-local-token"
```

Start API:

```text
python3 /Users/shiqiujing/Documents/M8A/apps/commander/mission-control/mission_control_api.py
```

Open Dashboard:

```text
file:///Users/shiqiujing/Documents/M8A/apps/dashboard/index.html
```

Enter the same local token in the Commander section.

## Risk Points

1. V1.2 still uses a lightweight local Python API, not a production web framework.
2. PostgreSQL is the only queue source; there is no distributed worker lock execution yet.
3. Approvals are audited locally, but there is no user account system beyond local token and `decided_by`.
4. WordPress draft simulator is intentionally local-only; real WordPress draft creation still needs connector design, credential isolation, and dry-run tests.
5. Dashboard updates by polling, not websocket realtime.

## Recommended Next Stage

V1.3 should add a controlled local execution loop:

1. Worker runner reads queued tasks from PostgreSQL.
2. Worker runner claims one task with lock protection.
3. Worker runner executes only local safe actions.
4. All external actions remain approval-only and simulated until connector credentials are separately approved.
