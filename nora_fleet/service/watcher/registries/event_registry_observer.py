
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Tuple

import logging

from pathlib import Path

from watchdog.observers import Observer

from nora_fleet.service.watcher.registries.registry_change_handler import RegistryChangeHandler
from nora_fleet.service.watcher.registries.registry_observer import RegistryObserver


class EventRegistryObserver(RegistryObserver):
    """
    Observer class for manifest file and its directory.
    """

    def __init__(self, manifest_path: str):
        # DEF - not doing multiple manifests yet cuz this path is not active.
        # See Polling version if we ever need to go there.
        self.manifest_path: str = str(Path(manifest_path).resolve())
        self.registry_path: str = str(Path(self.manifest_path).parent)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.observer: Observer = Observer()
        self.event_handler: RegistryChangeHandler = RegistryChangeHandler()

    def start(self):
        """
        Start running observer
        """
        self.observer.schedule(self.event_handler, path=self.registry_path, recursive=True)
        self.observer.start()
        self.logger.info("Registry watchdog started on: %s for manifest %s",
                         self.registry_path, self.manifest_path)

    def reset_event_counters(self) -> Tuple[int, int, int]:
        """
        Reset event counters and return current counters.
        """
        return self.event_handler.reset_event_counters()
