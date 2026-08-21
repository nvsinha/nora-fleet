
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT
"""
Canary module deliberately OUTSIDE any AGENT_TOOL_PATH used in tests.

Resolution tests reference it fully-qualified two ways:
- default mode resolves it (proving Phase 1 imports from anywhere on PYTHONPATH);
- strict mode must NOT import it (importing executes top-level code, which is
  the vulnerability the flag closes), asserted via absence from sys.modules.

Nothing else may import this module, or the strict test's never-imported
assertion loses its meaning.
"""


class CanaryTool:
    """A fixture class resolvable only by fully-qualified (Phase 1) import."""
