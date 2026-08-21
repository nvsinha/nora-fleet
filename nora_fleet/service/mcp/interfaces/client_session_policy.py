
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

MCP_SESSION_ID: str = "Mcp-Session-Id"
MCP_PROTOCOL_VERSION: str = "MCP-Protocol-Version"


class ClientSessionPolicy:
    """
    Interface for client sessions handling policy in the MCP service.
    """

    def create_session(self) -> ClientSession:
        """
        Create a new client session with the unique client id.
        This method may return None if session creation is not supported
        by the policy.

        :return: The created ClientSession or None
        """
        raise NotImplementedError

    def activate_session(self, session_id: str) -> bool:
        """
        Activate an existing client session with the given session id.
        Note that multiple session activations are currently allowed
        :param session_id: The session id to activate.
                 May be None if sessions are not supported by the policy
        :return: True if successful;
                 False if session with given id does not exist
        """
        raise NotImplementedError

    def delete_session(self, session_id: str) -> bool:
        """
        Delete an existing client session with the given session id.
        :param session_id: The session id to delete
                 May be None if sessions are not supported by the policy
        :return: True if successful;
                 False if session with given id does not exist
        """
        raise NotImplementedError

    def is_session_active(self, session_id: str) -> bool:
        """
        Check if the session with the given id is active.
        :param session_id: The session id to check
                 May be None if sessions are not supported by the policy
        :return: True if session exists and is active;
                 False otherwise
        """
        raise NotImplementedError
