# M8A V1 Final Architecture Audit

Date: 2026-07-06

## Final Architecture

```text
CEO / 石总
  ↓
Commander Console V2
  ↓
Mission Control API
  ↓
PostgreSQL Mission Queue
  ↓
Worker Runner
  ↓
Capability Layer
  ↓
Artifacts / Approvals / Task Events
  ↓
Exception Framework on any runtime failure
  ↓
Infrastructure Operator
  ↓
Recovery Plan
  ↓
CEO Approval if needed
```

## Module Status

| Module | Status | Freeze Decision |
| --- | --- | --- |
| Commander Layer | Stable CEO entry | Freeze |
| Mission Control | PostgreSQL task center | Freeze |
| Worker Runner | Unified execution entry | Freeze |
| Capability Layer | Draft-first module pattern | Freeze interface, allow new modules |
| Exception Framework | Unified failure entry | Freeze |
| Approval | CEO approval center | Freeze |
| Dashboard | CEO Operating System | Freeze CEO Home |

## Dependency Model

```text
Dashboard
  → Mission Control API
    → commander_missions
    → commander_tasks
    → commander_artifacts
    → commander_approvals
    → commander_task_events
    → commander_exceptions
    → commander_exception_events
    → Worker Runner
      → Capability Layer
        → Exception Framework on failure
```

## Capability Access Standard

Any future Capability must:

1. Be placed under `apps/commander/capabilities/`.
2. Be called by Worker Runner, not directly by Dashboard.
3. Return structured artifact payloads.
4. Create approvals for public, customer-facing, or external actions.
5. Route exceptions to Exception Framework.
6. Never store credentials in code, logs, artifacts, or reports.
7. Never publish without explicit approval.

## Platform Connector Standard

Any future platform connector must follow:

```text
Credential from environment / secure config
  ↓
Draft-only or read-only first
  ↓
Artifact
  ↓
Approval
  ↓
Controlled external action only after approved policy exists
  ↓
Exception Framework on failure
```

## Exception Standard

All runtime failures must call:

```text
create_exception_from_failure()
```

Required source fields:

- source_mission_id
- source_task_id
- source_system
- error_message

Exception output:

- Exception Mission
- Exception Queue record
- Infrastructure Operator task
- Recovery Plan artifact
- CEO Approval if required

## Worker Standard

Workers are role configurations. They must not become independent uncontrolled services.

Worker output must be:

```text
Task Event + Artifact + Approval when needed
```

## Mission Lifecycle

```text
created
→ queued
→ claimed
→ running
→ completed / failed / waiting_approval
→ archived
```

Failure path:

```text
failed
→ Exception Mission
→ Infrastructure Operator
→ Recovery Plan
```

## Approval Lifecycle

```text
pending
→ approved / rejected / cancelled
```

Approval means decision permission only. It does not imply automatic publishing.

## Frozen Modules

The following modules are frozen for V1:

- Commander Console V2 CEO Home
- Mission Control core lifecycle
- PostgreSQL Mission Queue model
- Worker Runner execution entry
- Approval model
- Exception Framework runtime entry
- Website Capability Draft Only safety model

## Extensible Modules

The following areas may extend without changing V1 architecture:

- New Capabilities under Capability Layer
- New Platform Connectors under draft-first rules
- New Worker handler actions
- Mission Detail views
- Company Health real data sources
- Exception classifiers and recovery plan templates

## Forbidden Changes After Freeze

Do not:

- Restructure CEO Home.
- Add parallel task state stores.
- Add direct Dashboard-to-platform actions.
- Bypass Mission Control.
- Bypass Worker Runner.
- Bypass Approval for public/external actions.
- Bypass Exception Framework on failure.
- Store secrets in reports, artifacts, code, or logs.

## Final Decision

Architecture Freeze: YES

Reason:

The previous blocker was that Exception Framework existed but was not connected to runtime failures. Unified Runtime Integration V1 now routes Worker, Mission API, Capability, 401, 500, timeout, and Cloudflare failures into Exception Framework.

