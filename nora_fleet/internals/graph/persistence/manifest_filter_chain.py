
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_common.config.config_filter_chain import ConfigFilterChain

from nora_fleet.internals.graph.persistence.manifest_dict_config_filter import ManifestDictConfigFilter
from nora_fleet.internals.graph.persistence.manifest_key_config_filter import ManifestKeyConfigFilter
from nora_fleet.internals.graph.persistence.served_manifest_config_filter import ServedManifestConfigFilter


class ManifestFilterChain(ConfigFilterChain):
    """
    ConfigFilterChain for manifest files
    """

    def __init__(self, manifest_file: str):
        """
        Constructor

        :param manifest_file: The name of the manifest file we are processing for logging purposes
        """
        super().__init__()

        # Order matters
        self.register(ManifestKeyConfigFilter(manifest_file))
        self.register(ManifestDictConfigFilter(manifest_file))
        self.register(ServedManifestConfigFilter(manifest_file, warn_on_skip=True, entry_for_skipped=True))
