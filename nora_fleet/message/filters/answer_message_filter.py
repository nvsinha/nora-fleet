
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


class AnswerMessageFilter(MessageFilter):
    """
    MessageFilter implementation for a message with "the answer" in it.
    """

    def allow_message(self, chat_message_dict: Dict[str, Any], message_type: ChatMessageType) -> bool:
        """
        Determine whether to allow the message through.

        :param chat_message_dict: The ChatMessage dictionary to process.
        :param message_type: The ChatMessageType of the chat_message_dictionary to process.
        :return: True if the message should be allowed through to the client. False otherwise.
        """
        if message_type not in (ChatMessageType.AI, ChatMessageType.AGENT_FRAMEWORK):
            # Final answers are only ever AI or AgentFramework Messages
            return False

        origin: List[Dict[str, Any]] = chat_message_dict.get("origin")
        if origin is not None and len(origin) > 1:
            # Final answers only come from the FrontMan,
            # whose origin length is the only one of length 1.
            return False

        text: str = chat_message_dict.get("text")
        structure: Dict[str, Any] = chat_message_dict.get("structure")
        if text is None and structure is None:
            # Final answers need to be text or structure.
            # There might be more options in the future.
            return False

        # Meets all our criteria. Let it through.
        return True
