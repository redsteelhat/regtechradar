"""Generic RSS/Atom feed parser — TODO."""
from src.sources.base import AbstractSource


class RSSGenericSource(AbstractSource):
    """Parse RSS/Atom feeds from registry config."""
    slug = "rss_generic"
    name = "RSS/Atom Feed"
    base_url = ""
    jurisdiction = []

    async def fetch(self) -> list[dict]:
        return []
