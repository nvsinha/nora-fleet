
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

import unittest
from pathlib import PurePosixPath, PureWindowsPath

from nora_fleet.internals.graph.persistence.agent_filetree_mapper import AgentFileTreeMapper
from nora_fleet.internals.graph.persistence.agent_standalone_mapper import AgentStandaloneMapper


class TestMapper(unittest.TestCase):
    """
    Tests different file mappers
    """

    def test_posix_mapping(self):
        """
        Tests mapping on POSIX platforms
        """
        mapper = AgentFileTreeMapper(PurePosixPath)

        manifest_entry = "folder/subfolder/agent_definition.hocon"
        agent_filepath = mapper.agent_name_to_filepath(manifest_entry)
        self.assertEqual(agent_filepath, r"folder/subfolder/agent_definition.hocon")

        agent_network = mapper.filepath_to_agent_network_name(agent_filepath)
        self.assertEqual(agent_network, r"folder/subfolder/agent_definition")

    def test_windows_mapping(self):
        """
        Tests mapping on Windows platforms
        """
        mapper = AgentFileTreeMapper(PureWindowsPath)

        manifest_entry = "folder/subfolder/agent_definition.hocon"
        agent_filepath = mapper.agent_name_to_filepath(manifest_entry)
        self.assertEqual(agent_filepath, r"folder\subfolder\agent_definition.hocon")

        agent_network = mapper.filepath_to_agent_network_name(agent_filepath)
        self.assertEqual(agent_network, r"folder/subfolder/agent_definition")

    def test_standalone_posix_mapping(self):
        """
        Tests mapping on POSIX platforms
        """
        mapper = AgentStandaloneMapper(PurePosixPath)

        file_entry = r"/folder/subfolder/agent_definition.hocon"
        agent_filepath = mapper.agent_name_to_filepath(file_entry)
        self.assertEqual(agent_filepath, r"/folder/subfolder/agent_definition.hocon")

        agent_network = mapper.filepath_to_agent_network_name(agent_filepath)
        self.assertEqual(agent_network, r"agent_definition")

    def test_standalone_windows_mapping(self):
        """
        Tests mapping on Windows platforms
        """
        mapper = AgentStandaloneMapper(PureWindowsPath)

        file_entry = r"C:\folder\subfolder\agent_definition.hocon"
        agent_filepath = mapper.agent_name_to_filepath(file_entry)
        self.assertEqual(agent_filepath, r"C:\folder\subfolder\agent_definition.hocon")

        agent_network = mapper.filepath_to_agent_network_name(agent_filepath)
        self.assertEqual(agent_network, r"agent_definition")
