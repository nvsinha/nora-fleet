
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Dict

from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.interfaces.agent_network_provider import AgentNetworkProvider


class SingleAgentNetworkProvider(AgentNetworkProvider):
    """
    Class providing current AgentNetwork for a given agent in the service scope.
    """
    def __init__(self, agent_name: str, agents_table: Dict[str, AgentNetwork]):
        """
        Constructor.
        :param agent_name: name of an agent to provide AgentNetwork instances for;
        :param agents_table: service-wide table mapping agent names to their
            currently active AgentNetwork instances.
            This table is assumed to be dynamically modified outside a single agent scope.
        """
        self.agent_name = agent_name
        self.agents_table: Dict[str, AgentNetwork] = agents_table

    def get_agent_network(self) -> AgentNetwork:
        """
        :return: Current AgentNetwork instance for specific agent name.
                None if this does not exist for the instance's agent_name.
        """
        return self.agents_table.get(self.agent_name)
