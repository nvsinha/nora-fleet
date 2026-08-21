# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

"""Aggregates and logs client disconnection analysis."""

import logging

from tests.load_tests.config import SEPARATOR_WIDTH

logger = logging.getLogger(__name__)


class DisconnectionReporter:
    """Aggregates and logs client disconnection analysis.

    Holds the collected stage summaries for analysis.
    """

    def __init__(self, stage_summaries) -> None:
        self._summaries = stage_summaries

    def log_disconnection_summary(self) -> None:
        """Log aggregate client disconnection report."""
        all_disconnections = []
        for idx, stage in enumerate(self._summaries):
            for disc in stage.get("disconnections") or []:
                disc_copy = dict(disc)
                disc_copy.update({"batch": idx + 1})
                all_disconnections.append(disc_copy)
        if not all_disconnections:
            return
        logger.info("\n%s", "=" * SEPARATOR_WIDTH)
        logger.info(
            "  CLIENT DISCONNECTIONS (%s detected in server log)",
            len(all_disconnections),
        )
        logger.info("=" * SEPARATOR_WIDTH)
        for disc in all_disconnections:
            logger.info(
                "  Batch %s: %s — %s still processing at disconnect",
                disc.get("batch", "?"),
                disc.get("request_id", "unknown"),
                disc.get("agent", "unknown"),
            )
        logger.info(
            "\n  These requests had their client disconnect"
            "\n  before the server finished. The server detected the"
            "\n  disconnection and cancelled in-flight tasks."
            "\n  If unexpected, consider increasing --idle-timeout.",
        )
