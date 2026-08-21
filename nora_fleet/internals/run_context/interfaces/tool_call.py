
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict


class ToolCall:
    """
    An interface representing a call to a tool
    """

    def get_id(self) -> str:
        """
        :return: The string id of this run
        """
        raise NotImplementedError

    def get_function_arguments(self) -> Dict[str, Any]:
        """
        :return: Returns a dictionary of the function arguments for the tool call
        """
        raise NotImplementedError

    def get_function_name(self) -> str:
        """
        :return: Returns the string name of the tool
        """
        raise NotImplementedError

    def get_invocation(self) -> str:
        """
        :return: String describing how the tool wants to be invoked.
                            Can be: "chatbot" - implies waiting for an answer.
                                    "event" - implies no answer needed
                                    None - implies chatbot
        """
        raise NotImplementedError
