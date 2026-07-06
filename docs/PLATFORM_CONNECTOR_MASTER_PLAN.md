# Platform Connector Master Plan

Date: 2026-07-06  
Project: M8A / Saiyu Daily Operating System  
Program: Platform Connector Center  
Status: Design only  
Scope: No development, no account connection, no credential creation

## 1. Executive Summary

M8A can become the control center for Saiyu's daily business operations, but the platforms should not be connected all at once.

The recommended strategy is:

1. Connect low-risk owned channels first.
2. Keep all public publishing behind human approval.
3. Use official APIs wherever possible.
4. Treat high-risk social and messaging platforms as semi-automatic until API access, app review, and compliance are confirmed.
5. Store all credentials centrally and never inside workflows, documents, or code.

Recommended first implementation:

```text
WordPress Draft Publishing
↓
Google Search Console
↓
GA4
↓
Gmail
↓
YouTube
↓
LinkedIn
↓
Facebook
↓
WhatsApp
↓
TikTok
↓
微信公众号
↓
视频号
↓
CRM
```

## Current Business Automation Readiness Baseline

Date: 2026-07-06  
Source: Operator input  
Status: Planning baseline, not a live system measurement

| Business Area | Current Readiness | Meaning |
|---|---:|---|
| 网站文章 | 90% | Article generation is close to usable; publishing still needs human review |
| 视频脚本 | 100% | Script generation capability is mature |
| WordPress | 40% | Connector plan exists; draft-to-publish pipeline is the next implementation priority |
| Facebook | 0% | No connector, credentials, or permission review yet |
| TikTok | 0% | No connector; API capability and semi-automation need evaluation |
| 客户回复 | 5% | Reply concept exists, but no real inquiry channel is connected |
| 售后 | 0% | No after-sales workflow; service FAQ and troubleshooting knowledge are missing |
| Overall Average | 34% | Business automation is content-ready but platform/customer automation is still early |

Current interpretation:

1. M8A's strongest production capability is content drafting.
2. The highest-return next step is WordPress, because it converts existing article capability into visible website output.
3. Facebook and TikTok should not be started before WordPress is stable.
4. Customer reply and after-sales should wait until product knowledge, service FAQ, and inquiry channels are connected.

## 2. Platform Connector Center

Platform Connector Center is the unified control layer for all external business platforms.

It should manage:

1. Platform registry.
2. Credential registry.
3. Permission scope.
4. Connection status.
5. API quota and rate limits.
6. Human approval requirements.
7. Publish logs.
8. Error logs.
9. Security review.
10. MVP rollout priority.

## 3. Operating Principles

### 3.1 Approval Modes

| Mode | Meaning | Allowed Platforms |
|---|---|---|
| Draft Only | M8A creates draft, human publishes manually | All platforms |
| Human Approved Publishing | M8A publishes after explicit approval | WordPress, YouTube, LinkedIn, Facebook after verification |
| Fully Automated Low-Risk Tasks | M8A runs non-public or low-risk actions automatically | Search Console reads, GA4 reads, internal logs |

### 3.2 Credential Principles

Credentials must be:

1. Stored in `.env` or secure credential storage.
2. Referenced by credential name, never by raw value.
3. Scoped to the minimum required permission.
4. Rotated when staff changes.
5. Audited by platform and owner.

Do not store:

1. API keys in workflow JSON.
2. OAuth tokens in Markdown docs.
3. Passwords in Dashboard HTML.
4. Personal account cookies.

## 4. Master Platform Matrix

