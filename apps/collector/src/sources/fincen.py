"""FinCEN (US) crawler — TODO."""
from src.sources.base import AbstractSource


class FinCENSource(AbstractSource):
    slug = "fincen"
    name = "Financial Crimes Enforcement Network"
    base_url = "https://www.fincen.gov"
    jurisdiction = ["US"]

    async def fetch(self) -> list[dict]:
        return []
