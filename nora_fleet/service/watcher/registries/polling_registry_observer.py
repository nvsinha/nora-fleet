
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from logging import getLogger
from logging import Logger

from pathlib import Path

from watchdog.observers.polling import PollingObserver

from nora_fleet.service.watcher.registries.registry_change_handler import RegistryChangeHandler
from nora_fleet.service.watcher.registries.registry_observer import RegistryObserver


class PollingRegistryObserver(RegistryObserver):
    """
    Observer class for manifest file and its directory.
    """

    def __init__(self, manifest_path: Union[str, List[str]], poll_seconds: int):

        self.manifest_path: Union[str, List[str]] = manifest_path
        self.registry_observers: Dict[str, PollingObserver] = {}
        self.logger: Logger = getLogger(self.__class__.__name__)
        self.poll_seconds: int = poll_seconds
        self.event_handler: RegistryChangeHandler = RegistryChangeHandler()

        split_manifest_paths: List[str] = manifest_path
        if isinstance(manifest_path, str):
            split_manifest_paths = manifest_path.split(" ")

        for split_component in split_manifest_paths:
            one_manifest_path: str = Path(split_component)
            registry_path: str = str(one_manifest_path.parent)
            if registry_path not in self.registry_observers:
                # One observer per unique registry path
                self.registry_observers[registry_path] = PollingObserver(timeout=self.poll_seconds)

    def start(self):
        """
        Start running observer
        """
        for registry_path, observer in self.registry_observers.items():
            observer.schedule(self.event_handler, path=registry_path, recursive=True)
            observer.start()
            self.logger.info("Registry polling watchdog started on: %s for manifest %s with polling every %d sec",
                             registry_path, self.manifest_path, self.poll_seconds)

    def reset_event_counters(self) -> Tuple[int, int, int]:
        """
        Reset event counters and return current counters.
        """
        return self.event_handler.reset_event_counters()
