# HK620 Knowledge Inbox

Product: HK620  
Product ID: `product_hk620`  
Purpose: receive real source materials before they enter the Knowledge Processing Queue.

## Supported File Types

| Type | Extensions |
|---|---|
| PDF | `.pdf` |
| Word | `.doc`, `.docx` |
| Excel | `.xls`, `.xlsx`, `.csv` |
| Image | `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.tif`, `.tiff` |
| Video | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` |
| Markdown | `.md`, `.markdown` |
| TXT | `.txt` |

## Intake Rules

1. Put only real HK620 source materials in this inbox.
2. Do not put generated product facts here unless they were reviewed and approved as source material.
3. Running the Inbox scanner registers each supported file.
4. Registration does not update Golden Knowledge.
5. Registration does not update Qdrant.
6. Registration creates a Knowledge Processing Queue item with status `new`.
7. Human review is required before any source can update Golden Knowledge.

## Processing Status

```text
new
processing
needs_review
approved
archived
```

## Required Metadata

The scanner records:

- file path
- file name
- file extension
- file type
- file size
- file hash
- source directory
- upload time
- uploader
- product ID
- duplicate status
