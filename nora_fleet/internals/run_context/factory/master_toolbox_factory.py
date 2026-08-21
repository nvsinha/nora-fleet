
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_fleet.internals.interfaces.context_type_toolbox_factory import ContextTypeToolboxFactory
from nora_fleet.internals.run_context.factory.master_llm_factory import MasterLlmFactory
from nora_fleet.internals.run_context.langchain.toolbox.toolbox_factory import ToolboxFactory


class MasterToolboxFactory:
    """
    Creates the correct kind of ContextTypeToolboxFactory
    """

    @staticmethod
    def create_toolbox_factory(config: Dict[str, Any] = None) -> ContextTypeToolboxFactory:
        """
        Creates an appropriate ContextTypeToolboxFactory

        :param config: The config dictionary which may or may not contain
                       keys for the context_type and default toolbox_config
        :return: A ContextTypeToolboxFactory appropriate for the context_type in the config.
        """

        toolbox_factory: ContextTypeToolboxFactory = None
        context_type: str = MasterLlmFactory.get_context_type(config)

        if context_type.startswith("openai"):
            toolbox_factory = None
        elif context_type.startswith("langchain"):
            toolbox_factory = ToolboxFactory(config)
        else:
            # Default case
            toolbox_factory = ToolboxFactory(config)

        return toolbox_factory
