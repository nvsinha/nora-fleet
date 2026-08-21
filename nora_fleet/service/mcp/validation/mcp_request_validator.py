
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""
from typing import Any
from typing import Dict
from typing import List

import jsonschema

from nora_common.validation.dictionary_validator import DictionaryValidator


class McpRequestValidator(DictionaryValidator):
    """
    Class implementing MCP request validation against MCP protocol schema.
    """
    def __init__(self, validation_schema: Dict[str, Any]):
        self.validation_schema = validation_schema

    def validate(self, candidate: Dict[str, Any]) -> List[str]:
        """
        Validate the dictionary data of incoming MCP request against MCP protocol schema.
        :param candidate: The request dictionary to validate
        :return: A list of error messages, if any
        """
        try:
            jsonschema.validate(instance=candidate, schema=self.validation_schema)
        except jsonschema.exceptions.ValidationError:
            # We don't return detailed validation errors to the client,
            # since they tend to be very long and complex.
            return [f"Request validation FAILED for MCP request: {candidate}"]
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return [f"Validation exception: {str(exc)}"]
        return None
