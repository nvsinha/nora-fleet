
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details
"""
from typing import Any, Dict, Optional
import os
import json
from json.decoder import JSONDecodeError
import logging

from http import HTTPStatus
from tornado.web import RequestHandler

from nora_common.logging.sensitive_logger import SensitiveLogger

from nora_fleet.service.utils.request_util import RequestUtil

try:
    import yappi
    HAS_PROFILER = True
except ImportError:
    HAS_PROFILER = False


class ProfilerControlHandler(RequestHandler):
    """
    Handler class for controlling run-time profiler (yappi) via HTTP API calls.
    """

    async def post(self):
        """
        Implementation of POST request handler for profiler control.
        """
        is_enabled: bool = os.getenv("ENABLE_RUN_TIME_STATISTICS", "false").lower() == "true"
        logger = logging.getLogger(self.__class__.__name__)

        if not is_enabled:
            self.set_status(HTTPStatus.SERVICE_UNAVAILABLE)
            self.write("Run-time profiler is disabled. "
                       "To enable it, set environment variable ENABLE_RUN_TIME_STATISTICS to 'true'.")
            logger.info("Run-time profiler is disabled.")
            return

        if not HAS_PROFILER:
            self.set_status(HTTPStatus.SERVICE_UNAVAILABLE)
            self.write("Profiler library yappi is not available. Please install it with 'pip install yappi'")
            self.logger.info("Profiler library yappi is not available. Please install it with 'pip install yappi'")
            return

        action: Optional[str] = None
        profiler_data_path: Optional[str] = None

        sensitive_logger = SensitiveLogger(logger)

        # Parse the JSON request body:
        request_dict: Dict[str, Any] = None
        try:
            # Parse JSON body
            request_dict = json.loads(self.request.body)
            action = request_dict.get("action", "none").lower()
            profiler_data_path = request_dict.get("profiler_data_path")
        except JSONDecodeError as exc:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write("Invalid JSON in request body")

            # Static analysis false-positive for Information Exposure Through an Error Message
            # We specifically use the SensitiveLogger instance to log the message.
            # This allows for a hardened server to turn off logging of this information
            # by setting the env var NORA_LOG_SENSITIVE to "false", while still allowing
            # developers to see the error message.
            sensitive_logger.info("Invalid JSON in request body: %s", str(exc))
            return

        try:
            if action == "start":
                # Set clock type to "wall" time to get more accurate profiling results in async code
                yappi.set_clock_type("wall")
                yappi.start()
                self.write("profiling started")
                logger.info("PROFILER STARTED")
            elif action == "stop":
                yappi.stop()
                stats = yappi.get_func_stats()
                # pylint: disable=no-member
                stats.save(profiler_data_path, type="pstat")
                self.write(f"profiling stopped and saved to {RequestUtil.safe_message(str(profiler_data_path))}")
                logger.info("PROFILER STOPPED AND SAVED TO %s", profiler_data_path)
            else:
                self.write("Invalid profiler control action. Expected 'start' or 'stop'.")
                sensitive_logger.info("Invalid profiler control action received: %s", action)
                self.set_status(HTTPStatus.BAD_REQUEST)
        except Exception as exception:  # pylint: disable=broad-exception-caught
            # Static analysis false-positive for Information Exposure Through an Error Message
            # We specifically use the SensitiveLogger instance to log the message.
            # This allows for a hardened server to turn off logging of this information
            # by setting the env var NORA_LOG_SENSITIVE to "false", while still allowing
            # developers to see the error message.
            sensitive_logger.error("Error during profiler control operation '%s': %s",
                                   action, str(exception), exc_info=True)
            self.write(f"FAILED to {RequestUtil.safe_message(str(action))} profiler")
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)

    def data_received(self, chunk):
        """
        This method is required to be implemented as part of RequestHandler subclass,
        but is not used in our case as we do not expect any data in the request body.
        """
