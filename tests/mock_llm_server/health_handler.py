
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

import tornado.web


class HealthHandler(tornado.web.RequestHandler):
    """
    Liveness probe at GET /healthz. Returns a fixed JSON object so external
    schedulers (Kubernetes, Docker, etc.) can confirm the process is up.
    """

    def get(self) -> None:
        """Return a fixed liveness payload."""
        self.write({"status": "ok"})

    def data_received(self, chunk):
        """Required override of RequestHandler abstract method; no-op for GET."""
        return
