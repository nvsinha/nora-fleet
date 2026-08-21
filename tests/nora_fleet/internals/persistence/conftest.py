
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Scoped conftest for the persistence tests.

The file name "conftest.py" is mandatory: pytest discovers this file by
that exact name and applies it automatically to tests in this directory
and below. It is never imported explicitly, so renaming it would
silently disable everything in it.

The project-wide tests/conftest.py declares an autouse fixture
`configure_llm_provider_keys` that skips any test missing an
OPENAI_API_KEY (or other provider key, depending on markers). Tests in
this directory exercise config restorers and the HOCON parse lock with
local fixture files and do not call any LLM provider, so the
project-wide skip condition does not apply. This conftest overrides
that fixture with a no-op for tests in this subtree only.
"""
import pytest


# pylint: disable=unused-argument
@pytest.fixture(autouse=True)
def configure_llm_provider_keys(request, monkeypatch):
    """
    Override of the project-wide configure_llm_provider_keys fixture.
    Persistence tests never call an LLM and therefore should not be
    skipped when no provider key is set.
    """
    return None
