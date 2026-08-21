
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_common.config.config_filter_chain import ConfigFilterChain

from nora_fleet.internals.graph.persistence.mcp_manifest_dict_config_filter import McpManifestDictConfigFilter
from nora_fleet.internals.graph.persistence.periodic_manifest_dict_config_filter import PeriodicManifestDictConfigFilter


class ManifestDictFilterChain(ConfigFilterChain):
    """
    ConfigFilterChain for manifest dictionary entries.
    """

    def __init__(self, manifest_file: str, agent_network: str):
        """
        Constructor

        :param manifest_file: The name of the manifest file we are processing for logging purposes
        :param agent_network: The name of the agent network for logging purposes
        """
        super().__init__()

        # Order matters
        self.register(McpManifestDictConfigFilter())
        self.register(PeriodicManifestDictConfigFilter(manifest_file, agent_network))
