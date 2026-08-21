
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.interfaces.agent_network_provider import AgentNetworkProvider


class FixedAgentNetworkProvider(AgentNetworkProvider):
    """
    Class providing fixed immutable AgentNetwork for a given agent in the service scope.
    """
    def __init__(self, agent_network: AgentNetwork):
        """
        Constructor.
        :param agent_network: AgentNetwork instance to be returned by this provider.
        """
        self.agent_network: AgentNetwork = agent_network

    def get_agent_network(self) -> AgentNetwork:
        """
        :return: Current AgentNetwork instance for specific agent name.
        """
        return self.agent_network
