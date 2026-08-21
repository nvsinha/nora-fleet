
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

from nora_fleet.internals.validation.network.tool_name_network_validator import ToolNameNetworkValidator

from tests.nora_fleet.internals.validation.network.abstract_network_validator_test import AbstractNetworkValidatorTest


class TestToolNameNetworkValidator(TestCase, AbstractNetworkValidatorTest):
    """
    Unit tests for ToolNameNetworkValidator class.
    """

    def create_validator(self) -> DictionaryValidator:
        """
        Creates an instance of the validator
        """
        return ToolNameNetworkValidator()

    def test_bad_name(self):
        """
        Tests a network where at least one of the nodes has a bad name
        """
        validator: DictionaryValidator = ToolNameNetworkValidator()

        # Open a known good network file
        config: Dict[str, Any] = self.restore("hello_world.hocon")

        # Invalidate per the test
        config["tools"][0]["name"] = "ann0un$er"

        errors: List[str] = validator.validate(config)
        self.assertEqual(1, len(errors))

    def test_deep_name(self):
        """
        Tests a network where at least one of the nodes has a reference to
        an exeternal network in a directory hierachy.
        """
        validator: DictionaryValidator = ToolNameNetworkValidator()

        # Open a known good network file
        config: Dict[str, Any] = self.restore("deep/math_guy_passthrough.hocon")

        errors: List[str] = validator.validate(config)
        self.assertEqual(0, len(errors))
