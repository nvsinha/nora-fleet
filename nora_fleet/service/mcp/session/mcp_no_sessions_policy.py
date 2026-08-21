
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""

from nora_fleet.service.mcp.interfaces.client_session_policy import ClientSessionPolicy
from nora_fleet.service.mcp.interfaces.client_session import ClientSession


class McpNoSessionsPolicy(ClientSessionPolicy):
    """
    Policy class for scenario when client sessions are not supported by the MCP service.
    """

    def create_session(self) -> ClientSession:
        """
        Create a None client session if client sessions are not supported.
        :return: None
        """
        return None

    def activate_session(self, session_id: str) -> bool:
        """
        For "no sessions" policy, always return True.
        """
        return True

    def delete_session(self, session_id: str) -> bool:
        """
        For "no sessions" policy, always return True.
        """
        return True

    def is_session_active(self, session_id: str) -> bool:
        """
        For "no sessions" policy, always return True.
        """
        return True
