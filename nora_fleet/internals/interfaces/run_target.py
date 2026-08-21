
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any


class RunTarget:
    """
    Interface for something that can be run as part of the course of a streaming_chat.
    """

    async def run_it(self, inputs: Any) -> Any:
        """
        Entry point method for the run.

        :param inputs: A list of inputs from the user.
        :return: The outputs of the run.
        """
        raise NotImplementedError
