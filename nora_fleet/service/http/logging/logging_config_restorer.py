
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict

from os import environ

from nora_common.persistence.interface.restorer import Restorer
from nora_common.persistence.easy.easy_hocon_persistence import EasyHoconPersistence
from nora_common.persistence.easy.easy_json_persistence import EasyJsonPersistence
from nora_common.persistence.easy.easy_yaml_persistence import EasyYamlPersistence

from nora_fleet import DEPLOY_DIR
from nora_fleet.internals.persistence.hocon_parse_lock import HoconParseLock


class LoggingConfigRestorer(Restorer):
    """
    Restorer for logging configuration.
    Allows for JSON or HOCON files as standard python logging configuration.
    """

    def __init__(self, default_file_reference: str = None):
        """
        :param default_file_reference: The file reference to use when restoring.
                Default is None, implying the file reference comes from an environment variable.
        """
        super().__init__()
        self.default_file_reference: str = default_file_reference
        if self.default_file_reference is None:
            self.default_file_reference = environ.get("AGENT_SERVICE_LOG_JSON",
                                                      DEPLOY_DIR.get_file_in_basis("logging.hocon"))

    def restore(self, file_reference: str = None) -> Dict[str, Any]:
        """
        :param file_reference: The file reference to use when restoring.
                Default is None, implying the file reference is up to the
                implementation.
        :return: an object from some persisted store
        """
        use_file_reference: str = file_reference

        if file_reference is None:
            use_file_reference = self.default_file_reference

        logging_config: Dict[str, Any] = {}
        if use_file_reference is None:
            raise ValueError("No logging config file specified")

        if use_file_reference.endswith(".hocon"):
            # pyhocon parsing mutates process-global pyparsing state and is not
            # thread-safe. See HoconParseLock.
            with HoconParseLock():
                logging_config = EasyHoconPersistence().restore(file_reference=use_file_reference)
        elif use_file_reference.endswith(".json"):
            logging_config = EasyJsonPersistence().restore(file_reference=use_file_reference)
        elif use_file_reference.endswith(".yaml") or use_file_reference.endswith(".yml"):
            logging_config = EasyYamlPersistence().restore(file_reference=use_file_reference)
        else:
            raise ValueError(f"Unsupported logging config file type: {use_file_reference}")

        return logging_config
