#!/usr/bin/env python3
"""COTAS / Codex Provider Adapter V1.

V1 is manual handoff only. COTAS is treated as Codex execution handoff,
not as a separate Commander or external platform authority.
"""

from __future__ import annotations

from pathlib import Path


PROVIDER_DIR = Path(__file__).resolve().parent
PACKAGE_PATH = PROVIDER_DIR / "COTAS_EXECUTION_PACKAGE.md"


def build_cotas_execution_package(mission: dict, cotas_step: dict | None = None) -> str:
    command = mission.get("command_text") or mission.get("title") or "Integration mission"
    task_title = (cotas_step or {}).get("task_title", "Design and plan API / Connector / Adapter integration")
    expected_output = (cotas_step or {}).get(
        "expected_output",
        "Connector design, adapter plan, test checklist, and implementation handoff notes.",
    )
    return f"""# COTAS Execution Package

Mission:
{mission.get("mission_name", "INTEGRATION_MISSION")}

Task:
{task_title}

Context:
CEO command: {command}

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
{expected_output}

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
{{
  "agent": "COTAS Integration Agent",
  "status": "completed | blocked | failed",
  "integration_plan": {{}},
  "required_credentials": [],
  "api_endpoints": [],
  "adapter_design": {{}},
  "test_plan": [],
  "risk_points": [],
  "approval_points": [],
  "next_steps": [],
  "exception": null
}}
```
"""


def create_cotas_execution_package(mission: dict, agent_plan: dict) -> dict:
    cotas_step = next(
        (step for step in agent_plan.get("task_sequence", []) if step.get("agent_name") == "COTAS Integration Agent"),
        None,
    )
    package = build_cotas_execution_package(mission, cotas_step)
    PACKAGE_PATH.write_text(package, encoding="utf-8")
    return {
        "provider": "cotas_codex",
        "mode": "manual_handoff",
        "api_called": False,
        "package_path": str(PACKAGE_PATH),
        "package_title": "COTAS_EXECUTION_PACKAGE.md",
        "package_content": package,
        "next_provider_stage": "Replace manual handoff with an approved Codex/COTAS execution channel when a safe contract exists.",
    }
