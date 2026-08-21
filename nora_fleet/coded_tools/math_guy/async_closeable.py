
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from logging import getLogger
from logging import Logger


class AsyncCloseable:
    """
    A simple object used to test the asynchronous close()-ing of objects on sly_data.
    """

    async def close(self):
        """
        Close the object
        """
        logger: Logger = getLogger(self.__class__.__name__)
        logger.info("async close() called")
