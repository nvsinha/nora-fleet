
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.internals.persistence.abstract_async_config_restorer import AbstractAsyncConfigRestorer


class RawManifestRestorer(AbstractAsyncConfigRestorer):
    """
    Implementation of the AbstractAsyncConfigRestorer interface that reads the contents
    of a single manifest file for agent networks/registries.
    The restore() and async_restore() methods both return a dictionary.
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__(file_purpose="agent network manifest", env_var="AGENT_MANIFEST_FILE", must_exist=False)
