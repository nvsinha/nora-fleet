
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_common.time.timeout import Timeout

from nora_fleet.client.direct_agent_storage_util import DirectAgentStorageUtil
from nora_fleet.interfaces.concierge_session import ConciergeSession
from nora_fleet.internals.network_providers.agent_network_storage import AgentNetworkStorage
from nora_fleet.session.direct_concierge_session import DirectConciergeSession
from nora_fleet.session.http_concierge_session import HttpConciergeSession


# pylint: disable=too-many-arguments,too-many-positional-arguments
class ConciergeSessionFactory:
    """
    Factory class for ConciregeSessions.
    """

    def create_session(self, session_type: str,
                       hostname: str = None,
                       port: int = None,
                       metadata: Dict[str, str] = None,
                       connect_timeout_in_seconds: float = None) -> ConciergeSession:
        """
        :param session_type: The type of session to create
        :param hostname: The name of the host to connect to (if applicable)
        :param port: The port on the host to connect to (if applicable)
        :param metadata: A metadata dictionary of key/value pairs to be inserted into
                         the header. Default is None. Preferred format is a
                         dictionary of string keys to string values.
        :param connect_timeout_in_seconds: A timeout in seconds after which attempts
                        to reach a server will stop. By default, this is None,
                        meaning sessions will try forever.
        """
        session: ConciergeSession = None

        umbrella_timeout: Timeout = None
        if connect_timeout_in_seconds is not None:
            umbrella_timeout = Timeout()
            umbrella_timeout.set_limit_in_seconds(connect_timeout_in_seconds)

        # Incorrectly flagged as destination of Trust Boundary Violation 1
        #   Reason: This is the place where the session_type enforced-string argument is
        #           actually checked for positive use.
        if session_type == "direct":
            # This only looks at public networks, which is what we want.
            network_storage: AgentNetworkStorage = DirectAgentStorageUtil.create_network_storage()
            session = DirectConciergeSession(network_storage, metadata=metadata)
        elif session_type in ("http", "https"):

            # If there is no port really specified, use the default port
            use_port = port
            if port is None:
                use_port = ConciergeSession.DEFAULT_PORT

            security_cfg: Dict[str, Any] = None
            if session_type == "https":
                # For now, to get the https scheme
                security_cfg = {}
            session = HttpConciergeSession(host=hostname, port=use_port,
                                           security_cfg=security_cfg, metadata=metadata,
                                           timeout_in_seconds=connect_timeout_in_seconds)
        else:
            # Incorrectly flagged as destination of Trust Boundary Violation 2
            #   Reason: This is the place where the session_type enforced-string argument is
            #           actually checked for negative use.
            raise ValueError(f"session_type {session_type} is not understood")

        return session
