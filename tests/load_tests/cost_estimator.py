# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

"""Estimate USD cost from LLM token counts and model pricing tables.

Uses per-model pricing for known OpenAI models and falls back to a
conservative default for unrecognized model strings.  Pricing is
matched by substring so dated model names (e.g. gpt-5.2-2025-12-11)
resolve to their base model entry.
"""

from tests.load_tests.config import DEFAULT_PRICING
from tests.load_tests.config import MODEL_PRICING
from tests.load_tests.config import TOKENS_PER_MILLION


class CostEstimator:
    """Estimate USD cost from token counts and model pricing."""

    @staticmethod
    def estimate(prompt_tokens, completion_tokens, model="unknown") -> float:
        """Estimate USD cost from token counts and model name.

        Looks up per-model pricing by substring match, then computes
        cost as (tokens / 1M) * rate for prompt and completion
        separately.
        """
        pricing = DEFAULT_PRICING
        for key in sorted(MODEL_PRICING, key=len, reverse=True):
            if key in model:
                pricing = MODEL_PRICING[key]
                break
        prompt_cost = (
            (prompt_tokens / TOKENS_PER_MILLION)
            * pricing.get("prompt", 0)
        )
        completion_cost = (
            (completion_tokens / TOKENS_PER_MILLION)
            * pricing.get("completion", 0)
        )
        return prompt_cost + completion_cost
