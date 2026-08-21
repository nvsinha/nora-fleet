
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""


class ClientSession:
    """
    Interface representing a client session with the MCP service.
    """

    def get_id(self) -> str:
        """
        Get the session id.
        """
        raise NotImplementedError

    def is_active(self) -> bool:
        """
        Check if the session is active.
        """
        raise NotImplementedError
