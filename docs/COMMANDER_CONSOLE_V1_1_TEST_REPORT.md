# M8A Commander Console V1.1 Test Report

Date: 2026-07-06

## Scope

Commander Console V1.1 improves the CEO experience of the existing Commander Console.

This stage only changes the local Dashboard and reuses existing Mission Control APIs.

No n8n, WordPress, external platform, Worker Runner, or auto-publishing integration was added.

## Modified Files

- `/Users/shiqiujing/Documents/M8A/apps/dashboard/index.html`
- `/Users/shiqiujing/Documents/M8A/apps/dashboard/styles.css`
- `/Users/shiqiujing/Documents/M8A/apps/commander/mission-control/README.md`

## New Files

- `/Users/shiqiujing/Documents/M8A/docs/COMMANDER_CONSOLE_V1_1_TEST_REPORT.md`

## Commander Console V1.1 Changes

### 1. Mission Search And Filters

Added:

- Mission search box.
- Status filter: active, queued, running, waiting_approval, completed, failed, archived.
- Product filter: HK620, Edge Banding, CNC, Six-sided Drilling.
- Market filter: 美国, 国内, 欧洲, 东南亚, 全球.

### 2. Approval Detail Modal

Added full approval review modal.

It displays:

- Mission.
- Task.
- Platform.
- Action Type.
- Risk Level.
- Payload summary.
- Decision Reason input.
- Approve button.
- Reject button.
- Full payload inside `查看原始数据`.

The full JSON payload is no longer exposed directly on the homepage.

### 3. Mission Archive Button

Mission Detail now includes:

- `归档 Mission` button.

Behavior:

- Calls existing `POST /api/missions/:id/archive`.
- Archived Mission no longer appears in active filter.
- Archived Mission remains visible in archived filter.
- Existing API writes `mission_status_changed` event.

### 4. Boss Daily View

Added:

- Today new Missions.
- Today completed Missions.
- Today pending approvals.
- Today failed tasks.
- Today generated artifacts.
- Top 3 recommended actions for 石总.

### 5. Chinese UX

Updated visible CEO-facing areas:

- Chinese titles.
- Chinese action buttons.
- Chinese helper text.
- Technical terms remain where useful, with Chinese context.
- Raw JSON is placed inside collapsible `查看原始数据`.

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

Enter the same token in the local API token field.

## Acceptance Test

Input:

```text
今天重点做 HK620，美国市场。
```

Test Mission:

`mission_hk620_us_growth_1783320321251`

| Check | Result |
|---|---|
| Mission search data works | PASS |
| Status filter data works | PASS |
| Product filter data works | PASS |
| Market filter data works | PASS |
| Approval detail payload exists | PASS |
| Approval reason can be saved | PASS |
| Approve updates status correctly | PASS |
| Failed task is visible | PASS |
| Failed task retry works | PASS |
| Mission archive works | PASS |
| Archived Mission removed from active board | PASS |
| Archived Mission findable in archived filter | PASS |
| Archive event written | PASS |
| Boss Daily View reads real data | PASS |
| Page uses real API data | PASS |
| No external platform connected | PASS |
| No n8n connected | PASS |
| No auto publish executed | PASS |

## Test Evidence

```json
{
  "mission_id": "mission_hk620_us_growth_1783320321251",
  "mission_created_status": "queued",
  "initial_task_count": 7,
  "initial_all_queued": true,
  "approval_modal_payload_available": true,
  "approval_platform": "WordPress",
  "approval_action_type": "simulate_wordpress_draft",
  "approval_status_after_decision": "approved",
  "approval_reason_saved": true,
  "failed_task_visible": true,
  "retry_status": "queued",
  "retry_count": 1,
  "archived_status": "archived",
  "not_in_active_board_after_archive": true,
  "findable_in_archived_filter": true,
  "archive_event_written": true,
  "search_hk620_count": 5,
  "status_filter_archived_count": 2,
  "product_filter_hk620_count": 5,
  "market_filter_usa_count": 5,
  "daily_view": {
    "today_new_missions": 5,
    "today_completed_missions": 0,
    "today_pending_approvals": 1,
    "today_failed_tasks": 1,
    "today_artifacts": 21
  },
  "external_platforms_connected": false,
  "n8n_connected": false,
  "auto_publish_executed": false
}
```

## Current Issues

1. Console is still static HTML and local API polling.
2. Filters are client-side; this is acceptable for current local data volume.
3. Approval modal is functional but not yet a rich document viewer.
4. Mission archive is available, but there is no bulk archive.
5. Product and market filters are fixed option lists.

## Recommended Next Stage

Commander Console V1.2 should focus on:

1. Better Mission Detail layout with tabs.
2. Approval history timeline.
3. Artifact full-page viewer.
4. Mission notes for 石总.
5. Only after the Console is stable, resume Worker Runner as a separate controlled sprint.
