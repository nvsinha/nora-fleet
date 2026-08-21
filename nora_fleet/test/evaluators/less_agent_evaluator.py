
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any

from nora_fleet.test.evaluators.abstract_agent_evaluator import AbstractAgentEvaluator


class LessAgentEvaluator(AbstractAgentEvaluator):
    """
    AbstractAgentEvaluator implementation that looks for inequalities of values in output.
    """

    def test_one(self, verify_value: Any, test_value: Any):
        """
        :param verify_value: The value to verify against
        :param test_value: The value appearing in the test sample
        """
        if self.negate:
            self.asserts.assertGreaterEqual(verify_value, test_value)
        else:
            self.asserts.assertLess(verify_value, test_value)
