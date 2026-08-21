
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.graph.activations.abstract_class_activation import AbstractClassActivation
from nora_fleet.internals.interfaces.context_type_toolbox_factory import ContextTypeToolboxFactory
from nora_fleet.internals.interfaces.invocation_context import InvocationContext


class ToolboxActivation(AbstractClassActivation):
    """
    A ClassActivation that resolves the full class reference from a predefined coded tool in the toolbox.

    Note that this class does not apply to Langchain's base tools.
    """

    def get_full_class_ref(self) -> str:
        """
        Returns the full class reference path from a predefined toolbox.

        This implementation looks up the tool by name in a toolbox, using the
        "toolbox" field in `agent_tool_spec`, then determine the class of that
        coded tool.

        :return: A dot-separated string representing the full class path.
        """
        tool_name: str = self.agent_tool_spec.get("toolbox")
        invocation_context: InvocationContext = self.run_context.get_invocation_context()
        toolbox_factory: ContextTypeToolboxFactory = invocation_context.get_toolbox_factory()
        return toolbox_factory.get_shared_coded_tool_class(tool_name)
