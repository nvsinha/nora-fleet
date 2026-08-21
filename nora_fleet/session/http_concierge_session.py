
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from json import loads
from requests import get as http_get

from nora_fleet.interfaces.concierge_session import ConciergeSession
from nora_fleet.session.abstract_http_service_agent_session import AbstractHttpServiceAgentSession


class HttpConciergeSession(AbstractHttpServiceAgentSession, ConciergeSession):
    """
    Implementation of ConciergeSession that talks to an HTTP service.
    This is largely only used by command-line tests.
    """

    def list(self, request_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        :param request_dict: A dictionary version of the ConciergeRequest
                    protobuf structure. Has the following keys:
                        <None>
        :return: A dictionary version of the ConciergeResponse
                    protobuf structure. Has the following keys:
                "agents" - the sequence of dictionaries describing available agents
        """
        path: str = self.get_request_path("list")
        try:
            response = http_get(path, json=request_dict, headers=self.get_headers(),
                                timeout=self.timeout_in_seconds)
            result_dict = loads(response.text)
            return result_dict
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise ValueError(self.help_message(path)) from exc
