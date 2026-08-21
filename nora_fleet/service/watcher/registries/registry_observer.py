
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Tuple

from nora_common.utils.startable import Startable


class RegistryObserver(Startable):
    """
    Interface for specific kinds of filesystem observing
    """

    def start(self):
        """
        Start running observer
        """
        raise NotImplementedError

    def reset_event_counters(self) -> Tuple[int, int, int]:
        """
        Reset event counters and return current counters.
        """
        raise NotImplementedError
