
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from copy import copy

from langchain_core.messages.base import BaseMessage

from nora_fleet.internals.journals.originating_journal import OriginatingJournal
from nora_fleet.message.processors.message_processor import MessageProcessor
from nora_fleet.message.types.base_message_dictionary_converter import BaseMessageDictionaryConverter
from nora_fleet.message.types.chat_message_type import ChatMessageType


class ExternalMessageProcessor(MessageProcessor):
    """
    MessageProcessor implementation for handling messages from an external agent network.
    """

    def __init__(self, journal: OriginatingJournal):
        """
        Constructor

        :param journal: The OriginatingJournal through which messages from
                    the external agent are passed.
        """
        self.journal: OriginatingJournal = journal

    async def async_process_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType):
        """
        Process the message asynchronously.
        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        """
        message_origin: List[Dict[str, Any]] = chat_message_dict.get("origin")
        if message_origin is None:
            return

        # Append the origin information from the external agent to our own
        origin: List[Dict[str, Any]] = copy(self.journal.get_origin())
        origin.extend(message_origin)

        # Send the message to the client with deepened origin information
        converter = BaseMessageDictionaryConverter(langchain_only=False)
        message: BaseMessage = converter.from_dict(chat_message_dict)
        await self.journal.write_message(message, origin=origin)

    def process_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType):
        """
        Process the message.
        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        """
        # We don't implement this because we need to do so asynchronously
        raise NotImplementedError
