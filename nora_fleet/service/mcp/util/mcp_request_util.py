
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

from nora_fleet.service.utils.request_util import RequestUtil
from nora_fleet.session.mcp_service_agent_session import MCP_VERSION


class McpRequestUtil:
    """
    Utility class for generating MCP protocol requests and responses.
    """

    @classmethod
    def get_mcp_version(cls) -> str:
        """
        Get the MCP protocol version supported by this service.
        :return: MCP protocol version string.
        """
        return MCP_VERSION

    @classmethod
    def get_handshake_response(cls, request_id) -> Dict[str, Any]:
        """
        Generate a standard MCP handshake response.
        :param request_id: MCP request id;
        :return: json dictionary with handshake request in MCP format suitable for sending to a client.
        """
        return {
            "jsonrpc": "2.0",
            "id": RequestUtil.safe_request_id(request_id),
            "result": {
                "protocolVersion": MCP_VERSION,
                "capabilities": {
                    "logging": {},
                    "prompts": {},
                    "resources": {},
                    "tools": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": "NoraFleet-MCPServer",
                    "title": "Nora Fleet MCP Server",
                    "version": "1.0.0"
                },
                "instructions": ""
            }
        }
