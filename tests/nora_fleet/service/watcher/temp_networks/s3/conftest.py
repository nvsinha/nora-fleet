
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Scoped conftest for the S3ReservationsStorage tests.

The project-wide tests/conftest.py declares an autouse fixture
`configure_llm_provider_keys` that skips any test missing an
OPENAI_API_KEY (or other provider key, depending on markers). Tests in
this directory exercise S3ReservationsStorage with a fully mocked S3
client and do not call any LLM provider, so the project-wide skip
condition does not apply. This conftest overrides that fixture with a
no-op for tests in this subtree only.
"""
import pytest


# pylint: disable=unused-argument
@pytest.fixture(autouse=True)
def configure_llm_provider_keys(request, monkeypatch):
    """
    Override of the project-wide configure_llm_provider_keys fixture.
    Reservation-storage tests never call an LLM and therefore should not
    be skipped when no provider key is set.
    """
    return None
