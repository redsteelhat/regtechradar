"""Regulatory source crawlers — registry loader + AbstractSource implementations."""
from src.sources.base import AbstractSource
from src.sources.registry import load_registry
from src.sources.eba import EBASource
from src.sources.esma import ESMASource
from src.sources.fatf import FATFSource
from src.sources.ecb import ECBSource
from src.sources.fca import FCASource
from src.sources.fincen import FinCENSource
from src.sources.bis import BISSource
from src.sources.eu_official import EuOfficialSource

# Registry slug → concrete source class (for factory)
SLUG_TO_CLASS: dict[str, type[AbstractSource]] = {
    "eba": EBASource,
    "esma": ESMASource,
    "fatf": FATFSource,
    "ecb": ECBSource,
    "fca": FCASource,
    "fincen": FinCENSource,
    "bis": BISSource,
    "eurlex": EuOfficialSource,
}


def get_sources(configs: list[dict] | None = None) -> list[AbstractSource]:
    """
    Build AbstractSource instances from registry (or given configs).

    Args:
        configs: If None, loads from registry via load_registry().

    Returns:
        List of source instances (only slugs present in SLUG_TO_CLASS).
    """
    if configs is None:
        configs = load_registry()
    sources: list[AbstractSource] = []
    for c in configs:
        slug = c.get("slug")
        if slug and slug in SLUG_TO_CLASS:
            sources.append(SLUG_TO_CLASS[slug].from_registry(c))
    return sources


__all__ = [
    "AbstractSource",
    "load_registry",
    "get_sources",
    "SLUG_TO_CLASS",
    "EBASource",
    "ESMASource",
    "FATFSource",
    "ECBSource",
    "FCASource",
    "FinCENSource",
    "BISSource",
    "EuOfficialSource",
]
