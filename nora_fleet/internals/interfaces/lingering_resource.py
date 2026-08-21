
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from __future__ import annotations


class LingeringResource:
    """
    Interface for encapsulating specific policy for different points of
    process lifetime. Specifically we have two notions as to when things
    might be closed and lifetimes ended:

        1) at the end of a request
        2) when the work for a request is complete

    These may or may not be the same time depending on the type of request
    we are getting.
    """

    async def close_of_request(self, parent_resource: LingeringResource = None):
        """
        Release resources owned by this context when the request is complete.
        This can happen earlier than when the work is complete.

        :param parent_resource: parent resource, if any
        """
        # Do nothing by default for easier implementation inheritance

    async def close_of_work(self, parent_resource: LingeringResource = None):
        """
        Release resources owned by this context when the work is all done.
        This can happen later than when the request is complete.

        :param parent_resource: parent resource, if any
        """
        # Do nothing by default for easier implementation inheritance
