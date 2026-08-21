
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""
from typing import Dict

import base64
from threading import Lock
import uuid

from nora_fleet.service.mcp.interfaces.client_session_policy import ClientSessionPolicy
from nora_fleet.service.mcp.session.mcp_client_session import McpClientSession

MCP_SESSION_ID: str = "Mcp-Session-Id"
MCP_PROTOCOL_VERSION: str = "MCP-Protocol-Version"


class McpSessionManager(ClientSessionPolicy):
    """
    Class creating and managing client sessions with the MCP service.
    """

    def __init__(self):
        # Lock to protect access to the sessions dictionary
        self.lock: Lock = Lock()
        self.sessions: Dict[str, McpClientSession] = {}

    def create_session(self) -> McpClientSession:
        """
        Create a new client session with the given client id.

        :return: The created MCPClientSession
        """
        session_id: str = self._generate_id()
        client_session: McpClientSession = McpClientSession(session_id)
        self.sessions[session_id] = client_session
        return client_session

    def activate_session(self, session_id: str) -> bool:
        """
        Activate an existing client session with the given session id.
        Note that multiple session activations are currently allowed
        :param session_id: The session id to activate
        :return: True if successful;
                 False if session with given id does not exist
        """
        with self.lock:
            session: McpClientSession = self.sessions.get(session_id)
            if session is not None:
                session.set_active(True)
                return True
            return False

    def delete_session(self, session_id: str) -> bool:
        """
        Delete an existing client session with the given session id.
        :param session_id: The session id to delete
        :return: True if successful;
                 False if session with given id does not exist
        """
        if session_id is None:
            return False
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False

    def is_session_active(self, session_id: str) -> bool:
        """
        Check if the session with the given id is active.
        :param session_id: The session id to check
        :return: True if session exists and is active;
                 False otherwise
        """
        if session_id is None:
            return False
        with self.lock:
            session: McpClientSession = self.sessions.get(session_id)
            if session is not None:
                return session.is_active()
            return False

    def _generate_id(self) -> str:
        """
        Generate a new unique session id.
        :return: The generated session id
        """
        # Generate 128-bit random UUID (cryptographically secure)
        raw = uuid.uuid4().bytes
        # Encode to Base32 (A–Z, 2–7), remove '=' padding
        token = base64.b32encode(raw).decode('ascii').rstrip('=')
        # Take first 16 characters (still ~80 bits entropy — plenty for uniqueness)
        token = token[:16]
        # Format as 4x4 groups
        return '-'.join(token[i:i + 4] for i in range(0, 16, 4))
