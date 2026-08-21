
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from langchain_core.runnables.base import Runnable
from langchain_core.runnables.passthrough import RunnablePassthrough

from nora_fleet.internals.interfaces.run_target import RunTarget
from nora_fleet.internals.interfaces.tracing_context import TracingContext
from nora_fleet.internals.run_context.langchain.tracing.nora_fleet_runnable import NoraFleetRunnable


class LangChainTracingContext(TracingContext):
    """
    TracingContext implementation for unadorned langchain runs.
    """

    def __init__(self, run_target: RunTarget, config: Dict[str, Any]):
        """
        Constructor

        :param run_target: The RunTarget instance to be traced
        :param config: The configuration for the tracing context
        """
        self.run_target: RunTarget = run_target
        self.config: Dict[str, Any] = config

    async def run_it(self, inputs: Any) -> Any:
        """
        Entry point method for the run.

        :param inputs: A list of inputs from the user.
        :return: The outputs of the run.
        """
        runnable = NoraFleetRunnable(run_target=self.run_target, tracing_context=self, **self.config)
        runnable_config: Dict[str, Any] = runnable.prepare_runnable_config(use_run_name=True)

        chain: Runnable = RunnablePassthrough() | runnable

        await self.ainvoke(chain, inputs, runnable_config)

        return inputs

    async def ainvoke(self, chain: Runnable, inputs: Any, runnable_config: Dict[str, Any]):
        """
        Invoke the chain with the inputs and config
        :param chain: The chain to invoke
        :param inputs: The inputs to the chain
        :param runnable_config: The config for the runnable
        """
        await chain.ainvoke(input=inputs, config=runnable_config)

    def clone(self) -> TracingContext:
        """
        Creates a copy the tracing context.

        :return: A clone of the tracing context.
        """
        clone = LangChainTracingContext(run_target=self.run_target, config=self.config)
        return clone

    def augment_config(self, runnable_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Augment the configuration however the implementation sees fit (if at all).
        :param runnable_config: The config for the runnable
        :return: The augmented config
        """
        # Do nothing special
        return runnable_config

    async def flush(self):
        """
        Flush the tracing context.
        """
        # Do nothing
