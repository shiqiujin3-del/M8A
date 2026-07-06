#!/usr/bin/env python3
"""Tests for Coze staging credential readiness check."""

from __future__ import annotations

import unittest

from check_coze_config import check_env


class CheckCozeConfigTest(unittest.TestCase):
    def test_not_ready_when_required_values_missing(self):
        result = check_env({})

        self.assertFalse(result["ready"])
        self.assertEqual(result["status"], "not_ready")
        self.assertEqual(result["required"]["M8A_COZE_API_TOKEN"], "missing")
        self.assertFalse(result["api_called"])
        self.assertFalse(result["secrets_printed"])

    def test_ready_when_required_values_exist_without_printing_values(self):
        env = {
            "M8A_COZE_BASE_URL": "https://example.invalid",
            "M8A_COZE_API_TOKEN": "redacted_value",
            "M8A_COZE_WORKFLOW_ID": "workflow_mock",
        }
        result = check_env(env)

        self.assertTrue(result["ready"])
        self.assertEqual(result["status"], "ready")
        serialized = str(result)
        self.assertNotIn("redacted_value", serialized)
        self.assertFalse(result["api_called"])
        self.assertFalse(result["safe_to_call_api"])

    def test_optional_workspace_does_not_block_readiness(self):
        env = {
            "M8A_COZE_BASE_URL": "https://example.invalid",
            "M8A_COZE_API_TOKEN": "redacted_value",
            "M8A_COZE_WORKFLOW_ID": "workflow_mock",
        }
        result = check_env(env)

        self.assertTrue(result["ready"])
        self.assertEqual(result["optional"]["M8A_COZE_WORKSPACE_ID"], "missing")


if __name__ == "__main__":
    unittest.main()
