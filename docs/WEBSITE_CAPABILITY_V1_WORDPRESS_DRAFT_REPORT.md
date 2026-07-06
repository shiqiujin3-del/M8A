# M8A Website Capability V1: WordPress Draft Only Report

Date: 2026-07-06

## Scope

Website Operator was upgraded from simulated WordPress payload generation to a dedicated Website Capability that can create WordPress drafts when credentials are configured.

Commander Console CEO Home was not restructured.

## Files Modified

- apps/commander/mission-control/worker_runner.py
- apps/commander/mission-control/README.md
- apps/dashboard/index.html

## Files Added

- apps/commander/capabilities/website/wordpress_draft.py
- apps/commander/mission-control/migrations/004_website_capability_v1.sql
- docs/WEBSITE_CAPABILITY_V1_WORDPRESS_DRAFT_REPORT.md

## Migration

`004_website_capability_v1.sql` extends `commander_artifacts.artifact_type` to allow:

```text
wordpress_draft
```

No existing records are removed.

## Website Capability

Location:

```text
apps/commander/capabilities/website/
```

Responsibilities:

1. Generate WordPress draft payload.
2. Validate draft payload.
3. Call WordPress REST API only when environment variables are configured.
4. Save draft result as artifact.
5. Create CEO approval.
6. Never publish.

## Required Environment Variables

```text
M8A_WORDPRESS_BASE_URL
M8A_WORDPRESS_USERNAME
M8A_WORDPRESS_APP_PASSWORD
```

No credential values are written to code, logs, artifacts, or reports.

## Draft Rules

The capability creates a WordPress post draft:

- status: draft
- title: HK620 Skeleton Door Strip Processing for the USA Market
- slug: hk620-skeleton-door-strip-processing-usa
- meta title: HK620 Skeleton Door Strip Processing | Saiyu
- meta description: HK620 skeleton door strip processing solution for factories targeting efficient grooved profile and edge banding preparation.
- content: 735 English words with H2 structure and Draft Review Required label.

## Approval Rules

Created approval:

- platform: WordPress
- action_type: review_wordpress_draft
- risk_level: medium
- status: pending

Approve:

- approval status becomes approved
- WordPress remains draft
- no publish API call

Reject:

- approval status becomes rejected
- WordPress draft is not deleted

## Safety Protection

Hard protections:

1. Reject payloads where `status != draft`.
2. Block publish/delete markers.
3. Only POST draft creation is implemented.
4. No DELETE implementation exists.
5. No publish implementation exists.
6. No update-published-content implementation exists.
7. Existing task artifacts are reused to prevent duplicate draft creation.

## Test Report

Test input:

```text
今天重点做 HK620，美国市场。
```

Test mode:

```text
WordPress environment variables intentionally unset.
```

Observed:

| Check | Result |
| --- | --- |
| Mission created | PASS |
| Website Operator executed by Runner | PASS |
| WordPress missing config did not crash | PASS |
| Local draft payload created | PASS |
| Task event written | PASS |
| Dashboard-readable message | PASS |
| Approval created | PASS |
| Approval action | review_wordpress_draft |
| Approval risk | medium |
| Approve does not publish | PASS |
| Duplicate run does not duplicate artifact / approval | PASS |
| n8n connection | None |
| Social connection | None |
| Auto publish | None |

Observed Website Operator output:

```text
task status: waiting_approval
artifact_type: draft_payload
simulation_status: waiting_config
message: WordPress 未配置，当前仅生成本地 Draft Payload。
approval: WordPress / review_wordpress_draft / medium / pending
event: wordpress_config_missing
```

Approve test:

```text
approval_status: approved
artifact_status: waiting_config
publish: false
```

Idempotency test:

```text
Before duplicate run: artifacts 7, approvals 3
After duplicate run:  artifacts 7, approvals 3
```

## Not Tested

Real WordPress draft creation was not executed in this test because WordPress environment variables were intentionally unset.

When credentials are added, the same capability will call:

```text
POST /wp-json/wp/v2/posts
```

with:

```text
status=draft
```

## Current Risks

1. Real WordPress API permissions still need live verification.
2. WordPress meta fields may require site-side registration to store custom SEO metadata.
3. The current content is deterministic draft text, not final approved marketing copy.
4. Task status enum does not include `waiting_config`; configuration wait is represented by artifact `simulation_status=waiting_config` and task event `wordpress_config_missing`.

## Next Stage Recommendation

Before connecting real WordPress credentials:

1. Confirm WordPress application password permissions.
2. Test draft creation on a staging WordPress site.
3. Add a Mission-scoped run-once button so Website Operator can be tested without touching older queued tasks.
4. Keep publish disabled until a separate Publishing Approval phase is approved.

