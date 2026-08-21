
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any


class AsyncHopper:
    """
    An interface whose clients store things for later use.
    """

    async def put(self, item: Any):
        """
        :param item: The item to put in the hopper.
        """
        raise NotImplementedError
