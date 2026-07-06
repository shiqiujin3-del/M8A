# 03 Directory Structure

## Root Structure

```text
M8A/
├── apps/
├── services/
├── workflows/
├── knowledge/
├── configs/
├── env/
├── logs/
├── backups/
├── scripts/
├── docs/
└── docker/
```

## Ownership Rules
- `apps/`: user-facing and integration applications
- `services/`: databases, caches, vector stores, and infrastructure services
- `workflows/`: n8n and automation workflow definitions
- `knowledge/`: source materials for retrieval and knowledge tests
- `configs/`: non-secret service configuration
- `env/`: local environment files, not committed when real secrets are present
- `logs/`: runtime logs and operational notes
- `backups/`: local backup exports
- `scripts/`: administrative and maintenance scripts
- `docs/`: project documentation and governance
- `docker/`: Dockerfiles and container-related assets

## Naming Standard
Use lowercase directory names and clear business-domain grouping.
