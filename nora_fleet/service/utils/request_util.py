
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""
from typing import Union

import html


class RequestUtil:
    """
    Utility class for sanitizing user-controlled values that flow back into
    HTTP / MCP responses, so HTML-based consumers cannot be tricked into
    rendering unescaped client input.
    """

    @staticmethod
    def safe_request_id(request_id: Union[int, str]) -> str:
        """
        Return HTML-safe representation of a user-supplied request id to be
        echoed back in a response.
        :param request_id: request id (as received from the user);
        :return: HTML-escaped request id string.
        """
        # Always return a string and always HTML-escape it to avoid XSS
        # vulnerabilities in any HTML-based consumers of the response.
        if isinstance(request_id, str):
            return html.escape(request_id)
        # For non-string IDs (including integers), convert to string first,
        # then escape to ensure the returned value is HTML-safe.
        return html.escape(str(request_id))

    @staticmethod
    def safe_message(msg: str) -> str:
        """
        Return HTML-safe representation of a string message to be echoed back
        in a response.
        :param msg: message string;
        :return: HTML-escaped message string.
        """
        return html.escape(msg)
