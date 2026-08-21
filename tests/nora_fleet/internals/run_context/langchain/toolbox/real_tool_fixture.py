
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Real (unmocked) langchain tool classes resolved by toolbox factory tests
through the same class paths an operator's toolbox info file would use.
"""

from typing import Any
from typing import Optional

from langchain_core.tools.base import BaseTool
from pydantic import BaseModel


class RealApiWrapper(BaseModel):
    """A real nested-arg class, standing in for an integration's API wrapper."""

    timeout: int = 10


class RealTool(BaseTool):
    """A real BaseTool subclass, standing in for an integration's tool class."""

    name: str = "real_tool"
    description: str = "A tool used to test unmocked toolbox instantiation."
    api_wrapper: Optional[RealApiWrapper] = None
    max_results: int = 5

    def _run(self, *args: Any, **kwargs: Any) -> str:
        """Minimal synchronous execution to satisfy BaseTool's interface."""
        return "ran"
