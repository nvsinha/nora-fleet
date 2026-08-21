
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_common.config.config_filter import ConfigFilter

from nora_fleet.internals.interfaces.storage_class import StorageClass


class McpManifestDictConfigFilter(ConfigFilter):
    """
    Implementation of the ConfigFilter interface that reads the contents
    of a single manifest configuration dictionary for an agent networks/registry,
    making sure the mcp setting is consistent with the rest of the manifest dictionary.
    """

    def filter_config(self, basis_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filters the given basis config.

        :param basis_config: The config dictionary to act as the basis
                for filtering
        :return: A config dictionary, potentially modified as per the
                policy encapsulated by the implementation
        """

        # MCP designated entries are considered public by default.
        if "mcp" not in basis_config:
            basis_config["mcp"] = False
        if basis_config["mcp"]:
            basis_config[StorageClass.PUBLIC] = True

        return basis_config
