
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from unittest import TestCase

from nora_fleet.message.utils.sly_data_redactor import SlyDataRedactor


class TestSlyDataRedactor(TestCase):
    """
    Unit tests for SlyDataRedactor class.
    """

    def test_assumptions(self):
        """
        Can we construct?
        """
        agent_spec = None
        redactor = SlyDataRedactor(agent_spec)
        self.assertIsNotNone(redactor)

    def test_true_false(self):
        """
        Tests basic true/false operations of the SlyDataRedactor
        """
        agent_spec = {
            "allow": {
                "sly_data": {
                    "yes": True,
                    "no": False
                }
            }
        }
        redactor = SlyDataRedactor(agent_spec, config_keys=["allow.sly_data"])

        sly_data = {
            "yes": 1,
            "no": 0,
            "not_mentioned": -1,
        }

        redacted: Dict[str, Any] = redactor.filter_config(sly_data)

        self.assertIsNotNone(redacted.get("yes"))
        self.assertIsNone(redacted.get("no"))
        self.assertIsNone(redacted.get("not_mentioned"))

    def test_brute_force_true(self):
        """
        Tests the let-everything-through case of the SlyDataRedactor
        """
        agent_spec = {
            "allow": {
                "sly_data": True
            }
        }
        redactor = SlyDataRedactor(agent_spec, config_keys=["allow.sly_data"])

        sly_data = {
            "yes": 1,
            "no": 0,
            "not_mentioned": -1,
        }

        redacted: Dict[str, Any] = redactor.filter_config(sly_data)

        self.assertIsNotNone(redacted.get("yes"))
        self.assertIsNotNone(redacted.get("no"))
        self.assertIsNotNone(redacted.get("not_mentioned"))

    def test_brute_force_false(self):
        """
        Tests explicit let-nothing-through case of the SlyDataRedactor
        """
        agent_spec = {
            "allow": {
                "sly_data": False
            }
        }
        redactor = SlyDataRedactor(agent_spec, config_keys=["allow.sly_data"])

        sly_data = {
            "yes": 1,
            "no": 0,
            "not_mentioned": -1,
        }

        redacted: Dict[str, Any] = redactor.filter_config(sly_data)

        self.assertIsNone(redacted.get("yes"))
        self.assertIsNone(redacted.get("no"))
        self.assertIsNone(redacted.get("not_mentioned"))

    def test_no_spec(self):
        """
        Tests implicit let-nothing-through case of the SlyDataRedactor
        """
        agent_spec = {
        }
        redactor = SlyDataRedactor(agent_spec, config_keys=["allow.sly_data"])

        sly_data = {
            "yes": 1,
            "no": 0,
            "not_mentioned": -1,
        }

        redacted: Dict[str, Any] = redactor.filter_config(sly_data)

        self.assertIsNone(redacted.get("yes"))
        self.assertIsNone(redacted.get("no"))
        self.assertIsNone(redacted.get("not_mentioned"))

    def test_key_list(self):
        """
        Tests basic list specification where listed keys get through
        """
        agent_spec = {
            "allow": {
                "sly_data": ["yes"]
            }
        }
        redactor = SlyDataRedactor(agent_spec, config_keys=["allow.sly_data"])

        sly_data = {
            "yes": 1,
            "no": 0,
            "not_mentioned": -1,
        }

        redacted: Dict[str, Any] = redactor.filter_config(sly_data)

        self.assertIsNotNone(redacted.get("yes"))
        self.assertIsNone(redacted.get("no"))
        self.assertIsNone(redacted.get("not_mentioned"))

    def test_translation(self):
        """
        Tests translation of keys for the SlyDataRedactor
        """
        agent_spec = {
            "allow": {
                "sly_data": {
                    "yes": "affirmative",
                    "no": "negative"
                }
            }
        }
        redactor = SlyDataRedactor(agent_spec, config_keys=["allow.sly_data"])

        sly_data = {
            "yes": 1,
            "no": 0,
            "not_mentioned": -1,
        }

        redacted: Dict[str, Any] = redactor.filter_config(sly_data)

        self.assertIsNone(redacted.get("yes"))
        self.assertIsNone(redacted.get("no"))
        self.assertIsNone(redacted.get("not_mentioned"))
        self.assertIsNotNone(redacted.get("affirmative"))
        self.assertIsNotNone(redacted.get("negative"))
