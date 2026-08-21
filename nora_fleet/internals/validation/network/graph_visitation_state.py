
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from enum import Enum


class GraphVisitationState(Enum):
    """
    Enum representing the state of a node in a graph traversal.
    """

    UNVISITED: int = 0
    CURRENTLY_BEING_PROCESSED: int = 1
    FULLY_PROCESSED: int = 2
