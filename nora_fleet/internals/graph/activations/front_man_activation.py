
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import List

from langchain_core.messages.base import BaseMessage

from nora_fleet.internals.graph.activations.calling_activation import CallingActivation
from nora_fleet.internals.interfaces.front_man import FrontMan
from nora_fleet.internals.interfaces.invocation_context import InvocationContext
from nora_fleet.internals.run_context.interfaces.run import Run


class FrontManActivation(CallingActivation, FrontMan):
    """
    A CallingActivation implementation which is the root of the call graph.
    """

    async def create_any_resources(self):
        """
        Creates resources that will be used throughout the lifetime of the component.
        """
        await self.create_resources()

    async def submit_message(self, user_input: str) -> List[BaseMessage]:
        """
        Entry-point method for callers of the root of the Activation tree.

        :param user_input: An input string from the user.
        :return: A list of response messages for the run
        """
        # Initialize our return value
        messages: List[BaseMessage] = []

        current_run: Run = await self.run_context.submit_message(user_input)

        terminate = False
        while not terminate:
            if self.run_context is None:
                # Breaking from inside a container during cleanup can yield a None
                # run_context
                break

            current_run = await self.run_context.wait_on_run(current_run, self.journal)

            if current_run.requires_action():
                current_run = await self.make_tool_function_calls(current_run)
            else:
                # Needs to get more information from the user on the basic task
                # of collecting information from the user about the current run.
                if self.run_context is None:
                    # Breaking from inside a container during cleanup can yield a None
                    # run_context
                    break
                messages = await self.run_context.get_response()
                terminate = True

        return messages

    def update_invocation_context(self, invocation_context: InvocationContext):
        """
        Update internal state based on the InvocationContext instance passed in.
        :param invocation_context: The context policy container that pertains to the invocation
        """
        self.journal = invocation_context.get_journal()
        if self.run_context is not None:
            self.run_context.update_invocation_context(invocation_context)

    async def build(self) -> BaseMessage:
        """
        Main entry point to the class.

        :return: A BaseMessage produced during this process.
        """
        # This is never called for a FrontMan, but is needed to satisfy the
        # class heirarchy stemming from CallableActivation.
        # A FrontMan is not Callable.
        raise NotImplementedError
