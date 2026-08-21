
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import List

from nora_fleet.internals.interfaces.async_hopper import AsyncHopper


class ListHopper(AsyncHopper):
    """
    An AsyncHopper implementation for tests that captures items in a list
    """

    def __init__(self):
        """
        Constructor
        """
        self.items: List[Any] = []

    async def put(self, item: Any):
        """
        :param item: The item to put in the hopper.
        """
        self.items.append(item)

    def get_items(self) -> List[Any]:
        """
        :return: The items in the hopper list
        """
        return self.items
