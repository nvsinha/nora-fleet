
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from nora_fleet.message.types.chat_message_type import ChatMessageType


class MessageProcessor:
    """
    An interface for processing a single message.
    """

    def reset(self):
        """
        Resets any previously accumulated state
        """

    def should_block_downstream_processing(self, chat_message_dict: Dict[str, Any],
                                           message_type: ChatMessageType) -> bool:
        """
        :param chat_message_dict: The ChatMessage dictionary to consider.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        :return: True if the given message should be blocked from further downstream
                processing.  False otherwise (the default).
        """
        _ = chat_message_dict, message_type
        return False

    def process_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType):
        """
        Process the message.
        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        """
        raise NotImplementedError

    async def async_process_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType):
        """
        Process the message asynchronously.
        By default, this simply calls the synchronous version.

        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        """
        self.process_message(chat_message_dict, message_type)

    def process_messages(self, chat_message_dicts: List[Dict[str, Any]]):
        """
        Convenience method for processing lists of messages.
        :param chat_message_dicts: The messages to process.
        """
        for message in chat_message_dicts:
            message_type: ChatMessageType = message.get("type")
            self.process_message(message, message_type)

    async def async_process_messages(self, chat_message_dicts: List[Dict[str, Any]]):
        """
        Convenience method for asynchronouslt processing lists of messages.
        :param chat_message_dicts: The messages to process.
        """
        for message in chat_message_dicts:
            message_type: ChatMessageType = message.get("type")
            await self.async_process_message(message, message_type)
