
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict
from typing import List
from typing import Union

from nora_fleet.internals.graph.registry.agent_network import AgentNetwork
from nora_fleet.internals.journals.message_journal import MessageJournal
from nora_fleet.message.filters.message_filter import MessageFilter
from nora_fleet.message.filters.message_filter_factory import MessageFilterFactory
from nora_fleet.message.processors.message_processor import MessageProcessor
from nora_fleet.message.processors.structure_message_processor import StructureMessageProcessor


class QueueFilter:
    """
    Prepares MessageFilter and MessageProcessors for use by the MessageJournal
    to be sure the output prodduced by the MessageJournal is suitable given the parameters
    of the request.
    """

    def __init__(self, chat_filter: Dict[str, Any], agent_network: AgentNetwork):
        """
        Constructor

        :param chat_filter: A dictionary form of chat.ChatFilter
        :param agent_network: An instance of AgentNetwork
        """
        self.message_filter: MessageFilter = MessageFilterFactory.create_message_filter(chat_filter)
        self.message_processor: MessageProcessor = self.create_outgoing_message_processor(agent_network)

    def create_outgoing_message_processor(self, agent_network: AgentNetwork) -> MessageProcessor:
        """
        :param agent_network: An instance of AgentNetwork
        :return: A MessageProcessor that filters messages outgoing to the client.
                How this works is based on settings on the front man.
                Can be None.
        """
        front_man_name: str = agent_network.find_front_man()
        front_man_spec: Dict[str, Any] = agent_network.get_agent_tool_spec(front_man_name)

        # Get the formats we should parse from the final answer from the config for the network.
        # As of 6/24/25, this is an unadvertised experimental feature.
        structure_formats: Union[str, List[str]] = front_man_spec.get("structure_formats")
        if structure_formats is None:
            return None

        # Eventually this might be a CompositeMessageProcessor
        message_processor: MessageProcessor = StructureMessageProcessor(structure_formats)
        return message_processor

    def apply_to_journal(self, message_journal: MessageJournal):
        """
        Apply the filter and processor to the MessageJournal
        """
        message_journal.set_message_filter(self.message_filter)
        message_journal.set_message_processor(self.message_processor)
