
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_fleet.message.filters.message_filter import MessageFilter
from nora_fleet.message.types.chat_message_type import ChatMessageType


class MaximalMessageFilter(MessageFilter):
    """
    MessageFilter implementation that lets everything through.
    """

    def allow_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType) -> bool:
        """
        Determine whether to allow the message through.

        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        :return: True if the message should be allowed through to the client. False otherwise.
        """
        # As long as the dictionary has some keys in it, we will pass it on.
        if any(chat_message_dict):
            return True

        return False
