
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from unittest import TestCase

from nora_common.validation.dictionary_validator import DictionaryValidator

from nora_fleet.internals.validation.network.missing_nodes_network_validator import MissingNodesNetworkValidator

from tests.nora_fleet.internals.validation.network.abstract_network_validator_test import AbstractNetworkValidatorTest


class TestMissingNodesNetworkValidator(TestCase, AbstractNetworkValidatorTest):
    """
    Unit tests for MissingNodesNetworkValidator class.
    """

    def create_validator(self) -> DictionaryValidator:
        """
        Creates an instance of the validator
        """
        return MissingNodesNetworkValidator()

    def test_missing_nodes(self):
        """
        Tests a network where there is an unreachable agent.
        """
        validator: DictionaryValidator = self.create_validator()

        # Open a known good network file
        config: Dict[str, Any] = self.restore("esp_decision_assistant.hocon")

        # Invalidate per the test - add a node at the predictor
        config["tools"][2]["tools"] = ["missing_node"]

        errors: List[str] = validator.validate(config)

        self.assertEqual(1, len(errors), errors[-1])

    def test_tools_as_string_does_not_iterate_chars(self):
        """
        Tests that a malformed `tools` field (string instead of list) does
        not silently iterate the string character-by-character, which would
        flag each character as a missing node. coerce_tools treats it as
        empty; the shape error is reported separately by ToolsShapeValidator.
        """
        validator: DictionaryValidator = self.create_validator()

        config: Dict[str, Any] = self.restore("hello_world.hocon")
        # announcer's tools as a string referring to an existing agent
        config["tools"][0]["tools"] = "synonymizer"

        errors: List[str] = validator.validate(config)
        # If we iterated chars, each char would be reported as missing.
        # With defensive coercion, no missing-node errors are reported.
        self.assertEqual(0, len(errors), errors)
