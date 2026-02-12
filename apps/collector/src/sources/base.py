"""Abstract base for source crawlers."""
from abc import ABC, abstractmethod
from typing import Any


class AbstractSource(ABC):
    """Base class for regulator/source crawlers."""

    slug: str = ""
    name: str = ""
    base_url: str = ""
    jurisdiction: list[str] = []

    @abstractmethod
    async def fetch(self) -> list[dict[str, Any]]:
        """Fetch new items from source. Returns list of raw item dicts."""
        ...
