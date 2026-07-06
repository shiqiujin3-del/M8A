# Laoli Engineering Knowledge Cards

Date: 2026-07-06  
Source Account: 东莞顾态老李  
Source Type: Publicly published videos  
Product Scope: HK620 and related engineering knowledge  
Status: Awaiting verified video links

## Boundary

M8A will not copy or download the videos.

M8A will create Engineering Knowledge Cards from public video sources. These cards are engineering review materials only. They do not directly update HK620 Golden Knowledge.

## Required Card Fields

Each video should produce one Engineering Knowledge Card containing:

| Field | Description |
|---|---|
| Theme | Main engineering topic of the video |
| Products Involved | Product models or machine categories mentioned |
| Process Flow | Steps or workflow shown or described |
| Engineering Experience | Practical lessons, setup notes, or field observations |
| Common Mistakes | Mistakes, wrong setup, misuse, or avoidable failures |
| FAQ | Questions implied or answered by the video |
| Adjustment Tips | Machine tuning, setup, calibration, or parameter hints |
| Applicable Scenarios | Where the knowledge applies |
| Confidence Level | `low`, `medium`, or `high` |
| Need 老李 Confirmation | `yes`, `no`, or `unclear` |

## Current Cards

No Engineering Knowledge Cards have been generated yet because no verified public video URLs were provided or located in the project.

## Engineering Review Queue

All future cards must enter:

```text
knowledge/products/HK620/10_Review/engineering_review_queue/
```

Initial status:

```text
needs_review
```

## Approval Rule

Only after human engineering review may a card be used to update:

1. HK620 Golden Knowledge.
2. PostgreSQL product knowledge.
3. Qdrant product knowledge vectors.
4. Product knowledge chunks.

## Next Action

Add verified public video links to:

```text
knowledge/products/HK620/05_Engineering_Notes/laoli_public_videos/VIDEO_SOURCE_LIST.md
```

Then create one Engineering Knowledge Card per video.
