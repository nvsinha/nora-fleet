
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Unit tests for StreamingChatHandler._build_heartbeat_frame().

The heartbeat payload is no longer user-configurable: only the heartbeat
interval is. The handler calls _build_heartbeat_frame() once at
initialize() time and writes that frame verbatim for every tick. These
tests pin the frame's wire shape so future refactors of how it is built
do not silently change what clients see.
"""

import json

from nora_fleet.message.types.chat_message_type import ChatMessageType
from nora_fleet.service.http.handlers.streaming_chat_handler import StreamingChatHandler


# These tests access a deliberately-internal helper directly; suppress
# protected-access warnings file-wide.
# pylint: disable=protected-access
class TestStreamingChatHandlerHeartbeatFrame:
    """
    Pins the wire-format invariants of the constant heartbeat frame:
    it must be a ChatResponse-shaped JSON line carrying an empty
    AGENT_PROGRESS ChatMessage and terminated with a newline.
    """

    def test_frame_ends_with_newline(self):
        """JSON-Lines framing requires a trailing newline on each frame."""
        frame: str = StreamingChatHandler._build_keep_alive_frame()
        assert frame.endswith("\n"), (
            f"Heartbeat frame must end with a newline for JSON-Lines framing; got {frame!r}."
        )

    def test_frame_wraps_chat_message_in_response_envelope(self):
        """
        The frame parses as a ChatResponse: a top-level "response" key
        whose value is the ChatMessage.
        """
        parsed = json.loads(StreamingChatHandler._build_keep_alive_frame().rstrip("\n"))
        assert "response" in parsed, (
            f"Expected the heartbeat frame to use the ChatResponse envelope; got {parsed}."
        )
        assert isinstance(parsed["response"], dict)

    def test_frame_is_an_empty_agent_progress_message(self):
        """
        The wrapped ChatMessage is an AGENT_PROGRESS (matching what the
        CLI's ThinkingFileMessageProcessor heartbeat-skip recognizes)
        with empty text and no structure / origin.
        """
        parsed = json.loads(StreamingChatHandler._build_keep_alive_frame().rstrip("\n"))
        chat_message = parsed["response"]
        expected_type_name: str = ChatMessageType.to_string(ChatMessageType.AGENT_PROGRESS)

        assert chat_message == {"type": expected_type_name, "text": ""}, (
            f"Heartbeat ChatMessage must be exactly an empty AGENT_PROGRESS; got {chat_message}."
        )

    def test_frame_is_a_single_json_line(self):
        """
        The frame must contain exactly one newline (the terminator) so
        clients reading line-by-line see one frame per tick.
        """
        frame: str = StreamingChatHandler._build_keep_alive_frame()
        assert frame.count("\n") == 1, (
            f"Heartbeat frame must contain exactly one newline; got {frame!r}."
        )

    def test_repeated_calls_yield_identical_frames(self):
        """
        The builder is deterministic: calling it twice yields the same
        bytes, so it's safe to call once at initialize() time and reuse.
        """
        first: str = StreamingChatHandler._build_keep_alive_frame()
        second: str = StreamingChatHandler._build_keep_alive_frame()
        assert first == second, (
            f"Heartbeat frame must be stable across calls; got {first!r} vs {second!r}."
        )