| Platform | Official API | Full Automation | Recommended Mode | MVP Priority |
|---|---|---|---|---|
| WordPress | Yes | Yes, but publish should require approval | Human Approved Publishing | P0 |
| Google Search Console | Yes | Yes for data reads; sitemap actions require caution | Fully automated read-only | P1 |
| GA4 | Yes | Yes for analytics reads | Fully automated read-only | P1 |
| Gmail | Yes | Yes technically; replies should require approval | Draft reply / approved send | P2 |
| YouTube | Yes | Yes technically; upload/public publish needs approval and quota | Draft/upload private or unlisted first | P3 |
| LinkedIn | Yes, restricted permissions | Yes after app approval | Human Approved Publishing | P4 |
| Facebook | Yes, permissions/app review required | Yes after approval | Human Approved Publishing | P5 |
| WhatsApp | Yes via Cloud API | Semi/full depending message type | Human approved for sales/support replies | P6 |
| TikTok | Yes, Content Posting API | Possible after app/scope/audit; evaluate carefully | Semi-automatic first | P7 |
| 微信公众号 | Yes, Chinese official account API | Possible with verified account and permissions | Semi-automatic first | P8 |
| 视频号 | Official API availability must be account-verified | Likely limited/permissioned | Evaluation first | P9 |
| CRM | Depends on chosen CRM | Depends on vendor | Reserved | P10 |

## 5. Platform Details

## 5.1 WordPress

Business use:

1. Create article drafts.
2. Upload media.
3. Update post status after approval.
4. Record published URL.
5. Trigger sitemap/index checks.

Official API:

Yes. WordPress REST API supports post listing, creation, update, and statuses such as `draft`, `pending`, `publish`, `future`, and `private`.

Automation level:

```text
Can be full automatic technically.
M8A should use Human Approved Publishing.
```

Login method:

1. WordPress Application Password.
2. OAuth/JWT plugin only if required by site policy.
3. Dedicated service user, not personal admin account.

Credential management:

```text
WORDPRESS_BASE_URL
WORDPRESS_USERNAME
WORDPRESS_APPLICATION_PASSWORD
WORDPRESS_DEFAULT_AUTHOR_ID
```

Rate limits:

WordPress core does not define one universal SaaS rate limit; actual limits depend on hosting, WAF, security plugin, and server capacity.

Risks:

1. Accidental public publishing.
2. Wrong category/tag.
3. SEO metadata plugin mismatch.
4. Media upload failure.
5. Duplicated slug.

Human approval points:

1. Product facts.
2. Public claims.
3. Title and meta.
4. Images and videos.
5. Publish action.

MVP:

```text
HK620 Approved Article → WordPress Draft → Human Approve → Publish → Record URL
```

## 5.2 Google Search Console

Business use:

1. Search performance.
2. Keyword opportunities.
3. URL indexing status.
4. Sitemap status.
5. Content gap detection.

Official API:

Yes. Search Console API supports Search Analytics queries. URL Inspection API and sitemap endpoints support indexing and sitemap status workflows.

Automation level:

```text
Full automation for read-only reports.
Manual review before making SEO decisions.
```

Login method:

1. Google OAuth.
2. Verified Search Console property.
3. Google Cloud project with APIs enabled.

Credential management:

```text
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REFRESH_TOKEN
SEARCH_CONSOLE_SITE_URL
```

Required scopes:

```text
https://www.googleapis.com/auth/webmasters.readonly
https://www.googleapis.com/auth/webmasters
```

Use read-only first.

Rate limits:

Google APIs use quotas. Exact quota must be checked in Google Cloud Console per project/API.

Risks:

1. Wrong property selected.
2. Domain property vs URL-prefix mismatch.
3. Misreading low-volume keyword data.
4. Assuming indexing is guaranteed after sitemap submission.

Human approval points:

1. SEO task priority.
2. Content creation decision.
3. Sitemap submission permission.

MVP:

```text
Daily Search Console Pull → Keyword Movement → Content Gap → Daily Brief
```

## 5.3 GA4

Business use:

1. Website visits.
2. Source/medium.
3. Landing pages.
4. Conversion events.
5. Daily business KPI.

Official API:

Yes. Google Analytics Data API supports GA4 report access.

Automation level:

```text
Full automation for read-only analytics.
```

Login method:

1. Google OAuth.
2. Service account if the GA4 property grants access.
3. Google Cloud project with Analytics Data API enabled.

Credential management:

```text
GA4_PROPERTY_ID
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REFRESH_TOKEN
```

Rate limits:

GA4 Data API has property/project quota limits. Must be tracked per property.

Risks:

