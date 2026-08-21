
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

# DEF - tangle to be resolved later
from nora_fleet.service.generic.async_agent_service_provider import AsyncAgentServiceProvider


class AgentAuthorizer:
    """
    Interface for authorizing agent specifics given metadata from a request.
    """

    async def allow_agent(self, agent_name: str, metadata: Dict[str, Any]) -> Tuple[bool, AsyncAgentServiceProvider]:
        """
        Is the request allowed for this agent?

        :param agent_name: name of an agent
        :param metadata: metadata from the request
        :return: a tuple of:
                * True if metadata says user is authrorized to route requests is allowed for this agent
                  False otherwise
                * instance of AsyncAgentService if it exists.  None otherwise
        """
        raise NotImplementedError

    async def list_agents(self, metadata: Dict[str, Any]) -> List[str]:
        """
        What is the list of allowed agents for this request?
        :param metadata: metadata from the request
        :return: a list of agent names allowed for this request
        """
        raise NotImplementedError
