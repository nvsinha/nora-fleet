
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from nora_fleet.internals.graph.activations.toolbox_activation import ToolboxActivation
from nora_fleet.internals.graph.preppers.activation_prepper import ActivationPrepper
from nora_fleet.internals.interfaces.agent_tool_factory import AgentToolFactory
from nora_fleet.internals.interfaces.callable_activation import CallableActivation
from nora_fleet.internals.run_context.interfaces.run_context import RunContext


class ToolboxActivationPrepper(ActivationPrepper):
    """
    ActivationPrepper implementation for toolbox activations.
    """

    def is_applicable(self, agent_tool_spec: Dict[str, Any]) -> bool:
        """
        :param agent_tool_spec: the agent tool spec dictionary. Can be None for external agents.
        :return: True if this ActivationPrepper is applicable to the given agent tool spec
        """
        return agent_tool_spec.get("toolbox") is not None

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def prepare_activation(self,
                           name: str,
                           agent_tool_spec: Dict[str, Any],
                           parent_agent_spec: Dict[str, Any],
                           args: Dict[str, Any],
                           sly_data: Dict[str, Any],
                           parent_run_context: RunContext,
                           factory: AgentToolFactory,
                           invocation: str) -> CallableActivation:
        """
        Assuming that is_applicable() has already been vetted, this method prepares a CallableActivation
        object for the given agent tool spec.

        :param name: the name of the agent tool
        :param agent_tool_spec: the agent tool spec dictionary
        :param parent_agent_spec: the parent agent spec dictionary
        :param args: the arguments dictionary
        :param sly_data: the sly data dictionary
        :param parent_run_context: the parent run context
        :param factory: the agent tool factory
        :param invocation: the invocation string ("chatbot" or "event")
        :return: a CallableActivation
        """
        use_args: Dict[str, Any] = self.merge_args(args, agent_tool_spec)
        return ToolboxActivation(parent_run_context, factory, use_args, agent_tool_spec, sly_data)
