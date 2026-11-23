# AI News — RSS-лента новостей об искусственном интеллекте

Небольшое веб-приложение показывает свежие публикации Wired об ИИ, переводит заголовки и описания на русский и открывает оригинал статьи по ссылке. Backend — FastAPI, интерфейс — обычные HTML/CSS/JavaScript.

## Запуск локально

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\uvicorn.exe app:app --reload --host 127.0.0.1 --port 8000
```

Откройте <http://127.0.0.1:8000>.

Лента задаётся переменной окружения `RSS_FEED_URL`; по умолчанию используется Wired AI RSS.

## Docker

```powershell
docker compose up --build -d
docker compose ps
```

Локально приложение будет доступно на <http://127.0.0.1:8140>. Проверка состояния: <http://127.0.0.1:8140/health>.

Остановить контейнер:

```powershell
docker compose down
```

## Размещение на VPS

Установите Docker Engine и Docker Compose plugin на Ubuntu VPS. Из PowerShell в корне проекта соберите архив только с нужными файлами и отправьте его на сервер:

```powershell
tar -czf rss-ai-deploy.tar.gz app.py rss_news.py requirements.txt Dockerfile docker-compose.yml .dockerignore .gitattributes .env.example web static
scp .\rss-ai-deploy.tar.gz ubuntu@109.66.243.108:/tmp/rss-ai-deploy.tar.gz
ssh ubuntu@109.66.243.108 "mkdir -p /opt/my_projects/rss-ai && tar -xzf /tmp/rss-ai-deploy.tar.gz -C /opt/my_projects/rss-ai && rm /tmp/rss-ai-deploy.tar.gz && cd /opt/my_projects/rss-ai && docker compose up -d --build"
```

Проверьте контейнер и health endpoint:

```bash
ssh ubuntu@109.66.243.108 'cd /opt/my_projects/rss-ai && docker compose ps && curl -fsS http://127.0.0.1:8140/health'
```

Контейнер слушает внутри порт 8000, а Compose публикует его только на `127.0.0.1:8140`. Порт 8120 на этом сервере занят проектом `rag-company-docs`, поэтому номер другой. Домен `rss-ai.praktik-ai.ru` уже резолвится на сервер через wildcard `*.praktik-ai.ru` — отдельная A-запись не нужна.

Публичный домен `https://rss-ai.praktik-ai.ru` предназначен для свободного доступа без регистрации. Лендинг опубликован владельцем отдельно от контейнера; кнопка «Открыть демо» ведёт на `/app/`. Чтобы этот маршрут работал, Caddy должен направлять `/app/` к FastAPI, а запросы приложения к `/api/news` и `/static/` — к контейнеру.

## Проверки

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py" -v
.\.venv\Scripts\python.exe -m py_compile rss_news.py app.py
docker build -t rss-ai:local .
```

Статический лендинг в каталоге `landing/` показывает открытый RSS-пример для сайта или компании; новости доступны бесплатно без регистрации, а кнопка «Открыть демо» ведёт на `/app/`.
