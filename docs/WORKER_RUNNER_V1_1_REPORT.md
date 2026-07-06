# M8A Worker Runner V1.1 Report

Date: 2026-07-06

## Scope

Worker Runner was upgraded from a manual executor to a controllable runner.

Commander Console V2 CEO Home remains frozen. No CEO Home restructuring was made.

## Files Modified

- apps/commander/mission-control/mission_control_api.py
- apps/commander/mission-control/worker_runner.py
- apps/commander/mission-control/README.md
- apps/dashboard/index.html

## Files Added

- docs/WORKER_RUNNER_V1_1_REPORT.md

## Runner Modes

| Mode | Description |
| --- | --- |
| Manual | Existing run-once and run-mission execution |
| Loop | Background loop checks queued tasks and executes one task per interval |
| Paused | Runner stays alive but does not claim new queued tasks |
| Stopped | Loop exits safely |

## Runner API

- POST /api/runner/start
- POST /api/runner/pause
- POST /api/runner/resume
- POST /api/runner/stop
- GET /api/runner/status
- POST /api/runner/run-once
- POST /api/runner/run-mission/:mission_id

Start payload:

```json
{
  "interval_seconds": 5,
  "mission_id": "optional_mission_id"
}
```

When `mission_id` is provided, Loop Mode only claims queued tasks from that Mission.

## Status Fields

GET /api/runner/status returns:

- mode
- is_running
- is_paused
- current_task_id
- last_task_id
- last_run_at
- last_error
- total_tasks_run_today
- interval_seconds
- mission_id

## Dashboard Control

Controls were added only inside Mission Detail:

- Start Runner
- Pause Runner
- Resume Runner
- Stop Runner
- Run Once
- Run This Mission
- Runner Status

No CEO Home entry point was restructured.

## Safety Rules

- No WordPress connection.
- No n8n connection.
- No external platform connection.
- No automatic publishing.
- External-facing work still creates only artifacts and approvals.
- Pause does not delete or mutate queued tasks.
- Stop exits the loop safely.
- Exceptions are caught and reported through runner status / events.

## Test Report

Input:

```text
今天重点做 HK620，美国市场。
```

Mission:

```text
mission_hk620_us_growth_1783324308809888000
```

Observed:

| Check | Result |
| --- | --- |
| Mission created | PASS |
| Initial tasks | 7 queued |
| Start Loop Mode | PASS |
| Loop interval | 1 second in test |
| Pause | PASS |
| Pause behavior | Running task finished, no new queued task was claimed |
| Resume | PASS |
| Stop | PASS |
| Status fields | PASS |
| run-once still works | PASS |
| run-mission still works | PASS |
| Artifacts | 7 |
| Approvals | 3 |
| Task events | 51 |
| Duplicate run | PASS, no extra artifacts or approvals |
| External platforms | Not connected |
| Auto publish | Not executed |

Final task states:

```text
completed
completed
completed
waiting_approval
waiting_approval
waiting_approval
completed
```

Control events recorded:

```text
runner_started
runner_paused
runner_resumed
runner_stopped
```

Status sample:

```json
{
  "mode": "stopped",
  "is_running": false,
  "is_paused": false,
  "current_task_id": null,
  "last_task_id": "mission_hk620_us_growth_1783324308809888000_task_002",
  "last_run_at": "2026-07-06T07:51:54Z",
  "last_error": null,
  "total_tasks_run_today": 17
}
```

Idempotency check:

```text
Before duplicate run: artifacts 7, approvals 3
After duplicate run:  artifacts 7, approvals 3
```

## Current Risks

1. Loop Mode is in-process. If the API process stops, the runner stops.
2. Runner state is runtime memory plus database event history, not a persisted daemon state table.
3. Global run-once still claims the oldest queued task unless a future scoped endpoint is added.
4. Handler outputs remain deterministic local drafts.
5. External actions remain simulated and approval-gated.

## Next Stage Recommendation

Freeze Worker Runner V1.1 behavior before adding platform access.

Recommended next step:

1. Add scoped run-once for the selected Mission.
2. Add clearer queue visibility per Mission.
3. Only then open WordPress Draft MVP, still without auto-publish.

