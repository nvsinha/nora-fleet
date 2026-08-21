
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


class ModelsHandler(ProxyHandler):
    """
    Implements GET /v1/models by recording against, or replaying from, the
    cassette. Most LangChain chat clients never call this, but it is proxied
    for parity with a real OpenAI endpoint so clients that introspect models
    still work fully offline in playback.
    """

    async def get(self) -> None:
        """Record or replay a models-list request."""
        await self.handle_request("GET", b"")
