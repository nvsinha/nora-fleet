
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
expire_reservations() sweep tests for LocalReservationsStorage.

Verifies that the sweep deletes only files whose expiration timestamp is
in the past and tolerates a missing storage directory (no crash before
start()).
"""
import pytest

from nora_fleet.service.watcher.temp_networks.local.local_reservations_storage import LocalReservationsStorage
from tests.nora_fleet.service.watcher.temp_networks.local.local_reservations_test_helpers \
    import LocalReservationsTestHelpers


class TestLocalReservationsStorageExpiration:
    """expire_reservations() removes only files whose expiration is in the past."""

    @pytest.mark.asyncio
    async def test_expire_removes_only_stale_files(self, tmp_path):
        """expire_reservations() deletes only the reservation files whose deadline has passed."""
        storage = LocalReservationsStorage(base_path=str(tmp_path))
        storage.start()

        fresh = LocalReservationsTestHelpers.make_reservation(
            prefix="fresh", lifetime_s=3600.0, expires_offset_s=3600.0)   # +1h
        stale = LocalReservationsTestHelpers.make_reservation(
            prefix="stale", lifetime_s=60.0, expires_offset_s=-60.0)      # -60s

        await storage.add_reservations(
            {
                fresh: LocalReservationsTestHelpers.make_spec(),
                stale: LocalReservationsTestHelpers.make_spec(),
            },
            source="unit-test",
        )

        # Sanity: both files present before sweep.
        files_before = sorted(p.name for p in tmp_path.iterdir())
        assert len(files_before) == 2

        storage.expire_reservations()

        files_after = sorted(p.name for p in tmp_path.iterdir())
        assert files_after == [f"{fresh.get_reservation_id()}.json"], (
            f"Expected only the fresh reservation to survive; got {files_after}"
        )

    def test_expire_on_missing_directory_is_no_op(self, tmp_path):
        """
        expire_reservations() called before any writes -- or with the storage
        directory missing -- should log and continue, not raise.
        """
        target = tmp_path / "never_created"
        storage = LocalReservationsStorage(base_path=str(target))
        # NOTE: not calling start() -- directory intentionally doesn't exist.
        storage.expire_reservations()   # must not raise
