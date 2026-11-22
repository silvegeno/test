# AGENTS.md — rss-ai

## Что это
Веб-приложение «AI News»: берёт RSS-ленту Wired об ИИ (по умолчанию `https://www.wired.com/feed/tag/ai/latest/rss`),
переводит заголовки и описания на русский и отдаёт страницу + JSON. Учебный демо-проект в репозитории
`silvegeno/test`, рабочая ветка `feature/rss-ai-news`.

## Стек
- Python 3.14, FastAPI + Uvicorn, feedparser 6.x, `translate` (неофициальный клиент Microsoft Translator).
- Фронтенд — чистый HTML/CSS/JS без сборки: `web/index.html`, `static/app.js`, `static/styles.css`.
- Контейнер: `python:3.14-slim`, пользователь 10001, read-only rootfs, tmpfs `/tmp` 16 МБ, `cap_drop: ALL`.
- CI (`.github/workflows/ci.yml`): unittest, py_compile, `docker build` на push в `feature/rss-ai-news` и на PR в `main`.

## Структура
```
app.py                  FastAPI: GET / (страница), /health, /api/news?limit=1..10; кэш 15 минут, общий Lock
rss_news.py             parse_rss(), translate_to_ru(), print_rss(); CLI-режим запускается напрямую
web/index.html          единственная страница интерфейса
static/app.js           fetch /api/news, рендер карточек, экранирование через textContent
static/styles.css       оформление
tests/test_rss_news.py  разбор локального сэмпла RSS, без сети
Dockerfile, docker-compose.yml, .dockerignore, .env.example
```

## Запуск
```bash
# локально, без Docker
.venv/Scripts/python.exe -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

# локально, Docker (порт 8140)
docker compose up -d --build && docker compose ps
curl -s http://127.0.0.1:8140/health
curl -s "http://127.0.0.1:8140/api/news?limit=2"

# проверки
.venv/Scripts/python.exe -m unittest discover -s . -p "test_*.py" -v
.venv/Scripts/python.exe -m py_compile rss_news.py app.py
```

## Сервер
- Каталог `/opt/my_projects/rss-ai` (ubuntu:ubuntu). Файлы кладутся tar'ом с Windows, git на сервере нет.
- `.env` на сервере: `RSS_FEED_URL`, `RSS_AI_PORT=8140`, chmod 600, секретов нет.
- Контейнер `rss-ai`: `127.0.0.1:8140 -> 8000`, `restart: unless-stopped`, healthcheck на `/health`.
- Публичный адрес `https://rss-ai.praktik-ai.ru` через Caddy + demo-gate (forward_auth на 127.0.0.1:8099).
  Аноним получает `401 «Нужен доступ»`; вход по ссылке `?k=`, которую выдаёт `gate.py grant`.
- DNS: wildcard `*.praktik-ai.ru` уже указывает на 109.66.243.108, отдельная A-запись не нужна.
- Реестр шлюза `/opt/demo-gate/projects.json`, запись `rss-ai`: `upstream 127.0.0.1:8140`,
  тиры `client` (24 ч) и `owner` (720 ч), блок `costs` отсутствует — платных операций нет, квота не расходуется.
- Изменения реестра применяются через `gen_caddy.py --write` → `caddy validate` → `systemctl reload caddy`;
  `praktik-bot` читает реестр при старте, после правки его надо перезапустить.

## Решения и даты
- 22.11.2026 — перешли с CLI-скрипта на веб-версию: FastAPI отдаёт и страницу, и API, второй веб-сервер не нужен.
- 22.11.2026 — кэш новостей на 15 минут в памяти процесса: переводится до 10 заголовков за раз, повторный
  запрос не дёргает ни ленту, ни перевод. Кэш не переживает рестарт контейнера — для демо приемлемо.
- 22.11.2026 — порт 8120 заменён на 8140 в compose, `.env.example` и README: 8120 на VPS занят проектом
  `rag-company-docs`. Правило «один проект — один порт на обеих сторонах» соблюдено.
- 22.11.2026 — деплой через tar/scp, а не `git pull`: на сервере нет deploy key к GitHub.
- 22.11.2026 — лендинга нет: аноним видит страницу шлюза 401, приложение открывается по токену.
  Следующий шаг — статический лендинг в `landing/` и ключ `landing.root` в реестре.
- 22.11.2026 — `/api/news` отдаёт 502 с понятным текстом, если лента или перевод недоступны; частичных
  ответов нет (исключение ломает формирование кэша целиком).

## Бэклог
- Лендинг `landing/` с первым экраном, `privacy/`, `robots.txt`, `llms.txt`: аноним получает описание
  проекта вместо 401, приложение остаётся за токеном.
- `translate` — неофициальный клиент Microsoft Translator: при лимите или смене endpoint `/api/news`
  отвечает 502. Нужен второй провайдер перевода или локальная модель как fallback.
- Кэшировать неудачу на 60 с, чтобы при недоступном переводе не ходить в сеть на каждый запрос.
- Тестов на `app.py` нет: добавить проверку `/health` и `/api/news` с подменой `translate_to_ru`.
- `description` из ленты иногда приходит с HTML-тегами; сейчас выводится текстом в кавычках-экранировании,
  при необходимости чистить `html.unescape` + strip тегов на стороне API.