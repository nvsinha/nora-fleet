
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

from http import HTTPStatus

from nora_fleet.interfaces.concierge_session import ConciergeSession
from nora_fleet.internals.interfaces.storage_class import StorageClass
from nora_fleet.internals.network_providers.agent_network_storage import AgentNetworkStorage
from nora_fleet.service.http.handlers.base_request_handler import BaseRequestHandler
from nora_fleet.session.direct_concierge_session import DirectConciergeSession


class ConciergeHandler(BaseRequestHandler):
    """
    Handler class for nora-fleet "concierge" API call.
    """

    async def get(self):
        """
        Implementation of GET request handler for "concierge" API call.
        """
        metadata: Dict[str, Any] = self.get_metadata()
        status_code, err_message = self.application.try_start_client_request(metadata, "/api/v1/list")
        if status_code != HTTPStatus.OK:
            self.do_finish(status_code, err_message)
            return

        network_storage_dict: Dict[str, AgentNetworkStorage] = self.server_context.get_network_storage_dict()
        public_storage: AgentNetworkStorage = network_storage_dict.get(StorageClass.PUBLIC)

        # See what the authorizer says
        allowed_agents: List[str] = await self.agent_policy.list_agents(metadata)

        try:
            data: Dict[str, Any] = {}
            session: ConciergeSession = DirectConciergeSession(public_storage, metadata=metadata)
            result_dict: Dict[str, Any] = session.list(data)

            # Maybe remove agents if the agent_policy has something to say.
            if allowed_agents is not None:
                result_dict = self.pare_allowed_agents(allowed_agents, result_dict)

            # Return response to the HTTP client
            self.set_header("Content-Type", "application/json")
            self.write(result_dict)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.process_exception(exc)
        finally:
            self.do_finish()
            self.application.finish_client_request(metadata, "/api/v1/list")

    def pare_allowed_agents(self, allowed_agents: List[str], result_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove agents which are not allowed.

        :param allowed_agents: A list of agent names that are allowed by the authorization system
        :param result_dict: A dictionary version of the ConciergeResponse
                protobuf structure. Has the following keys:
            "agents" - the sequence of dictionaries describing available agents
        :return: A dictionary version of the ConciergeResponse
                protobuf structure. Has the following keys:
            "agents" - the sequence of dictionaries describing available agents
        """

        empty: List[Dict[str, Any]] = []
        agent_infos: List[Dict[str, Any]] = result_dict.get("agents", empty)

        # Create a dictionary of agent names for quick lookup
        agent_info_dict: Dict[str, Dict[str, Any]] = {}
        for agent_info in agent_infos:
            agent_name: str = agent_info.get("agent_name")
            if agent_name in allowed_agents:
                agent_info_dict[agent_name] = agent_info

        # Recreate the list of agents in the results by taking the values from the dictionary
        result_dict["agents"] = list(agent_info_dict.values())
        return result_dict
