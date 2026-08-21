
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Tuple

from nora_fleet.interfaces.reservation import Reservation


class ReservationsStorage:
    """
    An interface for implementations of basic Reservations storage,
    supporting addition Reservations in bulk and retrieval of individual Reservations,
    as well as expiration of Reservations based on their lifetime.
    """

    async def add_reservations(self, reservations_dict: Dict[Reservation, Any],
                               source: str = None):
        """
        Add a set of reservations for agent networks en-masse

        :param reservations_dict: A mapping of Reservation -> some deployable entity
        :param source: A string describing where the deployment was coming from
        """
        raise NotImplementedError

    def get_one_reservation(self, obj_key: str) -> Tuple[Reservation, Any]:
        """
        Extract a single reservation.

        :param obj_key: unique key for the reservation
        :return: Tuple of (reservation, agent data) if successful
                 and reservation is not expired,
                 (None, None) otherwise
        """
        raise NotImplementedError

    def expire_reservations(self):
        """
        Remove Reservations that are expired
        """
        raise NotImplementedError
