
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Dict
from typing import List

from nora_fleet.interfaces.async_agent_session import AsyncAgentSession
from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.interfaces.agent_network_provider import AgentNetworkProvider
from nora_fleet.internals.interfaces.async_agent_session_factory import AsyncAgentSessionFactory
from nora_fleet.internals.interfaces.invocation_context import InvocationContext
from nora_fleet.internals.interfaces.storage_class import StorageClass
from nora_fleet.internals.network_providers.agent_network_storage import AgentNetworkStorage
from nora_fleet.internals.utils.external_agent_parsing import ExternalAgentParsing
from nora_fleet.session.async_direct_agent_session import AsyncDirectAgentSession
from nora_fleet.session.async_http_service_agent_session import AsyncHttpServiceAgentSession


class ExternalAgentSessionFactory(AsyncAgentSessionFactory):
    """
    Creates AgentSessions for external agents.
    """

    def __init__(self, use_direct: bool = False,
                 network_storage_dict: Dict[str, AgentNetworkStorage] = None):
        """
        Constructor

        :param use_direct: When True, will use a Direct session for
                    external agents that would reside on the same server.
        :param network_storage_dict: A dictionary of AgentNetworkStorage instances which keeps all
                                the AgentNetwork instances.  Only used with use_direct=True.
        """
        self.use_direct: bool = use_direct
        self.network_storage_dict: Dict[str, AgentNetworkStorage] = None
        if self.use_direct:
            # Only store the reference if we will need it
            self.network_storage_dict = network_storage_dict

    def create_session(self, agent_url: str,
                       invocation_context: InvocationContext,
                       invocation: str = None) -> AsyncAgentSession:
        """
        :param agent_url: An url string pointing to an external agent that came from
                    a tools list in an agent spec.
        :param invocation_context: The context policy container that pertains to the invocation
                    of the agent.
        :param invocation: String describing how the agent wants to be invoked.
                            Can be: "chatbot" - implies waiting for an answer.
                                    "event" - implies no answer needed
                                    None - implies chatbot
        :return: An AsyncAgentSession through which communications about the external agent can be made.
        """

        server_port: int = invocation_context.get_port()
        agent_location: Dict[str, str] = ExternalAgentParsing.parse_external_agent(agent_url, server_port=server_port)
        session: AsyncAgentSession = self.create_session_from_location_dict(agent_location,
                                                                            invocation_context,
                                                                            invocation)
        return session

    def get_networks_order(self, network_storage_dict: Dict[str, AgentNetworkStorage]) -> List[str]:
        """
        :param network_storage_dict: The dictionary of AgentNetworkStorage instances to check for networks.
        :return: A List of AgentNetworkStorage names in the order they should be checked.
        Note: we need our "temp" storage to be checked last,
        because in the general case this might involve querying external storage, which is potentially slow.
        """
        networks_order: List[str] = []
        if network_storage_dict is None:
            return networks_order

        for storage_name in network_storage_dict.keys():
            if storage_name != StorageClass.TEMP:
                networks_order.append(storage_name)

        if StorageClass.TEMP in network_storage_dict:
            networks_order.append(StorageClass.TEMP)

        return networks_order

    def create_session_from_location_dict(self, agent_location: Dict[str, str],
                                          invocation_context: InvocationContext,
                                          invocation: str = None) -> AsyncAgentSession:
        """
        :param agent_location: An agent location dictionary returned by
                    ExternalAgentParsing.parse_external_agent()
        :param invocation_context: The context policy container that pertains to the invocation
                    of the agent.
        :param invocation: String describing how the agent wants to be invoked.
                            Can be: "chatbot" - implies waiting for an answer.
                                    "event" - implies no answer needed
                                    None - implies chatbot
        :return: An AsyncAgentSession through which communications about the external agent can be made.
        """
        if agent_location is None:
            return None

        # Create the session.
        host = agent_location.get("host")
        port = agent_location.get("port")
        agent_name = agent_location.get("agent_name")

        # Note: It's possible we might want some filtering/translation of
        #       metadata keys not unlike what we are doing for sly_data.
        metadata: Dict[str, str] = None
        if invocation_context is not None:
            metadata = invocation_context.get_metadata()

        session: AsyncAgentSession = None
        if self.is_use_direct() and (host is None or len(host) == 0 or host == "localhost"):

            # Optimization: We want to create a different kind of session to minimize socket usage
            # and potentially relieve the direct user of the burden of having to start a server

            agent_network_provider: AgentNetworkProvider = None
            for network_storage_name in self.get_networks_order(self.network_storage_dict):

                network_storage = self.network_storage_dict.get(network_storage_name)
                # Be sure we have something
                agent_network_provider = network_storage.get_agent_network_provider(agent_name)
                if agent_network_provider is None:
                    continue

                if agent_network_provider.get_agent_network() is not None:
                    break

            if agent_network_provider is not None:
                agent_network: AgentNetwork = agent_network_provider.get_agent_network()
                if agent_network is not None:
                    safe_invocation_context: InvocationContext = invocation_context.safe_shallow_copy(invocation)
                    session = AsyncDirectAgentSession(agent_network, safe_invocation_context, metadata=metadata)

        if session is None:
            # When creating a session for external agents, specifically use None for the
            # streaming timeout.  This implies an infinite amount of time to let the
            # external agent get its job done.  The rationale here is that:
            #   a)  We do not know how long any given external agent is really going to take
            #       to do its job.
            #   b)  We figure that the regular connection aspects to the server in question
            #       have already been sorted out in the obligitory call to function() that
            #       precedes any streaming_chat() call.
            session = AsyncHttpServiceAgentSession(host, port, agent_name=agent_name,
                                                   metadata=metadata, streaming_timeout_in_seconds=None)

        return session

    def is_use_direct(self) -> bool:
        """
        :return: When True, will use a Direct session for external agents that would reside on the same server.
        """
        return self.use_direct
