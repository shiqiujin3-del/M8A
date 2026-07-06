# M8A Mission Control V1

Status: Phase 1.2 + Commander Console V2 Final + Worker Runner V1.1  
State source: PostgreSQL  
Queue backend: PostgreSQL  
External platforms: not connected

## Scope

Mission Control V1 provides:

1. Mission tables.
2. Task tables.
3. Task event logs.
4. Artifact records.
5. CEO-only approval records.
6. Worker role configuration.
7. Lightweight HTTP API.
8. Dashboard data endpoint.
9. Local API token authentication.
10. Mission Detail and CEO Approval Inbox support.
11. Failed task retry support.
12. Approval audit records.
13. WordPress draft simulator.
14. CEO Commander Console.
15. Mission search and filters.
16. Approval detail modal.
17. Boss Daily View.
18. Local Worker Runner V1.1.

## Run

Set a local API token first:

```text
export M8A_COMMANDER_API_TOKEN="change-this-local-token"
```

Start the API:

```text
python3 apps/commander/mission-control/mission_control_api.py
```

Default URL:

```text
http://localhost:8787
```

## Authentication

All `/api/*` routes require:

```text
Authorization: Bearer <M8A_COMMANDER_API_TOKEN>
```

Example:

```text
curl -H "Authorization: Bearer change-this-local-token" http://localhost:8787/api/missions
```

The health endpoint does not require authentication:

```text
curl http://localhost:8787/health
```

If the token is missing or wrong, the API returns:

```text
401
```

## Dashboard

Open:

```text
apps/dashboard/index.html
```

In the Commander section, enter the same local API token and click `Save`.

The Dashboard then reads:

```text
GET http://localhost:8787/api/dashboard/commander
```

Dashboard V1.1 shows:

1. Mission Detail.
2. Task List.
3. Task Events.
4. Artifacts.
5. CEO Approval Inbox.
6. Failed Tasks with Retry.
7. Approval Audit.
8. WordPress Draft Simulator.
9. CEO Command Center.
10. Mission Overview.
11. Active Mission Board.
12. Task Health Panel.
13. Artifact Preview Center.

Approve/Reject buttons only update local approval records and task events.

They do not publish to WordPress or any social platform.

## V1.2 API

Retry a failed task:

```text
POST /api/tasks/:id/retry
```

The retry endpoint only accepts failed tasks. It returns the task to `queued`,
increments `retry_count`, and writes a task event. A task cannot be retried
after `retry_count` reaches 2.

List approvals:

```text
GET /api/approvals
```

Get approval detail:

```text
GET /api/approvals/:id
```

Approval decisions support audit fields:

```json
{
  "decision": "approved",
  "decision_reason": "CEO reviewed local draft payload.",
  "decided_by": "石总"
}
```

For `simulate_wordpress_draft`, approval changes the local artifact status to
`simulated_ready`. It does not create or publish a real WordPress post.

List recent artifacts:

```text
GET /api/artifacts
```

This endpoint is read-only and is used by Commander Console V1.

## Worker Runner V1.1

Worker Runner executes queued tasks locally and writes results back to
PostgreSQL.

It does not connect to n8n, WordPress, Facebook, LinkedIn, TikTok, YouTube,
WhatsApp, CRM, or any external platform.

Supported local handlers:

1. Knowledge Manager: reads local HK620 knowledge and creates a knowledge artifact.
2. Business Analyst: creates USA market direction and Mission Summary artifacts.
3. Content Operator: creates an English Landing Page draft structure.
4. Website Operator: creates a simulated WordPress draft payload and CEO approval.
5. Distribution Operator: creates Facebook / LinkedIn / TikTok / YouTube draft payload and CEO approval.
6. Sales Assistant: creates a WhatsApp inquiry reply draft and CEO approval.

Runner API:

```text
POST /api/runner/run-once
POST /api/runner/run-mission/:mission_id
POST /api/runner/start
POST /api/runner/pause
POST /api/runner/resume
POST /api/runner/stop
GET /api/runner/status
```

Example:

```text
curl -X POST \
  -H "Authorization: Bearer change-this-local-token" \
  http://localhost:8787/api/runner/run-once
```

Start Loop Mode:

