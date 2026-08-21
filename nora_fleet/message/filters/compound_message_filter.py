
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from nora_fleet.message.filters.message_filter import MessageFilter
from nora_fleet.message.types.chat_message_type import ChatMessageType


class CompoundMessageFilter(MessageFilter):
    """
    A MessageFilter implementation that can service multiple other MessageFilter instances
    """

    def __init__(self, filters: List[MessageFilter] = None):
        """
        Constructor

        :param filters: A List of MessageFilter instances to simultaneously service
        """
        self.filters: List[MessageFilter] = filters
        if self.filters is None:
            self.filters = []

    def allow_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType) -> bool:
        """
        Determine whether to allow the message through.
        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        :return: True if the message should be allowed through to the client. False otherwise.
        """
        # If any one filter says to let a message through, then let it through.
        for one_filter in self.filters:
            if one_filter.allow_message(chat_message_dict, message_type):
                return True

        # Nobody wanted it.
        return False

    def add_message_filter(self, message_filter: MessageFilter):
        """
        Adds a message_filter to the list
        :param message_filter: A MessageFilter instance to service
        """
        self.filters.append(message_filter)
