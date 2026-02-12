"""Abstract base for source crawlers (regtech.md §6)."""
from abc import ABC, abstractmethod
from typing import Any


class AbstractSource(ABC):
    """
    Base class for regulator/source crawlers.

    Registry YAML'dan from_registry(config) ile doldurulur; fetch() alt sınıflarda implement edilir.
    """

    slug: str = ""
    name: str = ""
    base_url: str = ""
    jurisdiction: list[str] = []
    crawl_frequency: str = "6h"
    priority: int = 1
    crawl_targets: list[dict[str, Any]] = []
    content_selectors: dict[str, str] = {}

    @classmethod
    def from_registry(cls, config: dict[str, Any]) -> "AbstractSource":
        """
        Build instance from registry YAML entry.

        Args:
            config: One item from sources/registry.yaml (slug, name, base_url, jurisdiction,
                    crawl_targets, content_selectors, crawl_frequency, priority).

        Returns:
            Instance with attributes set from config.
        """
        inst = cls()
        inst.slug = config.get("slug", inst.slug)
        inst.name = config.get("name", inst.name)
        inst.base_url = config.get("base_url", inst.base_url).rstrip("/")
        inst.jurisdiction = list(config.get("jurisdiction", inst.jurisdiction))
        inst.crawl_frequency = config.get("crawl_frequency", inst.crawl_frequency)
        inst.priority = int(config.get("priority", inst.priority))
        inst.crawl_targets = list(config.get("crawl_targets", inst.crawl_targets))
        inst.content_selectors = dict(config.get("content_selectors", inst.content_selectors))
        return inst

    def full_url(self, path: str) -> str:
        """Path (e.g. /news) ile base_url birleştirir."""
        path = path.lstrip("/")
        return f"{self.base_url}/{path}" if path else self.base_url

    @abstractmethod
    async def fetch(self) -> list[dict[str, Any]]:
        """
        Fetch new items from source.

        Returns:
            List of raw item dicts: url, title, raw_html or extracted_text, published_at, etc.
        """
        ...
