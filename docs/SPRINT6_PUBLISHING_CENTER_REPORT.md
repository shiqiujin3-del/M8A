# Sprint 6 Publishing Center Report

Date: 2026-07-06  
Module: Publishing Center MVP  
Status: Business foundation complete  
Auto Publishing: Disabled  
First Target: WordPress

## 1. Executive Summary

Sprint 6 establishes M8A's first production-oriented business module: Publishing Center.

The goal is not automatic publishing. The goal is an enterprise publishing pipeline that can safely move approved knowledge into controlled publishing jobs, starting with WordPress.

Sprint 6 completed:

1. Publishing Center module directory.
2. WordPress-first publishing target.
3. PostgreSQL publishing tables.
4. Publish target registry for future channels.
5. Dashboard publishing status metrics.
6. WordPress V1 publishing process definition.
7. Publish log foundation.

Not completed by design:

1. No social media connection.
2. No automatic publishing.
3. No WordPress credential connection.
4. No content generation workflow.
5. No publishing workflow execution.

## 2. Publishing Center Scope

Publishing Center is the unified enterprise publishing layer for:

| Channel | Sprint 6 Status |
|---|---|
| Website | WordPress target initialized |
| LinkedIn | Planned, not connected |
| Facebook | Planned, not connected |
| TikTok | Planned, not connected |
| YouTube | Planned, not connected |
| 微信公众号 | Planned, not connected |
| 视频号 | Planned, not connected |

Sprint 6 only prepares WordPress.

## 3. WordPress V1 Pipeline

The first Publishing Center pipeline is:

```text
Approved Knowledge
↓
Generate Article
↓
WordPress Draft
↓
Human Review
↓
Approve
↓
Publish
↓
Update Sitemap
↓
Record URL
↓
Write Publish Log
```

### Business Rules

1. Only approved knowledge may enter publishing.
2. Article generation creates drafts only.
3. WordPress entry starts as draft or pending review.
4. Human review is required before publish.
5. Publish URL must be recorded.
6. Every status change must be logged.
7. Social channels are out of scope for Sprint 6.

## 4. PostgreSQL Tables

Four publishing tables were created.

### 4.1 `publish_targets`

Purpose:

Central registry of publishing channels.

Key fields:

```text
target_id
target_name
channel
platform
status
automation_level
requires_human_approval
credentials_required
notes
created_at
updated_at
```

Current targets:

| Target | Platform | Status | Automation Level |
|---|---|---|---|
| WordPress Website | WordPress | active_for_sprint6 | draft_only_then_human_publish |
| LinkedIn | LinkedIn | planned | not_connected |
| Facebook | Facebook | planned | not_connected |
| TikTok | TikTok | planned | not_connected |
| YouTube | YouTube | planned | not_connected |
| 微信公众号 | WeChat Official Account | planned | not_connected |
| 视频号 | WeChat Channels | planned | not_connected |

### 4.2 `publish_jobs`

Purpose:

Track each publishing task from draft to published state.

Key fields:

```text
job_id
product_id
knowledge_record_id
knowledge_version
content_id
content_type
target_id
job_status
approval_status
wordpress_post_id
draft_url
final_url
reviewer
scheduled_at
approved_at
published_at
created_at
updated_at
```

Initial count:

```text
0
```

Reason:

HK620 currently has no approved article ready for WordPress publishing.

### 4.3 `publish_history`

Purpose:

Record status transitions for publishing jobs.

Key fields:

```text
history_id
job_id
from_status
to_status
actor
event_note
created_at
```

### 4.4 `publish_logs`

Purpose:

Store technical and business logs for publishing actions.

Key fields:

```text
log_id
job_id
target_id
log_level
log_event
log_message
metadata
created_at
```

Initial log:

```text
publishing_center_initialized
```

## 5. Dashboard Update

Dashboard file updated:

```text
apps/dashboard/index.html
```

New Publishing Center metrics:

| Metric | Current Value |
|---|---:|
| Draft | 0 |
| Pending Review | 0 |
| Approved | 0 |
| Published Today | 0 |
| Failed | 0 |
| Queued | 0 |

Dashboard also displays:

```text
V1 Target: WordPress Website
Pipeline: Approved Article → WordPress Draft → Human Review → Publish → Log
Auto Publish: Disabled
Social Channels: Planned / Not Connected
```

## 6. WordPress Readiness

WordPress is selected as the first production publishing target because it supports a safe human-approved process:

```text
Create draft
↓
Human review in WordPress
↓
Publish
↓
Record post URL
```

Required credentials before implementation:

1. WordPress URL.
2. WordPress user with editor or admin permission.
3. WordPress Application Password or approved auth method.
4. Permission to create media.
5. Permission to create draft posts.
6. Permission to publish after human approval.

## 7. Current Blocking Condition

Publishing Center is ready, but no publish job was created.

Reason:

HK620 knowledge and content are still review-pending. There is no `approved` HK620 article yet.

Required before first job:

1. HK620 knowledge approved.
2. HK620 article approved.
3. WordPress credentials configured.
4. Reviewer assigned.

## 8. Production Boundaries

Strictly not allowed in Sprint 6:

1. Direct auto-publishing.
2. Social media publishing.
3. Publishing review-pending HK620 founder interview content.
4. Publishing unapproved technical parameters.
5. Publishing price, profit, warranty, or delivery claims without approval.
6. Updating sitemap before content is published.
7. Recording final URL without a real published URL.

## 9. Next Step

First production path:

```text
HK620 Approved Article
↓
Create publish_jobs record
↓
Create WordPress Draft
↓
Human Review
↓
Approve
↓
Publish
↓
Update Sitemap
↓
Record URL
↓
Write Publish Log
```

## 10. Final Result

Sprint 6 result:

```text
PASS
```

Publishing Center MVP is established as a production business module foundation.

Current operational status:

```text
Ready for WordPress draft publishing after approved article and credentials are available.
```
