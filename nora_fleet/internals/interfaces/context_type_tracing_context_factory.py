
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from nora_fleet.internals.interfaces.run_target import RunTarget
from nora_fleet.internals.interfaces.tracing_context import TracingContext


class ContextTypeTracingContextFactory:
    """
    Interface for Factory classes creating TracingContexts for RunTargets.
    """

    def create_tracing_context(self, config: Dict[str, Any], run_target: RunTarget) -> TracingContext:
        """
        Creates a RunTarget based on another RunTarget

        :param config: The configuration for the tracing context
        :param run_target: The RunTarget instance to be traced
        :return: An appropriate TracingContext
        """
        raise NotImplementedError
