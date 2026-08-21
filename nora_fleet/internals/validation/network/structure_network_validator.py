
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import List

from nora_common.validation.dictionary_validator import DictionaryValidator
from nora_common.validation.composite_dictionary_validator import CompositeDictionaryValidator

from nora_fleet.internals.validation.network.cycles_network_validator import CyclesNetworkValidator
from nora_fleet.internals.validation.network.missing_nodes_network_validator import MissingNodesNetworkValidator
from nora_fleet.internals.validation.network.tools_shape_validator import ToolsShapeValidator
from nora_fleet.internals.validation.network.unreachable_nodes_network_validator import UnreachableNodesNetworkValidator


class StructureNetworkValidator(CompositeDictionaryValidator):
    """
    Implementation of CompositeDictionaryValidator interface that uses multiple specific validators
    to do some standard validation for topological issues.
    This gets used by agent network designer.
    """

    def __init__(self):
        """
        Constructor
        """
        validators: List[DictionaryValidator] = [
            ToolsShapeValidator(),
            CyclesNetworkValidator(),
            MissingNodesNetworkValidator(),
            UnreachableNodesNetworkValidator(),
        ]
        super().__init__(validators)
