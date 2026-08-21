
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""

from nora_fleet.service.mcp.interfaces.client_session import ClientSession


class McpClientSession(ClientSession):
    """
    Class representing a client session with the MCP service.
    """

    def __init__(self, session_id: str):
        self.session_id: str = session_id

        # Flag indicating if the session is properly initialized
        # by handshake sequence and now active.
        self.session_is_active: bool = False

    def get_id(self) -> str:
        """
        Get the session id.
        """
        return self.session_id

    def is_active(self) -> bool:
        """
        Check if the session is active.
        """
        return self.session_is_active

    def set_active(self, is_active: bool) -> None:
        """
        Set the session active flag.
        """
        self.session_is_active = is_active
