
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.interfaces.agent_network_provider import AgentNetworkProvider


class AgentStorageSource:
    """
    Interface onto AgentNetworkStorage so that there is not a tangle with the service side.
    """

    def get_agent_network_provider(self, agent_name: str) -> AgentNetworkProvider:
        """
        Get AgentNetworkProvider for a specific agent
        :param agent_name: name of an agent
        """
        raise NotImplementedError
