
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from unittest import TestCase

from nora_fleet import REGISTRIES_DIR
from nora_fleet.internals.graph.persistence.agent_network_restorer import AgentNetworkRestorer
from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.graph.utils.allow_util import AllowUtil


class TestAllowUtil(TestCase):
    """
    Unit tests for AllowUtil class.
    """

    def get_agent_network(self, hocon_file: str) -> AgentNetwork:
        """
        :param hocon_file: the hocon file to restore
        :return: the AgentNetwork specified by the hocon file within the nora-fleet repo registries
        """
        file_reference: str = REGISTRIES_DIR.get_file_in_basis(hocon_file)
        restorer = AgentNetworkRestorer()
        agent_network: AgentNetwork = restorer.restore(file_reference=file_reference)
        return agent_network

    def test_allow_not_there(self):
        """
        Tests when the allow block is not present anywhere
        """
        agent_network: AgentNetwork = self.get_agent_network("hello_world.hocon")
        is_allowed: bool = AllowUtil.is_allowed(agent_network, "reservations", ["middleware"])
        self.assertFalse(is_allowed)

    def test_allow_in_agent(self):
        """
        Tests when the allow block is present in an agent
        """
        agent_network: AgentNetwork = self.get_agent_network("copy_cat.hocon")
        is_allowed: bool = AllowUtil.is_allowed(agent_network, "reservations", ["middleware"])
        self.assertTrue(is_allowed)

    def test_allow_in_middleware(self):
        """
        Tests when the allow block is present in an agent
        """
        agent_network: AgentNetwork = self.get_agent_network("copy_cat_middleware.hocon")
        is_allowed: bool = AllowUtil.is_allowed(agent_network, "reservations", ["middleware"])
        self.assertTrue(is_allowed)
