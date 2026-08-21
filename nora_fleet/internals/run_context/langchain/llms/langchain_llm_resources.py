
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
from __future__ import annotations

from typing import List

from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.runnables.base import RunnableSerializable

from nora_fleet.internals.interfaces.lingering_resource import LingeringResource
from nora_fleet.internals.run_context.langchain.llms.llm_policy import LlmPolicy


class LangChainLlmResources(LingeringResource):
    """
    LingeringResource implemenation representing a LangChain model paired
    together with run-time policy necessary for model usage by the service.
    """

    def __init__(self, model: BaseLanguageModel, llm_policy: LlmPolicy = None):
        """
        Constructor.
        :param model: Language model used.
        :param llm_policy: optional LlmPolicy object to manage connections to LLM host.
        """
        self.model: BaseLanguageModel = model
        self.llm_policy: LlmPolicy = llm_policy
        self.child_resources: List[LingeringResource] = []

    def get_model(self) -> RunnableSerializable:
        """
        :return: Effectively this is the BaseLanguageModel to use.
                 Most of the time this is the model that was passed into the constructor,
                 however if add_fallback_resources() is employed, this can become a
                 a composite RunnableWithFallbacks.  The common ancestor of both
                 BaseLanguageModel and RunnableWithFallbacks is RunnableSerializable.
        """
        return self.model

    def get_llm_policy(self) -> LlmPolicy:
        """
        :return: the LlmPolicy used by the model
        """
        return self.llm_policy

    def add_fallback_resources(self, llm_resources: List[LangChainLlmResources]):
        """
        Add a child resource to this one.
        :param llm_resources: a list of child LlmResources to use as fallbacks (in order)
        """
        if llm_resources is None or not isinstance(llm_resources, list):
            return

        if len(llm_resources) == 0:
            return

        # Add the child resources we need to clean up
        self.child_resources.extend(llm_resources)
        # Add the fallback models
        if self.model:
            fallback_models: List[BaseLanguageModel] = []
            for one_resource in llm_resources:
                fallback_models.append(one_resource.get_model())
            self.model = self.model.with_fallbacks(fallback_models)

    async def close_of_work(self, parent_resource: LingeringResource = None):
        """
        Release resources owned by this context when the work is all done.
        This can happen later than when the request is complete.

        :param parent_resource: parent resource, if any
        """
        # Note we are not changing the LlmPolicy interface to be LingeringResource at the moment.
        # This is something that could be extended external to nora-fleet for someone's pet LLM,
        # so we are not going there to preserve backwards compatibility.
        if self.llm_policy is not None:
            await self.llm_policy.delete_resources()

        # Close any child resources
        for child_resource in self.child_resources:
            await child_resource.close_of_work(self)
