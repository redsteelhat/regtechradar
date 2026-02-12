"""Celery configuration — broker Redis, beat schedule."""
# from celery import Celery
# app = Celery("regtech", broker=settings.redis_url, include=["src.tasks.crawl", "src.tasks.process", "src.tasks.notify"])
# app.conf.beat_schedule = { ... }
# TODO: wire settings.redis_url
app = None
