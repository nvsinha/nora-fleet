# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Type

from nora_common.config.file_of_class import FileOfClass
from nora_common.resolution.deprecation_redirect import DeprecationRedirect

# Normally we don't use __init__.py files to define anything,
# but here we define some constants that point to important directories in the distribution.
TOP_LEVEL_DIR = FileOfClass(__file__)
DEPLOY_DIR = FileOfClass(__file__, path_to_basis="./deploy")
REGISTRIES_DIR = FileOfClass(__file__, path_to_basis="./registries")


_DEPRECATION_REDIRECT = DeprecationRedirect(
    __name__,
    # A map from old class name to new class name for compatibility
    {
        "nora_fleet.internals.authorization.interfaces.abstract_authorizer.AbstractAuthorizer":
            "nora_fleet.service.authorization.interfaces.abstract_authorizer.AbstractAuthorizer",
        "nora_fleet.internals.authorization.interfaces.authorizer.Authorizer":
            "nora_fleet.service.authorization.interfaces.authorizer.Authorizer",
        "nora_fleet.internals.authorization.null.always_no_authorizer.AlwaysNoAuthorizer":
            "nora_fleet.service.authorization.null.always_no_authorizer.AlwaysNoAuthorizer",
        "nora_fleet.internals.authorization.null.always_yes_authorizer.AlwaysYesAuthorizer":
            "nora_fleet.service.authorization.null.always_yes_authorizer.AlwaysYesAuthorizer",
        "nora_fleet.internals.authorization.openfga.open_fga_authorizer.OpenFgaAuthorizer":
            "nora_fleet.service.authorization.openfga.open_fga_authorizer.OpenFgaAuthorizer",
        "nora_fleet.internals.messages.chat_message_type.ChatMessageType":
            "nora_fleet.message.types.chat_message_type.ChatMessageType",
        "nora_fleet.internals.messages.origination.Origination":
            "nora_fleet.internals.journals.origination.Origination",
        "nora_fleet.internals.parsers.structure.json_structure_parser.JsonStructureParser":
            "nora_fleet.message.parsers.structure.json_structure_parser.JsonStructureParser",
        "nora_fleet.internals.run_context.utils.external_agent_parsing.ExternalAgentParsing":
            "nora_fleet.internals.utils.external_agent_parsing.ExternalAgentParsing",
        "nora_fleet.message_processing.message_processor.MessageProcessor":
            "nora_fleet.message.processors.message_processor.MessageProcessor",
        "nora_fleet.message_processing.basic_message_processor.BasicMessageProcessor":
            "nora_fleet.message.processors.basic_message_processor.BasicMessageProcessor",
    },
    next_version="0.7.0"
)


def __getattr__(old_class: str) -> Type[Any]:
    """
    Redirect deprecated classes
    :param old_class: The old class name
    :return: The redirected class
    """
    return _DEPRECATION_REDIRECT.redirect_class(old_class)
