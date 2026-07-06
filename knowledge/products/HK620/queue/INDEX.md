# HK620 Knowledge Processing Queue

Purpose: track source files after Inbox registration and before knowledge approval.

Allowed statuses:

```text
new
processing
needs_review
approved
archived
```

Rules:

1. New files start as `new`.
2. AI or automation may help extract draft information, but cannot approve it.
3. Human review is required before `approved`.
4. Only approved items may update Golden Knowledge, PostgreSQL product knowledge tables, Qdrant, or chunks.
