
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from unittest import TestCase
from unittest.mock import patch

from nora_fleet.middleware import nora_fleet_summarization_middleware as nssm_module
from nora_fleet.middleware.nora_fleet_summarization_middleware import NoraFleetSummarizationMiddleware


class TestNoraFleetSummarizationMiddleware(TestCase):
    """
    Unit tests for NoraFleetSummarizationMiddleware.
    """

    def _build(self, **kwargs):
        """
        Construct the middleware with a patched parent ``__init__`` so we don't
        need a real LLM. Returns the kwargs that were forwarded to
        ``SummarizationMiddleware.__init__`` so tests can assert against them.
        """
        captured = {}

        def fake_super_init(_self, **passed):
            captured.update(passed)

        with patch.object(nssm_module.SummarizationMiddleware, "__init__", fake_super_init):
            NoraFleetSummarizationMiddleware(
                model="fake-model",
                chat_history=[],
                **kwargs,
            )
        return captured

    def test_hocon_list_trigger_items_are_coerced_to_tuples(self):
        """
        HOCON has no tuple type, so a `trigger` configured as a list-of-lists
        arrives here as nested lists. langchain>=1.3 rejects list items. The
        middleware should convert each inner list to a tuple before delegating.
        """
        forwarded = self._build(trigger=[["messages", 3], ["tokens", 1000]])

        self.assertEqual(forwarded["trigger"], [("messages", 3), ("tokens", 1000)])

    def test_hocon_list_keep_is_coerced_to_tuple(self):
        """
        `keep` is a single ContextSize. langchain>=1.3 still expects a tuple,
        but HOCON delivers it as a list — coerce it.
        """
        forwarded = self._build(keep=["messages", 1])

        self.assertEqual(forwarded["keep"], ("messages", 1))

    def test_dict_trigger_items_pass_through_untouched(self):
        """
        langchain>=1.3 also accepts dict (Mapping) clauses like {"messages": 3}.
        Callers that already use the dict form should not be modified.
        """
        trigger = [{"messages": 3}]

        forwarded = self._build(trigger=trigger)

        self.assertEqual(forwarded["trigger"], [{"messages": 3}])

    def test_tuple_inputs_pass_through_untouched(self):
        """
        Programmatic (non-HOCON) callers may already pass tuples — the
        coercion must not disturb them.
        """
        forwarded = self._build(
            trigger=[("messages", 3)],
            keep=("messages", 1),
        )

        self.assertEqual(forwarded["trigger"], [("messages", 3)])
        self.assertEqual(forwarded["keep"], ("messages", 1))

    def test_none_trigger_passes_through(self):
        """
        `trigger=None` (the default) must not be coerced into anything.
        """
        forwarded = self._build()

        self.assertIsNone(forwarded["trigger"])
