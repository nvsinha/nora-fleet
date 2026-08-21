
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

import json

from unittest import TestCase

from nora_common.config.config_filter import ConfigFilter
from nora_common.parsers.dictionary_extractor import DictionaryExtractor

from nora_fleet.internals.graph.filters.defaults_config_filter import DefaultsConfigFilter


class TestDefaultsConfigFilter(TestCase):
    """
    Unit tests for DefaultsConfigFilter class.
    """

    def get_filter(self) -> ConfigFilter:
        """
        Return the object we are testing
        """
        return DefaultsConfigFilter()

    def test_assumptions(self):
        """
        Can we construct?
        """
        my_filter: ConfigFilter = self.get_filter()
        self.assertIsNotNone(my_filter)

    def test_no_additions(self):
        """
        Tests basic non-operations of the ConfigFilter
        """
        my_filter: ConfigFilter = self.get_filter()

        dict_in: Dict[str, Any] = {
            "tools": [
                {
                    "name": "foo",
                    "function": {
                        "description": "blah blah"
                    }
                }
            ]
        }

        dict_out: Dict[str, Any] = my_filter.filter_config(dict_in)

        json_in: str = json.dumps(dict_in, indent=4, sort_keys=True)
        json_out: str = json.dumps(dict_out, indent=4, sort_keys=True)

        self.assertEqual(json_in, json_out)

    def test_global_sly_data_schema_only(self):
        """
        Tests when sly_data_schema is in the global defs only
        """
        my_filter: ConfigFilter = self.get_filter()

        dict_in: Dict[str, Any] = {
            # Typical BYOK
            "sly_data_schema": {
                "type": "object",
                "properties": {
                    "llm_config": {
                        "type": "object",
                        "properties": {
                            "openai_api_key": {
                                "type": "string",
                                "description": "The user's OpenAI API key"
                            }
                        }
                    }
                },
                "required": ["llm_config"]
            },
            "tools": [
                {
                    "name": "foo",
                    "function": {
                        "description": "blah blah"
                    }
                }
            ]
        }

        dict_out: Dict[str, Any] = my_filter.filter_config(dict_in)

        tools: List[Dict[str, Any]] = dict_out.get("tools")
        first_tool: Dict[str, Any] = tools[0]
        extractor: DictionaryExtractor = DictionaryExtractor(first_tool)

        value: Any = extractor.get("function.sly_data_schema")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, dict)

        value: Any = extractor.get("function.sly_data_schema.required")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 1)

    def test_local_sly_data_schema_only(self):
        """
        Tests when sly_data_schema is in the local defs only
        """
        my_filter: ConfigFilter = self.get_filter()

        dict_in: Dict[str, Any] = {
            "tools": [
                {
                    "name": "foo",
                    "function": {
                        "description": "blah blah",
                        "sly_data_schema": {
                            "type": "object",
                            "properties": {
                                "custom_value": {
                                    "type": "string",
                                    "description": "A custom string value"
                                }
                            },
                            "required": ["custom_value"]
                        }
                    }
                }
            ]
        }

        dict_out: Dict[str, Any] = my_filter.filter_config(dict_in)

        tools: List[Dict[str, Any]] = dict_out.get("tools")
        first_tool: Dict[str, Any] = tools[0]
        extractor: DictionaryExtractor = DictionaryExtractor(first_tool)

        value: Any = extractor.get("function.sly_data_schema")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, dict)

        value: Any = extractor.get("function.sly_data_schema.required")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 1)

    def test_sly_data_schema_both(self):
        """
        Tests when sly_data_schema is in both the global defs and local defs
        """
        my_filter: ConfigFilter = self.get_filter()

        dict_in: Dict[str, Any] = {
            # Typical BYOK
            "sly_data_schema": {
                "type": "object",
                "properties": {
                    "llm_config": {
                        "type": "object",
                        "properties": {
                            "openai_api_key": {
                                "type": "string",
                                "description": "The user's OpenAI API key"
                            }
                        }
                    }
                },
                "required": ["llm_config"]
            },
            "tools": [
                {
                    "name": "foo",
                    "function": {
                        "description": "blah blah",
                        "sly_data_schema": {
                            "type": "object",
                            "properties": {
                                "custom_value": {
                                    "type": "string",
                                    "description": "A custom string value"
                                }
                            },
                            "required": ["custom_value"]
                        }
                    }
                }
            ]
        }

        dict_out: Dict[str, Any] = my_filter.filter_config(dict_in)

        tools: List[Dict[str, Any]] = dict_out.get("tools")
        first_tool: Dict[str, Any] = tools[0]
        extractor: DictionaryExtractor = DictionaryExtractor(first_tool)

        value: Any = extractor.get("function.sly_data_schema")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, dict)

        value: Any = extractor.get("function.sly_data_schema.properties")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, dict)
        self.assertEqual(len(value.keys()), 2)

        value: Any = extractor.get("function.sly_data_schema.required")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 2)

    def test_sly_data_schema_both_union(self):
        """
        Tests when sly_data_schema is in both the global defs and local defs
        and they have the same key
        """
        my_filter: ConfigFilter = self.get_filter()

        dict_in: Dict[str, Any] = {
            # Typical BYOK
            "sly_data_schema": {
                "type": "object",
                "properties": {
                    "llm_config": {
                        "type": "object",
                        "properties": {
                            "openai_api_key": {
                                "type": "string",
                                "description": "The user's OpenAI API key"
                            }
                        }
                    }
                },
                "required": ["llm_config"]
            },
            "tools": [
                {
                    "name": "foo",
                    "function": {
                        "description": "blah blah",
                        # Typical BYOK
                        "sly_data_schema": {
                            "llm_config": {
                                "type": "object",
                                "properties": {
                                    "openai_api_key": {
                                        "type": "string",
                                        "description": "The user's OpenAI API key"
                                    }
                                }
                            },
                            "required": ["llm_config"]
                        }
                    }
                }
            ]
        }

        dict_out: Dict[str, Any] = my_filter.filter_config(dict_in)

        tools: List[Dict[str, Any]] = dict_out.get("tools")
        first_tool: Dict[str, Any] = tools[0]
        extractor: DictionaryExtractor = DictionaryExtractor(first_tool)

        value: Any = extractor.get("function.sly_data_schema")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, dict)

        value: Any = extractor.get("function.sly_data_schema.properties")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, dict)
        self.assertEqual(len(value.keys()), 1)

        value: Any = extractor.get("function.sly_data_schema.required")
        self.assertIsNotNone(value)
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 1)
