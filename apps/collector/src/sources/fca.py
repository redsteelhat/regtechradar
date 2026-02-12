"""FCA (UK) crawler — TODO."""
from src.sources.base import AbstractSource


class FCASource(AbstractSource):
    slug = "fca"
    name = "Financial Conduct Authority"
    base_url = "https://www.fca.org.uk"
    jurisdiction = ["UK"]

    async def fetch(self) -> list[dict]:
        return []
