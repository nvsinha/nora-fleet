
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import List

from nora_common.validation.dictionary_validator import DictionaryValidator
from nora_common.validation.composite_dictionary_validator import CompositeDictionaryValidator

from nora_fleet.internals.validation.network.keyword_network_validator import KeywordNetworkValidator
from nora_fleet.internals.validation.network.missing_nodes_network_validator import MissingNodesNetworkValidator
from nora_fleet.internals.validation.network.parameters_schema_network_validator import \
    ParametersSchemaNetworkValidator
from nora_fleet.internals.validation.network.tool_name_network_validator import ToolNameNetworkValidator
from nora_fleet.internals.validation.network.tools_shape_validator import ToolsShapeValidator
from nora_fleet.internals.validation.network.unreachable_nodes_network_validator import UnreachableNodesNetworkValidator
from nora_fleet.internals.validation.network.url_network_validator import UrlNetworkValidator


class ManifestNetworkValidator(CompositeDictionaryValidator):
    """
    Implementation of CompositeDictionaryValidator interface that uses multiple specific validators
    to do some standard validation upon reading in an agent network description.
    """

    def __init__(self, external_network_names: List[str] = None, mcp_servers: List[str] = None,
                 network_name: str = None):
        """
        Constructor

        :param external_network_names: A list of external network names
        :param mcp_servers: A list of MCP servers, as read in from a mcp_info.hocon file
        :param network_name: The agent network name for diagnostic log lines
        """
        validators: List[DictionaryValidator] = [
            # Note we do use the CyclesNetworkValidator here because cycles are actually OK.
            ToolsShapeValidator(network_name=network_name),
            KeywordNetworkValidator(network_name=network_name),
            MissingNodesNetworkValidator(),
            UnreachableNodesNetworkValidator(network_name=network_name),
            # No ToolBoxNetworkValidator yet.
            ToolNameNetworkValidator(),
            ParametersSchemaNetworkValidator(network_name=network_name),
            UrlNetworkValidator(external_network_names, mcp_servers,
                                network_name=network_name),
        ]
        super().__init__(validators)
