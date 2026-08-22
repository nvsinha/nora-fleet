
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from unittest import TestCase

import pytest

from parameterized import parameterized

from nora_fleet.test.unittest.dynamic_hocon_unit_tests import DynamicHoconUnitTests


class TestIntegrationTestHocons(TestCase):
    """
    Data-driven dynamic test cases where each test case is specified by a single hocon file.
    """

    # A single instance of the DynamicHoconUnitTests helper class.
    # We pass it our source file location and a relative path to the common
    # root of the test hocon files listed in the @parameterized.expand()
    # annotation below so the instance can find the hocon test cases listed.
    DYNAMIC = DynamicHoconUnitTests(__file__, path_to_basis="../../fixtures")

    @parameterized.expand(DynamicHoconUnitTests.from_hocon_list([
        # These can be in any order.
        # Ideally more basic functionality will come first.
        # Barring that, try to stick to alphabetical order.
        "esp_decision_assistant/fallbacks_and_commondef_values.hocon",
        "music_nerd_pro_sly/combination_responses_with_history_direct.hocon",

        # List more hocon files as they become available here.
    ]), skip_on_empty=True)
    @pytest.mark.integration
    def test_hocon(self, test_name: str, test_hocon: str):
        """
        Test method for a single parameterized test case specified by a hocon file.
        Arguments to this method are given by the iteration that happens as a result
        of the magic of the @parameterized.expand annotation above.

        :param test_name: The name of a single test.
        :param test_hocon: The hocon file of a single data-driven test case.
        """
        # Call the guts of the dynamic test driver.
        # This will expand the test_hocon file name from the expanded list to
        # include the file basis implied by the __file__ and path_to_basis above.
        self.DYNAMIC.one_test_hocon(self, test_name, test_hocon)
