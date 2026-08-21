
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
import json
import tornado

from nora_common.utils.startable import Startable

from nora_fleet.service.http.logging.http_logger import HttpLogger
from nora_fleet.service.utils.service_resources import ServiceResources


class ResourcesUsageLogger(Startable):
    """
    Class for periodic logging of server run-time resource usage:
    file descriptors and open inet connections on server port.
    """

    def __init__(self, log_interval_seconds: int, http_port: int, logger: HttpLogger):
        """
        Constructor
        :param log_interval_seconds: interval in seconds between logging resource usage
        :param http_port: http port to use
        :param logger: HttpLogger instance for logging
        """
        self.log_interval_seconds = log_interval_seconds
        self.http_port: int = http_port
        self.logger: HttpLogger = logger
        self.periodic_callback = tornado.ioloop.PeriodicCallback(
            self.run_resources_usage,
            self.log_interval_seconds * 1000
        )

    def log_resources_usage(self):
        """
        Log current usage of server run-time resources:
        file descriptors and open inet connections on server port.
        """
        snapshot_dict: Dict[str, Any] = ServiceResources.get_snapshot_dict(self.http_port)
        self.logger.info({}, "Used: %s", json.dumps(snapshot_dict, indent=4))

    async def run_resources_usage(self):
        """
        Execute collecting and logging of server run-time resources
        in on-blocking mode w.r.t. server event loop.
        This is done because enumerating of some system resources
        could be relatively slow.
        """
        loop = tornado.ioloop.IOLoop.current()
        return await loop.run_in_executor(None, self.log_resources_usage)

    def start(self):
        """
        Start periodic logging of resource usage.
        """
        self.periodic_callback.start()
