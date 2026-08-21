
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from nora_common.config.config_filter import ConfigFilter
from nora_common.config.config_filter_chain import ConfigFilterChain

from nora_fleet.internals.graph.filters.defaults_config_filter import DefaultsConfigFilter
from nora_fleet.internals.graph.filters.dictionary_common_defs_config_filter \
    import DictionaryCommonDefsConfigFilter
from nora_fleet.internals.graph.filters.name_correction_config_filter import NameCorrectionConfigFilter
from nora_fleet.internals.graph.filters.string_common_defs_config_filter import StringCommonDefsConfigFilter


class NetworkConfigFilterChain(ConfigFilter):
    """
    A reusable ConfigFilter that applies the standard agent network
    filter chain: commondefs substitution, defaults injection, and
    name correction.

    This is the canonical ordering of filters for any agent network
    config dictionary.  Both AgentNetworkRestorer and the validation
    layer use this to ensure configs are fully resolved before
    further processing.
    """

    def filter_config(self, basis_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        :param basis_config: Raw agent network config dictionary
        :return: A fully resolved config dictionary
        """
        filter_chain = ConfigFilterChain()
        filter_chain.register(DictionaryCommonDefsConfigFilter())
        filter_chain.register(StringCommonDefsConfigFilter())
        filter_chain.register(DefaultsConfigFilter())
        filter_chain.register(NameCorrectionConfigFilter())

        config: Dict[str, Any] = filter_chain.filter_config(basis_config)
        return config
