
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT


class AgentNameMapper:
    """
    An abstract policy defining conversion
    between agent name as specified in a manifest file
    and a file path (relative to registry root directory) to this agent definition file.
    """

    def agent_name_to_filepath(self, agent_name: str) -> str:
        """
        Converts an agent name from manifest file to file path to this agent definition file.
        """
        raise NotImplementedError()

    def filepath_to_agent_network_name(self, filepath: str) -> str:
        """
        Converts a file path to agent definition file (relative to registry root directory)
        to agent network name identifying it to the service.
        """
        raise NotImplementedError()
