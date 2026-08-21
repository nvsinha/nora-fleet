
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_fleet.internals.interfaces.invocation_context import InvocationContext
from nora_fleet.internals.interfaces.tracing_context import TracingContext
from nora_fleet.internals.run_context.factory.master_llm_factory import MasterLlmFactory
from nora_fleet.internals.run_context.interfaces.run_context import RunContext
from nora_fleet.internals.run_context.interfaces.tool_caller import ToolCaller
from nora_fleet.internals.run_context.langchain.core.langchain_run_context import LangChainRunContext


class RunContextFactory:
    """
    Creates the correct kind of RunContext
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    @staticmethod
    def create_run_context(parent_run_context: RunContext,
                           tool_caller: ToolCaller,
                           invocation_context: InvocationContext = None,
                           chat_context: Dict[str, Any] = None,
                           config: Dict[str, Any] = None,
                           tracing_context: TracingContext = None) \
            -> RunContext:
        """
        Creates an appropriate RunContext

        :param parent_run_context: The parent RunContext (if any) to pass
                             down its resources to a new RunContext created by
                             this call.
        :param tool_caller: The ToolCaller whose lifespan matches that
                            of the newly created RunContext
        :param invocation_context: The context policy container that pertains to the invocation
                    of the agent.
        :param chat_context: A ChatContext dictionary that contains all the state necessary
                to carry on a previous conversation, possibly from a different server.
        :param config: The config dictionary which may or may not contain
                       keys for the context_type and default llm_config
        :param tracing_context: A TracingContext for the request
        """

        # Initialize return value
        run_context: RunContext = None

        empty: Dict[str, Any] = {}
        use_config: Dict[str, Any] = config
        if use_config is None:
            use_config = empty

        # Get some fields from the config with reasonable defaults
        default_llm_config: Dict[str, Any] = {
            "model_name": "gpt-5.2",
            "verbose": False
        }
        use_llm_config: Dict[str, Any] = use_config.get("llm_config") or default_llm_config

        # Prepare for sanity in checks below
        context_type: str = MasterLlmFactory.get_context_type(use_config)

        use_invocation_context: InvocationContext = invocation_context
        if use_invocation_context is None and parent_run_context is not None:
            use_invocation_context = parent_run_context.get_invocation_context()

        if context_type.startswith("openai"):
            raise ValueError("OpenAI Assistants implementation is no longer supported by OpenAI.")

        if context_type.startswith("langchain"):
            run_context = LangChainRunContext(use_llm_config, parent_run_context,
                                              tool_caller, use_invocation_context,
                                              chat_context, use_config.get("middleware_config"),
                                              tracing_context=tracing_context)
        else:
            # Default case
            run_context = LangChainRunContext(use_llm_config, parent_run_context,
                                              tool_caller, use_invocation_context,
                                              chat_context, use_config.get("middleware_config"),
                                              tracing_context=tracing_context)

        return run_context
