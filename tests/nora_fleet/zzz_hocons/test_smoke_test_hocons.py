
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


class TestSmokeTestHocons(TestCase):
    """
    Data-driven dynamic test cases where each test case is specified by a single hocon file.
    """

    # A single instance of the DynamicHoconUnitTests helper class.
    # We pass it our source file location and a relative path to the common
    # root of the test hocon files listed in the @parameterized.expand()
    # annotation below so the instance can find the hocon test cases listed.
    DYNAMIC = DynamicHoconUnitTests(__file__, path_to_basis="../../fixtures")

    # Hocon test cases that are temporarily disabled at runtime via pytest.skip().
    # We deliberately keep these listed in the @parameterized.expand() blocks
    # below so they remain visible in test reports as SKIPPED (with a reason)
    # rather than being silently commented out. To disable a new hocon, append
    # an entry to this dict. Remove an entry once its underlying blocker is
    # resolved.
    DISABLED_HOCONS = {
        "music_nerd_pro_llm_azure/combination_responses_with_history_direct.hocon":
            "Issue #910: disabled until #909 is resolved.",
        "music_nerd_pro_llm_bedrock_claude/combination_responses_with_history_direct.hocon":
            "Issue #910: disabled until #909 is resolved.",
        "music_nerd_pro_llm_anthropic/combination_responses_with_history_direct.hocon":
            "Issue #936: disabled until #909 is resolved.",
        "music_nerd_pro_llm_openrouter/combination_responses_with_history_direct.hocon":
            "Disabled until OPENROUTER_API_KEY is added to the GitHub Actions secrets.",
        "music_nerd_pro_llm_ollama/combination_responses_with_history_http.hocon":
            "Issue #1226: disabled until #909 is resolved.",
    }

    def _skip_if_disabled(self, test_hocon: str) -> None:
        """Skip the current test if its hocon is listed in DISABLED_HOCONS."""
        reason = self.DISABLED_HOCONS.get(test_hocon)
        if reason is not None:
            pytest.skip(reason)

    @parameterized.expand(DynamicHoconUnitTests.from_hocon_list([
        # These can be in any order.
        # Ideally more basic functionality will come first.
        # Barring that, try to stick to alphabetical order.
        "music_nerd_pro/combination_responses_with_history_direct.hocon",

        # List more hocon files as they become available here.
    ]), skip_on_empty=True)
    @pytest.mark.smoke
    @pytest.mark.smoke_default_llm_provider
    def test_hocon_with_server(self, test_name: str, test_hocon: str):
        """
        Test method for a single parameterized test case specified by a hocon file.
        Arguments to this method are given by the iteration that happens as a result
        of the magic of the @parameterized.expand annotation above.

        :param test_name: The name of a single test.
        :param test_hocon: The hocon file of a single data-driven test case.
        """
        # Skip hocons listed in DISABLED_HOCONS (e.g. temporarily blocked tests).
        self._skip_if_disabled(test_hocon)

        # Call the guts of the dynamic test driver.
        # This will expand the test_hocon file name from the expanded list to
        # include the file basis implied by the __file__ and path_to_basis above.
        self.DYNAMIC.one_test_hocon(self, test_name, test_hocon)

    @parameterized.expand(DynamicHoconUnitTests.from_hocon_list([
        # These can be in any order.
        # Ideally more basic functionality will come first.
        # Barring that, try to stick to alphabetical order.
        "music_nerd_pro/combination_responses_with_history_mcp.hocon",
        "copy_cat/create_and_use_temp_network_http.hocon",
        "copy_cat_middleware/create_temp_network_http.hocon",
        # Issue #734:
        # "music_nerd_pro_sly/combination_responses_with_history_mcp.hocon",

        # List more hocon files as they become available here.
    ]), skip_on_empty=True)
    @pytest.mark.smoke
    @pytest.mark.smoke_needs_server
    def test_hocon_with_server_default_llm(self, test_name: str, test_hocon: str):
        """
        Test method for a single parameterized test case specified by a hocon file.
        Arguments to this method are given by the iteration that happens as a result
        of the magic of the @parameterized.expand annotation above.

        :param test_name: The name of a single test.
        :param test_hocon: The hocon file of a single data-driven test case.
        """
        # Skip hocons listed in DISABLED_HOCONS (e.g. temporarily blocked tests).
        self._skip_if_disabled(test_hocon)

        # Call the guts of the dynamic test driver.
        # This will expand the test_hocon file name from the expanded list to
        # include the file basis implied by the __file__ and path_to_basis above.
        self.DYNAMIC.one_test_hocon(self, test_name, test_hocon)

    @parameterized.expand(DynamicHoconUnitTests.from_hocon_list([
        # These can be in any order.
        # Ideally more basic functionality will come first.
        # Barring that, try to stick to alphabetical order.
        "music_nerd_pro_llm_anthropic/combination_responses_with_history_direct.hocon",
        "music_nerd_pro_llm_gemini/combination_responses_with_history_direct.hocon",
        "music_nerd_pro_llm_azure/combination_responses_with_history_direct.hocon",
        "music_nerd_pro_llm_bedrock_claude/combination_responses_with_history_direct.hocon",
        "music_nerd_pro_llm_openrouter/combination_responses_with_history_direct.hocon",

        # List more hocon files as they become available here.
    ]), skip_on_empty=True)
    @pytest.mark.smoke
    @pytest.mark.smoke_non_default_llm_provider
    def test_hocon_with_non_default_llm(self, test_name: str, test_hocon: str):
        """
        Test method for a single parameterized test case specified by a hocon file.
        Arguments to this method are given by the iteration that happens as a result
        of the magic of the @parameterized.expand annotation above.

        :param test_name: The name of a single test.
        :param test_hocon: The hocon file of a single data-driven test case.
        """
        # Skip hocons listed in DISABLED_HOCONS (e.g. temporarily blocked tests).
        self._skip_if_disabled(test_hocon)

        # Call the guts of the dynamic test driver.
        # This will expand the test_hocon file name from the expanded list to
        # include the file basis implied by the __file__ and path_to_basis above.
        self.DYNAMIC.one_test_hocon(self, test_name, test_hocon)

    @parameterized.expand(DynamicHoconUnitTests.from_hocon_list([
        # These can be in any order.
        # Ideally more basic functionality will come first.
        # Barring that, try to stick to alphabetical order.
        "music_nerd_pro_llm_ollama/combination_responses_with_history_http.hocon",

        # List more hocon files as they become available here.
    ]), skip_on_empty=True)
    @pytest.mark.smoke
    @pytest.mark.smoke_non_default_llm_provider_needs_server
    @pytest.mark.ollama
    def test_hocon_with_server_non_default_llm(self, test_name: str, test_hocon: str):
        """
        Test method for a single parameterized test case specified by a hocon file.
        Arguments to this method are given by the iteration that happens as a result
        of the magic of the @parameterized.expand annotation above.

        :param test_name: The name of a single test.
        :param test_hocon: The hocon file of a single data-driven test case.
        """
        # Skip hocons listed in DISABLED_HOCONS (e.g. temporarily blocked tests).
        self._skip_if_disabled(test_hocon)

        # Call the guts of the dynamic test driver.
        # This will expand the test_hocon file name from the expanded list to
        # include the file basis implied by the __file__ and path_to_basis above.
        self.DYNAMIC.one_test_hocon(self, test_name, test_hocon)
