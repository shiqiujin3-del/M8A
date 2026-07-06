# Sprint 5 Automation Feasibility Plan

Date: 2026-07-06  
Scope: Publishing and Customer Automation Feasibility  
Status: Planning only  
Implementation: Not started

## 1. Executive Answer

M8A can support website publishing automation, video publishing preparation, customer reply drafting, and after-sales assistance.

However, M8A should not move directly to full automation.

Recommended rollout:

```text
Knowledge Approved
↓
Draft Created
↓
Human Review
↓
Platform Draft / Scheduled Item
↓
Human Publish Approval
↓
Publish
↓
URL / Result Logged
```

Best Sprint 6 MVP:

```text
HK620 Approved Article
↓
WordPress Draft
↓
Human Approve
↓
Publish
```

Reason:

WordPress has mature REST APIs for media and posts, supports draft and publish statuses, and allows URL recording after post creation. This fits M8A's current review-first knowledge governance.

## 2. Website Publishing Automation

### 2.1 Feasibility

Website publishing automation is highly feasible.

Recommended first target:

```text
WordPress
```

WordPress REST API supports:

1. Creating posts.
2. Updating posts.
3. Setting status such as `draft`, `pending`, `future`, and `publish`.
4. Uploading media.
5. Returning post IDs and links.

### 2.2 Automation Flow

```text
Approved Product Knowledge
↓
Generate Article Draft
↓
Generate Metadata
↓
Upload Media
↓
Create WordPress Draft
↓
Human Review In WordPress
↓
Publish
↓
Submit / refresh sitemap
↓
Record URL
↓
Track GA4 / Search Console
```

### 2.3 Auto Upload Materials

Can be automated for:

1. Product images.
2. PDFs.
3. Article images.
4. Download files.

Recommended rule:

Only approved source files may be uploaded.

### 2.4 Auto Generate Articles

Feasible, but should be review-gated.

Allowed:

1. Generate article draft from approved product knowledge.
2. Generate FAQ blocks.
3. Generate meta title.
4. Generate meta description.
5. Generate internal link suggestions.

Not allowed without review:

1. New technical claims.
2. Price claims.
3. Delivery claims.
4. Warranty claims.
5. Industry-first claims.
6. Customer case claims.

### 2.5 Auto Publish To WordPress

Technically feasible.

Recommended modes:

| Mode | Feasibility | Recommendation |
|---|---|---|
| Create WordPress draft | High | Sprint 6 MVP |
| Create pending review post | High | Good after role setup |
| Schedule post | High | Use after review process is stable |
| Direct publish | High technically, risky operationally | Not recommended initially |

### 2.6 Auto Update Sitemap

Feasible in two ways:

1. WordPress SEO plugin or native sitemap updates after publish.
2. Search Console API can submit sitemap URLs and read sitemap status.

Recommended:

Use WordPress-generated sitemap first. Use Search Console API later for sitemap submit and status checks.

### 2.7 Auto Record URL

Feasible.

M8A should record:

```text
product_id
knowledge_version
content_id
wordpress_post_id
post_status
url
publish_time
reviewer
```

### 2.8 Risks And Human Review Points

Risks:

1. Publishing unapproved facts.
2. SEO duplication.
3. Wrong product parameters.
4. Wrong media.
5. Broken formatting.
6. Unauthorized public claims.

Human review required before:

1. Publishing.
2. Updating existing product pages.
3. Adding specs.
4. Adding customer cases.
5. Using founder interview content publicly.

## 3. Video Publishing Automation

### 3.1 Feasibility

Video automation should be split into two layers:

1. Content preparation automation.
2. Platform publishing automation.

Content preparation is feasible now:

1. Generate video script.
2. Generate title.
3. Generate caption.
4. Generate cover text.
5. Generate platform-specific variants.
6. Generate publishing checklist.

Platform publishing varies by platform.

### 3.2 Platform Support

| Platform | API Auto Publish Feasibility | Recommendation |
|---|---|---|
| YouTube | High | API upload and scheduling can be automated after OAuth approval |
| TikTok | Medium to High | Content Posting API can support direct posting for approved apps/accounts |
| Facebook | Medium to High | Page publishing and video publishing can be automated with Meta permissions |
| 抖音 | Medium / uncertain | Treat as semi-automatic until official account/API access is confirmed |
| 视频号 | Low to Medium | Treat as semi-automatic unless verified official API access is available |

### 3.3 Auto Generate Video Script

Feasible.

M8A can generate:

1. English short video script.
2. Chinese short video script.
3. Scene-by-scene script.
4. Voiceover.
5. On-screen text.
6. CTA.

Rule:

Only approved product knowledge may be used for factual statements.

### 3.4 Auto Generate Title And Cover Copy

Feasible.

Examples of safe generated fields:

```text
title
subtitle
cover text
caption
hashtags
thumbnail copy
```

Must avoid:

1. Unsupported performance claims.
2. Price claims.
3. Industry-first claims.
4. Customer identity claims.

### 3.5 Auto Schedule Publishing

Feasible for platforms with official scheduling/upload support.