1. Wrong GA4 property.
2. Missing conversion events.
3. Bot/internal traffic pollution.
4. Privacy/compliance limitations.

Human approval points:

1. KPI interpretation.
2. Lead attribution.
3. Conversion definition.

MVP:

```text
Daily GA4 Pull → Visits / Landing Pages / Conversions → Daily Brief
```

## 5.4 Facebook

Business use:

1. Publish Page posts.
2. Publish images/videos where permitted.
3. Read Page performance.
4. Track campaign content.

Official API:

Yes, via Meta Graph API and Pages API, but permissions and app review are required.

Automation level:

```text
Possible after app review.
Recommended semi-automatic first.
```

Login method:

1. Meta Developer App.
2. Facebook Login.
3. Page access token.
4. Business Manager permissions.

Credential management:

```text
META_APP_ID
META_APP_SECRET
FACEBOOK_PAGE_ID
FACEBOOK_PAGE_ACCESS_TOKEN
```

Rate limits:

Meta Graph API applies app/page-level limits. Exact values depend on app status, usage, and permissions.

Risks:

1. Permission approval delays.
2. Token expiration.
3. Content policy violations.
4. Page role mismatch.
5. Unexpected API version changes.

Human approval points:

1. Product claims.
2. Images/videos.
3. Public post copy.
4. Final publish.

MVP:

```text
Approved Social Draft → Facebook Draft Queue → Human Copy/Paste or API Publish after approval
```

## 5.5 LinkedIn

Business use:

1. Publish company page posts.
2. Publish article links.
3. Publish images/videos/documents.
4. Track B2B content distribution.

Official API:

Yes. LinkedIn Posts API supports organic and sponsored posts, but permissions are restricted and require correct organization roles.

Automation level:

```text
Possible after permissions are approved.
Recommended Human Approved Publishing.
```

Login method:

1. LinkedIn Developer App.
2. OAuth 2.0.
3. Organization admin/content admin role.

Credential management:

```text
LINKEDIN_CLIENT_ID
LINKEDIN_CLIENT_SECRET
LINKEDIN_ORGANIZATION_URN
LINKEDIN_REFRESH_TOKEN
```

Required permissions:

1. `w_organization_social`.
2. `r_organization_social`.
3. `w_member_social` if member posting is required.

Rate limits:

LinkedIn applies API throttles and product access limitations. Exact limits depend on approved product and app.

Risks:

1. Restricted permissions.
2. Organization role mismatch.
3. API version header requirement.
4. Asset upload flow complexity for images/videos.

Human approval points:

1. B2B claim review.
2. Brand tone.
3. Public release.

MVP:

```text
Approved LinkedIn Draft → Human Review → Company Page Post
```

## 5.6 YouTube

Business use:

1. Upload product videos.
2. Set title/description/tags.
3. Schedule publish.
4. Track video IDs and URLs.

Official API:

Yes. YouTube Data API supports video upload through `videos.insert`.

Automation level:

```text
Technically yes.
Recommended: upload private/unlisted first, public publish only after human approval.
```

Login method:

1. Google OAuth.
2. YouTube channel authorization.
3. Google Cloud project.

Credential management:

```text
YOUTUBE_CLIENT_ID
YOUTUBE_CLIENT_SECRET
YOUTUBE_REFRESH_TOKEN
YOUTUBE_CHANNEL_ID
```

Required scope:

```text
https://www.googleapis.com/auth/youtube.upload
```

Rate limits:

YouTube Data API uses quota. Official upload method has defined upload quota behavior; project audit may be required to lift private-only restrictions for unverified projects.

Risks:

1. Unverified API project uploads restricted to private visibility.
2. Copyright or music claims.
3. Wrong made-for-kids setting.
4. Synthetic media disclosure.
5. Public publishing before review.

Human approval points:

1. Video content.
2. Product claim.
3. Title/description.
4. Thumbnail.
5. Publish visibility.

MVP:

```text
Approved Video Asset → Upload Private/Unlisted → Human Approve → Schedule Publish
```

## 5.7 TikTok

Business use:

1. Publish short videos.
2. Publish photo posts where supported.
3. Check publish status.
4. Track content URLs.

