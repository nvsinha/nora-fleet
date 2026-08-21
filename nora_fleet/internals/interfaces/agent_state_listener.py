
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.interfaces.agent_storage_source import AgentStorageSource


class AgentStateListener:
    """
    Abstract interface for publishing agent state changes -
    when an agent is being added or removed from the service.
    """

    def agent_added(self, agent_name: str, source: AgentStorageSource):
        """
        Agent is being added to the service.
        :param agent_name: name of an agent
        :param source: The AgentStorageSource source of the message
        """
        raise NotImplementedError

    def agent_modified(self, agent_name: str, source: AgentStorageSource):
        """
        Existing agent has been modified in service scope.
        :param agent_name: name of an agent
        :param source: The AgentStorageSource source of the message
        """
        raise NotImplementedError

    def agent_removed(self, agent_name: str, source: AgentStorageSource):
        """
        Agent is being removed from the service.
        :param agent_name: name of an agent
        :param source: The AgentStorageSource source of the message
        """
        raise NotImplementedError
