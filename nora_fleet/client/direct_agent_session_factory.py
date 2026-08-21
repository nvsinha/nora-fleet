
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_common.time.timeout import Timeout
from nora_common.asyncio.asyncio_executor_pool import AsyncioExecutorPool

from nora_fleet.client.direct_agent_storage_util import DirectAgentStorageUtil
from nora_fleet.interfaces.agent_session import AgentSession
from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.graph.persistence.agent_network_restorer import AgentNetworkRestorer
from nora_fleet.internals.graph.persistence.registry_manifest_restorer import RegistryManifestRestorer
from nora_fleet.internals.interfaces.agent_network_provider import AgentNetworkProvider
from nora_fleet.internals.interfaces.context_type_llm_factory import ContextTypeLlmFactory
from nora_fleet.internals.interfaces.context_type_toolbox_factory import ContextTypeToolboxFactory
from nora_fleet.internals.interfaces.storage_class import StorageClass
from nora_fleet.internals.network_providers.agent_network_storage import AgentNetworkStorage
from nora_fleet.internals.network_providers.expiring_agent_network_storage import ExpiringAgentNetworkStorage
from nora_fleet.internals.reservations.direct_agent_reservationist import DirectAgentReservationist
from nora_fleet.internals.run_context.factory.master_toolbox_factory import MasterToolboxFactory
from nora_fleet.internals.run_context.factory.master_llm_factory import MasterLlmFactory
from nora_fleet.session.direct_agent_session import DirectAgentSession
from nora_fleet.session.external_agent_session_factory import ExternalAgentSessionFactory
from nora_fleet.session.missing_agent_check import MissingAgentCheck
from nora_fleet.session.session_invocation_context import SessionInvocationContext


class DirectAgentSessionFactory:
    """
    Sets up everything needed to use a DirectAgentSession more as a library.
    This includes:
        * Some reading of AgentNetworks
        * Setting up AgentNetworkStorage with agent networks
          which were read in
        * Initializing an LlmFactory
    """

    def __init__(self):
        """
        Constructor
        """
        # Read the manifest once and pass that into the Util call below.
        manifest_restorer = RegistryManifestRestorer()
        manifest_networks: Dict[str, Dict[str, AgentNetwork]] = manifest_restorer.restore()

        self.network_storage_dict: Dict[str, AgentNetworkStorage] = {
            StorageClass.TEMP: ExpiringAgentNetworkStorage()
        }

        for storage_class in StorageClass.ALL_PERMANENT:
            storage: AgentNetworkStorage = DirectAgentStorageUtil.create_network_storage(manifest_networks,
                                                                                         storage_type=storage_class)
            self.network_storage_dict[storage_class] = storage

    def create_session(self, agent_name: str, use_direct: bool = False,
                       metadata: Dict[str, str] = None, umbrella_timeout: Timeout = None) -> AgentSession:
        """
        :param agent_name: The name of the agent to use for the session.
                This name can be something in the manifest file (with no file suffix)
                or a specific full-reference to an agent network's hocon file.
        :param use_direct: When True, will use a Direct session for
                    external agents that would reside on the same server.
        :param metadata: A grpc metadata of key/value pairs to be inserted into
                         the header. Default is None. Preferred format is a
                         dictionary of string keys to string values.
        :param umbrella_timeout: A Timeout object to periodically check in loops.
                        Default is None (no timeout).
        """

        agent_network: AgentNetwork = self.get_agent_network(agent_name)
        config: Dict[str, Any] = agent_network.get_config()
        llm_factory: ContextTypeLlmFactory = MasterLlmFactory.create_llm_factory(config)
        toolbox_factory: ContextTypeToolboxFactory = MasterToolboxFactory.create_toolbox_factory(config)
        # Load once now that we know what tool registry to use.
        llm_factory.load()
        toolbox_factory.load()

        factory = ExternalAgentSessionFactory(use_direct=use_direct, network_storage_dict=self.network_storage_dict)
        executors_pool = AsyncioExecutorPool()

        # DEF - We could do max_lifetime here, but waiting until that seems necessary.
        reservationist = DirectAgentReservationist(set([self.network_storage_dict.get(StorageClass.TEMP)]))
        invocation_context = SessionInvocationContext(agent_name,
                                                      factory,
                                                      executors_pool,
                                                      llm_factory,
                                                      toolbox_factory,
                                                      metadata,
                                                      reservationist)
        invocation_context.start()
        session: DirectAgentSession = DirectAgentSession(agent_network=agent_network,
                                                         invocation_context=invocation_context,
                                                         metadata=metadata,
                                                         umbrella_timeout=umbrella_timeout)
        return session

    def get_agent_network(self, agent_name: str) -> AgentNetwork:
        """
        :param agent_name: The name of the agent whose AgentNetwork we want to get.
                This name can be something in the manifest file (with no file suffix)
                or a specific full-reference to an agent network's hocon file.
        :return: The AgentNetwork corresponding to that agent.
        """

        if agent_name is None or len(agent_name) == 0:
            return None

        agent_network: AgentNetwork = None
        if agent_name.endswith(".hocon") or agent_name.endswith(".json"):
            # We got a specific file name
            restorer = AgentNetworkRestorer()
            agent_network = restorer.restore(file_reference=agent_name)
        else:
            # Use the standard stuff available via the manifest file.
            for storage_type in StorageClass.ALL_PERMANENT:
                storage: AgentNetworkStorage = self.network_storage_dict.get(storage_type)
                agent_network_provider: AgentNetworkProvider = storage.get_agent_network_provider(agent_name)
                if agent_network_provider is None:
                    continue
                agent_network = agent_network_provider.get_agent_network()
                if agent_network is not None:
                    break

        # Common place for nice error messages when networks are not found
        MissingAgentCheck.check_agent_network(agent_network, agent_name)

        return agent_network
