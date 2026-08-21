
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from logging import getLogger
from logging import Logger


class SyncCloseable:
    """
    A simple object used to test the synchronous close()-ing of objects on sly_data.
    """

    def close(self):
        """
        Close the object
        """
        logger: Logger = getLogger(self.__class__.__name__)
        logger.info("sync close() called")
