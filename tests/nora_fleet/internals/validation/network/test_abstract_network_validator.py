
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

from nora_fleet.internals.validation.network.abstract_network_validator import AbstractNetworkValidator


class TestAbstractNetworkValidator(TestCase):
    """
    Unit tests for the static utility methods on AbstractNetworkValidator.

    These are cross-cutting helpers used by concrete validators to read
    tool-related fields safely (`coerce_tools`, `coerce_args_tools`),
    classify tool strings (`is_url_or_path`), and filter dict-shaped tool
    entries (`remove_dictionary_tools`). The shape-checking validator
    (ToolsShapeValidator) surfaces malformed `tools` / `args.tools` as
    user-facing errors; these helpers are the matching tolerant readers
    used during graph traversal — they must not raise on malformed input.
    """

    # ---- coerce_tools ----

    def test_coerce_tools_returns_list_as_is(self):
        """Returns a real list, not a dict_values view."""
        agent_spec: Dict[str, Any] = {"tools": ["a", "b"]}
        result: List[Any] = AbstractNetworkValidator.coerce_tools(agent_spec)
        self.assertEqual(["a", "b"], result)

    def test_coerce_tools_coerces_string_to_empty(self):
        """tools as a string should not be iterated char-by-char."""
        agent_spec: Dict[str, Any] = {"tools": "synonymizer"}
        result: List[Any] = AbstractNetworkValidator.coerce_tools(agent_spec)
        self.assertEqual([], result)

    def test_coerce_tools_missing_returns_empty(self):
        """tools as a bare string should not raise AttributeError on .values()."""
        agent_spec: Dict[str, Any] = {}
        result: List[Any] = AbstractNetworkValidator.coerce_tools(agent_spec)
        self.assertEqual([], result)

    # ---- coerce_args_tools ----

    def test_coerce_args_tools_dict_returns_values(self):
        """Returns a real list, not a dict_values view."""
        agent_spec: Dict[str, Any] = {"args": {"tools": {"a": "agent_a", "b": "agent_b"}}}
        result: List[Any] = AbstractNetworkValidator.coerce_args_tools(agent_spec)
        self.assertIsInstance(result, list)
        self.assertEqual(sorted(result), ["agent_a", "agent_b"])

    def test_coerce_args_tools_list_returns_as_is(self):
        """Returns a real list, not a dict_values view."""
        agent_spec: Dict[str, Any] = {"args": {"tools": ["agent_a", "agent_b"]}}
        result: List[Any] = AbstractNetworkValidator.coerce_args_tools(agent_spec)
        self.assertEqual(["agent_a", "agent_b"], result)

    def test_coerce_args_tools_wrong_type_returns_empty(self):
        """args.tools as a bare string should not raise AttributeError on .values()."""
        agent_spec: Dict[str, Any] = {"args": {"tools": "synonymizer"}}
        result: List[Any] = AbstractNetworkValidator.coerce_args_tools(agent_spec)
        self.assertEqual([], result)

    def test_coerce_args_tools_missing_returns_empty(self):
        """args.tools as a bare string should not raise AttributeError on .values()."""
        agent_spec: Dict[str, Any] = {}
        result: List[Any] = AbstractNetworkValidator.coerce_args_tools(agent_spec)
        self.assertEqual([], result)

    # ---- is_url_or_path ----

    def test_is_url_or_path_absolute_path(self):
        """Absolute paths (starting with '/') should be recognized."""
        self.assertTrue(AbstractNetworkValidator.is_url_or_path("/some/path/to/file"))

    def test_is_url_or_path_http_url(self):
        """HTTP URLs should be recognized as well."""
        self.assertTrue(AbstractNetworkValidator.is_url_or_path("http://example.com/api"))

    def test_is_url_or_path_https_url(self):
        """HTTPS URLs should be recognized as well."""
        self.assertTrue(AbstractNetworkValidator.is_url_or_path("https://example.com/api"))

    def test_is_url_or_path_agent_name(self):
        """Agent names should not be recognized as URLs or paths."""
        self.assertFalse(AbstractNetworkValidator.is_url_or_path("synonymizer"))

    def test_is_url_or_path_empty_string(self):
        """Empty strings should not raise an exception."""
        self.assertFalse(AbstractNetworkValidator.is_url_or_path(""))

    def test_is_url_or_path_relative_path(self):
        """Only absolute paths (starting with '/') are recognized."""
        self.assertFalse(AbstractNetworkValidator.is_url_or_path("relative/path"))

    # ---- remove_dictionary_tools ----

    def test_remove_dictionary_tools_all_strings(self):
        """
        If all tools are strings, return them as-is.
        """
        down_chains: List[Any] = ["a", "b", "c"]
        result: List[str] = AbstractNetworkValidator.remove_dictionary_tools(down_chains)
        self.assertEqual(["a", "b", "c"], result)

    def test_remove_dictionary_tools_mixed(self):
        """
        If some tools are dictionary entries, remove them.
        """
        down_chains: List[Any] = ["a", {"server": "mcp"}, "b"]
        result: List[str] = AbstractNetworkValidator.remove_dictionary_tools(down_chains)
        self.assertEqual(["a", "b"], result)

    def test_remove_dictionary_tools_only_dicts(self):
        """
        If all tools are dictionary entries, return an empty list.
        """
        down_chains: List[Any] = [{"server": "mcp"}, {"server": "other"}]
        result: List[str] = AbstractNetworkValidator.remove_dictionary_tools(down_chains)
        self.assertEqual([], result)

    def test_remove_dictionary_tools_empty(self):
        """
        An empty list should not raise an exception.
        """
        result: List[str] = AbstractNetworkValidator.remove_dictionary_tools([])
        self.assertEqual([], result)
