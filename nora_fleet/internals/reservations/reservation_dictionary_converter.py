
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

from nora_common.serialization.interface.dictionary_converter import DictionaryConverter

from nora_fleet.interfaces.reservation import Reservation
from nora_fleet.internals.reservations.agent_reservation import AgentReservation


class ReservationDictionaryConverter(DictionaryConverter):
    """
    DictionaryConverter implementation for converting Reservations back and forth to dictionaries.
    """

    def to_dict(self, obj: Reservation) -> Dict[str, Any]:
        """
        :param obj: The Reservation object to be converted into a dictionary
        :return: A data-only dictionary that represents all the data for
                the given object, either in primitives
                (booleans, ints, floats, strings), arrays, or dictionaries.
                If obj is None, then the returned dictionary should also be
                None.  If obj is not the correct type, it is also reasonable
                to return None.
        """
        reservation: Reservation = obj

        obj_dict: Dict[str, Any] = {
            "id": reservation.get_reservation_id(),
            "lifetime_in_seconds": reservation.get_lifetime_in_seconds(),
            "expiration_time_in_seconds": reservation.get_expiration_time_in_seconds()
        }

        return obj_dict

    def from_dict(self, obj_dict: Dict[str, Any]) -> Reservation:
        """
        :param obj_dict: The data-only dictionary to be converted into an object
        :return: An object instance created from the given dictionary.
                If obj_dict is None, the returned object should also be None.
                If obj_dict is not the correct type, it is also reasonable
                to return None.
        """
        reservation = AgentReservation(obj_dict.get("lifetime_in_seconds"))
        reservation.id = obj_dict.get("id")
        if reservation.id is None:
            reservation.id = obj_dict.get("reservation_id")
        reservation.expiration_time_in_seconds = obj_dict.get("expiration_time_in_seconds")

        return reservation
