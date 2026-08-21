
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict
from typing import Sequence

from nora_common.serialization.interface.dictionary_converter import DictionaryConverter

from nora_fleet.message.types.chat_message_type import ChatMessageType


class McpChatResponseDictionaryConverter(DictionaryConverter):
    """
    A DictionaryConverter implementation which can convert MCP service response
    to native nora-fleet service response format.
    """

    def to_dict(self, obj: object) -> Dict[str, object]:
        """
        :param obj: The MCP response to be converted into a dictionary
        :return: A data-only dictionary that represents both:
                 native nora-fleet service response - under "response" key
                 original MCP response - under "mcp_response" key
        """
        empty: Dict[str, Any] = {}
        if not isinstance(obj, dict):
            return empty
        chat_response: Dict[str, Any] = obj
        result: Dict[str, Any] = chat_response.get("result", None)
        if result is None:
            return empty
        has_error: bool = result.get("isError", True)
        if has_error:
            return empty
        content_seq: Sequence[Dict[str, Any]] = result.get("content", [])
        if len(content_seq) == 0:
            return empty
        # "structuredContent" is MCP standard key for content with additional structure.
        structured_data: Dict[str, Any] = result.get("structuredContent", None)
        response: Dict[str, Any] = content_seq[0]
        final_response: Dict[str, Any] = {
            "response": {
                "type": ChatMessageType.AGENT_FRAMEWORK.name,
                "text": response.get("text", "")
            },
            "mcp_response": chat_response
        }
        if structured_data is not None:
            message_structured_data: Dict[str, Any] = structured_data.get("structure", None)
            if message_structured_data is not None:
                final_response["response"]["structure"] = message_structured_data
            chat_context_data: Dict[str, Any] = structured_data.get("chat_context", None)
            if chat_context_data is not None:
                final_response["response"]["chat_context"] = chat_context_data
        return final_response

    def from_dict(self, obj_dict: Dict[str, object]) -> object:
        """
        :param obj_dict: The data-only dictionary to be converted into an object
        :return: An object instance created from the given dictionary.
                If obj_dict is None, the returned object should also be None.
                If obj_dict is not the correct type, it is also reasonable
                to return None.
        """
        raise NotImplementedError
