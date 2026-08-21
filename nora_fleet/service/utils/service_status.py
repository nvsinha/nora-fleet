
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

class ServiceStatus:
    """
    Class for registering and reporting overall status of the service,
    primarily for interaction with external deployment environment.
    """

    def __init__(self, service_name: str):
        """
        Constructor.
        """
        self.service_name: str = service_name
        self.service_requested: bool = True
        self.service_ready: bool = False

    def set_status(self, status: bool):
        """
        Set the status of a service
        """
        self.service_ready = status

    def is_ready(self) -> bool:
        """
        True if service is ready
        """
        return self.service_ready

    def set_requested(self, requested: bool):
        """
        Set if a service is requested by nora-fleet server.
        """
        self.service_requested = requested

    def is_requested(self) -> bool:
        """
        True if service is requested.
        """
        return self.service_requested

    def get_service_name(self) -> str:
        """
        Return service name
        """
        return self.service_name
