"""ESMA crawler — TODO."""
from src.sources.base import AbstractSource


class ESMASource(AbstractSource):
    slug = "esma"
    name = "European Securities and Markets Authority"
    base_url = "https://www.esma.europa.eu"
    jurisdiction = ["EU"]

    async def fetch(self) -> list[dict]:
        return []
