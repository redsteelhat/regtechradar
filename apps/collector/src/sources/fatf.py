"""FATF crawler — TODO."""
from src.sources.base import AbstractSource


class FATFSource(AbstractSource):
    slug = "fatf"
    name = "Financial Action Task Force"
    base_url = "https://www.fatf-gafi.org"
    jurisdiction = ["GLOBAL"]

    async def fetch(self) -> list[dict]:
        return []
