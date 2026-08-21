
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from unittest import TestCase

from tests.load_tests.config import STATUS_CREATED
from tests.load_tests.config import STATUS_FAILED
from tests.load_tests.config import STATUS_KILLED
from tests.load_tests.config import STATUS_TIMEOUT
from tests.load_tests.validation.output_validator import OutputValidator


class TestCountResults(TestCase):
    """
    Unit tests for OutputValidator.count_results().

    These counts drive the run's verdict and the numbers in
    raw_results.json, so a request must never vanish between the
    result list and the totals.
    """

    def test_each_status_is_counted(self):
        """Every known status lands in its own bucket."""
        counts = OutputValidator.count_results([
            {"status": STATUS_CREATED},
            {"status": STATUS_CREATED},
            {"status": STATUS_FAILED},
            {"status": STATUS_TIMEOUT},
            {"status": STATUS_KILLED},
        ])

        self.assertEqual(counts[STATUS_CREATED], 2)
        self.assertEqual(counts[STATUS_FAILED], 1)
        self.assertEqual(counts[STATUS_TIMEOUT], 1)
        self.assertEqual(counts[STATUS_KILLED], 1)

    def test_no_results_counts_zero_not_empty(self):
        """An aborted stage still reports every bucket, all zero."""
        counts = OutputValidator.count_results([])

        self.assertEqual(
            counts,
            {
                STATUS_CREATED: 0,
                STATUS_FAILED: 0,
                STATUS_TIMEOUT: 0,
                STATUS_KILLED: 0,
            },
        )

    def test_unknown_status_counts_as_failed(self):
        """An unrecognized status is a failure, never a success.

        Counting it anywhere else -- or dropping it -- would let a
        run's totals disagree with the number of requests fired.
        """
        counts = OutputValidator.count_results([{"status": "WEIRD"}])

        self.assertEqual(counts[STATUS_FAILED], 1)
        self.assertEqual(counts[STATUS_CREATED], 0)

    def test_missing_status_counts_as_failed(self):
        """A result with no status recorded is treated as a failure."""
        counts = OutputValidator.count_results([{}])

        self.assertEqual(counts[STATUS_FAILED], 1)

    def test_totals_match_the_number_of_results(self):
        """No request is lost or double-counted, whatever its status."""
        results = [
            {"status": STATUS_CREATED},
            {"status": "WEIRD"},
            {},
            {"status": STATUS_TIMEOUT},
        ]

        counts = OutputValidator.count_results(results)

        self.assertEqual(sum(counts.values()), len(results))
