
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from __future__ import annotations

from typing import Any
from typing import Dict

from nora_fleet.internals.interfaces.run_target import RunTarget


class TracingContext(RunTarget):
    """
    Interface for a single request's tracing needs.
    """

    async def run_it(self, inputs: Any) -> Any:
        """
        Entry point method for the run.

        :param inputs: A list of inputs from the user.
        :return: The outputs of the run.
        """
        raise NotImplementedError

    def clone(self) -> TracingContext:
        """
        Creates a copy the tracing context.

        :return: A clone of the tracing context.
        """
        raise NotImplementedError

    def augment_config(self, runnable_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Augment the configuration however the implementation sees fit (if at all).
        :param runnable_config: The config for the runnable
        :return: The augmented config
        """
        raise NotImplementedError

    async def flush(self):
        """
        Flush the tracing context.
        """
        raise NotImplementedError
