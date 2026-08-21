
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_fleet.internals.interfaces.context_type_llm_factory import ContextTypeLlmFactory
from nora_fleet.internals.run_context.langchain.llms.default_llm_factory import DefaultLlmFactory


class MasterLlmFactory:
    """
    Creates the correct kind of ContextTypeLlmFactory
    """

    @staticmethod
    def create_llm_factory(config: Dict[str, Any] = None) -> ContextTypeLlmFactory:
        """
        Creates an appropriate ContextTypeLlmFactory

        :param config: The config dictionary which may or may not contain
                       keys for the context_type and default llm_config
        :return: A ContextTypeLlmFactory appropriate for the context_type in the config.
        """

        llm_factory: ContextTypeLlmFactory = None
        context_type: str = MasterLlmFactory.get_context_type(config)

        if context_type.startswith("openai"):
            llm_factory = None
        elif context_type.startswith("langchain"):
            llm_factory = DefaultLlmFactory(config)
        else:
            # Default case
            llm_factory = DefaultLlmFactory(config)

        return llm_factory

    @staticmethod
    def get_context_type(config: Dict[str, Any]) -> str:
        """
        :param config: The config dictionary which may or may not contain
                       keys for the context_type and default llm_config
        :return: The context type for the config
        """
        empty: Dict[str, Any] = {}
        use_config: Dict[str, Any] = config
        if use_config is None:
            use_config = empty

        # Prepare for sanity in checks below
        context_type: str = use_config.get("context_type")
        if context_type is None:
            context_type = "langchain"
        lower_context_type: str = context_type.lower()

        return lower_context_type
