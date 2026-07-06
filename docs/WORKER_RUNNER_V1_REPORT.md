# M8A Worker Runner V1 Report

Date: 2026-07-06

## Scope

Worker Runner V1 was added after Commander Console V2 Final was frozen.

No CEO Home redesign was made. New controls were added only inside Mission Detail.

## Files Modified

- apps/commander/mission-control/mission_control_api.py
- apps/commander/mission-control/README.md
- apps/dashboard/index.html

## Files Added

- apps/commander/mission-control/worker_runner.py
- docs/WORKER_RUNNER_V1_REPORT.md

## Runner API

- POST /api/runner/run-once
- POST /api/runner/run-mission/:mission_id
- GET /api/runner/status

All routes require the existing local Authorization header:

```text
Authorization: Bearer <M8A_COMMANDER_API_TOKEN>
```

## Supported Local Handlers

| Worker | Action | Result |
| --- | --- | --- |
| Knowledge Manager | read_hk620_product_knowledge | HK620 knowledge artifact |
| Business Analyst | generate_us_market_direction | USA market direction artifact |
| Content Operator | generate_english_landing_page_structure | Landing Page draft structure |
| Website Operator | simulate_wordpress_draft | WordPress draft payload + CEO approval |
| Distribution Operator | generate_social_distribution_drafts | Social draft payload + CEO approval |
| Sales Assistant | generate_whatsapp_inquiry_reply | WhatsApp reply draft + CEO approval |
| Business Analyst | generate_mission_summary | Mission Summary artifact |

## Safety Rules

- No n8n connection.
- No real WordPress connection.
- No Facebook / LinkedIn / TikTok / YouTube connection.
- No WhatsApp connection.
- No CRM connection.
- No automatic publishing.
- External-facing actions only create draft payloads and approval records.

## Idempotency

Worker Runner prevents duplicate work by:

1. Claiming only tasks with status `queued`.
2. Updating task status before execution.
3. Reusing an existing artifact for the same task.
4. Reusing an existing approval for the same task and artifact.

## Dashboard

Mission Detail now includes:

- Run Next Task
- Run This Mission
- Runner Status

CEO Home fixed entry points were not restructured:

- Commander Brief
- Company Health
- Today Company Created
- Approval Inbox
- Mission Detail
- End Of Day

## Test Result

Input:

```text
今天重点做 HK620，美国市场。
```

Observed:

| Check | Result |
| --- | --- |
| Mission created | PASS |
| Initial tasks | 7 queued |
| Failed task retry | PASS, failed -> queued, retry_count = 1 |
| run-once | PASS, executed exactly 1 queued task |
| run-mission | PASS |
| Final task states | completed / waiting_approval |
| Artifacts created | 7 |
| Approvals created | 3 |
| Task events written | 49 |
| Duplicate run | PASS, no extra artifacts or approvals |
| Real external platform access | None |

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

Approval platforms:

```text
WordPress
Facebook / LinkedIn / TikTok / YouTube
WhatsApp
```

Duplicate run check:

```text
Before: artifacts 7, approvals 3
After:  artifacts 7, approvals 3
```

## Current Risks

1. Runner uses PostgreSQL directly through the existing Docker/Postgres pattern.
2. The current local Runner is synchronous, not a long-running background daemon.
3. Handler content is deterministic local draft content, not LLM-generated content.
4. Mission dependency ordering is simple task_order execution.
5. External publish actions remain approval-only simulations.

## Next Stage Recommendation

Build Worker Runner V1.1 only after CEO approval:

1. Add a controlled background loop with start/stop controls.
2. Add richer handler outputs using approved knowledge only.
3. Keep all external actions approval-gated until WordPress Draft MVP is explicitly opened.

