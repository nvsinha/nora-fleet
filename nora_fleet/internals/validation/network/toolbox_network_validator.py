
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict
from typing import List

from logging import getLogger
from logging import Logger

from nora_fleet.internals.validation.network.abstract_network_validator import AbstractNetworkValidator


class ToolboxNetworkValidator(AbstractNetworkValidator):
    """
    AbstractNetworkValidator for toolbox references.
    """

    def __init__(self, tools: Dict[str, Any]):
        """
        Constructor

        :param tools: A dictionary of tools, as read in from a toolbox_info.hocon file
        """
        self.logger: Logger = getLogger(self.__class__.__name__)
        self.tools: Dict[str, Any] = tools

    def validate_name_to_spec_dict(self, name_to_spec: Dict[str, Any]) -> List[str]:
        """
        Validate the agent network, specifically in the form of a name -> agent spec dictionary.

        :param name_to_spec: The name -> agent spec dictionary to validate
        :return: A list of error messages
        """
        errors: List[str] = []

        self.logger.info("Validating toolbox agents...")

        for agent_name, agent in name_to_spec.items():
            if agent.get("instructions") is None:  # This is a toolbox agent
                if self.tools is None or not isinstance(self.tools, Dict):
                    errors.append(f"Toolbox is unavailable. Cannot create Toolbox agent '{agent_name}'.")
                elif agent_name not in self.tools:
                    errors.append(f"Toolbox agent '{agent_name}' has no matching tool in toolbox.")
                elif agent.get("tools"):
                    errors.append(
                        "Toolbox agent cannot have 'tools'. "
                        f"[{agent.get('tools')}] cannot be under Toolbox agent '{agent_name}'"
                    )

        return errors
