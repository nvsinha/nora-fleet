
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_fleet.internals.run_context.interfaces.agent_spec_provider import AgentSpecProvider
from nora_fleet.internals.run_context.interfaces.agent_network_inspector import AgentNetworkInspector
from nora_fleet.internals.run_context.interfaces.run import Run


class ToolCaller(AgentSpecProvider):
    """
    Interface for Tools that call Agents/LLMs as functions.
    This is called by langchain Tools and implemented by CallingTool.
    """

    async def make_tool_function_calls(self, component_run: Run) -> Run:
        """
        Calls all of the callable_components' functions

        :param component_run: The Run which the component is operating under
        :return: A potentially updated Run for the component
        """
        raise NotImplementedError

    def get_inspector(self) -> AgentNetworkInspector:
        """
        :return: The AgentNetworkInspector that contains the specs of all the tools
        """
        raise NotImplementedError

    def get_agent_tool_spec(self) -> Dict[str, Any]:
        """
        :return: the dictionary describing the data-driven agent
        """
        raise NotImplementedError

    def get_name(self) -> str:
        """
        :return: the name of the data-driven agent as it comes from the spec
        """
        raise NotImplementedError

    def get_sly_data(self) -> Dict[str, Any]:
        """
        :return: A mapping whose keys might be referenceable by agents, but whose
                 values should not appear in agent chat text. Can be an empty dictionary.
        """
        raise NotImplementedError
