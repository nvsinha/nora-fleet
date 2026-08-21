
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""

import contextvars
import logging


class LogContextFilter(logging.Filter):
    """
    Custom logging filter for Http server.
    """

    def filter(self, record):
        """
        Logging filter: add key-value pairs from log_context
        to logging record to be used.
        """
        ctx = LogContextFilter.log_context.get()
        for key, value in ctx.items():
            setattr(record, key, value)
        return True

    @classmethod
    def set_log_context(cls):
        """
        Create log context class instance.
        """
        cls.log_context = contextvars.ContextVar("http_server_context", default={})
