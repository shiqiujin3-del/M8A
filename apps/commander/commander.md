# Commander Gateway

Version: V1  
Status: initialized  
Date: 2026-07-06  
Purpose: M8A single command entry

## Role

Commander Gateway is the only command entry for M8A.

All digital employees, workflows, and platform connectors must receive work through Commander Gateway.

## Control Rule

```text
Human / Boss Request
↓
Commander Gateway
↓
Mission Queue
↓
Dispatcher
↓
Digital Employee / Workflow / Connector
↓
Result Log
↓
Daily Brief
```

## Digital Employees

Commander Gateway can dispatch tasks to:

1. Content Operator.
2. Knowledge Manager.
3. Website Operator.
4. Distribution Operator.
5. Sales Assistant.
6. Business Analyst.

## Mission Status

Allowed mission status:

1. planned.
2. queued.
3. running.
4. needs_human_review.
5. completed.
6. failed.
7. archived.
8. paused.
9. cancelled.

## Safety Rules

1. Commander Gateway does not publish directly.
2. Commander Gateway does not bypass human review.
3. Commander Gateway does not store raw credentials.
4. Commander Gateway does not create new platforms.
5. Commander Gateway only dispatches to existing M8A capabilities.

## Current Mission

```text
HK620_US_GROWTH
```

Status:

```text
archived
```
