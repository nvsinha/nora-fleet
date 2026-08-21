
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from copy import deepcopy
from threading import Lock

from nora_fleet.internals.interfaces.agent_network_provider import AgentNetworkProvider
from nora_fleet.service.interfaces.event_loop_logger import EventLoopLogger
from nora_fleet.service.interfaces.server_context_lite import ServerContextLite
from nora_fleet.service.generic.async_agent_service import AsyncAgentService
from nora_fleet.service.generic.agent_server_logging import AgentServerLogging


# pylint: disable=too-many-instance-attributes
class AsyncAgentServiceProvider:
    """
    Class providing lazy construction of AsyncAgentService instance
    with given constructor parameters.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self,
                 request_logger: EventLoopLogger,
                 security_cfg: Dict[str, Any],
                 agent_name: str,
                 agent_network_provider: AgentNetworkProvider,
                 server_logging: AgentServerLogging,
                 server_context: ServerContextLite):
        """
        Constructor.
        :param request_logger: The instance of the EventLoopLogger that helps
                        log information from running event loop
        :param security_cfg: A dictionary of parameters used to
                        secure the TLS and the authentication of the gRPC
                        connection.  Supplying this implies use of a secure
                        GRPC Channel.  If None, uses insecure channel.
        :param agent_name: The agent name for the service
        :param agent_network_provider: The AgentNetworkProvider to use for the session.
        :param server_logging: An AgentServerLogging instance initialized so that
                        spawned asynchronous threads can also properly initialize
                        their logging.
        :param server_context: The ServerContext object containing global-ish state
        """
        self.request_logger = request_logger
        self.security_cfg = deepcopy(security_cfg)
        self.server_logging: AgentServerLogging = server_logging
        self.agent_network_provider: AgentNetworkProvider = agent_network_provider
        self.agent_name: str = agent_name
        self.lock: Lock = Lock()
        self.server_context: ServerContextLite = server_context
        self.service_instance: AsyncAgentService = None

    def get_service(self) -> AsyncAgentService:
        """
        Get service instance.
        Create it if it is not instantiated yet.
        """
        if self.service_instance is None:
            with self.lock:
                if self.service_instance is None:
                    self.service_instance = AsyncAgentService(
                        self.request_logger,
                        self.security_cfg,
                        self.agent_name,
                        self.agent_network_provider,
                        self.server_logging,
                        self.server_context)
        return self.service_instance

    def reset_service(self):
        """
        Reset service instance to None to allow re-creation on next get_service() call
        in case underlying AgentNetwork has changed.
        """
        with self.lock:
            self.service_instance = None

    def service_created(self) -> bool:
        """
        Return True if service instance has already been instantiated;
               False otherwise
        """
        return self.service_instance is not None
