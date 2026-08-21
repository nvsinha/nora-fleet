
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from nora_fleet.interfaces.agent_session import AgentSession


class ConciergeSession:
    """
    Interface for a Concierge session.
    """

    # Default port for the Concierge HTTP Service
    # This port number will also be mentioned in its Dockerfile
    DEFAULT_HTTP_PORT: int = AgentSession.DEFAULT_HTTP_PORT

    # Default port for the Concierge Service
    # This port number will also be mentioned in its Dockerfile
    DEFAULT_PORT: int = DEFAULT_HTTP_PORT

    def list(self, request_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        :param request_dict: A dictionary version of the ConciergeRequest
                    protobuf structure. Has the following keys:
                        <None>
        :return: A dictionary version of the ConciergeResponse
                    protobuf structure. Has the following keys:
                "agents" - the sequence of dictionaries describing available agents
        """
        raise NotImplementedError
