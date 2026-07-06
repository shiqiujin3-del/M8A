# 07 Workflow Standard

## Workflow Naming
`domain_purpose_version`, for example: `website_product_sync_v1`.

## Required Metadata
- Owner
- Business domain
- Trigger type
- Input sources
- Output destinations
- External systems touched
- Error handling owner
- Version

## Folder Mapping
- Marketing: `workflows/marketing/`
- Sales: `workflows/sales/`
- Website: `workflows/website/`
- GEO: `workflows/geo/`
- Factory: `workflows/factory/`
- Automation: `workflows/automation/`
- Tests: `workflows/test/`

## Safety Rules
- Test workflows must not write to production systems.
- Production writes require approval and rollback notes.
- Every workflow must define failure behavior.
