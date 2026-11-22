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

Публичный HTTPS-доступ выдаёт общий шлюз `demo-gate`, а не контейнер. Регистрация проекта на сервере:

```bash
# строка в /opt/demo-gate/projects.json
#  "rss-ai": {"title": "AI News", "host": "https://rss-ai.praktik-ai.ru",
#             "upstream": "127.0.0.1:8140",
#             "tiers": {"client": {"ttl_h": 24}, "owner": {"ttl_h": 720}}}
python3 /opt/demo-gate/gen_caddy.py --write
sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl reload caddy
python3 /opt/demo-gate/gate.py grant --project rss-ai --tier client   # выдаёт ссылку ?k=
```

Анонимный запрос без cookie получает `401 «Нужен доступ»` — это норма; приложение открывается по ссылке `?k=`, выданной `gate.py grant`. Платные операции у проекта отсутствуют, поэтому `costs` в реестре не заданы и квота не расходуется.

## Проверки

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py" -v
.\.venv\Scripts\python.exe -m py_compile rss_news.py app.py
docker build -t rss-ai:local .
```

Статический лендинг демо находится в каталоге `landing/`: главная страница, политика конфиденциальности, локальные изображения и шрифты, SEO-файлы и форма заявки на доступ.
