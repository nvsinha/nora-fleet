
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Unit tests for ThinkingFileMessageProcessor's handling of AGENT_PROGRESS
heartbeat messages emitted by the nora-fleet HTTP server.

The server may emit empty-text AGENT_PROGRESS messages as keepalive ticks
to prevent intermediate proxies and clients from dropping idle streaming
connections during long quiet periods. The CLI's thinking-file logger
must treat those as no-ops; real AGENT_PROGRESS messages with content
must continue to be written.
"""

from pathlib import Path

from nora_fleet.client.thinking_file_message_processor import ThinkingFileMessageProcessor
from nora_fleet.message.types.chat_message_type import ChatMessageType


class TestThinkingFileMessageProcessorHeartbeat:
    """
    Verifies that the thinking-file logger silently drops empty-content
    AGENT_PROGRESS heartbeats and still writes real AGENT_PROGRESS messages.
    """

    def _make_processor(self, thinking_dir: Path) -> ThinkingFileMessageProcessor:
        # thinking_file=None forces the per-origin file path under thinking_dir.
        return ThinkingFileMessageProcessor(thinking_file=None, thinking_dir=str(thinking_dir))

    def test_heartbeat_with_empty_text_is_skipped(self, tmp_path):
        """
        A heartbeat message (AGENT_PROGRESS, text="", no structure, no origin)
        should produce no files in the thinking_dir.
        """
        processor = self._make_processor(tmp_path)
        heartbeat = {"type": "AGENT_PROGRESS", "text": ""}

        processor.process_message(heartbeat, ChatMessageType.AGENT_PROGRESS)

        assert not list(tmp_path.iterdir()), (
            "Expected the thinking_dir to remain empty after a heartbeat; "
            f"got {[p.name for p in tmp_path.iterdir()]}."
        )

    def test_heartbeat_without_text_field_is_skipped(self, tmp_path):
        """
        An AGENT_PROGRESS frame missing the text field altogether is also a
        no-op tick and must be skipped.
        """
        processor = self._make_processor(tmp_path)
        heartbeat = {"type": "AGENT_PROGRESS"}

        processor.process_message(heartbeat, ChatMessageType.AGENT_PROGRESS)

        assert not list(tmp_path.iterdir()), (
            "Expected the thinking_dir to remain empty after a heartbeat with "
            f"no text field; got {[p.name for p in tmp_path.iterdir()]}."
        )

    def test_real_agent_progress_message_is_still_written(self, tmp_path):
        """
        A real AGENT_PROGRESS message with non-empty text and an origin must
        still produce an entry in the thinking_dir.
        """
        processor = self._make_processor(tmp_path)
        real = {
            "type": "AGENT_PROGRESS",
            "text": "halfway done",
            "origin": [{"tool": "calculator", "instantiation_index": 0}],
        }

        processor.process_message(real, ChatMessageType.AGENT_PROGRESS)

        files = list(tmp_path.iterdir())
        assert len(files) == 1, (
            f"Expected one file for a real AGENT_PROGRESS message; got {files}."
        )
        contents = files[0].read_text()
        assert "halfway done" in contents, (
            f"Expected the progress text to appear in the thinking file; got:\n{contents}"
        )
        assert "AGENT_PROGRESS" in contents

    def test_agent_progress_with_structure_only_is_still_written(self, tmp_path):
        """
        An AGENT_PROGRESS message with a structure payload but no text is a
        real progress report (e.g. from AgentProgressReporter.async_report_progress)
        and must be written even though the text is absent.
        """
        processor = self._make_processor(tmp_path)
        real = {
            "type": "AGENT_PROGRESS",
            "structure": {"step": 3, "total": 7},
            "origin": [{"tool": "planner", "instantiation_index": 0}],
        }

        processor.process_message(real, ChatMessageType.AGENT_PROGRESS)

        files = list(tmp_path.iterdir())
        assert len(files) == 1, (
            f"Expected one file for a structured progress message; got {files}."
        )
        contents = files[0].read_text()
        assert '"step": 3' in contents, (
            f"Expected the structure JSON to appear in the thinking file; got:\n{contents}"
        )
