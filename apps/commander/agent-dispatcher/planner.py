#!/usr/bin/env python3
"""Planner for converting routed Agents into an Agent Execution Plan."""

from __future__ import annotations


BANANA_TASKS = {
    "Research Agent": {
        "task_title": "Research Banana API requirements",
        "expected_output": "Banana API capability map, docs checklist, auth model, risk notes.",
        "depends_on": [],
        "approval_point": "CEO approval required if paid plan or external account access is needed.",
    },
    "Infrastructure Agent": {
        "task_title": "Plan Banana API credentials and network access",
        "expected_output": "Credential requirements, environment variables, webhook/security plan.",
        "depends_on": ["Research Agent"],
        "approval_point": "CEO approval required before storing production credentials or changing security policy.",
    },
    "Code Agent": {
        "task_title": "Plan Banana API connector implementation",
        "expected_output": "Implementation plan, files to add, test strategy, rollback plan.",
        "depends_on": ["Infrastructure Agent"],
        "approval_point": "CEO approval required before production code changes or external write actions.",
    },
    "COTAS Integration Agent": {
        "task_title": "Prepare Codex/COTAS connector and adapter execution package",
        "expected_output": "COTAS execution package with adapter design, test script plan, test report format, security rules, and return schema.",
        "depends_on": ["Infrastructure Agent"],
        "approval_point": "CEO approval required before COTAS/Codex performs real code changes, credential use, or external API calls.",
    },
    "QA Agent": {
        "task_title": "Validate Banana API integration plan",
        "expected_output": "Acceptance criteria, failure cases, safety checklist, go/no-go recommendation.",
        "depends_on": ["Code Agent"],
        "approval_point": "CEO signoff required before moving from plan to implementation.",
    },
}


class AgentPlanner:
    def build_plan(self, mission: dict, route: dict) -> dict:
        steps = []
        for index, agent in enumerate(route["selected_agents"], start=1):
            template = BANANA_TASKS.get(agent["name"], {
                "task_title": f"{agent['name']} mission planning task",
                "expected_output": f"{agent['name']} produces a planning artifact.",
                "depends_on": [],
                "approval_point": "CEO approval required before public or external actions.",
            })
            steps.append({
                "step": index,
                "agent_name": agent["name"],
                "agent_role": agent["role"],
                "task_title": template["task_title"],
                "dependencies": template["depends_on"],
                "expected_output": template["expected_output"],
                "approval_point": template["approval_point"],
                "estimated_runtime": agent["estimated_runtime"],
                "cost": agent["cost"],
                "status": "planned",
            })
        steps.append({
            "step": len(steps) + 1,
            "agent_name": "Commander Review",
            "agent_role": "CEO reviews the Agent Plan before any real AI, code, credential, or platform work starts.",
            "task_title": "Review Agent Execution Plan",
            "dependencies": [steps[-1]["agent_name"]] if steps else [],
            "expected_output": "CEO go/no-go decision for the next execution sprint.",
            "approval_point": "CEO approval required before moving from mock planning to real execution.",
            "estimated_runtime": "2-5 minutes",
            "cost": "no_cost",
            "status": "waiting_ceo_review",
        })

        return {
            "mission_name": mission.get("mission_name", "CONNECT_BANANA_API"),
            "mission_objective": mission.get("objective") or mission.get("command_text"),
            "planner_version": "agent_planner_v1_mock",
            "execution_mode": "mock_dispatch_only",
            "task_sequence": steps,
            "dependencies": [
                {"from": step["dependencies"], "to": step["agent_name"]}
                for step in steps if step["dependencies"]
            ],
            "approval_points": [
                {"agent": step["agent_name"], "approval_point": step["approval_point"]}
                for step in steps
            ],
            "expected_outputs": [
                {"agent": step["agent_name"], "output": step["expected_output"]}
                for step in steps
            ],
        }
