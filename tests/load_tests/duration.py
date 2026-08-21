# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

"""Parse human-friendly timeout durations into whole seconds."""

import argparse


class DurationParser:
    """Parse human-friendly durations into whole seconds.

    A bare number is seconds (so existing commands are unchanged); an
    optional ``s``/``m``/``h`` suffix scales it, e.g. ``90s``, ``20m``,
    ``2h``, ``0.5h``.  Designed to be used as an argparse ``type``.
    """

    _UNITS = {"s": 1, "m": 60, "h": 3600}

    @staticmethod
    def parse(value: str) -> int:
        """Return whole seconds for ``value``; raise on bad input."""
        text = str(value).strip().lower()
        if not text:
            raise argparse.ArgumentTypeError("empty duration")
        unit = 1
        if text[-1] in DurationParser._UNITS:
            unit = DurationParser._UNITS[text[-1]]
            text = text[:-1]
        try:
            seconds = float(text) * unit
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"invalid duration '{value}': use seconds or a s/m/h "
                "suffix, e.g. 90s, 20m, 2h"
            ) from exc
        if seconds < 0:
            raise argparse.ArgumentTypeError(
                f"duration must be non-negative: '{value}'"
            )
        return int(round(seconds))
