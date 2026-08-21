
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict


class AgentNetworkInspector:
    """
    Interface describing an entity that can examine the configuration of the
    agent network spec.
    Having this interface breaks some circular dependencies.
    """

    def get_config(self) -> Dict[str, Any]:
        """
        :return: The entire config dictionary given to the instance.
        """
        raise NotImplementedError

    def get_agent_tool_spec(self, name: str) -> Dict[str, Any]:
        """
        :param name: The name of the agent tool to get out of the registry
        :return: The dictionary representing the spec registered agent
        """
        raise NotImplementedError

    def get_name_from_spec(self, agent_spec: Dict[str, Any]) -> str:
        """
        :param agent_spec: A single agent to register
        :return: The agent name as per the spec
        """
        raise NotImplementedError

    def find_front_man(self) -> str:
        """
        :return: A single tool name to use as the root of the chat agent.
                 This guy will be user facing.  If there are none or > 1,
                 an exception will be raised.
        """
        raise NotImplementedError

    def get_size_in_bytes(self) -> int:
        """
        :return: The size in bytes of this AgentNetwork
        """
        raise NotImplementedError
