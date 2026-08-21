
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from logging import Logger
from logging import getLogger
from os import environ

from nora_common.logging.sensitive_logger import SensitiveLogger
from nora_common.resolution.resolver_util import ResolverUtil

from nora_fleet.service.authorization.interfaces.authorizer import Authorizer
from nora_fleet.service.authorization.null.always_yes_authorizer import AlwaysYesAuthorizer


class AuthorizerFactory:
    """
    Factory class for getting the appropriate Authorizer instance
    """

    @staticmethod
    def create_authorizer() -> Authorizer:
        """
        Factory method for creating the appropriate Authorizer instance
        """
        authorizer: Authorizer = None

        auth_classname: str = environ.get("AGENT_AUTHORIZER")
        if auth_classname is not None and len(auth_classname) > 0:
            # Note that this will raise an exception if the class is not found
            authorizer = ResolverUtil.create_instance(auth_classname, "AGENT_AUTHORIZER env var", Authorizer)
        else:
            authorizer = AlwaysYesAuthorizer()

        # We don't leave the room unless we have what we came for
        if authorizer is None:
            raise ValueError(f"Unable to create an Authorizer instance from env var AGENT_AUTHORIZER: {auth_classname}")

        logger: Logger = getLogger(__name__)
        sensitive_logger: Logger = SensitiveLogger(logger)

        # Static analysis false-positive for Filtering Sensitive Logs
        # We specifically use the SensitiveLogger instance to log the message.
        # This allows for a hardened server to turn off logging of this information
        # by setting the env var NORA_LOG_SENSITIVE to "false", while still allowing
        # developers to see the error message.
        sensitive_logger.info("Using Authorizer: %s.%s", authorizer.__class__.__module__, authorizer.__class__.__name__)

        return authorizer
