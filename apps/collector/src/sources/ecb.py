"""ECB crawler — TODO."""
from src.sources.base import AbstractSource


class ECBSource(AbstractSource):
    slug = "ecb"
    name = "European Central Bank"
    base_url = "https://www.ecb.europa.eu"
    jurisdiction = ["EU"]

    async def fetch(self) -> list[dict]:
        return []
