
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
S3ReservationsStorage.add_reservations is last-writer-wins for a given
reservation id: a second call writes a new JSON blob to the same S3 key,
replacing the first one.
"""
import pytest

from tests.nora_fleet.service.watcher.temp_networks.s3.s3_reservations_storage_test_base \
    import S3ReservationsStorageTestBase


class TestOverwriteDuplicateId(S3ReservationsStorageTestBase):
    """
    The storage uses plain put_object with no conditional header, so S3's
    default "second write wins" semantics apply. This is intentional: it
    lets callers refresh a reservation's expiration or swap the agent_spec
    by re-issuing add_reservations under the same id.

    Catches a future regression that "protects" against duplicate ids by
    skipping the second put or by merging old and new payloads instead of
    replacing.
    """

    @pytest.mark.asyncio
    async def test_add_reservations_overwrites_on_duplicate_id(self):
        """
        Write twice under the same reservation id with different lifetimes
        and different agent specs; verify the second write fully replaces
        the first.
        """
        # Single reservation id reused across both writes.
        reservation_id = "copy_cat-test-UUID-0003"

        # First write: short lease, original model.
        first_reservation = self._make_reservation(
            reservation_id, lifetime_seconds=60.0,
        )
        first_spec = self._make_agent_spec("copy_cat")
        first_spec["llm_config"]["model_name"] = "gpt-4o"
        await self.storage.add_reservations({first_reservation: first_spec})

        # Second write: same id, longer lease, different model.
        second_reservation = self._make_reservation(
            reservation_id, lifetime_seconds=7200.0,
        )
        second_spec = self._make_agent_spec("copy_cat")
        second_spec["llm_config"]["model_name"] = "gpt-5.2"
        await self.storage.add_reservations({second_reservation: second_spec})

        # Read back; the storage should expose only the second write.
        returned_reservation, returned_network = \
            self.storage.get_one_reservation(reservation_id)

        # Reservation reflects the second write's lease.
        self.assertEqual(
            7200.0,
            returned_reservation.get_lifetime_in_seconds(),
            "lifetime_in_seconds reflects the first write; the second "
            "add_reservations call did not overwrite the S3 object.",
        )
        self.assertEqual(
            second_reservation.get_expiration_time_in_seconds(),
            returned_reservation.get_expiration_time_in_seconds(),
            "expiration_time_in_seconds does not match the second write.",
        )

        # Agent spec reflects the second write's content.
        self.assertEqual(
            "gpt-5.2",
            returned_network.get_config().get("llm_config").get("model_name"),
            "llm_config.model_name reflects the first write; the second "
            "add_reservations call did not overwrite the S3 object.",
        )

        # Exactly one S3 object exists for this id - the storage didn't
        # leak a second blob under a different key, and didn't merge the
        # two payloads. Goes through the FakeS3Client's in-memory dict
        # because we own that layer in this test.
        matching_keys = [
            key for key in self.fake_s3.objects
            if key.endswith(f"{reservation_id}.json")
        ]
        self.assertEqual(
            1,
            len(matching_keys),
            f"Expected exactly one S3 object for {reservation_id}, found "
            f"{len(matching_keys)}: {matching_keys}",
        )
