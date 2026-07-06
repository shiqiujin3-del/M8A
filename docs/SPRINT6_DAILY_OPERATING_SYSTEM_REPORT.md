# Sprint 6 Daily Operating System Report

Date: 2026-07-06  
System Name: Saiyu Daily Operating System  
Version: DOS V1  
Status: Business operation dashboard initialized

## 1. Daily Brief Structure

M8A DOS V1 changes the first screen from technical infrastructure status to a business operating brief.

Daily Brief sections:

1. Growth Score.
2. Today's Top Priorities.
3. Website Situation.
4. GEO / SEO.
5. Content Center.
6. Product Knowledge.
7. Publishing.
8. Customer.
9. Growth KPI.

The purpose is:

```text
Boss opens M8A
↓
Sees today's operating score
↓
Sees top 3 priorities
↓
Knows what to approve, publish, collect, or follow up
```

## 2. Growth Score Design

Growth Score gives Saiyu's daily AI operating health a score out of 100.

Current score:

```text
38 / 100
```

Current score is low because M8A has the operating structure, but key business data sources and approval loops are not finished yet.

### 2.1 Score Structure

| Module | Max Score | Current Score | Current Reason |
|---|---:|---:|---|
| Knowledge Score | 20 | 13 | HK620 has 1 approved_internal record and 8 approved_internal cards |
| GEO / SEO Score | 20 | 2 | Search Console, keyword, and AI Search data are TODO |
| Content Score | 20 | 14 | 9 drafts moved from blocked_pending_product_review to needs_human_content_review |
| Website Score | 15 | 2 | Sitemap, index, 404, and Core Web Vitals are TODO |
| Publishing Score | 10 | 3 | WordPress target exists, but publish jobs are 0 |
| Customer Score | 10 | 1 | Inquiry, reply, CRM data are TODO |
| Analytics Score | 5 | 3 | Daily report exists, but GA4/Search Console are TODO |
| Total | 100 | 38 | Sprint 6-A updated baseline |

### 2.2 Knowledge Score

Inputs:

1. HK620 Knowledge Coverage.
2. Approved Knowledge count.
3. Review Pending count.
4. Inbox unprocessed files.
5. Queue backlog.

Current:

```text
HK620 structure: available
Approved Knowledge: 1 approved_internal Golden Record + 8 approved_internal Founder Cards
Review Pending: 7 Founder Cards + technical specs + media + service FAQ
Inbox: 0
Queue: 0
```

Main deduction:

HK620 now has internal approved knowledge, but public approved knowledge remains 0 and technical/media/service materials are still incomplete.

### 2.3 GEO / SEO Score

Inputs:

1. Today's keyword opportunities.
2. Search Console changes.
3. New or declining keywords.
4. AI Search mentions.
5. Content Gap count.

Current:

```text
TODO: Search Console integration
TODO: AI Search monitor
TODO: keyword opportunity source
```

Main deduction:

No real SEO/GEO data source is connected yet.

### 2.4 Content Score

Inputs:

1. Content generated today.
2. Content pending review.
3. Content approved.
4. Video script count.
5. FAQ count.

Current:

```text
Generated drafts: 9
Drafts ready for human review: 9
Approved drafts: 0
Video scripts: 2
FAQ: 10-question draft
```

Main deduction:

Content Operator has produced the first daily content package, but all drafts still require human content approval before publishing.

### 2.5 Website Score

Inputs:

1. Website health.
2. Sitemap status.
3. 404 count.
4. New article count.
5. Index status.

Current:

```text
TODO: website health source
TODO: sitemap source
TODO: 404 source
TODO: index source
```

Main deduction:

Website operating data is not connected yet.

### 2.6 Publishing Score

Inputs:

1. Draft count.
2. Pending Review count.
3. Approved count.
4. Published Today count.
5. Failed count.

Current:

```text
Publishing targets: 7
WordPress active target: 1
Publish jobs: 0
Failed: 0
```

Main deduction:

No approved article has entered the publishing pipeline.

### 2.7 Customer Score

Inputs:

1. Today's inquiry count.
2. Pending reply count.
3. Replied count.
4. High-intent lead count.
5. Overdue count.

Current:

```text
TODO: website form
TODO: WhatsApp
TODO: WeChat
TODO: Email
TODO: CRM
```

Main deduction:

Customer data sources are not connected yet.

### 2.8 Analytics Score

Inputs:

1. GA4 data availability.
2. Search Console data availability.
3. Daily report generated.
4. Abnormal events.

Current:

```text
Daily DOS report: generated
TODO: GA4
TODO: Search Console
```

## 3. Today's Top Priorities Logic

Top priorities are generated from score deductions.

Current top 3 after Sprint 6-A:

1. 准备 Search Console 接入权限.
2. 补 HK620 技术参数和产品媒体.
3. 审核 Content Operator 今日 9 份 HK620 内容草稿.

Priority rules:

