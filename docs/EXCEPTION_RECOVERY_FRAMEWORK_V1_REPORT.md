# M8A Exception & Recovery Framework V1 Report

Date: 2026-07-06

## Scope

Exception & Recovery Framework V1 establishes a unified enterprise exception system.

This phase does not fix Cloudflare. It creates the process for turning failures into structured recovery work.

## Important Constraint Handling

The user required:

- Do not connect new platforms.
- Do not modify Commander Home.
- Do not modify Mission Control.
- Do not modify Worker Runner.

Therefore V1 was implemented as an independent framework and tested through a local Cloudflare 403 simulation. Automatic live wiring into Worker Runner / Mission Control is documented as the next integration phase.

## Architecture

```text
Capability / Platform / Worker / API Failure
        ↓
Exception Framework
        ↓
Exception Mission
        ↓
Exception Queue
        ↓
Infrastructure Operator
        ↓
Recovery Plan
        ↓
CEO Approval if required
        ↓
Resolved / Ignored / Archived
```

## Infrastructure Operator

Worker added:

```text
Infrastructure Operator
```

Responsibilities:

- Cloudflare
- DNS
- SSL
- REST API
- OAuth
- Webhook
- WordPress
- Network
- Security

It investigates infrastructure and platform exceptions before CEO involvement.

## Exception Queue

New statuses:

```text
new
investigating
waiting_approval
resolved
ignored
archived
```

The user-facing wording maps to:

```text
New -> new
Investigating -> investigating
Waiting Approval -> waiting_approval
Resolved -> resolved
Ignored -> ignored
Archived -> archived
```

## Recovery Plan

For Cloudflare 1010 / HTTP 403, V1 generates:

- Reason analysis
- Possible causes
- Recommended actions
- Impact scope
- Risk level
- Whether CEO approval is needed

Example recovery plan:

```text
Reason: Cloudflare blocked the platform/API request before the action could reach WordPress.
Possible causes:
- Cloudflare WAF or bot rule blocked the local API request.
- REST API authenticated request pattern is not allowlisted.
- Source IP, user agent, or security score triggered Error 1010.
Recommended actions:
- Review Cloudflare Security Events.
- Create a narrow allow rule for trusted M8A source and WordPress REST draft endpoint.
- Avoid disabling global security rules.
- Retry draft-only verification after allowlist is confirmed.
Needs CEO: YES
```

## Dashboard

Independent Exception Center added:

```text
apps/commander/exception-framework/exception_center.html
```

Snapshot source:

```text
apps/commander/exception-framework/exception_center_snapshot.json
```

This avoids modifying Commander Console CEO Home.

Exception Center shows:

- Today exception count
- Investigating
- Waiting CEO
- Resolved
- Average recovery time
- Exception Queue items
- Recovery Plan

## Files Modified

None of the following were modified:

- Mission Control API
- Worker Runner
- Commander Console CEO Home

## Files Added

- apps/commander/mission-control/migrations/005_exception_framework_v1.sql
- apps/commander/exception-framework/exception_framework.py
- apps/commander/exception-framework/simulate_cloudflare_403.py
- apps/commander/exception-framework/exception_center_snapshot.py
- apps/commander/exception-framework/exception_center.html
- apps/commander/exception-framework/exception_center_snapshot.json
- docs/EXCEPTION_RECOVERY_FRAMEWORK_V1_REPORT.md

## Database Objects

New tables:

- commander_exceptions
- commander_exception_events

Seeded worker:

- Infrastructure Operator

## Test Report

Test:

```text
Simulate Cloudflare 403 / Error 1010
```

Result:

| Requirement | Result |
| --- | --- |
| Create Exception Mission | PASS |
| Enter Exception Queue | PASS |
| Assign Infrastructure Operator | PASS |
| Generate Recovery Plan | PASS |
| Requires CEO when needed | PASS |
| CEO Approval Inbox record created | PASS |
| Dashboard can see exception through Exception Center snapshot | PASS |
| Close/archive exception | PASS |

Database verification:

```text
commander_exceptions: 1
Infrastructure Operator: 1
approve_recovery_plan approvals: 1
EXCEPTION_MISSION records: 1
```

Created exception:

```text
exception_id: exception_1783329300640939000
exception_mission_id: mission_exception_1783329300640943000
error_code: HTTP_403_CLOUDFLARE_1010
assigned_worker_name: Infrastructure Operator
requires_ceo_approval: true
status after close: archived
```

## Future Platform Integration Contract

All future capabilities and platforms should call Exception Framework with:

```json
{
  "source_mission_id": "mission id",
  "source_task_id": "task id",
  "source_system": "WordPress | Cloudflare | OAuth | Webhook | API | n8n | Platform",
  "error_message": "original error summary"
}
```

The framework then:

1. Classifies the exception.
2. Creates or reuses an active exception record.
3. Creates Exception Mission.
4. Assigns Infrastructure Operator.
5. Generates Recovery Plan.
6. Creates CEO approval when required.
7. Exposes the exception in Exception Center.

## Next Integration Phase

To make every live Worker/API failure automatically route into Exception Framework, the next phase needs explicit authorization to modify:

- Worker Runner failure handler
- Mission Control API failure handler
- Dashboard data endpoint
- Commander Console exception display

Until that authorization is given, V1 remains independent and verified by simulation.

