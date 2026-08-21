
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import List


class Invocations:
    """
    Constants for invocation types
    """

    EVENT: str = "event"
    CHATBOT: str = "chatbot"

    ALL: List[str] = [EVENT, CHATBOT]
