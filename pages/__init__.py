"""Auto-discover and import all page modules so PageFactory.register() calls are executed."""

import importlib
import pkgutil

__all__: list[str] = []

# Dynamically import every module in the pages/ package.
# This triggers PageFactory.register() in each page module automatically.
# No manual imports needed — just create a new page file in pages/ and it works.
for _importer, _modname, _ispkg in pkgutil.iter_modules(__path__):
    if not _modname.startswith("_"):
        importlib.import_module(f"{__name__}.{_modname}")
