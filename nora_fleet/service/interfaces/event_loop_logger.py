
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""
from typing import Any
from typing import Dict


class EventLoopLogger:
    """
    Interface for a logger used in event loop request processing.
    Each logger call has request-specific metadata,
    which should be presented in the logger output.
    """

    def info(self, metadata: Dict[str, Any], msg: str, *args):
        """
        "Info" logging method.
        Prepare logger filter with request-specific metadata
        and delegate logging to underlying standard Logger.
        """
        raise NotImplementedError

    def warning(self, metadata: Dict[str, Any], msg: str, *args):
        """
        "Warning" logging method.
        Prepare logger filter with request-specific metadata
        and delegate logging to underlying standard Logger.
        """
        raise NotImplementedError

    def debug(self, metadata: Dict[str, Any], msg: str, *args):
        """
        "Debug" logging method.
        Prepare logger filter with request-specific metadata
        and delegate logging to underlying standard Logger.
        """
        raise NotImplementedError

    def error(self, metadata: Dict[str, Any], msg: str, *args):
        """
        "Error" logging method.
        Prepare logger filter with request-specific metadata
        and delegate logging to underlying standard Logger.
        """
        raise NotImplementedError
