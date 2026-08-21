
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

from nora_fleet.internals.journals.journal import Journal


class CompoundJournal(Journal):
    """
    A Journal implementation that can service multiple other Journal instances
    """

    def __init__(self, journals: List[Journal] = None):
        """
        Constructor

        :param journals: A List of Journal instances to simultaneously service
        """
        self.journals: List[Journal] = journals
        if self.journals is None:
            self.journals = []

    def add_journal(self, journal: Journal):
        """
        Adds a journal to the list
        :param journal: A Journal instance to service
        """
        self.journals.append(journal)

    async def write_message(self, message: BaseMessage, origin: List[Dict[str, Any]]):
        """
        Writes a BaseMessage entry into the journal
        :param message: The BaseMessage instance to write to the journal
        :param origin: A List of origin dictionaries indicating the origin of the run.
                The origin can be considered a path to the original call to the front-man.
                Origin dictionaries themselves each have the following keys:
                    "tool"                  The string name of the tool in the spec
                    "instantiation_index"   An integer indicating which incarnation
                                            of the tool is being dealt with.
        """
        for journal in self.journals:
            await journal.write_message(message, origin)
