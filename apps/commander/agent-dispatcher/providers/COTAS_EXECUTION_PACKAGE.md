# COTAS Execution Package

Mission:
INTEGRATION_MISSION

Task:
Prepare Codex/COTAS connector and adapter execution package

Context:
CEO command: 帮我接 Coze API 到 M8A

M8A is the Commander system. COTAS means Codex execution handoff. COTAS/Codex is an execution agent only. It must not become Commander and must not bypass Mission Control, Approval, or Exception Framework.

Allowed Actions:
- Research third-party API documentation.
- Design connector contract.
- Design adapter implementation plan.
- Draft test scripts.
- Draft test report.
- Return structured findings to M8A as an artifact.

Forbidden Actions:
- Do not publish content.
- Do not modify production websites.
- Do not save or expose secrets.
- Do not bypass CEO Approval.
- Do not bypass Mission Control.
- Do not bypass Exception Framework.
- Do not call external production APIs unless explicitly approved in a later sprint.
- Do not deploy.

Expected Output:
COTAS execution package with adapter design, test script plan, test report format, security rules, and return schema.

Acceptance Criteria:
- Provide API capability summary.
- List required credentials without real secret values.
- List API endpoints and methods.
- Identify adapter files that would be needed.
- Provide test cases.
- Identify risks and approval points.
- Return a clear go/no-go recommendation.

Security Rules:
- Mask all secrets.
- Never write credentials to code, logs, artifacts, or reports.
- Treat external write actions as approval-gated.
- Route failures through Exception Framework.
- Use mock mode unless CEO approves real integration.

Return Format:
```json
{
  "agent": "COTAS Integration Agent",
  "status": "completed | blocked | failed",
  "integration_plan": {},
  "required_credentials": [],
  "api_endpoints": [],
  "adapter_design": {},
  "test_plan": [],
  "risk_points": [],
  "approval_points": [],
  "next_steps": [],
  "exception": null
}
```
