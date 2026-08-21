
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_fleet.message.filters.chat_context_message_filter import ChatContextMessageFilter
from nora_fleet.message.processors.message_processor import MessageProcessor
from nora_fleet.message.types.chat_message_type import ChatMessageType


class ChatContextMessageProcessor(MessageProcessor):
    """
    Implementation of the MessageProcessor that looks for the chat_context
    in the stream which is used to continue the conversation.
    """

    def __init__(self):
        """
        Constructor
        """
        self.chat_context: Dict[str, Any] = {}
        self.sly_data: Dict[str, Any] = None
        self.filter = ChatContextMessageFilter()

    def get_chat_context(self) -> Dict[str, Any]:
        """
        :return: The chat_context discovered from the agent session interaction
                Empty dictionaries or None values simply start a new conversation.
        """
        return self.chat_context

    def get_sly_data(self) -> Dict[str, Any]:
        """
        :return: The sly_data discovered from the agent session interaction
        """
        return self.sly_data

    def reset(self):
        """
        Resets any previously accumulated state
        """
        self.chat_context = {}
        self.sly_data = None

    def process_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType):
        """
        Process the message.
        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        """
        if not self.filter.allow_message(chat_message_dict, message_type):
            # Filter says no
            return

        # Normally the very last message holds the chat_context.
        # Keep accumulating until it comes past, as long as there is something.
        self.chat_context = chat_message_dict.get("chat_context", self.chat_context)
        self.sly_data = chat_message_dict.get("sly_data", self.sly_data)
