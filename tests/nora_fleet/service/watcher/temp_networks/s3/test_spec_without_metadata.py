
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
The "metadata" key on an agent_spec is documented as optional in the
project's HOCON registry files (see registries/*.hocon: "Optional
metadata describing this agent network"). Callers may legitimately
hand a metadata-less spec to add_reservations. The storage's read
path requires metadata.reservation on every stored object, so the
write path must initialize the field when missing - otherwise
downstream reads would crash.

This module exercises the storage's defensive init branch:
    if agent_spec.get("metadata") is None:
        agent_spec["metadata"] = {}
    agent_spec["metadata"].update(new_metadata)
"""
from json import loads
import pytest

from tests.nora_fleet.service.watcher.temp_networks.s3.s3_reservations_storage_test_base \
    import S3ReservationsStorageTestBase


class TestSpecWithoutMetadata(S3ReservationsStorageTestBase):
    """
    Existing tests T1-T10 all pass agent_specs that include a
    pre-populated "metadata" key (built by _make_agent_spec). This
    test exercises the other side of the storage's metadata-init
    branch: input specs that arrive without a "metadata" key.
    """

    @pytest.mark.asyncio
    async def test_add_initializes_metadata_when_spec_lacks_key(self):
        """
        When the input agent_spec has no "metadata" key,
        add_reservations should:
          - Not raise (the is-None guard fires before .update).
          - Write exactly one S3 object.
          - Persist the storage-injected reservation+stored_at fields
            inside metadata so the read path can reconstruct the
            reservation.

        Catches a regression where the is-None guard is dropped
        (KeyError on .update), where init creates the wrong shape, or
        where init silently no-ops the write entirely.
        """
        reservation_id = "copy_cat-test-UUID-0011"
        reservation = self._make_reservation(reservation_id, lifetime_seconds=600.0)

        # Build an agent_spec with NO "metadata" key. This shape
        # mirrors a fresh registry entry whose "Optional metadata"
        # field was left out.
        spec_without_metadata = {
            "name": "copy_cat",
            "llm_config": {"model_name": "gpt-5.2"},
            "tools": [
                {
                    "name": "copy_cat",
                    "function": {
                        "description": "Frontman that delegates to the copyist.",
                    },
                    "instructions": "Always call the copyist tool.",
                    "tools": ["copyist"],
                }
            ],
        }

        # Precondition: the input genuinely has no metadata key.
        # If this fails, the test isn't exercising the branch we
        # think it is.
        self.assertNotIn(
            "metadata",
            spec_without_metadata,
            "Precondition violated: spec_without_metadata unexpectedly "
            "has a 'metadata' key.",
        )

        # The call should NOT raise. If it does, the is-None guard
        # has been removed and KeyError fires on .update().
        await self.storage.add_reservations({reservation: spec_without_metadata})

        # Exactly one S3 object was written. Catches a regression
        # where the missing-metadata path silently no-ops the write.
        self.assertEqual(
            1,
            len(self.fake_s3.objects),
            f"Expected exactly one S3 object after writing a spec "
            f"without metadata; bucket has {list(self.fake_s3.objects)}.",
        )

        # The reservation round-trips via the public read API. This
        # is the end-to-end check that the storage-injected metadata
        # was written correctly enough for the read path to find it.
        result_reservation, result_network = self.storage.get_one_reservation(
            reservation_id
        )
        self.assertIsNotNone(
            result_reservation,
            f"get_one_reservation returned None for {reservation_id!r} "
            f"after writing a spec without metadata; the storage's "
            f"metadata initialization did not produce a readable object.",
        )
        self.assertEqual(
            reservation_id,
            result_reservation.get_reservation_id(),
            "Read-back reservation id does not match the written id.",
        )
        self.assertIsNotNone(
            result_network,
            f"get_one_reservation returned None for the network for "
            f"{reservation_id!r}; the agent_spec round-trip is broken.",
        )

        # On-disk JSON has the storage-injected fields under metadata,
        # confirming the init branch produced the right shape (not
        # just an empty stub or a shape the read path tolerates by
        # accident).
        body = self.fake_s3.objects[f"reservations/{reservation_id}.json"]
        parsed = loads(body.decode("utf-8"))
        self.assertIn(
            "metadata",
            parsed,
            f"On-disk JSON has no 'metadata' key after the init branch "
            f"fired; got top-level keys: {list(parsed)}.",
        )
        self.assertIn(
            "reservation",
            parsed["metadata"],
            f"On-disk metadata is missing the storage-injected "
            f"'reservation' field; got metadata keys: "
            f"{list(parsed['metadata'])}.",
        )
        self.assertEqual(
            reservation_id,
            parsed["metadata"]["reservation"]["id"],
            "On-disk metadata.reservation.id does not match the "
            "written reservation id.",
        )
