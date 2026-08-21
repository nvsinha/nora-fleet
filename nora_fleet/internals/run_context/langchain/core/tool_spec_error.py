
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT


class ToolSpecError(ValueError):
    """
    Raised when a tool's function spec (an OpenAI-function-style dictionary)
    cannot be converted into a working tool - for example an unrecognized
    parameter type string or a parameter name that pydantic cannot accept
    as a field name.

    Subclasses ValueError so that existing broad handlers and the network
    validators keep catching it, while callers that need to distinguish
    "the spec is bad" from other ValueErrors (like the connectivity errors
    reported by external agent adapters) can catch this type specifically.
    """
