
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import List

from nora_fleet.internals.interfaces.agent_state_listener import AgentStateListener
from nora_fleet.internals.interfaces.agent_storage_source import AgentStorageSource


class RecordingListener(AgentStateListener):
    """
    A test listener that records all state change notifications.
    """

    def __init__(self):
        self.added: List[str] = []
        self.modified: List[str] = []
        self.removed: List[str] = []

    def agent_added(self, agent_name: str, source: AgentStorageSource):
        self.added.append(agent_name)

    def agent_modified(self, agent_name: str, source: AgentStorageSource):
        self.modified.append(agent_name)

    def agent_removed(self, agent_name: str, source: AgentStorageSource):
        self.removed.append(agent_name)

    def reset(self):
        """
        Reset the state of the listener.
        """
        self.added.clear()
        self.modified.clear()
        self.removed.clear()
