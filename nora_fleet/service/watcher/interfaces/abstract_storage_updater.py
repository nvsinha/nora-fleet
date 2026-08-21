
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.service.watcher.interfaces.storage_updater import StorageUpdater


class AbstractStorageUpdater(StorageUpdater):
    """
    Abstract base class for StorageUpdater implementations for common policy
    about checking for when it is needed to do update_storage().
    """

    def __init__(self, update_period_in_seconds: int):
        """
        Constructor

        :param update_period_in_seconds: An int describing how long this instance
                ideally wants to go between calls to update_storage().
        """
        self.last_update: float = 0.0
        self.update_period_in_seconds: int = update_period_in_seconds

    def start(self):
        """
        Perform start up.
        """
        raise NotImplementedError

    def update_storage(self):
        """
        Perform an update
        """
        raise NotImplementedError

    def get_update_period_in_seconds(self) -> int:
        """
        :return: An int describing how long this instance ideally wants to go between
                calls to update_storage().
        """
        return self.update_period_in_seconds

    def needs_updating(self, time_now_in_seconds: float) -> bool:
        """
        :param time_now_in_seconds: The current time in seconds.
                    We expect this to be from time.time()
        :return: True if this instance needs updating. False otherwise.
        """
        update_period: int = self.get_update_period_in_seconds()
        if update_period <= 0:
            # Never
            return False

        next_update: float = self.last_update + float(update_period)
        if time_now_in_seconds < next_update:
            # Not yet
            return False

        self.last_update = time_now_in_seconds
        return True