1. If Approved Knowledge = 0, prioritize knowledge review.
2. If content drafts exist but approved content = 0, prioritize review.
3. If website/GEO data is TODO, prioritize Search Console.
4. If publish jobs = 0 and approved article exists, prioritize WordPress Draft.
5. If customer overdue count > 0, prioritize customer response.

## 4. Dashboard Design

Updated file:

```text
apps/dashboard/index.html
```

Dashboard now displays:

1. Growth Score: 38 / 100.
2. Yesterday Score: 31 / 100.
3. Score Change: +7.
4. Main deduction reasons.
5. Today's top 3 priorities.
6. Website Situation.
7. GEO / SEO.
8. Content Center.
9. Product Knowledge.
10. Publishing.
11. Customer.
12. Growth KPI.
13. Content Operator Today.

The homepage no longer focuses on Docker, Redis, Qdrant, or infrastructure status.

## 4.1 Content Operator Today

Digital Employee No.1:

```text
Content Operator
```

Today completed:

| Output | Count | Status |
|---|---:|---|
| Website Article | 1 | needs_human_review |
| Chinese GEO Article | 1 | needs_human_review |
| FAQ | 10 questions | needs_human_review |
| Meta Title | 1 | needs_human_review |
| Meta Description | 1 | needs_human_review |
| LinkedIn Draft | 1 | needs_human_review |
| Facebook Draft | 1 | needs_human_review |
| Short Video Script CN | 1 | needs_human_review |
| Short Video Script EN | 1 | needs_human_review |

Daily totals:

```text
Today Content Produced: 9 draft records
Today Pending Review: 9
Today Approved: 0
Today Published: 0
```

Content Operator does not publish content. All output remains in Draft Queue until human review.

## 5. Daily Operation Workflow Design

No new Workflow was created in this Sprint.

Daily Operation Workflow design:

```text
Knowledge Check
↓
Website Check
↓
SEO Check
↓
GEO Check
↓
Content Check
↓
Publishing Check
↓
Customer Check
↓
Analytics Check
↓
Calculate Growth Score
↓
Generate Daily Brief
```

Each check should read from existing systems:

| Step | Source |
|---|---|
| Knowledge Check | PostgreSQL product tables, Inbox, Queue |
| Website Check | WordPress, Search Console |
| SEO Check | Search Console |
| GEO Check | GEO monitor / AI Search references |
| Content Check | Draft Queue |
| Publishing Check | publish_jobs, publish_history, publish_logs |
| Customer Check | CRM, Email, WhatsApp, WeChat, website forms |
| Analytics Check | GA4, Search Console |

## 6. Business KPI Definition

Growth KPI:

| KPI | Definition | Current |
|---|---|---|
| Knowledge Coverage | Approved and reviewable product knowledge coverage | Structure complete, approved 0 |
| Content Produced | Drafts generated today or currently in queue | 9 |
| Published | Published content count | 0 |
| Google Indexed | Indexed URLs | TODO Search Console |
| AI Search Mentions | Mentions in AI search / answer engines | TODO GEO monitor |
| Website Visits | Website sessions/users | TODO GA4 |
| Leads | New inquiries / leads | TODO CRM |
| Customer Replies | Replies sent or pending | TODO CRM / Email / WhatsApp / WeChat |

## 7. Future Daily Automation Logic

Daily automation should run in three maturity stages.

### Stage 1: Manual Refresh

Current DOS V1 stage.

1. Read existing PostgreSQL data.
2. Read existing draft/publish queues.
3. Generate static Daily Brief.
4. Display TODO for missing data sources.

### Stage 2: Scheduled Internal Brief

After Search Console, GA4, and WordPress credentials are configured:

1. Run scheduled Daily Operation Workflow every morning.
2. Pull website, SEO, publishing, and analytics data.
3. Calculate Growth Score.
4. Generate Daily Brief.
5. Save report to docs/logs.

### Stage 3: Actionable Daily Operating System

After customer and publishing systems are connected:

1. Create prioritized tasks.
2. Assign reviewer/owner.
3. Track task completion.
4. Compare daily score trend.
5. Alert if customer replies or publishing tasks are overdue.

## 8. Data Source TODOs

Required next data connections:

1. GA4.
2. Search Console.
3. WordPress.
4. Sitemap status.
5. 404 / Core Web Vitals source.
6. AI Search / GEO mention monitor.
7. Website form.
8. Email.
9. WhatsApp / WeChat.
10. CRM.

## 9. Final Result

Sprint 6 DOS V1 status:

```text
PASS
```

M8A now has a business-first operating homepage:

```text
赛宇今日经营简报
```

Current conclusion for today:

1. Review HK620 founder interview knowledge cards.
2. Fill HK620 technical specification gaps.
3. Connect Search Console so SEO/GEO score can become real.

M8A has stopped being a technical status board and is now positioned as Saiyu's Daily Operating System.
