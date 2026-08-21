
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from nora_fleet.message.parsers.structure.json_structure_parser import JsonStructureParser
from nora_fleet.message.parsers.structure.structure_parser import StructureParser


class StructureParserFactory:
    """
    Factory for creating StructureParser instances based on a string type
    """

    def create_structure_parser(self, parser_type: str) -> StructureParser:
        """
        Creates a structure parser given the string type

        :param parser_type: A string describing the format of the structure parser.
        """

        structure_parser: StructureParser = None

        if parser_type is None or not isinstance(parser_type, str):
            structure_parser = None
        elif parser_type.lower() == "json":
            structure_parser = JsonStructureParser()

        return structure_parser
