"""Load source definitions from YAML registry (regtech.md §6)."""
from pathlib import Path
from typing import Any

import yaml


def load_registry(path: Path | str | None = None) -> list[dict[str, Any]]:
    """
    Load source registry from YAML file.

    Args:
        path: Path to registry.yaml. If None, uses config.settings.registry_path
              relative to package root (apps/collector).

    Returns:
        List of source config dicts (slug, name, base_url, jurisdiction, crawl_targets, etc.).
    """
    if path is None:
        try:
            from src.config import settings
            path = settings.registry_path
        except Exception:
            path = "sources/registry.yaml"
    path = Path(path)
    if not path.is_absolute():
        # apps/collector'den çalıştığımızda cwd'ye göre
        base = Path(__file__).resolve().parents[2]  # apps/collector
        path = base / path
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("sources", [])
