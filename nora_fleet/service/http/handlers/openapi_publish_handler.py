
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

from http import HTTPStatus

from nora_fleet.service.http.handlers.base_request_handler import BaseRequestHandler


class OpenApiPublishHandler(BaseRequestHandler):
    """
    Handler class for nora-fleet OpenAPI service spec publishing"concierge" API call.
    """

    async def get(self):
        """
        Implementation of GET request handler
        for "publish my OpenAPI specification document" call.
        """
        metadata: Dict[str, Any] = self.get_metadata()
        status_code, err_message = self.application.try_start_client_request(metadata, "/api/v1/docs")
        if status_code != HTTPStatus.OK:
            self.do_finish(status_code, err_message)
            return

        # Return json data to the HTTP client
        self.set_header("Content-Type", "application/json")
        self.write(self.openapi_service_spec)
        self.do_finish()
        self.application.finish_client_request(metadata, "/api/v1/docs")
