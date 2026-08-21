
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
See class comment for details.
"""
from __future__ import annotations

from tests.record_playback_llm_server.proxy_handler import ProxyHandler


class ChatCompletionsHandler(ProxyHandler):
    """
    Implements POST /v1/chat/completions by recording against, or replaying
    from, the cassette. The streaming vs one-shot decision is taken from the
    request body's `stream` flag, exactly as a real OpenAI endpoint would.
    """

    async def post(self) -> None:
        """Record or replay a chat-completions request."""
        await self.handle_request("POST", self.request.body or b"")
