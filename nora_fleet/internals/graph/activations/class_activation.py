
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.graph.activations.abstract_class_activation import AbstractClassActivation


class ClassActivation(AbstractClassActivation):
    """
    A ClassActivation that retrieves the full class reference directly from the class specification
    in agent network hocon.
    """

    def get_full_class_ref(self) -> str:
        """
        Returns the full class reference path directly from the class specification.

        This implementation expects the fully qualified class name to be provided
        in the "class" field of the `agent_tool_spec` dictionary.

        :return: A dot-separated string representing the full class path.
        """
        return self.agent_tool_spec.get("class")
