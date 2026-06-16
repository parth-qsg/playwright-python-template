"""Path helpers and environment-detection utilities."""

from __future__ import annotations

import os
from pathlib import Path


def get_project_root() -> Path:
    """Return the repository root — the directory that contains pyproject.toml."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return here.parent


def ensure_dir(path: str | Path) -> Path:
    """Create *path* (and parents) if it does not exist; return a ``Path``."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def is_running_in_docker() -> bool:
    """Return ``True`` when the process is running inside a Docker container."""
    if Path("/.dockerenv").exists():
        return True
    cgroup = Path("/proc/1/cgroup")
    return cgroup.exists() and "docker" in cgroup.read_text()


def resolve_path(relative: str) -> Path:
    """Resolve a *relative* path from the project root."""
    return get_project_root() / relative
