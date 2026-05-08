"""
Inpui Compatibility Shim.

This module implements a Python MetaPathFinder that intercepts all imports of
the 'homeassistant' package and transparently redirects them to the 'inpui'
package. This ensures:

1. The internal codebase (which still has residual `from homeassistant import ...`
   statements) continues to work without a full find-and-replace sweep.
2. Third-party custom components, HACS integrations, and Add-ons that hardcode
   `from homeassistant.core import HomeAssistant` continue to work seamlessly.

This shim must be installed into sys.meta_path before any other imports occur.
"""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import sys
import types

_LEGACY_NAMESPACE = "homeassistant"
_NEW_NAMESPACE = "inpui"


class InpuiCompatShim(importlib.abc.MetaPathFinder):
    """Intercepts 'homeassistant.*' imports and redirects to 'inpui.*'."""

    def find_spec(
        self,
        fullname: str,
        path: object,
        target: types.ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        """Intercept homeassistant import requests and redirect to inpui."""
        # Only intercept 'homeassistant' or 'homeassistant.*'
        if fullname != _LEGACY_NAMESPACE and not fullname.startswith(
            _LEGACY_NAMESPACE + "."
        ):
            return None

        # Translate the requested name to the new namespace
        new_name = _NEW_NAMESPACE + fullname[len(_LEGACY_NAMESPACE):]

        # Avoid infinite recursion: if we already have it in sys.modules, reuse it
        if new_name in sys.modules:
            # Register the alias so future lookups are instant
            sys.modules[fullname] = sys.modules[new_name]
            return sys.modules[new_name].__spec__

        # Remove ourselves temporarily to avoid recursive interception
        sys.meta_path.remove(self)
        try:
            # Import the real inpui module
            real_module = importlib.import_module(new_name)
        except ImportError:
            return None
        finally:
            # Always re-insert ourselves at position 0
            sys.meta_path.insert(0, self)

        # Register the module under both names
        sys.modules[fullname] = real_module
        return real_module.__spec__


def install() -> None:
    """Install the compatibility shim into the Python import system.

    This must be called as early as possible — before any other imports.
    Calling it multiple times is safe (idempotent).
    """
    for finder in sys.meta_path:
        if isinstance(finder, InpuiCompatShim):
            return  # Already installed

    sys.meta_path.insert(0, InpuiCompatShim())

    # Pre-seed the top-level alias so `import homeassistant` resolves instantly
    import inpui  # noqa: PLC0415
    sys.modules[_LEGACY_NAMESPACE] = inpui
