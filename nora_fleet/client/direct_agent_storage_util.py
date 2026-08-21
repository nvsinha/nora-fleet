
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Dict

from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.graph.persistence.registry_manifest_restorer import RegistryManifestRestorer
from nora_fleet.internals.interfaces.storage_class import StorageClass
from nora_fleet.internals.network_providers.agent_network_storage import AgentNetworkStorage


class DirectAgentStorageUtil:
    """
    Sets up AgentNetworkStorage for direct usage.
    """

    @staticmethod
    def create_network_storage(manifest_networks: Dict[str, Dict[str, AgentNetwork]] = None,
                               storage_type: str = StorageClass.PUBLIC) -> AgentNetworkStorage:
        """
        Creates an AgentNetworkStorage instance for a given type.

        :param manifest_networks: Optional structure that is handed back from a RegistryManifestRestorer.restore()
                        call.  This has major keys being different network storage options like
                        "public" and "protected". The values are agent name -> AgentNetwork mappings.
                        By default the value is None, indicating we need to get this information
                        by calling the RegistryManifestRestorer.
        :param storage_type: The type of storage ("public" or "protected")
                        Default value is "public".
        :return: An AgentNetworkStorage populated from the Registry Manifest
        """
        network_storage = AgentNetworkStorage()

        if manifest_networks is None:
            manifest_restorer = RegistryManifestRestorer()
            manifest_networks = manifest_restorer.restore()

        storage_networks: Dict[str, AgentNetwork] = manifest_networks.get(storage_type)
        if storage_networks is None:
            return None

        for agent_name, agent_network in storage_networks.items():
            network_storage.add_agent_network(agent_name, agent_network)

        return network_storage
