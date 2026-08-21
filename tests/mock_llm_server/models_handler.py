
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

import time

import tornado.web

from tests.mock_llm_server.mock_state import MockState


class ModelsHandler(tornado.web.RequestHandler):
    """
    Implements GET /v1/models so OpenAI-style clients can introspect the
    list of available models. The mock server reports exactly one model
    whose name is the value configured in MockState.model_name.
    """

    def initialize(self, state: MockState) -> None:
        """Receive the shared MockState from the Tornado application."""
        # pylint: disable=attribute-defined-outside-init
        self.state = state

    def get(self) -> None:
        """Return a one-entry list containing the mock model."""
        self.write(
            {
                "object": "list",
                "data": [
                    {
                        "id": self.state.model_name,
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "mock",
                    }
                ],
            }
        )

    def data_received(self, chunk):
        """Required override of RequestHandler abstract method; no-op for GET."""
        return
