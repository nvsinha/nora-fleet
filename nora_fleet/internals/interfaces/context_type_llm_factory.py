
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Any
from typing import Dict


class ContextTypeLlmFactory:
    """
    Interface for Factory classes creating LLM BaseLanguageModels

    Most methods take a config dictionary which consists of the following keys:

        "model_name"                The name of the model.
                                    Default if not specified is "gpt-3.5-turbo"

        "temperature"               A float "temperature" value with which to
                                    initialize the chat model.  In general,
                                    higher temperatures yield more random results.
                                    Default if not specified is the provider's default.

        "prompt_token_fraction"     The fraction of total tokens (not necessarily words
                                    or letters) to use for a prompt. Each model_name
                                    has a documented number of max_tokens it can handle
                                    which is a total count of message + response tokens
                                    which goes into the calculation involved in
                                    get_max_prompt_tokens().
                                    By default the value is 0.5.

        "max_tokens"                The maximum number of tokens to use in
                                    get_max_prompt_tokens(). By default this comes from
                                    the model description in this class.
    """

    def load(self):
        """
        Goes through the process of loading any user extensions and/or configuration
        files
        """
        raise NotImplementedError

    def create_llm(self, config: Dict[str, Any], sly_data: Dict[str, Any] = None) -> Any:
        """
        Create an llm instance BaseLanguageModel from the fully-specified llm config.
        :param config: The fully specified llm config from which the LLM instance
                    should be created.
        :param sly_data: A user-provided dictionary of private data,
                from which we might extract API keys to use for user billing.
                Can be None indicating no API keys are provided at all and the system defaults will be used.
        :return: An llm instance native to the context type.
                Can raise a ValueError if the config's class or model_name value is
                unknown to this method.
                Can return None if required llm_config keys are not provided.
        """
        raise NotImplementedError

    def create_llm_with_fallbacks(self, config: Dict[str, Any],
                                  sly_data: Dict[str, Any] = None,
                                  num_fallbacks: int = None) -> Any:
        """
        :param config: A dictionary which describes which LLM to use, perhaps with fallbacks specified.
        :param sly_data: A user-provided dictionary of private data,
                from which we might extract API keys to use for user billing.
                Can be None indicating no API keys are provided at all and the system defaults will be used.
        :param num_fallbacks: The number of fallbacks to try. Default value of None implies all.
        :return: An LLM instance native to the context type that deals with fallback specifications.
        """
        raise NotImplementedError
