
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

from nora_fleet.service.http.logging.http_logger import HttpLogger
from nora_fleet.service.utils.request_util import RequestUtil


class McpResourcesProcessor:
    """
    Class implementing "resources"-related MCP requests.
    Overall MCP documentation can be found here:
    https://modelcontextprotocol.io/specification/2025-06-18/server/resources
    """

    def __init__(self, logger: HttpLogger):
        self.logger: HttpLogger = logger

    async def list_resources(self, request_id, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        List available MCP resources.
        :param request_id: MCP request id;
        :param metadata: http-level request metadata;
        :return: json dictionary with resources list in MCP format
        """
        _ = metadata
        return {
            "jsonrpc": "2.0",
            "id": RequestUtil.safe_request_id(request_id),
            "result": {
                "resources": []
            }
        }
