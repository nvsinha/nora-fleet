
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Constructor-validation tests for LocalReservationsStorage.

Verifies that the base_path can come from the constructor argument or the
AGENT_RESERVATIONS_LOCAL_PATH environment variable, and that missing both
raises ValueError.
"""
import pytest

from nora_fleet.service.watcher.temp_networks.local.local_reservations_storage import LocalReservationsStorage


class TestLocalReservationsStorageConstructor:
    """
    Constructor validation: path can come from the base_path arg or the
    AGENT_RESERVATIONS_LOCAL_PATH env var; missing both is an error.
    """

    def test_missing_path_raises(self, monkeypatch):
        """No base_path arg and no env var -> ValueError."""
        monkeypatch.delenv("AGENT_RESERVATIONS_LOCAL_PATH", raising=False)
        with pytest.raises(ValueError, match="Local path for reservations"):
            LocalReservationsStorage()

    def test_env_var_fallback(self, monkeypatch, tmp_path):
        """base_path defaults from the env var when the arg is empty."""
        monkeypatch.setenv("AGENT_RESERVATIONS_LOCAL_PATH", str(tmp_path))
        storage = LocalReservationsStorage()
        assert storage.base_path == str(tmp_path.resolve())

    def test_explicit_arg_wins_over_env(self, monkeypatch, tmp_path):
        """A non-empty base_path arg is used even when the env var is set."""
        monkeypatch.setenv("AGENT_RESERVATIONS_LOCAL_PATH", "/some/env/path")
        storage = LocalReservationsStorage(base_path=str(tmp_path))
        assert storage.base_path == str(tmp_path.resolve())
