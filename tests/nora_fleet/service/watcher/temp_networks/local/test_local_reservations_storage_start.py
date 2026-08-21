
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
start() lifecycle tests for LocalReservationsStorage.

Verifies that start() creates the storage directory if it does not exist
and is idempotent against an existing directory.
"""
from nora_fleet.service.watcher.temp_networks.local.local_reservations_storage import LocalReservationsStorage


class TestLocalReservationsStorageStart:
    """start() creates the storage directory if it does not exist."""

    def test_start_creates_missing_directory(self, tmp_path):
        """start() creates the base directory when it does not yet exist."""
        target = tmp_path / "reservations_dir_that_does_not_exist_yet"
        assert not target.exists()
        LocalReservationsStorage(base_path=str(target)).start()
        assert target.is_dir()

    def test_start_is_idempotent_on_existing_directory(self, tmp_path):
        """start() must not fail when the base directory already exists."""
        target = tmp_path / "already_there"
        target.mkdir()
        LocalReservationsStorage(base_path=str(target)).start()
        assert target.is_dir()
