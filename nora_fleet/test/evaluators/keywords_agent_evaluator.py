
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any

from nora_fleet.test.evaluators.abstract_agent_evaluator import AbstractAgentEvaluator


class KeywordsAgentEvaluator(AbstractAgentEvaluator):
    """
    AbstractAgentEvaluator implementation that looks for specific keywords in output.
    """

    def test_one(self, verify_value: Any, test_value: Any):
        """
        :param verify_value: The value to verify against
        :param test_value: The value appearing in the test sample
        """
        if self.negate:
            self.asserts.assertNotIn(verify_value, test_value)
        else:
            self.asserts.assertIn(verify_value, test_value)
