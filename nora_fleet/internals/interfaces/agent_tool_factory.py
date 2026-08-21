
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from __future__ import annotations

from typing import Any
from typing import Dict

from nora_fleet.internals.interfaces.callable_activation import CallableActivation
from nora_fleet.internals.run_context.interfaces.run_context import RunContext


class AgentToolFactory:
    """
    Interface describing a factory that creates agent tools.
    Having this interface breaks some circular dependencies.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def create_agent_activation(self,
                                parent_run_context: RunContext,
                                parent_agent_spec: Dict[str, Any],
                                name: str,
                                sly_data: Dict[str, Any],
                                args: Dict[str, Any] = None,
                                factory: AgentToolFactory = None,
                                invocation: str = None) -> CallableActivation:
        """
        Create an active node for an agent from its spec.

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
        raise NotImplementedError

    def get_config(self) -> Dict[str, Any]:
        """
        :return: The entire config dictionary given to the instance.
        """
        raise NotImplementedError

    def get_agent_tool_path(self) -> str:
        """
        :return: The path under which tools for this registry should be looked for.
        """
        raise NotImplementedError

    def get_name_from_spec(self, agent_spec: Dict[str, Any]) -> str:
        """
        :param agent_spec: A single agent to register
        :return: The agent name as per the spec
        """
        raise NotImplementedError
