
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from threading import Event

from nora_common.asyncio.asyncio_executor import AsyncioExecutor

from nora_fleet.interfaces.reservationist import Reservationist
from nora_fleet.internals.chat.async_collating_queue import AsyncCollatingQueue
from nora_fleet.internals.interfaces.async_agent_session_factory import AsyncAgentSessionFactory
from nora_fleet.internals.interfaces.context_type_toolbox_factory import ContextTypeToolboxFactory
from nora_fleet.internals.interfaces.context_type_llm_factory import ContextTypeLlmFactory
from nora_fleet.internals.interfaces.lingering_resource import LingeringResource
from nora_fleet.internals.journals.journal import Journal
from nora_fleet.internals.journals.origination import Origination


class InvocationContext(LingeringResource):
    """
    Top-level interface for encapsulating specific policy classes that pertain to
    a single invocation of an AgentSession or AsyncAgentSession, whether by way of a
    service call or library call.

    An InvocationContext will last for the duration of the work initiated by Session/request,
    which could outlive the Session/request itself, depending on just how its invocation is
    configured.
    """

    def start(self):
        """
        Starts the active components of this invocation context.
        Do this separately from constructor for more control.
        """
        raise NotImplementedError

    def get_effective_invocation(self) -> str:
        """
        :return: The effective invocation of the session
        """
        raise NotImplementedError

    def get_async_session_factory(self) -> AsyncAgentSessionFactory:
        """
        :return: The AsyncAgentSessionFactory associated with the invocation
        """
        raise NotImplementedError

    def get_asyncio_executor(self) -> AsyncioExecutor:
        """
        :return: The AsyncioExecutor associated with the invocation
        """
        raise NotImplementedError

    def get_origination(self) -> Origination:
        """
        :return: The Origination instance carrying state about tool instantation
                during the course of the AgentSession.
        """
        raise NotImplementedError

    def get_journal(self) -> Journal:
        """
        :return: The Journal instance that allows message reporting
                during the course of the AgentSession.
        """
        raise NotImplementedError

    def get_queue(self) -> AsyncCollatingQueue:
        """
        :return: The AsyncCollatingQueue instance via which messages are streamed to the
                QueueFilter mechanics
        """
        raise NotImplementedError

    def get_metadata(self) -> Dict[str, str]:
        """
        :return: The metadata to pass along with any request
        """
        raise NotImplementedError

    async def close_of_request(self, parent_resource: LingeringResource = None):
        """
        Release resources owned by this context when the request is complete.
        This can happen earlier than when the work is complete.

        :param parent_resource: The parent resource, if any
        """
        raise NotImplementedError

    async def close_of_work(self, parent_resource: LingeringResource = None):
        """
        Release resources owned by this context when the work is all done.
        This can happen later than when the request is complete.

        :param parent_resource: The parent resource, if any
        """
        raise NotImplementedError

    def get_request_reporting(self) -> Dict[str, Any]:
        """
        :return: The request reporting dictionary
        """
        raise NotImplementedError

    def is_cloned(self) -> bool:
        """
        :return: True if this instance is a clone of a request's original
                InvocationContext, created to invoke an external agent network
                on the same server via a direct session.
                False for the original InvocationContext of a request.
        """
        raise NotImplementedError

    def get_llm_factory(self) -> ContextTypeLlmFactory:
        """
        :return: The ContextTypeLlmFactory instance for the session
        """
        raise NotImplementedError

    def get_toolbox_factory(self) -> ContextTypeToolboxFactory:
        """
        :return: The ContextTypeToolboxFactory instance for the session
        """
        raise NotImplementedError

    def get_reservationist(self) -> Reservationist:
        """
        :return: The Reservationist instance for the session
        """
        raise NotImplementedError

    def get_port(self) -> int:
        """
        :return: The port on which the server was started
        """
        raise NotImplementedError

    def get_work_done_event(self) -> Event:
        """
        :return: The Event (synchronous) that will be set when work is done for this event
        """
        raise NotImplementedError

    def add_resource(self, resource: LingeringResource):
        """
        :param resource: The resource to add
        """
        raise NotImplementedError
