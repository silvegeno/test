"""Парсинг RSS с переводом на русский.

Перевод не должен валить ленту: если провайдер недоступен или исчерпал бесплатную квоту,
элементы отдаются с оригинальным текстом и пометкой translated = False, а вызывающий код
показывает предупреждение. Готовые переводы кешируются на диск, чтобы перезапуск контейнера
не расходовал квоту заново.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import feedparser

logger = logging.getLogger("rss_ai.translate")

DEFAULT_CACHE_PATH = Path(os.getenv("TRANSLATION_CACHE_PATH", "data/translation-cache.json"))
SOURCE_LANG = "en"
TARGET_LANG = "ru"
NOT_STATED = "Не указана"


def parse_rss(rss_source: str, limit: int = 5) -> list[dict[str, str]]:
    """Первые limit элементов ленты в виде словарей."""
    news_list = []
    feed = feedparser.parse(rss_source, agent="Mozilla/5.0")
    for entry in feed.entries[:limit]:
        news_list.append(
            {
                "published": entry.get("published", NOT_STATED),
                "title": entry.get("title", NOT_STATED),
                "link": entry.get("link", NOT_STATED),
                "description": entry.get("description", NOT_STATED),
            }
        )
    return news_list


def provider_name() -> str:
    return (os.getenv("TRANSLATE_SERVICE") or "mymemory").strip() or "mymemory"


def _load_cache(path: Path) -> dict[str, str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError):
        logger.warning("Кеш переводов не читается, начинаю с пустого")
        return {}
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value) for key, value in raw.items()}


def _save_cache(path: Path, cache: dict[str, str]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")
        temporary.replace(path)
    except OSError as error:
        logger.warning("Кеш переводов не сохранить: %s", error)


def _translate_text(text: str) -> str:
    """Один вызов провайдера. Отдельная функция, чтобы её можно было подменить в тестах."""
    from translate import Translator

    return Translator(from_lang=SOURCE_LANG, to_lang=TARGET_LANG, service=provider_name()).translate(text)


def translate_to_ru(
    items: list[dict[str, str]],
    cache_path: Path | None = None,
    translator=None,
) -> list[dict[str, str]]:
    """Переводит title и description. При отказе провайдера оставляет оригинал.

    После первой ошибки перебор прекращается: если провайдер ответил 429, остальные вызовы
    только расходуют лимит и время ответа.
    """
    path = Path(cache_path) if cache_path else DEFAULT_CACHE_PATH
    cache = _load_cache(path)
    translate_one = translator or _translate_text
    state = {"stopped": False}
    added = 0

    def ensure(text: str) -> tuple[str, bool]:
        nonlocal added
        if not text or text == NOT_STATED:
            return text, True
        if text in cache:
            return cache[text], True
        if state["stopped"]:
            return text, False
        try:
            translated = translate_one(text)
        except Exception as error:  # провайдер недоступен, квота, таймаут — лента важнее
            state["stopped"] = True
            logger.warning("Перевод недоступен (%s): %s", type(error).__name__, error)
            return text, False
        if not translated:
            state["stopped"] = True
            return text, False
        cache[text] = translated
        added += 1
        return translated, True

    for item in items:
        title, title_ok = ensure(item.get("title") or "")
        description, description_ok = ensure(item.get("description") or "")
        item["title"] = title
        item["description"] = description
        item["translated"] = bool(title_ok and description_ok)

    if added:
        _save_cache(path, cache)
    if any(not item["translated"] for item in items):
        logger.warning("Часть ленты отдана без перевода: провайдер %s недоступен", provider_name())
    return items


def print_rss(news_list: list[dict[str, str]]) -> None:
    for value in news_list:
        print(value["published"])
        print(value["title"])
        print(value["link"])
        print(value["description"])
        print("-" * 80)


if __name__ == "__main__":
    source = os.getenv("RSS_FEED_URL", "https://www.wired.com/feed/tag/ai/latest/rss")
    print_rss(translate_to_ru(parse_rss(source, 10)))