Official API:

Yes. TikTok Content Posting API supports direct posting, but app approval, user authorization, domain verification, and audit restrictions apply.

Automation level:

```text
Potentially full automatic after approval and audit.
Recommended semi-automatic first.
```

Login method:

1. TikTok Developer App.
2. OAuth authorization.
3. Approved `video.publish` scope.
4. Target user authorization.

Credential management:

```text
TIKTOK_CLIENT_KEY
TIKTOK_CLIENT_SECRET
TIKTOK_ACCESS_TOKEN
TIKTOK_OPEN_ID
```

Rate limits:

TikTok applies API limits by endpoint/app/user. Exact limits must be checked after app registration and product approval.

Risks:

1. App review/audit.
2. Unaudited clients may be restricted to private visibility.
3. Video format restrictions.
4. Commercial content compliance.
5. Music/copyright issues.

Human approval points:

1. Video script.
2. Final video.
3. Caption and hashtags.
4. Commercial/product claims.
5. Final publish.

MVP:

```text
Approved Short Video Script → Manual Video Creation → TikTok Draft/Manual Publish
```

## 5.8 微信公众号

Business use:

1. Publish Chinese articles.
2. Manage drafts.
3. Push approved content.
4. Track article URLs.

Official API:

Yes, for verified official accounts with correct permissions. Final availability depends on account type and platform permissions.

Automation level:

```text
Possible, but recommended semi-automatic first.
```

Login method:

1. 微信公众平台账号.
2. AppID / AppSecret.
3. Access token.
4. IP whitelist if required.

Credential management:

```text
WECHAT_OFFICIAL_APP_ID
WECHAT_OFFICIAL_APP_SECRET
WECHAT_OFFICIAL_ACCESS_TOKEN
```

Rate limits:

WeChat APIs have access token and endpoint limits. Exact values must be confirmed in the account console and official docs.

Risks:

1. Account type limitation.
2. IP whitelist.
3. Content review/policy rejection.
4. Token expiration.
5. Chinese copy compliance.

Human approval points:

1. Chinese article.
2. Product claims.
3. Images.
4. Final push/publish.

MVP:

```text
Approved Chinese Article → 公众号 Draft → Human Review → Manual Publish
```

## 5.9 视频号

Business use:

1. Publish short product videos.
2. Track content.
3. Support Chinese-market video operations.

Official API:

Requires account-level verification. Public automation support may be limited and permissioned. Treat as evaluation until Saiyu's account confirms available APIs.

Automation level:

```text
Evaluation required.
Assume semi-automatic until proven otherwise.
```

Login method:

1. 视频号/微信生态 account login.
2. Official platform permissions if available.
3. Possible manual publish workflow.

Credential management:

```text
WECHAT_CHANNELS_ACCOUNT_ID
WECHAT_CHANNELS_APP_ID
WECHAT_CHANNELS_APP_SECRET
```

Rate limits:

Unknown until account/API access is confirmed.

Risks:

1. API may not support the needed publishing workflow.
2. High platform policy sensitivity.
3. Manual mobile approval may be required.
4. Content review risk.

Human approval points:

1. Video script.
2. Final video.
3. Caption.
4. Publish timing.

MVP:

```text
Approved Video Script → Manual Video Creation → 视频号 Manual Publish Checklist
```

## 5.10 Gmail

Business use:

1. Read business inquiries.
2. Draft replies.
3. Send approved replies.
4. Label customer messages.
5. Feed CRM later.

Official API:

Yes. Gmail API supports creating and sending email messages.

Automation level:

```text
Technically full automation.
Recommended draft-only or approved-send for customers.
```

Login method:

1. Google OAuth.
2. Workspace account authorization.
3. Domain-wide delegation only if Saiyu uses Google Workspace and approves it.

Credential management:

```text
GMAIL_CLIENT_ID
GMAIL_CLIENT_SECRET
GMAIL_REFRESH_TOKEN
GMAIL_SENDER_ACCOUNT
```

Required scopes:

Use least privilege first:

```text
gmail.readonly
gmail.compose
gmail.send
```

