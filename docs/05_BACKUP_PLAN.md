# 05 Backup Plan

## Backup Targets
- PostgreSQL data
- n8n workflow exports
- Qdrant collections
- configuration files
- documentation
- logs required for audit

## Backup Frequency
To be defined by environment: development, staging, production.

## Retention
To be defined before production use.

## Storage Locations
- Local backups: `backups/`
- External backup destination: to be selected

## Restore Test
Every backup plan must include a restore test procedure.
