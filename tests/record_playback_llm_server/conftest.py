
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Local pytest configuration for the record/playback proxy tests.
"""
import pytest


@pytest.fixture(autouse=True)
def configure_llm_provider_keys():
    """
    Override the repo-wide autouse fixture of the same name (tests/conftest.py),
    which skips tests when no LLM provider API key is present. These proxy tests
    drive a local in-process fake upstream and never contact a real LLM, so no
    provider key is required.
    """
    yield