Rate limits:

Gmail API and Google Workspace mail sending limits apply. Exact quotas depend on account type.

Risks:

1. Sending wrong reply.
2. Exposing confidential pricing.
3. Spam/compliance issues.
4. Misclassifying customer intent.

Human approval points:

1. Sales quote.
2. Technical promise.
3. Price/payment/shipping.
4. Customer complaint.
5. New or high-value customer.

MVP:

```text
Read Inquiry → Retrieve Product Knowledge → Generate Reply Draft → Human Approve → Send
```

## 5.11 WhatsApp

Business use:

1. Receive customer messages.
2. Generate reply drafts.
3. Send approved replies.
4. Escalate high-intent leads.

Official API:

Yes, through WhatsApp Business Platform / Cloud API.

Automation level:

```text
Possible for approved templates and session replies.
Recommended human-approved replies first.
```

Login method:

1. Meta Business account.
2. WhatsApp Business Account.
3. Phone number registration.
4. Cloud API token.

Credential management:

```text
WHATSAPP_BUSINESS_ACCOUNT_ID
WHATSAPP_PHONE_NUMBER_ID
WHATSAPP_ACCESS_TOKEN
WHATSAPP_VERIFY_TOKEN
```

Rate limits:

WhatsApp applies messaging limits, quality ratings, template approval, and conversation windows.

Risks:

1. Template rejection.
2. Sending outside allowed window.
3. Account quality downgrade.
4. Customer privacy issues.
5. Wrong technical/sales response.

Human approval points:

1. Quote.
2. Technical promise.
3. Complaint.
4. After-sales issue.
5. High-intent lead.

MVP:

```text
Incoming WhatsApp → Classify → Draft Reply → Human Approve → Send
```

## 5.12 CRM

Business use:

1. Store leads.
2. Track customer status.
3. Record conversations.
4. Create tasks.
5. Trigger follow-up.

Official API:

Depends on the CRM selected.

Automation level:

```text
Reserved.
Can be full automation after CRM is chosen.
```

Login method:

Depends on vendor:

1. API key.
2. OAuth.
3. Private app token.

Credential management:

```text
CRM_PROVIDER
CRM_BASE_URL
CRM_API_KEY
CRM_CLIENT_ID
CRM_CLIENT_SECRET
```

Rate limits:

Depends on CRM vendor.

Risks:

1. Duplicate leads.
2. Wrong owner assignment.
3. Poor data hygiene.
4. Privacy/compliance risk.

Human approval points:

1. Lead qualification rules.
2. Deal stage changes.
3. Sales ownership.
4. Deleting/merging records.

MVP:

```text
Manual CRM Selection → Lead Schema → Inquiry Capture → Follow-up Task
```

## 6. Recommended Implementation Order

### P0: WordPress

Reason:

1. Highest direct business value.
2. Owned channel.
3. Official API is mature.
4. Fits current Publishing Center.
5. Can start with draft-only mode.

MVP:

```text
Approved HK620 Article → WordPress Draft → Human Approval → Publish → URL Log
```

### P1: Google Search Console

Reason:

1. Drives Daily Brief.
2. Gives real keyword opportunities.
3. Low risk because first phase is read-only.

MVP:

```text
Daily Search Analytics Pull → Keyword Movement → Content Gap
```

### P1: GA4

Reason:

1. Gives real website traffic data.
2. Improves Growth Score and boss dashboard.
3. Low risk read-only integration.

MVP:

```text
Daily GA4 Pull → Visits / Landing Pages / Conversions
```

### P2: Gmail

Reason:

1. Starts customer automation safely.
2. Draft-only mode reduces risk.
3. Can feed future CRM.

MVP:

```text
Customer Email → Product Knowledge Retrieval → Reply Draft
```

### P3: YouTube

Reason:

1. Strong product-media value.
2. Official upload API exists.
3. Can upload private/unlisted first.

MVP:

```text
Approved Video → Upload Private/Unlisted → Human Approve → Publish
```

### P4: LinkedIn

Reason:

1. B2B value.
2. API exists.
3. Permissions are more complex than owned channels.

