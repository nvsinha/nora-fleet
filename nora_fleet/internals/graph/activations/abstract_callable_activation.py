
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from langchain_core.messages.base import BaseMessage

from nora_fleet.internals.interfaces.agent_tool_factory import AgentToolFactory
from nora_fleet.internals.interfaces.callable_activation import CallableActivation
from nora_fleet.internals.run_context.interfaces.agent_network_inspector import AgentNetworkInspector
from nora_fleet.internals.run_context.interfaces.run_context import RunContext


class AbstractCallableActivation(CallableActivation):
    """
    An abstract implementation of the CallableActivation interface
    containing common policy for all tools.

    Worth noting that this is used as a base implementation for:
        * ClassActivation
        * ExternalActivation
        * CallingActivation
    """

    def __init__(self,
                 factory: AgentToolFactory,
                 agent_tool_spec: Dict[str, Any],
                 sly_data: Dict[str, Any]):
        """
        Constructor

        :param factory: The factory for Agent Tools.
        :param agent_tool_spec: The dictionary describing the JSON agent tool
                            to be used by the instance
        :param sly_data: A mapping whose keys might be referenceable by agents, but whose
                 values should not appear in agent chat text. Can be an empty dictionary.
        """
        self.factory: AgentToolFactory = factory
        self.agent_tool_spec: Dict[str, Any] = agent_tool_spec
        self.sly_data: Dict[str, Any] = sly_data

        # Subclasses should set up the RunContext for themselves and get the journal from it
        # because not everyone needs an llm_config
        self.run_context: RunContext = None

    def get_agent_tool_spec(self) -> Dict[str, Any]:
        """
        :return: the dictionary describing the data-driven agent
        """
        return self.agent_tool_spec

    def get_name(self) -> str:
        """
        :return: the name of the data-driven agent as it comes from the spec
        """
        agent_spec: Dict[str, Any] = self.get_agent_tool_spec()
        agent_name: str = self.factory.get_name_from_spec(agent_spec)
        return agent_name

    def get_inspector(self) -> AgentNetworkInspector:
        """
        :return: The factory containing all the tool specs
        """
        # For now, our inspector is an AgentToolFactory
        return self.factory

    def get_sly_data(self) -> Dict[str, Any]:
        """
        :return: A mapping whose keys might be referenceable by agents, but whose
                 values should not appear in agent chat text. Can be an empty dictionary.
        """
        return self.sly_data

    def get_origin(self) -> List[Dict[str, Any]]:
        """
        :return: A List of origin dictionaries indicating the origin of the run.
                The origin can be considered a path to the original call to the front-man.
                Origin dictionaries themselves each have the following keys:
                    "tool"                  The string name of the tool in the spec
                    "instantiation_index"   An integer indicating which incarnation
                                            of the tool is being dealt with.
        """
        return self.run_context.get_origin()

    async def close_of_work(self, parent_resource: RunContext = None):
        """
        Release resources owned by this context when the work is all done.
        This can happen later than when the request is complete.

        :param parent_resource: parent resource, if any. Expected to be the
                RunContext which contains the scope of operation of this CallableActivation
        """
        if self.run_context is not None:
            await self.run_context.close_of_work(parent_resource)
            self.run_context = None

    async def build(self) -> BaseMessage:
        """
        Main entry point to the class.

        :return: A BaseMessage produced during this process.
        """
        raise NotImplementedError
