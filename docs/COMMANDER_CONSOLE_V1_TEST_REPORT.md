# M8A Commander Console V1 Test Report

Date: 2026-07-06

## Scope

Commander Console V1 integrates existing Mission Control V1 / V1.1 / V1.2 capabilities into a CEO-facing control console.

This sprint does not add Worker Runner execution logic.

No external platform, n8n, WordPress, or publishing connection was added.

## Modified Files

- `/Users/shiqiujing/Documents/M8A/apps/dashboard/index.html`
- `/Users/shiqiujing/Documents/M8A/apps/dashboard/styles.css`
- `/Users/shiqiujing/Documents/M8A/apps/commander/mission-control/mission_control_api.py`
- `/Users/shiqiujing/Documents/M8A/apps/commander/mission-control/README.md`

## New Files

- `/Users/shiqiujing/Documents/M8A/docs/COMMANDER_CONSOLE_V1_TEST_REPORT.md`

## Removed / Paused

- Worker Runner development was paused per CEO instruction.
- No `worker_runner.py` is active or connected.

## Commander Console Areas

### 1. CEO Command Center

Includes:

- CEO command input.
- Default command: `今天重点做 HK620，美国市场。`
- Create Mission button.
- Mission creation result with `mission_id` and status.
- Mission Detail selection support.

### 2. Mission Overview

Displays:

- Total Missions.
- Active Missions.
- Waiting Approval Missions.
- Completed Missions.
- Failed Missions.
- Today's new Missions.
- Recent 5 Missions.

### 3. Active Mission Board

Displays active, queued, running, and waiting approval Missions:

- Mission name.
- Product.
- Market.
- Status.
- Progress.
- Pending approval count.
- Failed task count.
- View Detail button.

### 4. CEO Approval Inbox

Displays all pending approvals:

- Mission.
- Task.
- Platform.
- Action Type.
- Risk Level.
- Payload preview.
- Decision reason input.
- Approve button.
- Reject button.

### 5. Task Health Panel

Displays:

- Queued tasks.
- Running tasks.
- Failed tasks.
- Completed tasks.
- Failed task list.
- Retry count.
- Retry button.

### 6. Artifact Preview Center

Displays recent artifacts:

- Mission.
- Task.
- Artifact type.
- Title.
- Content preview.
- Status.
- Quality score.

## Mission Detail

Mission Detail displays:

- Mission basic info.
- Task list.
- Task Events.
- Artifacts.
- Approvals.
- Mission Summary.

## API Changes

Added one lightweight read-only endpoint:

```text
GET /api/artifacts
```

Purpose:

Allow Artifact Preview Center to read recent real artifacts from PostgreSQL.

Existing APIs reused:

- `GET /api/dashboard/commander`
- `GET /api/missions`
- `GET /api/missions/:id`
- `GET /api/tasks`
- `GET /api/approvals`
- `GET /api/approvals/:id`
- `POST /api/missions`
- `POST /api/approvals/:id/decision`
- `POST /api/tasks/:id/retry`

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

Enter the same token in the Commander Console token field.

## Acceptance Test

Input:

```text
今天重点做 HK620，美国市场。
```

Test result:

| Check | Result |
|---|---|
| Dashboard opens with Commander Console areas | PASS |
| Create Mission from CEO command | PASS |
| Created Mission appears in Active Mission Board | PASS |
| Mission Detail can be loaded | PASS |
| Approval Inbox can display pending approvals | PASS |
| Approval decision reason is saved | PASS |
| Approve action works locally | PASS |
| Task Health Panel can detect failed tasks | PASS |
| Retry failed task works | PASS |
| Artifact Preview Center reads recent artifacts | PASS |
| Page reads real API data | PASS |
| No external platform connected | PASS |
| n8n not connected | PASS |
| No real publish executed | PASS |

## Test Evidence

Created Mission:

`mission_hk620_us_growth_1783319646041`

Created status:

`queued`

Mission count:

`4`

Detail task count:

`7`

Pending approvals visible:

`2`

Approval decision:

`approved`

Decision reason saved:

`true`

Failed task visible:

`true`

Retry result:

`queued`

Retry count after retry:

`1`

Artifact preview count:

`20`

External connections:

```json
{
  "external_platforms_connected": false,
  "n8n_connected": false,
  "real_publish_executed": false
}
```

## Current Gaps

1. Console is a static HTML frontend reading the local API; there is no user account system beyond local token.
2. Mission progress is calculated from task state only.
3. Artifact preview is text-first; large payloads are summarized rather than opened in a rich editor.
4. Mission Summary depends on existing artifacts; if no summary artifact exists, the detail page shows an empty summary state.
5. No Worker Runner is connected in this sprint.

## Recommended Next Stage

Commander Console V1.1 should improve CEO usability:

1. Add filter tabs: Active, Waiting Approval, Failed, Completed.
2. Add a safer approval modal with full payload preview.
3. Add Mission search by product, market, and status.
4. Add a one-click "Archive Completed Mission" action.
5. Only after Console stabilizes, resume Worker Runner V1.3 as a separate controlled sprint.
