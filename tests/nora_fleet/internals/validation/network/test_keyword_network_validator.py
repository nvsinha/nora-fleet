
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

from nora_fleet.internals.validation.network.keyword_network_validator import KeywordNetworkValidator

from tests.nora_fleet.internals.validation.network.abstract_network_validator_test import AbstractNetworkValidatorTest


class TestKeywordNetworkValidator(TestCase, AbstractNetworkValidatorTest):
    """
    Unit tests for KeywordNetworkValidator class.
    """

    def create_validator(self) -> DictionaryValidator:
        """
        Creates an instance of the validator
        """
        return KeywordNetworkValidator()

    def test_empty_instructions(self):
        """
        Tests a network where at least one of the nodes has empty instructions
        """
        validator: DictionaryValidator = self.create_validator()

        config: Dict[str, Any] = self.restore("hello_world.hocon")
        config["tools"][0]["instructions"] = ""

        errors: List[str] = validator.validate(config)
        self.assertEqual(1, len(errors))

    def test_instructions_wrong_type(self):
        """
        Tests a network where instructions is not a string
        """
        validator: DictionaryValidator = self.create_validator()

        config: Dict[str, Any] = self.restore("hello_world.hocon")
        config["tools"][0]["instructions"] = 123

        errors: List[str] = validator.validate(config)
        self.assertEqual(1, len(errors))
        self.assertIn("must be a str", errors[0])

    def test_description_empty(self):
        """
        Tests a network where function.description is empty
        """
        validator: DictionaryValidator = self.create_validator()

        config: Dict[str, Any] = self.restore("hello_world.hocon")
        config["tools"][0]["function"]["description"] = ""

        errors: List[str] = validator.validate(config)
        self.assertEqual(1, len(errors))
        self.assertIn("function.description", errors[0])

    def test_description_wrong_type(self):
        """
        Tests a network where function.description is not a string
        """
        validator: DictionaryValidator = self.create_validator()

        config: Dict[str, Any] = self.restore("hello_world.hocon")
        config["tools"][0]["function"]["description"] = 123

        errors: List[str] = validator.validate(config)
        self.assertEqual(1, len(errors))
        self.assertIn("must be a str", errors[0])

    def test_function_wrong_type(self):
        """
        Tests a network where function is not a dict
        """
        validator: DictionaryValidator = self.create_validator()

        config: Dict[str, Any] = self.restore("hello_world.hocon")
        config["tools"][0]["function"] = "not a dict"

        errors: List[str] = validator.validate(config)
        self.assertEqual(1, len(errors))
        self.assertIn("'function' must be a dict", errors[0])

    def test_keywords_filter(self):
        """
        Tests that the keywords parameter controls which validations run
        """
        validator = KeywordNetworkValidator(keywords={"description"})

        config: Dict[str, Any] = self.restore("hello_world.hocon")
        # Empty instructions should be ignored when only validating description
        config["tools"][0]["instructions"] = ""

        errors: List[str] = validator.validate(config)
        self.assertEqual(0, len(errors))
