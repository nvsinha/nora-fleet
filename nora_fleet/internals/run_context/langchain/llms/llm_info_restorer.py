
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet import TOP_LEVEL_DIR
from nora_fleet.internals.persistence.abstract_async_config_restorer import AbstractAsyncConfigRestorer


class LlmInfoRestorer(AbstractAsyncConfigRestorer):
    """
    Implementation of the AbstractAsyncConfigRestorer interface to read in an LlmInfo dictionary
    instance given a hocon file name.
    The restore() and async_restore() methods both return dictionary instances.
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__(file_purpose="llm_info")

    def get_file_path(self, file_reference: str = None) -> str:
        """
        :param file_reference: The file reference to use when restoring.
                Default is None, implying the file reference is up to the
                implementation.
        :return: a string representing the file path to use
        """
        use_file: str = file_reference

        if file_reference is None or len(file_reference) == 0:
            # Read from the default
            use_file = TOP_LEVEL_DIR.get_file_in_basis("internals/run_context/langchain/llms/default_llm_info.hocon")

        return use_file
