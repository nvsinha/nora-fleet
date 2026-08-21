
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT


class AgentServer:
    """
    Interface for an AgentServer, regardless of transport mechanism
    """

    # A space-delimited list of http metadata request keys to forward to logs/other requests
    DEFAULT_FORWARDED_REQUEST_METADATA: str = "request_id user_id"

    def stop(self):
        """
        Stop the server.
        """
        raise NotImplementedError
