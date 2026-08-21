
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from nora_fleet.internals.journals.origination import Origination


class ToolArgumentReporting:
    """
    Utility class to assist in preparing arguments dictionaries when reporing starting a tool.
    """

    # List of keys for policy objects that cannot be serialized in a message.
    # The first two are set in AbstractClassActivation.
    # The last one is injected by Langgraph when using MCP tools with langchain-mcp-adapters>=0.1.14.
    POLICY_OBJECT_KEYS: List[str] = ["reservationist", "progress_reporter", "runtime"]

    @staticmethod
    def prepare_tool_start_dict(tool_args: Dict[str, Any],
                                origin: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Common code to prepare a tool start dictionary.

        :param tool_args: The arguments that will be passed to the tool
        :param origin: A List of origin dictionaries indicating the origin of the run.
        :return: A dictionary for a future journal entry
        """

        modified_tool_args: Dict[str, Any] = tool_args.copy()

        # Combine the original tool tool_args with origin metadata, if available.
        if origin is not None:
            modified_tool_args["origin"] = origin

            full_name: str = Origination.get_full_name_from_origin(origin)
            modified_tool_args["origin_str"] = full_name

        # Remove policy object keys from the args that cannot be serialized in a message.
        for key in ToolArgumentReporting.POLICY_OBJECT_KEYS:
            if key in modified_tool_args:
                del modified_tool_args[key]

        # Create a dictionary for a future journal entry for this invocation
        tool_start_dict: Dict[str, Any] = {
            "tool_start": True,
            "tool_args": modified_tool_args
        }

        return tool_start_dict
