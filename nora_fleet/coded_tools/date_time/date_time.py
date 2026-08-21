
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from datetime import datetime
from datetime import timezone
from logging import getLogger
from logging import Logger

from nora_fleet.interfaces.coded_tool import CodedTool


class DateTime(CodedTool):
    """
    CodedTool implementation which provides a current date and time
    """

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> str:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    None

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
                but whose values are meant to be kept out of the chat stream.

                This dictionary is largely to be treated as read-only.
                It is possible to add key/value pairs to this dict that do not
                yet exist as a bulletin board, as long as the responsibility
                for which coded_tool publishes new entries is well understood
                by the agent chain implementation and the coded_tool implementation
                adding the data is not invoke()-ed more than once.

                Keys expected for this implementation are:
                    None

        :return:
            In case of successful execution:
                The current UTC date and time as a string.
        """
        # Get current UTC time
        now: datetime = datetime.now(timezone.utc)

        # Format it in a user-friendly way
        friendly_time: str = now.strftime("%A, %B %d, %Y at %I:%M %p %Z")

        logger: Logger = getLogger(self.__class__.__name__)
        logger.debug("Current UTC date and time: %s", friendly_time)

        return str(now)
