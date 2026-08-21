
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Helpers shared by the restorer test files in this directory.
"""
from typing import Any
from typing import Dict

from pathlib import Path

from nora_fleet.internals.persistence.abstract_async_config_restorer import AbstractAsyncConfigRestorer


class ConcreteRestorer(AbstractAsyncConfigRestorer):
    """Minimal concrete subclass – inherits all behaviour from the abstract base."""


# The dictionary the valid.json and valid.hocon fixture files deserialize to.
VALID_DICT: Dict[str, Any] = {"key": "value", "nested": {"a": 1}}

# Directory containing .json and .hocon fixture files used by the tests.
FIXTURES_DIR: Path = Path(__file__).parent.parent.parent.parent / "fixtures"
