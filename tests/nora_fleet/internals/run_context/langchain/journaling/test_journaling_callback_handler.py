
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from nora_fleet.internals.run_context.langchain.journaling.journaling_callback_handler import JournalingCallbackHandler
from nora_fleet.message.types.agent_message import AgentMessage


class TestOnToolStartInvokingLabel:
    """on_tool_start should journal a diagnostic "Invoking" label even when the
    serialized tool carries no name."""

    @staticmethod
    def _make_handler():
        """Build a handler whose calling-agent journal records written messages."""
        calling_agent_journal = MagicMock()
        calling_agent_journal.write_message = AsyncMock()
        handler = JournalingCallbackHandler(
            calling_agent_journal=calling_agent_journal,
            base_journal=MagicMock(),
            parent_origin=[],
            origination=MagicMock(),
        )
        return handler, calling_agent_journal

    @pytest.mark.asyncio
    async def test_uses_tool_name_when_present(self):
        """A serialized tool with a name is reported verbatim."""
        handler, journal = self._make_handler()
        await handler.on_tool_start({"name": "search"}, "input", run_id=uuid4(), tags=[], inputs={})
        message = journal.write_message.call_args.args[0]
        assert isinstance(message, AgentMessage)
        assert message.content == "Invoking: `search` with:"
        assert message.structure["invoked_agent_name"] == "search"

    @pytest.mark.asyncio
    async def test_falls_back_to_placeholder_when_name_missing(self):
        """A serialized tool with no name yields a diagnostic placeholder label
        instead of an empty "Invoking: ``"; the raw value is still reported."""
        handler, journal = self._make_handler()
        await handler.on_tool_start({}, "input", run_id=uuid4(), tags=[], inputs={})
        message = journal.write_message.call_args.args[0]
        assert message.content == "Invoking: `<unnamed tool>` with:"
        assert message.structure["invoked_agent_name"] is None