Recommended approach:

```text
Generate platform draft
↓
Human review
↓
Create scheduled item where API allows
↓
Human final publish approval
```

### 3.6 API Auto Publish vs Semi-Auto

| Platform | Auto Publish | Semi-Auto Needed |
|---|---|---|
| YouTube | Yes, with YouTube Data API and OAuth | Human review still required |
| TikTok | Possible through Content Posting API if app/account approved | Required if account/API not approved |
| Facebook | Possible for Pages with Meta Graph API permissions | Required for personal accounts or missing permissions |
| 抖音 | Needs official open platform confirmation | Recommended initially |
| 视频号 | Needs official channel/API confirmation | Recommended initially |

### 3.7 Risks And Review Points

Risks:

1. Platform policy violations.
2. Wrong claims in captions.
3. Misleading thumbnails.
4. Unapproved customer/video footage.
5. Music/copyright problems.
6. Duplicate content.

Human review required before:

1. Uploading video.
2. Publishing video.
3. Using customer footage.
4. Using founder interview claims.
5. Claiming machine performance.

## 4. Customer Reply Automation

### 4.1 Feasibility

Customer reply automation is feasible, but should start as reply drafting.

Recommended initial mode:

```text
Customer Question
↓
Intent Classification
↓
Product Knowledge Retrieval
↓
Reply Draft
↓
Human Review
↓
Send
```

### 4.2 Auto Identify Customer Questions

Feasible categories:

1. Product inquiry.
2. Technical specification request.
3. Price inquiry.
4. Delivery inquiry.
5. Warranty inquiry.
6. Service issue.
7. Dealer / distributor inquiry.
8. Unknown / unclear.

### 4.3 Auto Retrieve Product Knowledge

Feasible using:

1. PostgreSQL product metadata.
2. Qdrant product chunks.
3. Approved Golden Knowledge.
4. Approved FAQ.
5. Approved service documents.

Rule:

If knowledge status is not approved, response must say information needs confirmation or must route to human.

### 4.4 Auto Generate Reply Draft

Feasible.

Safe draft topics:

1. Basic product description from approved knowledge.
2. Request for missing customer requirements.
3. Send approved product page link.
4. Send approved catalog.
5. Ask clarifying questions.

### 4.5 Questions That Can Be Auto-Replied

Only after approved knowledge exists:

1. What is HK620?
2. What process does HK620 support?
3. Which approved materials can I read?
4. Can you send a catalog?
5. Can I talk to sales?
6. Basic intake questions.

### 4.6 Questions That Must Transfer To Human

Must transfer:

1. Price.
2. Discount.
3. Delivery time.
4. Contract terms.
5. Warranty.
6. Installation plan.
7. Custom machine request.
8. Complaint.
9. Safety issue.
10. Serious machine fault.
11. Customer data deletion/privacy request.
12. Any unapproved knowledge area.

### 4.7 Channel Integration

| Channel | Integration Method | Automation Level |
|---|---|---|
| WhatsApp | WhatsApp Business Platform / Cloud API | Draft now, later controlled auto reply |
| 微信 | WeChat Official Account / WeCom depending account type | Semi-auto initially |
| Website Form | Form webhook to n8n / CRM | High |
| Email | IMAP/SMTP or provider API | High |

Recommended start:

Website form and email first. WhatsApp second. WeChat after account/API capabilities are confirmed.

## 5. After-Sales Automation

### 5.1 Feasibility

After-sales automation is feasible as support triage and troubleshooting draft generation.

It should not replace service engineers for high-risk faults.

### 5.2 Auto Identify Fault Type

Possible categories:

1. Feeding issue.
2. Edge banding issue.
3. Grooving issue.
4. Cutting issue.
5. Glue issue.
6. Electrical issue.
7. Pneumatic issue.
8. Safety issue.
9. Unknown issue.

### 5.3 Auto Generate Troubleshooting Steps

Feasible only when approved service knowledge exists.

Output should be:

1. Step-by-step draft.
2. Safety warning.
3. Required photos/videos from customer.
4. Escalation rule.
5. Related document/video recommendation.

### 5.4 Auto Recommend Videos / Documents

Feasible after approved materials exist:

1. Product manual.
2. Service FAQ.
3. Troubleshooting video.
4. Operation video.
5. Maintenance checklist.

### 5.5 Auto Create Service Ticket

Feasible.

Ticket fields:

```text
customer_name
contact_channel
machine_model
serial_number
fault_type
description
photos
videos
urgency
assigned_person
status
created_at
```

### 5.6 Must Transfer To Human

Human required:

1. Safety risk.
2. Electrical issue.
3. Mechanical damage.
4. Installation issue.
5. Warranty dispute.
6. Refund or compensation.
7. Repeated fault.
8. Customer complaint.
9. Unknown issue.

## 6. Approval Model

### 6.1 Draft Only

Default mode for Sprint 5 and early Sprint 6.

Allowed:

1. Generate article draft.
2. Generate reply draft.
3. Generate video script draft.
4. Generate service troubleshooting draft.
5. Save to queue.

