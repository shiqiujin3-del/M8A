#!/usr/bin/env python3
"""Coze Provider V1 mock-only tests."""

from __future__ import annotations

import json
import os
import socket
import unittest
from unittest import mock

from coze_provider import CozeProvider, build_mock_task


class CozeProviderMockTest(unittest.TestCase):
    def test_provider_initializes(self):
        provider = CozeProvider()
        self.assertEqual(provider.provider_name, "coze")
        self.assertEqual(provider.execution_mode, "mock_only")

    def test_mock_only_mode_runs(self):
        result = CozeProvider().run(build_mock_task())
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["provider_name"], "coze")
        self.assertEqual(result["execution_mode"], "mock_only")

    def test_does_not_read_env(self):
        with mock.patch.object(os, "environ", side_effect=AssertionError("env should not be read")):
            result = CozeProvider().run(build_mock_task())
        self.assertEqual(result["status"], "completed")
        self.assertFalse(result["env_read"])

    def test_does_not_access_network(self):
        with mock.patch.object(socket, "create_connection", side_effect=AssertionError("network should not be used")):
            result = CozeProvider().run(build_mock_task())
        self.assertEqual(result["status"], "completed")
        self.assertFalse(result["network_accessed"])
        self.assertFalse(result["external_api_called"])

    def test_output_schema_is_valid(self):
        result = CozeProvider().run(build_mock_task())
        required = [
            "provider_name",
            "execution_mode",
            "status",
            "summary",
            "capabilities",
            "limitations",
            "risks",
            "next_steps",
            "requires_approval",
        ]
        for key in required:
            self.assertIn(key, result)
        json.dumps(result, ensure_ascii=False)

    def test_requires_approval_true(self):
        result = CozeProvider().run(build_mock_task())
        self.assertTrue(result["requires_approval"])

    def test_forbidden_actions_not_executed(self):
        result = CozeProvider().run(build_mock_task())
        self.assertFalse(result["forbidden_actions_executed"])
        self.assertTrue(result["design"]["safety_boundary"]["no_publish"])

    def test_failure_sample_returns_blocked(self):
        task = build_mock_task()
        task.pop("mission_id")
        result = CozeProvider().run(task)
        self.assertEqual(result["status"], "blocked")
        self.assertFalse(result["external_api_called"])

    def test_v1_freeze_modules_not_required(self):
        result = CozeProvider().run(build_mock_task())
        self.assertEqual(result["status"], "completed")
        self.assertNotIn("mission_control_api", json.dumps(result))
        self.assertNotIn("worker_runner", json.dumps(result))
        self.assertNotIn("exception_framework.py", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
