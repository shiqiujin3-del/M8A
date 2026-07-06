# Website + Content Collaboration SOP V1

Date: 2026-07-06

## Purpose

This SOP defines how Research Agent, Content Agent, Website Agent, QA Agent, and CEO Approval collaborate inside M8A.

The goal is to safely produce website-ready content without bypassing Mission Control, Approval, or Exception Framework.

## Collaboration Flow

```text
Research Agent
  ↓
Content Agent
  ↓
Website Agent
  ↓
QA Agent
  ↓
CEO Approval
```

## 1. Research Agent

### Input

- CEO Mission objective.
- Product / market / platform target.
- Existing product knowledge.
- External research scope if approved.

### Output

```text
research_summary
```

Required handoff:

```json
{
  "research_summary": "",
  "target_market": "",
  "opportunities": [],
  "constraints": [],
  "source_references": [],
  "recommended_content_direction": []
}
```

### Handoff To

Content Agent.

## 2. Content Agent

### Input

- Research summary.
- Approved product knowledge.
- Mission objective.
- Target language.
- Target content type.

### Output

```text
artifact_type = content_draft
```

Required handoff:

```json
{
  "content_draft_artifact_id": "",
  "title": "",
  "content_type": "",
  "draft_body": "",
  "source_references": [],
  "claims_requiring_review": [],
  "missing_information": [],
  "review_required": true
}
```

### Handoff To

Website Agent.

## 3. Website Agent

### Input

- content_draft artifact.
- Source references.
- SEO/GEO metadata requirements.
- Target site.
- Approval context.

### Output

```text
artifact_type = wordpress_draft
```

or:

```text
artifact_type = draft_payload
```

Required handoff:

```json
{
  "wordpress_draft_artifact_id": "",
  "title": "",
  "slug": "",
  "status": "draft",
  "meta_title": "",
  "meta_description": "",
  "content_preview": "",
  "approval_required": true,
  "publish": false
}
```

### Handoff To

QA Agent.

## 4. QA Agent

### Input

- content_draft artifact.
- wordpress_draft / draft_payload artifact.
- Source references.
- Approval context.

### Checks

QA Agent checks:

1. Source references exist.
2. Product claims are approved or clearly marked.
3. Metadata exists.
4. Draft status is not publish.
5. No secret-like content exists.
6. No external platform was modified without approval.
7. Missing information is clearly marked.
8. Content and website payload match the Mission objective.

### Output

```text
artifact_type = qa_review_result
```

Required handoff:

```json
{
  "qa_status": "passed | failed | needs_human_review",
  "summary": "",
  "checks": [],
  "risks": [],
  "recommendation": "",
  "requires_ceo_approval": true
}
```

### Handoff To

CEO Approval.

## 5. CEO Approval

CEO sees:

- Mission objective.
- Content draft summary.
- Website draft summary.
- QA result.
- Risk points.
- Approval recommendation.

CEO may:

- approve
- reject
- request revision

Approval does not automatically publish unless a future approved publishing workflow exists.

## Standard Artifacts

### Content Agent Artifact

```text
artifact_type = content_draft
```

Required fields:

- title
- content_type
- language
- product
- market
- knowledge_version
- source_references
- draft_body
- claims_requiring_review
- missing_information
- review_required
- public_use_allowed

### Website Agent Artifact

```text
artifact_type = wordpress_draft
```

Required fields:

- title
- slug
- status=draft
- meta_title
- meta_description
- content_preview
- source_content_artifact_id
- source_knowledge_version
- review_required
- publish=false
- approval_required

## Approval Rules

Approval is required for:

- Public website content.
- WordPress drafts.
- Product claims.
- Technical specifications.
- Customer-facing messaging.
- Publishing.
- Sitemap or URL changes.

## Exception Rules

All failures must route to Exception Framework:

- Missing source references.
- Missing approved knowledge.
- Forbidden public claim.
- Secret-like content detected.
- WordPress draft failure.
- Metadata validation failure.
- QA failed result.
- Any external platform error.

## Daily Workflow

```text
Morning Mission Review
  ↓
Research Agent prepares direction
  ↓
Content Agent creates content_draft
  ↓
Website Agent creates wordpress_draft / draft_payload
  ↓
QA Agent reviews
  ↓
CEO Approval
  ↓
End Of Day summary
```

## Operating Principle

Content creates message.

Website prepares delivery.

QA protects quality.

CEO decides public use.

