
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from os import getenv

from nora_fleet.internals.interfaces.context_type_tracing_context_factory import ContextTypeTracingContextFactory
from nora_fleet.internals.interfaces.run_target import RunTarget
from nora_fleet.internals.interfaces.tracing_context import TracingContext
from nora_fleet.internals.run_context.langchain.tracing.langchain_tracing_context import LangChainTracingContext
from nora_fleet.internals.run_context.langchain.tracing.langfuse_tracing_context import LangfuseTracingContext


class LangChainTracingContextFactory(ContextTypeTracingContextFactory):
    """
    Interface for Factory classes creating tracing contexts for RunTargets.
    """

    def create_tracing_context(self, config: Dict[str, Any], run_target: RunTarget) -> TracingContext:
        """
        Creates a RunTarget based on another RunTarget

        :param config: The configuration for the tracing context
        :param run_target: The RunTarget instance to be traced
        :return: An appropriate TracingContext
        """
        tracing_context: TracingContext = None

        test_for_langfuse: bool = getenv("LANGFUSE_ENABLED", "false").lower() == "true"

        if test_for_langfuse:
            tracing_context = LangfuseTracingContext(run_target=run_target, config=config)
        else:
            tracing_context = LangChainTracingContext(run_target=run_target, config=config)

        return tracing_context
