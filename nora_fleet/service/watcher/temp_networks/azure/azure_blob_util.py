
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from azure.core.exceptions import AzureError


class AzureBlobUtil:
    """Utilities for Azure Blob Storage operations."""

    DEFAULT_RESERVATIONS_PREFIX: str = "reservations/"

    @staticmethod
    def is_retryable_client_error(err: AzureError) -> bool:
        """
        Determine if an AzureError is worth retrying based on error code and HTTP status.

        :param err: The AzureError exception to evaluate
        :return: True if the error is likely transient and worth retrying, False otherwise
        """
        status_code = getattr(err, 'status_code', None)
        error_code = str(getattr(err, 'error_code', '')).lower() if hasattr(err, 'error_code') else ''

        retryable_codes = {
            'serverbisy',
            'operationtimeout',
            'throttlingexception',
            'requesttimeoutexception',
            'internalerror',
            'serviceunavailable',
        }

        if error_code in retryable_codes:
            return True

        if isinstance(status_code, int) and (status_code == 408 or 500 <= status_code < 600):
            return True

        return False

    @staticmethod
    def get_error_code(err: AzureError) -> str:
        """
        Safely extract the error code from an AzureError.

        :param err: The AzureError exception
        :return: The error code as a string, or empty string if not available
        """
        if hasattr(err, 'error_code'):
            code = err.error_code
            return str(code) if code is not None else ""
        return ""
