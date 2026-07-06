# 02 System Architecture

## Architecture Layers
1. Apps layer
2. Services layer
3. Workflow layer
4. Knowledge layer
5. Configuration and secrets layer
6. Observability layer
7. Backup and recovery layer

## Core Components
- n8n orchestration
- Dashboard monitoring
- MCP integration layer
- PostgreSQL data storage
- Redis cache and queue support
- Qdrant vector database
- Optional local model service via Ollama

## Data Flow
To be defined in later deployment phases.

## Trust Boundaries
- Local development machine
- Internal Docker network
- External APIs
- Website and publishing systems

## Open Decisions
- Production host model
- Secret manager choice
- Backup destination
- Monitoring stack
