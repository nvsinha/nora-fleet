
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
from typing import List

import http
import os

from http import HTTPStatus

from tornado.web import RequestHandler
from nora_fleet.service.http.logging.http_logger import HttpLogger
from nora_fleet.service.utils.server_status import ServerStatus


class HealthCheckHandler(RequestHandler):
    """
    Handler class for API endpoint health check.
    """

    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=too-many-positional-arguments,too-many-arguments
    def initialize(self,
                   forwarded_request_metadata: List[str],
                   server_status: ServerStatus,
                   op: str,
                   logging_config: Dict[str, Any],
                   versions: Dict[str, Any]):
        """
        This method is called by Tornado framework to allow
        injecting service-specific data into local handler context.
        Here we use it to inject CORS headers if so configured.
        :param forwarded_request_metadata: list of client metadata keys;
        :param server_status: current server status to query;
        :param op: requested healthcheck operation:
                   "ready" for /readyz query
                   "live" for /livez query
        :param logging_config: logging configuration dictionary
        :param versions: pre-computed library version dict returned in the
                   "versions" field of a successful health response. Supplied
                   from ServerStatus.get_versions() so per-request handlers
                   do not have to re-resolve importlib metadata on every probe.
        """
        self.logger = HttpLogger(forwarded_request_metadata, logging_config)
        if op == "ready":
            self.status = server_status.is_server_ready()
        else:
            self.status = server_status.is_server_live()
        self.server_name = server_status.get_server_name()
        self.versions = versions

        if os.environ.get("AGENT_ALLOW_CORS_HEADERS") is not None:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.set_header("Access-Control-Allow-Headers", "Content-Type, Transfer-Encoding")

    async def get(self):
        """
        Implementation of GET request handler for API health check.
        """

        try:
            if self.status:
                result_dict: Dict[str, Any] = {
                    "service": self.server_name,
                    "status": "ok",
                    "versions": self.versions,
                }
                self.set_header("Content-Type", "application/json")
                self.write(result_dict)
            else:
                # Set "service unavailable" status
                self.set_status(HTTPStatus.SERVICE_UNAVAILABLE)
                self.write({"error": "Service Unavailable"})
        except Exception:  # pylint: disable=broad-exception-caught
            # Handle unexpected errors
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.write({"error": "Internal server error"})
        finally:
            self.finish()

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get request metadata
        """
        return {}

    def data_received(self, chunk):
        """
        Method overrides abstract method of RequestHandler
        with no-op implementation.
        """
        return

    async def options(self, *_args, **_kwargs):
        """
        Handles OPTIONS requests for CORS support
        """
        # No body needed. Just return a 204 No Content
        self.set_status(http.HTTPStatus.NO_CONTENT)
        self.finish()
