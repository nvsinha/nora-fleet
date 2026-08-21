
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT


class AgentSessionConstants:
    """
    Interface for shared constants between AgentSession and AsyncAgentSession
    """

    # Default port for the Agent HTTP Service
    # This port number will also be mentioned in its Dockerfile
    DEFAULT_HTTP_PORT: int = 8080

    DEFAULT_PORT: int = DEFAULT_HTTP_PORT