```text
curl -X POST \
  -H "Authorization: Bearer change-this-local-token" \
  -H "Content-Type: application/json" \
  -d '{"interval_seconds":5,"mission_id":"optional_mission_id"}' \
  http://localhost:8787/api/runner/start
```

When `mission_id` is provided, Loop Mode only claims queued tasks from that
Mission. This is the recommended Dashboard behavior because the control buttons
live inside Mission Detail.

Status returns:

```json
{
  "mode": "manual | loop | paused | stopped",
  "is_running": true,
  "is_paused": false,
  "current_task_id": null,
  "last_task_id": "task id",
  "last_run_at": "timestamp",
  "last_error": null,
  "total_tasks_run_today": 1
}
```

Idempotency rules:

1. A task is claimed only when its status is `queued`.
2. Existing artifacts for the same task are reused.
3. Existing approvals for the same task and artifact are reused.
4. External-facing actions only create draft payloads and approval records.
5. Approval does not publish or send anything.
6. Pause stops new task claims without deleting queued tasks.
7. Stop requests safe loop shutdown.

## Website Capability V1: WordPress Draft Only

Website Operator now calls:

```text
apps/commander/capabilities/website/wordpress_draft.py
```

Required environment variables:

```text
M8A_WORDPRESS_BASE_URL
M8A_WORDPRESS_USERNAME
M8A_WORDPRESS_APP_PASSWORD
```

### WordPress Staging Config Preparation

Create a local `.env` file from the example:

```text
cp /Users/shiqiujing/Documents/M8A/.env.example /Users/shiqiujing/Documents/M8A/.env
```

Fill only the staging WordPress values:

```text
M8A_WORDPRESS_BASE_URL=https://your-staging-wordpress.example
M8A_WORDPRESS_USERNAME=your-staging-username
M8A_WORDPRESS_APP_PASSWORD=your-staging-application-password
```

Do not commit `.env`.

Export the variables before starting Mission Control:

```text
set -a
source /Users/shiqiujing/Documents/M8A/.env
set +a
export M8A_COMMANDER_API_TOKEN="change-this-local-token"
```

Confirm the variables are loaded without printing secrets:

```text
python3 /Users/shiqiujing/Documents/M8A/apps/commander/capabilities/website/check_wordpress_config.py
```

Expected ready output:

```text
BASE_URL configured
USERNAME configured
APP_PASSWORD configured
ready
```

Start Mission Control API:

```text
python3 /Users/shiqiujing/Documents/M8A/apps/commander/mission-control/mission_control_api.py
```

Rules:

1. Only WordPress post drafts are allowed.
2. The payload must use `status=draft`.
3. Publish, delete, and update-published-content actions are blocked.
4. Missing WordPress configuration does not crash the task.
5. Missing configuration creates a local `draft_payload` artifact and pending approval.
6. Successful WordPress draft creation creates a `wordpress_draft` artifact and pending approval.
7. Approval only changes approval status. It does not publish the WordPress draft.

The Website Operator approval action is:

```text
review_wordpress_draft
```


## Commander Console V1

Open:

```text
file:///Users/shiqiujing/Documents/M8A/apps/dashboard/index.html
```

The top of the Dashboard is now the CEO Commander Console.

Use it to:

1. Enter a CEO command.
2. Create a Mission.
3. Review Mission overview metrics.
4. View active Missions.
5. Open Mission Detail.
6. Approve or reject pending approvals with a decision reason.
7. Retry failed tasks.
8. Preview recent artifacts.
9. Search and filter Missions.
10. Archive Missions.
11. Review full approval payload inside the Approval Detail modal.

Example command:

```text
今天重点做 HK620，美国市场。
```

Commander Console reads real Mission Control API data. It does not use hardcoded
Mission, Approval, Task, or Artifact state.

Commander Console V1.1 adds:

1. Mission search.
2. Status filters: active, queued, running, waiting approval, completed, failed, archived.
3. Product filters: HK620, Edge Banding, CNC, Six-sided Drilling.
4. Market filters: USA, China, Europe, Southeast Asia, Global.
5. Boss Daily View.
6. Approval Detail modal with full payload behind `查看原始数据`.
7. Archive Mission button in Mission Detail.

## Safety

V1 does not connect WordPress, Facebook, LinkedIn, TikTok, YouTube, WhatsApp, CRM, or n8n.
