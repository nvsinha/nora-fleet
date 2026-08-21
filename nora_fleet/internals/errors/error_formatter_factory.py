
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from nora_fleet.internals.errors.json_error_formatter import JsonErrorFormatter
from nora_fleet.internals.errors.string_error_formatter import StringErrorFormatter
from nora_fleet.internals.interfaces.error_formatter import ErrorFormatter


class ErrorFormatterFactory:
    """
    Factory class to create an appropriate ErrorFormatter
    """

    @staticmethod
    def create_formatter(name: str = "string") -> ErrorFormatter:
        """
        Creates an ErrorFormatter given the name.

        :param name: The name of the error formatter to use
        :return: An ErrorFormatter instance.
        """

        # Default
        formatter: ErrorFormatter = StringErrorFormatter()
        if name is None:
            return formatter

        if name.lower() == "json":
            formatter = JsonErrorFormatter()

        # When the need arises, we could conceivably add class name lookup
        # for error formatters here, not unlike the way we do for coded tools.

        return formatter
