
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.graph.registry.agent_network import AgentNetwork


class AgentNetworkProvider:
    """
    Abstract interface for providing an AgentNetwork instance at run-time.
    """
    def get_agent_network(self) -> AgentNetwork:
        """
        :return: AgentNetwork instance or None if no such AgentNetwork is available.
        """
        raise NotImplementedError
