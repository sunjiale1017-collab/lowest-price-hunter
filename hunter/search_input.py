"""Safe exact-model override for approved, config-defined merchant search pages.

This does not discover arbitrary products from natural language; a model or SKU is required.
"""
import re
from urllib.parse import quote

_MODEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{1,59}\Z", re.ASCII)


def with_model(config: dict, model: str | None) -> dict:
    """Return a copy whose search page URLs target the requested exact model.

    Never repurpose fixed product URLs for another model: doing so could produce
    false product matches. Search URLs must be predefined by the operator.
    """
    if model is None:
        return config
    if not _MODEL.fullmatch(model):
        raise ValueError("--model must be 2-60 ASCII letters/digits with optional . _ -; supply an exact SKU/model")
    sources = config.get('sources', [])
    if not sources or any('{query}' not in s.get('search_url', '') for s in sources):
        raise ValueError("--model requires sources with search_url={query}; use --config config/europe.json")
    safe_sources = []
    for source in sources:
        source = dict(source)
        source['url'] = source['search_url'].replace('{query}', quote(model, safe=''))
        safe_sources.append(source)
    return {**config, 'model': model, 'sources': safe_sources, 'research_sources': []}
