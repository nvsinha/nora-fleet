
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict
from typing import List

from logging import getLogger
from logging import Logger

from nora_common.resolution.resolver import Resolver

from nora_fleet.service.authorization.interfaces.authorizer import Authorizer


class AbstractAuthorizer(Authorizer):
    """
    Partial Authorizer implementation that allows for late-binding via a resolver.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.resolver: Resolver = Resolver()
        self.logger: Logger = getLogger(self.__class__.__name__)

    async def __aenter__(self) -> Authorizer:
        """
        Opens a scoped session with this Authorizer.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Closes a scoped session with this Authorizer.
        :return: True to suppress exception. False or None to propagate exception.
        """
        # Do nothing

    async def authorize(self, actor: Dict[str, Any], action: str, resource: Dict[str, Any]) -> bool:
        """
        :param actor: The actor dictionary with the keys "type" and "id" identifying what
                      is seeking permission.  Most often this is of the form:
                        {
                            "type": "User",
                            "id": "<username>"
                        }
        :param action:  The action for which the user is asking permission for.
                        Most often this is one of the Permission values of:
                            "create", "read", "update" or "delete".
        :param resource: The resource dictionary with the keys "type" and "id" identifying
                      just what is to be authorized for use.  For instance:
                        {
                            "type": "AgentNetwork",
                            "id": "hello_world"
                        }
        :return: True if the actor is allowed to take the requested action on the resource.
                 False otherwise.
        """
        raise NotImplementedError

    async def grant(self, actor: Dict[str, Any], relation: str, resource: Dict[str, Any]) -> bool:
        """
        :param actor: The actor dictionary with the keys "type" and "id" identifying what
                      will be permitted.  Most often this is of the form:
                        {
                            "type": "User",
                            "id": "<username>"
                        }
        :param relation: The relation for which the user will be permitted.
                     Most often this is one of the strings from the Role enum.

        :param resource: The resource dictionary with the keys "type" and "id" identifying
                      just what is to be authorized for use.  For instance:
                        {
                            "type": "AgentNetwork",
                            "id": "hello_world"
                        }
        :return: True if the grant succeeded, False if the grant already existed.
        """
        # Having this interface is more for completeness than fulfilling Nora Fleet server functionality
        return False

    async def revoke(self, actor: Dict[str, Any], relation: str, resource: Dict[str, Any]) -> bool:
        """
        :param actor: The actor dictionary with the keys "type" and "id" identifying what
                      will no longer be permitted.  Most often this is of the form:
                        {
                            "type": "User",
                            "id": "<username>"
                        }
        :param relation: The relation for which the user will no longer be permitted.
                     Most often this is one of the strings from the Role enum.

        :param resource: The resource dictionary with the keys "type" and "id" identifying
                      just what is to be no longer authorized for use.  For instance:
                        {
                            "type": "AgentNetwork",
                            "id": "hello_world"
                        }
        :return: True if the revoke succeeded, False if the revoke already existed.
        """
        # Having this interface is more for completeness than fulfilling Nora Fleet server functionality
        return False

    async def list(self, actor: Dict[str, Any], relation: str, resource: Dict[str, Any]) -> List[str]:
        """
        Return a list of resource ids that the actor has the given relation to,
        as per the graph specified by the authorization model.

        :param actor: The actor dictionary with the keys "type" and "id" identifying what
                      entity's relation should be checked.  Most often this is of the form:
                        {
                            "type": "User",
                            "id": "<username>"
                        }
        :param relation: The relation for which the user's permissions will be checked.
                        Most often this is one of the Permission values of:
                            "create", "read", "update" or "delete".

        :param resource: The resource dictionary with the keys "type" and "id" identifying
                      just what is to be authorized for use.  For instance:
                        {
                            "type": "AgentNetwork",
                            # Note: "id" is not specified. We want a list of these returned.
                        }
        :return: A list of resource ids that the actor has the given relation with.
                 An empty return list implies that the actor has access to no objects
                 of the given resource type.
        """
        raise NotImplementedError

    async def query(self, actor: Dict[str, Any], relation: str, resource: Dict[str, Any]) -> List[str]:
        """
        Instead of a boolean answer from authorize() above, this method gives a list
        of resources of the given resource type (in the dict) that the actor has the
        *direct* given relation to.  This does not take authorization policy graphs
        into account.

        :param actor: The actor dictionary with the keys "type" and "id" identifying what
                      will be permitted.  Most often this is of the form:
                        {
                            "type": "User",
                            "id": "<username>"
                        }
        :param relation: The relation for which the user will be permitted.
                     Most often this is one of the strings from the Role enum.

        :param resource: The resource dictionary with the keys "type" and "id" identifying
                      just what is to be authorized for use.  For instance:
                        {
                            "type": "AgentNetwork",
                            "id": "hello_world"
                        }
        :return: A list of relations (which can be None or empty) that the actor
                has the given relation with.
        """
        # Return None indicating some other mechanism should be used
        # Having this interface is more for completeness than fulfilling Nora Fleet server functionality
        return None
