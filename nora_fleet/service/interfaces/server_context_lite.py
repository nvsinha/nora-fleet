
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Dict

from janus import Queue

from nora_common.asyncio.asyncio_executor_pool import AsyncioExecutorPool

from nora_fleet.internals.chat.async_collating_queue import AsyncCollatingQueue
from nora_fleet.internals.network_providers.agent_network_storage import AgentNetworkStorage


class ServerContextLite:
    """
    Interface for getting a subset of information from the ServerContext.
    """

    def get_queues(self) -> Queue[AsyncCollatingQueue]:
        """
        :return: The janus Queue of queues for temporary agent deployment
        """
        raise NotImplementedError

    def get_server_port(self) -> int:
        """
        :return: The Server port
        """
        raise NotImplementedError

    def get_executor_pool(self) -> AsyncioExecutorPool:
        """
        :return: The AsyncioExecutorPool
        """
        raise NotImplementedError

    def get_event_work_queue(self) -> AsyncCollatingQueue:
        """
        :return: The event work queue
        """
        raise NotImplementedError

    def get_network_storage_dict(self) -> Dict[str, AgentNetworkStorage]:
        """
        :return: The Network Storage dictionary
        """
        raise NotImplementedError
