
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from tests.nora_fleet.internals.run_context.langchain.llms.custom_llm_factory import CustomLlmFactory


class TestLlmFactory:
    """
    Test creating custom Factory class for LLM operations
    """

    def test_llm_factory(self):
        """
        This method specifies the default LlmPolicy class that will be used for any LLMs
        instantiated by this factory that don't specify an llm_policy_class in their config.
        """
        _ = CustomLlmFactory()
