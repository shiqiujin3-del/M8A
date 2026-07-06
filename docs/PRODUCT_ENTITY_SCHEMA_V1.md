# Product Entity Schema V1

Version: V1  
Date: 2026-07-06  
Owner: M8A Product Knowledge Center  
Status: Active Standard

## 1. Purpose

This schema defines the standard structure for every product knowledge asset in M8A.

All product records must follow this schema before they can be used by content, sales, website, customer service, or analytics workflows.

The schema separates:

1. Product metadata stored in PostgreSQL.
2. Searchable semantic chunks stored in Qdrant.
3. Review and version status used by the Product Knowledge Center.

## 2. Product Entity

Every product must have one Product Entity.

| Field | Required | Description |
|---|---:|---|
| `product_id` | Yes | Stable internal ID, for example `product_hk620` |
| `product_model` | Yes | Product model, for example `HK620` |
| `product_name` | Yes | Human-readable product name |
| `category` | Yes | Product category |
| `subcategory` | No | More specific product grouping |
| `primary_language` | Yes | Main language of the record |
| `status` | Yes | `draft`, `review_pending`, `approved`, `archived` |
| `source_confidence` | Yes | `low`, `medium`, `high` |
| `owner_center` | Yes | Default: `Product Knowledge Center` |
| `created_at` | Yes | Creation timestamp |
| `updated_at` | Yes | Last update timestamp |

## 3. Golden Knowledge Record

Every product should have one current Golden Knowledge Record.

The Golden Knowledge Record is the approved or reviewable source used by other M8A centers.

Required sections:

1. Product Identity
2. Technical Specifications
3. Core Features
4. Applications
5. Target Customers
6. Advantages
7. Limitations
8. FAQs
9. Sales Talking Points
10. Related Videos
11. Related Images
12. Website URLs
13. Existing GEO Articles
14. Existing Short Video Scripts
15. Source Documents
16. Version History
17. Review Status

## 4. Review Status

Allowed values:

| Status | Meaning |
|---|---|
| `draft` | Created but not ready for review |
| `review_pending` | Ready for human review |
| `revision_required` | Human reviewer requires changes |
| `approved` | Approved for use by downstream centers |
| `archived` | No longer used for new generation |

Rules:

1. AI-generated product facts must not be marked `approved` without human review.
2. Missing source fields must be marked `TBD` instead of being guessed.
3. Downstream public-facing content should use only `approved` product knowledge.
4. Qdrant payload status must match the PostgreSQL review status.

## 5. PostgreSQL Tables

### 5.1 `m8a_product_entities`

Stores product-level metadata.

```text
product_id
product_model
product_name
category
subcategory
primary_language
status
source_confidence
owner_center
created_at
updated_at
```

### 5.2 `m8a_product_knowledge_records`

Stores full Golden Knowledge Records as structured JSON.

```text
record_id
product_id
version
record_status
source_summary
record
created_at
updated_at
```

### 5.3 `m8a_product_knowledge_chunks`

Stores chunk metadata and Qdrant references.

```text
chunk_id
product_id
record_id
chunk_type
chunk_title
chunk_text
qdrant_collection
qdrant_point_id
embedding_method
embedding_dimension
review_status
created_at
updated_at
```

## 6. Qdrant Chunk Standard

Each product must be written to Qdrant as multiple focused chunks.

Required chunks:

1. Overview
2. Technical Specifications
3. Applications
4. Advantages
5. FAQ
6. Sales
7. Troubleshooting

Do not store the whole product record as one large chunk.

Recommended Qdrant payload:

```text
entity_type
product_id
product_model
record_id
chunk_id
chunk_type
chunk_title
language
review_status
source_confidence
version
source_documents
created_at
updated_at
```

## 7. Source Rules

Every factual statement should be linked to one of these source types:

1. Product manual
2. Website page
3. Engineering note
4. Sales note
5. Customer service record
6. Approved internal document
7. Human reviewer input

If no source exists, the field must be:

```text
TBD - source required
```

## 8. Downstream Usage Rules

| Center | Allowed Usage |
|---|---|
| Product Knowledge Center | Create, review, update, retrieve |
| GEO Content Center | Use approved knowledge for draft generation |
| Website Operation Center | Use approved knowledge for page updates |
| Sales Center | Use approved knowledge for customer reply drafts |
| Analytics Center | Measure coverage, freshness, gaps, and usage |

## 9. Versioning

Each Golden Knowledge Record must include version history.

Minimum version fields:

```text
version
date
change_summary
changed_by
review_status
```

## 10. V1 Standard

For M8A V1, a product knowledge asset is complete only when:

1. Product metadata exists in PostgreSQL.
2. The Golden Knowledge Record exists as a structured document.
3. The required Qdrant chunks are written separately.
4. Missing source fields are clearly marked.
5. Review status is explicit.
6. The record can be reused by future content, website, sales, and analytics workflows.
