"""Scheduled crawl tasks — per-source frequency."""
# TODO: @celery_app.task def crawl_source(slug): ...
def crawl_source(slug: str) -> None:
    """Crawl a single source by slug."""
    pass
