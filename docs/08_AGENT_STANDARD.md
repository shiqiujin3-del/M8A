# 08 Agent Standard

All future M8A agents must follow this standard.

## Agent Identity
- Agent name:
- Agent ID:
- Version:
- Owner:
- Business domain:
- Status: draft | test | staging | production | retired

## Responsibility
- Primary responsibility:
- Tasks allowed:
- Tasks forbidden:
- Escalation conditions:

## Inputs
- Input sources:
- Input schema:
- Required fields:
- Optional fields:
- Validation rules:

## Outputs
- Output destination:
- Output schema:
- Success response:
- Failure response:
- Human review requirement:

## Model Usage
- Default model:
- Fallback model:
- Temperature policy:
- Token budget:
- Prompt location:
- Evaluation method:

## MCP Usage
- MCP servers allowed:
- MCP tools allowed:
- MCP tools forbidden:
- Required authentication:
- Timeout policy:

## Tool Usage
- Local tools allowed:
- External APIs allowed:
- Write operations allowed:
- Read-only operations:
- Rate limits:

## Logging
- Log location:
- Required log fields:
- Sensitive data masking:
- Retention period:
- Audit owner:

## Permissions
- Filesystem access:
- Database access:
- Network access:
- WordPress access:
- GitHub access:
- Social media access:

## Error Handling
- Retry policy:
- Circuit breaker condition:
- Human escalation path:
- Rollback action:
- Alert destination:

## Version Control
- Version number:
- Changelog entry:
- Test evidence:
- Approval record:

## Release Checklist
- Inputs validated
- Outputs validated
- No secrets in prompts or logs
- External writes reviewed
- Rollback path documented
- Owner assigned