MVP:

```text
Approved LinkedIn Draft → Human Approve → Company Page Publish
```

### P5: Facebook

Reason:

1. Useful distribution channel.
2. Requires Meta app permissions.
3. Should follow after content governance is stable.

MVP:

```text
Approved Facebook Draft → Human Approve → Publish
```

### P6: WhatsApp

Reason:

1. High customer value.
2. High risk if wrong replies are sent.
3. Template/session rules need careful setup.

MVP:

```text
Incoming Message → Reply Draft → Human Approve
```

### P7: TikTok

Reason:

1. High reach potential.
2. API exists but app approval/audit makes it less predictable.
3. Video production workflow must mature first.

MVP:

```text
Approved Script → Manual Video → Manual/Semi-Auto TikTok Publish
```

### P8: 微信公众号

Reason:

1. Important Chinese content channel.
2. Requires account verification and platform-specific operations.
3. Chinese article approval workflow must be stable first.

MVP:

```text
Approved Chinese Article → 公众号 Draft → Human Publish
```

### P9: 视频号

Reason:

1. Important Chinese video channel.
2. API automation capability must be verified inside the actual account.

MVP:

```text
Approved Video Script → Manual Video → 视频号 Checklist
```

### P10: CRM

Reason:

1. CRM should be chosen after inquiry sources are clear.
2. Avoid building around the wrong CRM.

MVP:

```text
Define Lead Schema → Choose CRM → Connect Inquiry Sources
```

## 7. Credential Registry Design

Recommended registry fields:

| Field | Purpose |
|---|---|
| platform_id | wordpress, ga4, search_console, etc. |
| credential_name | Human-readable credential alias |
| credential_type | API key, OAuth, token, app password |
| owner | Internal owner |
| scopes | Permissions granted |
| environment | dev, staging, prod |
| expires_at | Token expiration |
| rotation_policy | Rotation cadence |
| last_tested_at | Last successful connection test |
| status | missing, configured, valid, expired, revoked |

## 8. Connector Status Model

Each connector should use the same lifecycle:

```text
planned
↓
credentials_required
↓
credentials_configured
↓
read_test_passed
↓
write_test_passed
↓
human_approval_enabled
↓
production_ready
↓
paused
```

## 9. Risk Controls

Mandatory controls:

1. No public publish without human approval.
2. No customer reply without human approval in MVP.
3. Read-only mode before write mode.
4. Separate test credential from production credential.
5. Every external action must write a log.
6. Every public output must store source knowledge version.
7. Every platform must have a rollback/manual fallback.

## 10. Source References

Official references checked for this plan:

1. WordPress REST API Posts: https://developer.wordpress.org/rest-api/reference/posts/
2. Google Search Console Search Analytics API: https://developers.google.com/webmaster-tools/v1/how-tos/search_analytics
3. Google Analytics Data API: https://developers.google.com/analytics/devguides/reporting/data/v1
4. YouTube Data API videos.insert: https://developers.google.com/youtube/v3/docs/videos/insert
5. Gmail API sending guide: https://developers.google.com/workspace/gmail/api/guides/sending
6. LinkedIn Posts API: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api
7. TikTok Content Posting API: https://developers.tiktok.com/doc/content-posting-api-get-started/
8. Meta developer documentation should be rechecked inside the Meta developer account before implementation.
9. WeChat official account and video account API documentation should be rechecked inside Saiyu's verified account before implementation.

## 11. Final Recommendation

M8A should not start with social media automation.

The safest and highest-value order is:

```text
1. WordPress Draft Publishing
2. Search Console Daily Data
3. GA4 Daily Data
4. Gmail Reply Drafts
5. YouTube Private/Unlisted Upload
6. LinkedIn Approved Publish
7. Facebook Approved Publish
8. WhatsApp Draft Reply
9. TikTok Semi-Automatic Publishing
10. 微信公众号 Draft Publishing
11. 视频号 Manual/Semi-Automatic Publishing
12. CRM Integration
```

This order lets M8A become the business control layer without creating unnecessary account, compliance, or public publishing risk.
