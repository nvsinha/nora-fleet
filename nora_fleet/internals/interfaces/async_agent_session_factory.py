
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any

from nora_fleet.interfaces.async_agent_session import AsyncAgentSession


class AsyncAgentSessionFactory:
    """
    Creates asynchronous AsyncAgentSessions for external agents.
    """

    def create_session(self, agent_url: str, invocation_context: Any, invocation: str = None) -> AsyncAgentSession:
        """
        :param agent_url: A url string pointing to an external agent that came from
                    a tools list in an agent spec.
        :param invocation_context: The context policy container that pertains to the invocation
                    of the agent.

                    Note: At this interface level we are typing this as Any to avoid
                    an import cycle.  This will always be an InvocationContext.

        :param invocation: String describing how the agent wants to be invoked.
                            Can be: "chatbot" - implies waiting for an answer.
                                    "event" - implies no answer needed
                                    None - implies chatbot

        :return: An implementation of AsyncAgentSession through which
                 communications about external agents can be made.
        """
        raise NotImplementedError

    def is_use_direct(self) -> bool:
        """
        :return: When True, will use a Direct session for external agents that would reside on the same server.
        """
        raise NotImplementedError
