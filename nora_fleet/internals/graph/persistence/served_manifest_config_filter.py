
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from logging import getLogger
from logging import Logger

from nora_common.config.config_filter import ConfigFilter


class ServedManifestConfigFilter(ConfigFilter):
    """
    Implementation of the ConfigFilter interface that reads the contents
    of a single manifest file for agent networks/registries, removing any entries
    that are not supposed to be served.
    """

    def __init__(self, manifest_file: str, warn_on_skip: bool = True, entry_for_skipped: bool = False):
        """
        Constructor

        :param manifest_file: The name of the manifest file we are processing for logging purposes
        :param warn_on_skip: If True, a warning will be logged if an entry is skipped
        :param entry_for_skipped: If True, the skipped entry will be included in the keys of the
                                output dictionary but the value will be None.
        """
        self.logger: Logger = getLogger(self.__class__.__name__)
        self.manifest_file: str = manifest_file
        self.warn_on_skip: bool = warn_on_skip
        self.entry_for_skipped: bool = entry_for_skipped

    def filter_config(self, basis_config: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Filters the given basis config.

        :param basis_config: The config dictionary to act as the basis
                for filtering
        :return: A config dictionary, potentially modified as per the
                policy encapsulated by the implementation
        """

        filtered: Dict[str, Dict[str, Any]] = {}

        for key, value in basis_config.items():

            skip: bool = False
            if value is None:
                skip = True
            elif isinstance(value, dict) and not value.get("serve", False):
                skip = True

            if skip:
                if self.warn_on_skip:
                    self.logger.warning("Manifest entry for %s in file %s will not be served, " +
                                        "per the 'serve' key in its config (default is False). Skipping.",
                                        key, self.manifest_file)
                # Instead of merely omitting the entry, we set it to None.
                # This allows for multiple manifest overlays to work.
                if self.entry_for_skipped:
                    filtered[key] = value
            else:
                filtered[key] = value

        return filtered
