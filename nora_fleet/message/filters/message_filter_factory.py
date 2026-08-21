
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import Type

from nora_fleet.message.filters.maximal_message_filter import MaximalMessageFilter
from nora_fleet.message.filters.message_filter import MessageFilter
from nora_fleet.message.filters.minimal_message_filter import MinimalMessageFilter

TYPE_TO_MESSAGE_FILTER_CLASS: Dict[Any, Type[MessageFilter]] = {
    0:  MinimalMessageFilter,
    1:  MinimalMessageFilter,
    2:  MaximalMessageFilter,

    "UNKNOWN":  MinimalMessageFilter,
    "MINIMAL":  MinimalMessageFilter,
    "MAXIMAL":  MaximalMessageFilter,
}


class MessageFilterFactory:
    """
    Class for creating MessageFilters
    """

    @staticmethod
    def create_message_filter(chat_filter: Dict[str, Any]) -> MessageFilter:
        """
        :param chat_filter: The ChatFilter dictionary to process.
        :return: A MessageFilter that corresponds to the contents
        """

        # For now the default is MAXIMAL simply to emulate current behavior.
        # After the ChatFilter API gets released this will eventually change to "MINIMAL".
        default: str = "MINIMAL"
        chat_filter_type: Any = default

        # Get what was in the request
        if chat_filter is not None:
            chat_filter_type = chat_filter.get("chat_filter_type", chat_filter_type)

        # Change strings so they are suitable for lookup
        if isinstance(chat_filter_type, str):
            chat_filter_type = chat_filter_type.upper()

        chat_filter_class: MessageFilter = TYPE_TO_MESSAGE_FILTER_CLASS.get(chat_filter_type)
        if chat_filter_class is None:
            chat_filter_class = TYPE_TO_MESSAGE_FILTER_CLASS.get(default)

        # Instantiate the class and return
        message_filter: MessageFilter = chat_filter_class()
        return message_filter
