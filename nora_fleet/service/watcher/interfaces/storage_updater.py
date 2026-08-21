
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_common.utils.startable import Startable


class StorageUpdater(Startable):
    """
    Interface for specific updating jobs that the Watcher performs.
    """

    def start(self):
        """
        Perform start up.
        """
        raise NotImplementedError

    def get_update_period_in_seconds(self) -> int:
        """
        :return: An int describing how long this updater ideally wants to go between
                calls to update_storage().
        """
        raise NotImplementedError

    def needs_updating(self, time_now_in_seconds: float) -> bool:
        """
        :param time_now_in_seconds: The current time in seconds.
                    We expect this to be from time.time()
        :return: True if this instance needs updating. False otherwise.
        """
        raise NotImplementedError

    def update_storage(self):
        """
        Perform an update
        """
        raise NotImplementedError
