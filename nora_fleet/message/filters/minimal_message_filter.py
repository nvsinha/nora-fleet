
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import List

from nora_fleet.message.filters.chat_context_message_filter import ChatContextMessageFilter
from nora_fleet.message.filters.compound_message_filter import CompoundMessageFilter
from nora_fleet.message.filters.message_filter import MessageFilter


class MinimalMessageFilter(CompoundMessageFilter):
    """
    A CompoundMessageFilter that lets the minimal messages needed for an agent interaction
    go through.
    """

    def __init__(self):
        """
        Constructor
        """
        filters: List[MessageFilter] = [
            ChatContextMessageFilter(),
        ]
        super().__init__(filters)
