
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import List


class StorageClass:
    """
    Constants for AgentNetwork storage classes
    """

    PUBLIC: str = "public"          # The default - listed in Concierge
    PROTECTED: str = "protected"    # Not listed in Concierge, but still accessible by web API

    # Reserved for temporary networks that expire
    TEMP: str = "temp"              # Not listed in Concierge, accessible by web API

    # Note: "temp" not listed here because it is so unlike everything else.
    ALL_PERMANENT: List[str] = [PUBLIC, PROTECTED]
