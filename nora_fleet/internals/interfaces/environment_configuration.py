
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from typing import Any
from typing import Dict

import os


class EnvironmentConfiguration:
    """
    Easy policy add on for the get_value_or_env() method for various classes that
    are effected by configuration via dictionary/hocon and/or environment variables.
    """

    @staticmethod
    def get_value_or_env(config: Dict[str, Any], key: str, env_key: str,
                         none_obj: Any = None) -> Any:
        """
        :param config: The config dictionary to search
        :param key: The key for the config to look for
        :param env_key: The os.environ key whose value should be gotten if either
                        the key does not exist or the value for the key is None
        :param none_obj:  An optional object instance to test.
                          If present this method will return None, implying
                          that some other external object/mechanism is supplying the values.
        """
        if none_obj is not None:
            return None

        value = None
        if config is not None:
            value = config.get(key)

        if value is None and env_key is not None:
            value = os.getenv(env_key)

        return value
