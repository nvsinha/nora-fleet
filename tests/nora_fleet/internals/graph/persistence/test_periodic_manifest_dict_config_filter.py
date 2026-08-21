
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

from nora_fleet.internals.graph.persistence.periodic_manifest_dict_config_filter import PeriodicManifestDictConfigFilter


class TestPeriodicManifestDictConfigFilter(TestCase):
    """
    Unit tests for PeriodicManifestDictConfigFilter class.
    """

    def test_assumptions(self):
        """
        Tests when the allow block is not present anywhere
        """
        config_filter = PeriodicManifestDictConfigFilter("manifest.hocon", "agent_network")
        self.assertIsNotNone(config_filter)

    def test_no_value(self):
        """
        Tests when the "periodic" key does not exist
        """
        config_filter = PeriodicManifestDictConfigFilter("manifest.hocon", "agent_network")

        basis_config: Dict[str, Any] = {}
        filtered_config: Dict[str, Any] = config_filter.filter_config(basis_config)
        self.assertIsNotNone(filtered_config)

        periodic: bool = filtered_config.get("periodic")
        self.assertIsNotNone(periodic)
        self.assertFalse(periodic)

    def test_false(self):
        """
        Tests when the "periodic" key is false
        """
        config_filter = PeriodicManifestDictConfigFilter("manifest.hocon", "agent_network")

        basis_config: Dict[str, Any] = {
            "periodic": False
        }
        filtered_config: Dict[str, Any] = config_filter.filter_config(basis_config)
        self.assertIsNotNone(filtered_config)

        periodic: bool = filtered_config.get("periodic")
        self.assertIsNotNone(periodic)
        self.assertFalse(periodic)

    def test_true(self):
        """
        Tests when the "periodic" key is false
        """
        config_filter = PeriodicManifestDictConfigFilter("manifest.hocon", "agent_network")

        basis_config: Dict[str, Any] = {
            "periodic": True
        }
        filtered_config: Dict[str, Any] = config_filter.filter_config(basis_config)
        self.assertIsNotNone(filtered_config)

        periodic: Dict[str, Any] = filtered_config.get("periodic")
        self.assertIsNotNone(periodic)

        # None is OK. Default is True.
        enabled: bool = periodic.get("enable")
        self.assertIsNone(enabled)

        interactions: List[Dict[str, Any]] = periodic.get("interactions")
        self.assertIsNotNone(interactions)
        self.assertEqual(1, len(interactions))
