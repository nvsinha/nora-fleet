
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_fleet.internals.graph.registry.activation_factory import ActivationFactory
from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.interfaces.agent_tool_factory import AgentToolFactory
from nora_fleet.internals.interfaces.callable_activation import CallableActivation
from nora_fleet.internals.interfaces.front_man import FrontMan
from nora_fleet.internals.run_context.interfaces.agent_network_inspector import AgentNetworkInspector
from nora_fleet.internals.run_context.interfaces.run_context import RunContext


class AgentToolRegistry(AgentNetworkInspector, AgentToolFactory):
    """
    Puts together an AgentNetwork data-only spec with an ActivationFactory
    so that a single entity can handle both interfaces.
    """

    def __init__(self, agent_network: AgentNetwork):
        """
        Constructor

        :param agent_network: The AgentNetwork configuration to base all our info on
        """
        self.agent_network: AgentNetwork = agent_network
        self.factory = ActivationFactory(self.agent_network)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def create_agent_activation(self, parent_run_context: RunContext,
                                parent_agent_spec: Dict[str, Any],
                                name: str,
                                sly_data: Dict[str, Any],
                                args: Dict[str, Any] = None,
                                factory: AgentToolFactory = None,
                                invocation: str = None) -> CallableActivation:
        """
        Create an active node for an agent from its spec.
        This is how CallableActivations create other CallableActivations.

        :param parent_run_context: The RunContext of the agent calling this method
        :param parent_agent_spec: The spec of the agent calling this method.
        :param name: The name of the agent to get out of the registry
        :param sly_data: A mapping whose keys might be referenceable by agents, but whose
                 values should not appear in agent chat text. Can be an empty dictionary.
        :param args: A dictionary of arguments for the newly constructed agent
        :param factory: A factory that will be used to create the agent tool
        :param invocation: The invocation style of the activation.
        :return: The CallableActivation agent referred to by the name.
        """
        return self.factory.create_agent_activation(parent_run_context, parent_agent_spec,
                                                    name, sly_data, args, self, invocation)

    def create_front_man(self,
                         sly_data: Dict[str, Any] = None,
                         parent_run_context: RunContext = None) -> FrontMan:
        """
        Find and create the FrontMan for DataDrivenChat.

        :param sly_data: A mapping whose keys might be referenceable by agents, but whose
                 values should not appear in agent chat text. Can be an empty dictionary.
        :param parent_run_context: A RunContext instance
        """
        return self.factory.create_front_man(sly_data, parent_run_context, self)

    def get_agent_tool_path(self) -> str:
        """
        :return: The path under which tools for this registry should be looked for.
        """
        return self.factory.get_agent_tool_path()

    def get_config(self) -> Dict[str, Any]:
        """
        :return: The entire config dictionary given to the instance.
        """
        return self.agent_network.get_config()

    def get_agent_tool_spec(self, name: str) -> Dict[str, Any]:
        """
        :param name: The name of the agent tool to get out of the registry
        :return: The dictionary representing the spec registered agent
        """
        return self.agent_network.get_agent_tool_spec(name)

    def get_name_from_spec(self, agent_spec: Dict[str, Any]) -> str:
        """
        :param agent_spec: A single agent to register
        :return: The agent name as per the spec
        """
        return self.agent_network.get_name_from_spec(agent_spec)

    def find_front_man(self) -> str:
        """
        :return: A single tool name to use as the root of the chat agent.
                 This guy will be user facing.  If there are none or > 1,
                 an exception will be raised.
        """
        return self.agent_network.find_front_man()

    def get_agent_llm_info_file(self) -> str:
        """
        :return: The absolute path of agent llm info file for llm extension.
        """
        return self.agent_network.get_agent_llm_info_file()

    def get_size_in_bytes(self) -> int:
        """
        :return: The size in bytes of this AgentNetwork
        """
        return self.agent_network.get_size_in_bytes()
