from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rss_news import parse_rss, translate_to_ru

BASE_DIR = Path(__file__).resolve().parent
FEED_URL = os.getenv("RSS_FEED_URL", "https://www.wired.com/feed/tag/ai/latest/rss")
CACHE_SECONDS = 15 * 60
RETRY_SECONDS = 10 * 60
MAX_ITEMS = 10

logger = logging.getLogger("rss_ai")
app = FastAPI(title="AI News", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

_cache_lock = Lock()
_cached_items: list[dict[str, str]] = []
_cached_at = 0.0
_cached_updated_at: str | None = None


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "web" / "index.html")


@app.get("/app", include_in_schema=False)
@app.get("/app/", include_in_schema=False)
def demo() -> FileResponse:
    """Страница приложения по /app/: в корне домена Caddy отдаёт лендинг."""
    return FileResponse(BASE_DIR / "web" / "index.html")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


def translation_available(items: list[dict[str, str]]) -> bool:
    """Лента считается переведённой, только если переведены все её элементы."""
    return bool(items) and all(item.get("translated", True) for item in items)


def _get_cached_items() -> tuple[list[dict[str, str]], str | None]:
    global _cached_items, _cached_at, _cached_updated_at

    with _cache_lock:
        now = time.monotonic()
        # лента без перевода кешируется короче: провайдер может восстановиться раньше
        ttl = CACHE_SECONDS if translation_available(_cached_items) else RETRY_SECONDS
        if now - _cached_at < ttl:
            return _cached_items, _cached_updated_at

        items = parse_rss(FEED_URL, MAX_ITEMS)
        if not items:
            raise HTTPException(
                status_code=502,
                detail="Источник вернул пустую ленту. Попробуйте позже.",
            )

        _cached_items = translate_to_ru(items)
        _cached_at = now
        _cached_updated_at = datetime.now(timezone.utc).isoformat()
        return _cached_items, _cached_updated_at


@app.get("/api/news", tags=["news"])
def news(limit: Annotated[int, Query(ge=1, le=MAX_ITEMS)] = 5) -> dict:
    try:
        items, updated_at = _get_cached_items()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to fetch RSS news")
        raise HTTPException(
            status_code=502,
            detail="Лента сейчас недоступна. Попробуйте позже.",
        ) from exc

    selected = items[:limit]
    return {
        "items": selected,
        "updated_at": updated_at,
        "translation_available": translation_available(selected),
    }
