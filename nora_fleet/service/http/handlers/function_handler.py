
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

from nora_fleet.service.generic.async_agent_service import AsyncAgentService
from nora_fleet.service.http.handlers.base_request_handler import BaseRequestHandler


class FunctionHandler(BaseRequestHandler):
    """
    Handler class for nora-fleet "function" API call.
    """

    async def get(self, agent_name: str):
        """
        Implementation of GET request handler for "function" API call.
        """
        metadata: Dict[str, Any] = self.get_metadata()
        service: AsyncAgentService = await self.get_service(agent_name, metadata)
        if service is None:
            return

        status_code, err_message = self.application.try_start_client_request(metadata, f"{agent_name}/function")
        if status_code != HTTPStatus.OK:
            self.do_finish(status_code, err_message)
            return

        try:
            data: Dict[str, Any] = {}
            result_dict: Dict[str, Any] = await service.function(data, metadata)

            # Return service response to the HTTP client
            self.set_header("Content-Type", "application/json")
            self.write(result_dict)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.process_exception(exc)
        finally:
            self.do_finish()
            self.application.finish_client_request(metadata, f"{agent_name}/function")
