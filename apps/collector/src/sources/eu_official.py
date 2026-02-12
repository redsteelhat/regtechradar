"""EUR-Lex / Official Journal crawler — TODO (custom parser)."""
from src.sources.base import AbstractSource


class EuOfficialSource(AbstractSource):
    slug = "eurlex"
    name = "EUR-Lex (Official Journal)"
    base_url = "https://eur-lex.europa.eu"
    jurisdiction = ["EU"]

    async def fetch(self) -> list[dict]:
        return []
