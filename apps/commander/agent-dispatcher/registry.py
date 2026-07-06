#!/usr/bin/env python3
"""Agent Registry for M8A Agent Dispatcher V1.

This registry is local and declarative. It does not call real AI providers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    role: str
    capabilities: list[str]
    priority: int
    estimated_runtime: str
    cost: str
    approval_policy: dict
    exception_policy: dict
    status: str

    def to_dict(self) -> dict:
        return asdict(self)


AGENTS: list[AgentDefinition] = [
    AgentDefinition(
        name="Research Agent",
        role="Researches requirements, API docs, platform constraints, and integration risks.",
        capabilities=["api_research", "requirements_discovery", "risk_scan", "source_summary"],
        priority=10,
        estimated_runtime="5-10 minutes",
        cost="mock_only",
        approval_policy={"requires_ceo_approval_for": ["external_account_access", "paid_api_plan"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
    AgentDefinition(
        name="Code Agent",
        role="Plans implementation changes and code tasks after requirements are clear.",
        capabilities=["implementation_plan", "code_change_plan", "test_plan", "integration_contract"],
        priority=30,
        estimated_runtime="10-30 minutes",
        cost="mock_only",
        approval_policy={"requires_ceo_approval_for": ["production_code_change", "external_write_action"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
    AgentDefinition(
        name="COTAS Integration Agent",
        role="API / Connector / Adapter Development Agent powered by Codex/COTAS manual handoff.",
        capabilities=[
            "api_research",
            "connector_design",
            "adapter_development_plan",
            "test_script_plan",
            "test_report_generation",
            "artifact_handoff",
        ],
        priority=30,
        estimated_runtime="15-45 minutes",
        cost="manual_handoff",
        approval_policy={"requires_ceo_approval_for": ["code_execution", "credential_use", "external_api_connection", "production_change"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
    AgentDefinition(
        name="QA Agent",
        role="Checks safety, acceptance criteria, regression risk, and test evidence.",
        capabilities=["qa_plan", "acceptance_test", "safety_review", "regression_review"],
        priority=40,
        estimated_runtime="5-15 minutes",
        cost="mock_only",
        approval_policy={"requires_ceo_approval_for": ["release_signoff"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
    AgentDefinition(
        name="Website Agent",
        role="Plans website-side draft, page, sitemap, and content operations.",
        capabilities=["wordpress_draft_plan", "website_payload_review", "sitemap_check", "content_structure"],
        priority=35,
        estimated_runtime="5-20 minutes",
        cost="mock_only",
        approval_policy={"requires_ceo_approval_for": ["publish", "update_live_page"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
    AgentDefinition(
        name="Infrastructure Agent",
        role="Plans credentials, network, auth, API, DNS, Cloudflare, webhook, and security setup.",
        capabilities=["credential_plan", "api_auth_plan", "network_check", "webhook_plan", "security_review"],
        priority=20,
        estimated_runtime="5-20 minutes",
        cost="mock_only",
        approval_policy={"requires_ceo_approval_for": ["oauth_scope", "security_policy_change", "production_secret"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
    AgentDefinition(
        name="Business Analyst Agent",
        role="Maps business goal, value, market impact, and CEO summary.",
        capabilities=["business_goal_mapping", "roi_estimate", "mission_summary", "priority_reasoning"],
        priority=50,
        estimated_runtime="5-10 minutes",
        cost="mock_only",
        approval_policy={"requires_ceo_approval_for": ["business_priority_change"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
    AgentDefinition(
        name="Content Agent",
        role="Plans content assets, draft structures, and messaging from approved knowledge.",
        capabilities=["content_plan", "draft_outline", "faq_plan", "social_draft_plan"],
        priority=45,
        estimated_runtime="5-20 minutes",
        cost="mock_only",
        approval_policy={"requires_ceo_approval_for": ["public_content_use", "customer_facing_claim"]},
        exception_policy={"on_failure": "route_to_exception_framework", "owner": "Infrastructure Agent"},
        status="active",
    ),
]


class AgentRegistry:
    def __init__(self, agents: list[AgentDefinition] | None = None):
        self._agents = agents or AGENTS

    def list_agents(self) -> list[dict]:
        return [agent.to_dict() for agent in sorted(self._agents, key=lambda item: item.priority)]

    def get(self, name: str) -> dict:
        for agent in self._agents:
            if agent.name == name:
                return agent.to_dict()
        raise KeyError(f"Agent not found: {name}")

    def find_by_capability(self, capability: str) -> list[dict]:
        matches = [agent for agent in self._agents if capability in agent.capabilities and agent.status == "active"]
        return [agent.to_dict() for agent in sorted(matches, key=lambda item: item.priority)]


def default_registry() -> AgentRegistry:
    return AgentRegistry()
