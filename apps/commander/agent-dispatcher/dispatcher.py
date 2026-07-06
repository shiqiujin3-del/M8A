#!/usr/bin/env python3
"""Agent Dispatcher Runtime V1.

Dispatcher does not execute real AI work. It selects Agents, orders them,
collects mock results, and returns a plan to Commander.
"""

from __future__ import annotations

from agent_runtime import MockAgentRuntime
from planner import AgentPlanner
from providers.cotas_provider import create_cotas_execution_package
from registry import default_registry
from router import AgentRouter


class AgentDispatcher:
    def __init__(self):
        self.registry = default_registry()
        self.router = AgentRouter(self.registry)
        self.planner = AgentPlanner()
        self.runtime = MockAgentRuntime()

    def dispatch(self, mission: dict) -> dict:
        try:
            route = self.router.route(mission)
            plan = self.planner.build_plan(mission, route)
            runtime_result = self.runtime.run_plan(plan)
            provider_packages = {}
            if any(step["agent_name"] == "COTAS Integration Agent" for step in plan["task_sequence"]):
                provider_packages["cotas"] = create_cotas_execution_package(mission, plan)
            return {
                "dispatcher": "agent_dispatcher_v1",
                "status": "planned",
                "mission": mission,
                "registry": self.registry.list_agents(),
                "route": route,
                "agent_plan": plan,
                "mock_runtime_result": runtime_result,
                "provider_packages": provider_packages,
                "exception_policy": "Any future runtime failure must call Exception Framework create_exception_from_failure().",
            }
        except Exception as exc:
            return {
                "dispatcher": "agent_dispatcher_v1",
                "status": "failed",
                "error": str(exc),
                "exception_policy": "In integrated mode this failure must route to Exception Framework.",
            }


def dispatch_mission(mission: dict) -> dict:
    return AgentDispatcher().dispatch(mission)
