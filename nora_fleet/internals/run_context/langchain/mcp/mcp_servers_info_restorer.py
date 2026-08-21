
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict
from typing import Optional

from nora_fleet.internals.persistence.abstract_async_config_restorer import AbstractAsyncConfigRestorer


class McpServersInfoRestorer(AbstractAsyncConfigRestorer):
    """
    Implementation of the AbstractAsyncConfigRestorer that reads the MCP servers info file.
    The restore() and async_restore() methods both return a dictionary.

    NOTE: This class is highly experimental and implementation of MCP servers
    is very likely to change in future releases.
    """

    def __init__(self):
        # If the MCP info file does not exist, use values from the network HOCON file.
        super().__init__(file_purpose="MCP servers info", env_var="MCP_SERVERS_INFO_FILE", must_exist=False)

    def filter_config(self, basis_config: Dict[str, Any], file_path: str = None) -> Optional[Dict[str, Any]]:
        """
        :param basis_config: A dictionary with MCP servers information
        :param file_path: The path to the MCP servers info file
        :return: a dictionary with MCP servers information or None if there is no config (no file, or file not found)
        """

        # Basic file checking help in here
        use_basis_config: Optional[Dict[str, Any]] = super().filter_config(basis_config, file_path)

        # If there is no config (no file, or file not found), just return None to indicate that.
        if use_basis_config is None:
            return None

        # Keys (MCP endpoint urls, quoted in HOCON source) are quote-sanitized
        # at parse time (sanitize_keys=True), so only whitespace normalization
        # is left to do here.
        result_dict: Dict[str, Any] = {}
        for key, value in use_basis_config.items():
            use_key: str = key.strip()
            result_dict[use_key] = value

        return result_dict