Not allowed:

1. Publish.
2. Send customer reply.
3. Update approved knowledge.
4. Make public claims.

### 6.2 Human Approved Publishing

Recommended production mode.

Flow:

```text
AI draft
↓
Knowledge source citation
↓
Human review
↓
Create platform draft
↓
Human publish approval
↓
Publish
↓
Record URL / result
```

Best for:

1. WordPress article publishing.
2. Product pages.
3. YouTube videos.
4. TikTok/Facebook posts.
5. Customer replies involving product claims.

### 6.3 Fully Automated Low-Risk Tasks

Allowed only for low-risk operations.

Examples:

1. Register uploaded source files.
2. Create internal draft queue item.
3. Notify reviewer.
4. Record published URL after human publish.
5. Pull GA4 data.
6. Pull Search Console data.
7. Categorize incoming questions.
8. Create service ticket from form submission.

Not allowed as fully automated initially:

1. Publishing public content.
2. Sending price replies.
3. Sending warranty replies.
4. Updating Golden Knowledge.
5. Changing product specs.

## 7. Required Credentials

| System | Required Credentials / Permissions | Purpose |
|---|---|---|
| WordPress | Admin/editor account, Application Password or OAuth/plugin auth, REST API access | Create drafts, upload media, publish after approval |
| GA4 | Google Cloud project, GA4 property access, Data API credentials | Read analytics and performance data |
| Search Console | Verified site property, Search Console API access | Submit/list sitemap, inspect indexing status |
| YouTube | Google Cloud project, YouTube Data API enabled, OAuth consent, channel access | Upload and schedule videos |
| TikTok | TikTok Developer app, Content Posting API access, approved scopes, business/creator authorization | Post or schedule videos if eligible |
| Facebook | Meta app, Page access token, required Page/video permissions | Publish Page posts/videos |
| 微信 / 视频号 / 公众号 | Official account admin access, app credentials where available, publishing permissions | Semi-auto or approved API publishing depending account capability |
| WhatsApp | Meta Business account, WhatsApp Business Platform / Cloud API, phone number ID, access token, templates | Customer messaging and template messages |
| Email | SMTP/IMAP or provider API credentials | Receive inquiries and send approved replies |
| CRM | API token/admin access, lead/ticket permissions | Create leads, log interactions, create after-sales tickets |

## 8. Risk Matrix

| Area | Main Risk | Mitigation |
|---|---|---|
| Website publishing | Wrong or unapproved claims | Human approval before publish |
| Video publishing | Policy/copyright/claim risk | Platform checklist and review |
| Customer reply | Price or warranty mistake | Human takeover rules |
| After-sales | Safety or machine damage | Service escalation |
| Knowledge update | Polluting Golden Knowledge | Approval gate |
| Credentials | Token leakage | Store in credentials manager, never docs |
| Analytics | Misreading data | Use dashboards with context |

## 9. Sprint 6 MVP Recommendation

Recommended first automation:

```text
HK620 Approved Article
↓
WordPress Draft
↓
Human Approve
↓
Publish
```

### Why This Is Best

1. Lowest business risk among publishing automations.
2. WordPress supports drafts and status transitions.
3. Human approval can be preserved.
4. URL can be recorded after publishing.
5. It creates a visible business outcome without automating customer commitments.

### Sprint 6 Scope

Build only:

1. Read approved HK620 article draft.
2. Create WordPress draft.
3. Upload approved media.
4. Set status to `draft` or `pending`.
5. Record WordPress post ID.
6. Human approves in WordPress.
7. Publish.
8. Record final URL.

Do not build in Sprint 6:

1. Auto social publishing.
2. Auto customer reply.
3. Auto after-sales diagnosis.
4. Auto Golden Knowledge update.
5. Auto publish without human approval.

## 10. Source Notes

Planning references used:

1. WordPress REST API supports posts with status values including `draft`, `pending`, `future`, and `publish`, and supports media endpoints.
2. YouTube Data API supports video insert/upload through the `videos.insert` endpoint.
3. TikTok Content Posting API supports app/account-dependent posting flows.
4. Google Search Console API supports sitemap list/get/submit operations.
5. Google Analytics Data API supports programmatic reporting for dashboards and automation.
6. Meta/WhatsApp/Facebook automation depends on Meta app permissions, business verification, Page access, and channel-specific policies.
7. WeChat, 视频号, and 抖音 should be treated as semi-automatic until official account/API permissions are verified for the specific business account.

## 11. Final Conclusion

M8A can achieve the requested automation vision, but the correct rollout is staged.

Recommended order:

1. WordPress draft publishing.
2. Website URL logging and Search Console / GA4 reporting.
3. Customer reply drafting for website forms and email.
4. WhatsApp controlled reply drafting.
5. Video script and publishing package generation.
6. YouTube/TikTok/Facebook API publishing after account permissions are ready.
7. After-sales ticketing and troubleshooting draft.

Final Sprint 5 decision:

```text
Feasible, but review-gated.
Sprint 6 should start with HK620 Approved Article → WordPress Draft → Human Approve → Publish.
```
