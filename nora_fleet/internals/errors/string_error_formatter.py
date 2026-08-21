
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.interfaces.error_formatter import ErrorFormatter


class StringErrorFormatter(ErrorFormatter):
    """
    Implementation of ErrorFormatter interface which compiles error information
    into a string.   See parent interface for more details.
    """

    def format(self, agent_name: str, message: str, details: str = None) -> str:
        """
        Format an error message

        :param agent_name: A string describing the name of the agent experiencing
                the error.
        :param message: The specific message describing the error occurrence.
        :param details: An optional string describing further details of how/where the
                error occurred.  Think: traceback.
        :return: String encapsulation and/or filter of the error information
                presented in the arguments.
        """
        error: str = f"Error from {agent_name}: {message}"
        if details is not None:
            error = f"{error} ({details})"
        return error
