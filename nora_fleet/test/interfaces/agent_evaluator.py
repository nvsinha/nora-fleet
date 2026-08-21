
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any

from nora_fleet.message.processors.basic_message_processor import BasicMessageProcessor


class AgentEvaluator:
    """
    Interface definition for evaluating part of an agent's response
    """

    def evaluate(self, processor: BasicMessageProcessor, test_key: str, verify_for: Any):
        """
        Evaluate the contents of the BasicMessageProcessor

        :param processor: The BasicMessageProcessor to evaluate
        :param test_key: the compound .-delimited key of the response value to test
        :param verify_for: The data to evaluate the response against
        """
        raise NotImplementedError
