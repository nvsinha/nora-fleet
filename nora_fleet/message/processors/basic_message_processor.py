
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

import json

from nora_fleet.message.processors.answer_message_processor import AnswerMessageProcessor
from nora_fleet.message.processors.chat_context_message_processor import ChatContextMessageProcessor
from nora_fleet.message.processors.composite_message_processor import CompositeMessageProcessor
from nora_fleet.message.processors.message_processor import MessageProcessor
from nora_fleet.message.processors.token_accounting_message_processor import TokenAccountingMessageProcessor


class BasicMessageProcessor(CompositeMessageProcessor):
    """
    A CompositeMessageProcessor that provides the most basic operations
    that most everyone needs.
    """

    def __init__(self, message_processors: List[MessageProcessor] = None):
        """
        Constructor

        :param message_processors: An ordered List of additional MessageProcessors with which
                     this instance will process messages
        """
        super().__init__(message_processors)

        self.answer = AnswerMessageProcessor()
        self.chat_context = ChatContextMessageProcessor()
        self.token_accounting = TokenAccountingMessageProcessor()

        # These always go first because they should never be blocked
        self.message_processors.insert(0, self.chat_context)
        self.message_processors.insert(0, self.answer)
        self.message_processors.append(self.token_accounting)

    def get_answer(self) -> str:
        """
        :return: The final answer from the agent session interaction
        """
        return self.answer.get_answer()

    def get_answer_origin(self) -> List[Dict[str, Any]]:
        """
        :return: The origin of the final answer from the agent session interaction
        """
        return self.answer.get_answer_origin()

    def get_sly_data(self) -> Dict[str, Any]:
        """
        :return: Any sly_data that was returned
        """
        return self.chat_context.get_sly_data()

    def get_chat_context(self) -> Dict[str, Any]:
        """
        :return: The chat_context discovered from the agent session interaction
                Empty dictionaries or None values simply start a new conversation.
        """
        return self.chat_context.get_chat_context()

    def get_structure(self) -> Dict[str, Any]:
        """
        :return: Any dictionary structure that was contained within the final answer
                 from the agent session interaction, if such a specific breakout was desired.
        """
        return self.answer.get_structure()

    def get_compiled_answer(self) -> str:
        """
        :return: All components of the "answer" except for sly_data compiled into
                 a single string.  This includes the results of these methods in order:
                    get_answer()
                    get_structure()
        """
        compiled: str = self.get_answer()

        # Add a structure to the mix in a uniform manner, if there is one
        structure: Dict[str, Any] = self.get_structure()
        if structure is not None:
            string_struct: str = json.dumps(structure, indent=4, sort_keys=True)
            if compiled is None:
                compiled = ""
            compiled += f"\n```json\n{string_struct}\n```"

        return compiled

    def get_token_accounting(self) -> Dict[str, Any]:
        """
        :return: The token accounting dictionary from the streaming_chat() session.
        """
        return self.token_accounting.get_token_accounting()
