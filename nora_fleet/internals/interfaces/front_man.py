
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from langchain_core.messages.base import BaseMessage

from nora_fleet.internals.interfaces.invocation_context import InvocationContext
from nora_fleet.internals.interfaces.lingering_resource import LingeringResource


class FrontMan(LingeringResource):
    """
    Interface that describes how a chat interface can interact with a FrontMan
    """

    async def create_any_resources(self):
        """
        Creates resources that will be used throughout the lifetime of the component.
        """
        raise NotImplementedError

    def update_invocation_context(self, invocation_context: InvocationContext):
        """
        Update internal state based on the InvocationContext instance passed in.
        :param invocation_context: The context policy container that pertains to the invocation
        """
        raise NotImplementedError

    def get_origin(self) -> List[Dict[str, Any]]:
        """
        :return: A List of origin dictionaries indicating the origin of the run.
                The origin can be considered a path to the original call to the front-man.
                Origin dictionaries themselves each have the following keys:
                    "tool"                  The string name of the tool in the spec
                    "instantiation_index"   An integer indicating which incarnation
                                            of the tool is being dealt with.
        """
        raise NotImplementedError

    def get_agent_tool_spec(self) -> Dict[str, Any]:
        """
        :return: the dictionary describing the data-driven agent
        """
        raise NotImplementedError

    async def submit_message(self, user_input: str) -> List[BaseMessage]:
        """
        Entry-point method for callers of the root of the Activation tree.

        :param user_input: An input string from the user.
        :return: A list of response messages for the run
        """
        raise NotImplementedError

    async def close_of_request(self, parent_resource: LingeringResource = None):
        """
        Release resources owned by this context when the request is complete.
        This can happen earlier than when the work is complete.

        :param parent_resource: parent resource, if any
        """
        raise NotImplementedError

    async def close_of_work(self, parent_resource: LingeringResource = None):
        """
        Release resources owned by this context when the work is all done.
        This can happen later than when the request is complete.

        :param parent_resource: parent resource, if any. Expected to be the
                RunContext which contains the scope of operation of this CallableActivation
        """
        raise NotImplementedError
