"""EBA (European Banking Authority) crawler."""
from src.sources.base import AbstractSource


class EBASource(AbstractSource):
    """EBA crawler — TODO implement fetch()."""

    slug = "eba"
    name = "European Banking Authority"
    base_url = "https://www.eba.europa.eu"
    jurisdiction = ["EU"]

    async def fetch(self) -> list[dict]:
        """Fetch EBA updates."""
        return []
