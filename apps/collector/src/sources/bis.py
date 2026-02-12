"""BIS/BCBS crawler — TODO."""
from src.sources.base import AbstractSource


class BISSource(AbstractSource):
    slug = "bis"
    name = "Bank for International Settlements"
    base_url = "https://www.bis.org"
    jurisdiction = ["GLOBAL"]

    async def fetch(self) -> list[dict]:
        return []
