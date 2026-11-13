# Eiva Userbot

Eiva is a Telegram userbot built with Python and Telethon. It loads command plugins from `Eivabot/plugins` and assistant modules from `Eivabot/assistant`.

## Requirements

- Python 3.11
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A user session string for the account that will run the userbot
- PostgreSQL and MongoDB only for features that use those databases

The project automates actions on a Telegram account. Use it only with an account you control and respect Telegram limits and policies.

## Local setup

```sh
git clone https://github.com/TeamEiva/Eiva-Userbot.git
cd Eiva-Userbot
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env
```

Fill the required variables in `.env`: `APP_ID`, `API_HASH`, `EivaBOT_SESSION`, and `BOT_TOKEN`. Keep `.env` private and never commit session strings or tokens. `BOT_USERNAME` is optional and is not used for authentication.

Generate a user session with `python Eiva_string.py`. The script authenticates interactively; protect its output as a password. Set the resulting session string as `EivaBOT_SESSION` and remove it from shell history or temporary files.

Run the application with `python -m Eivabot` (or `./start.sh` on Linux/macOS). The process validates required configuration before connecting. Plugin import failures are logged and do not stop other plugins from loading.

## Databases

SQL-backed features use local SQLite (`eiva.db`) by default. Set `DATABASE_URL` to a SQLAlchemy-supported PostgreSQL URL for a persistent remote database. Set `MONGO_DB_URL` to enable MongoDB-backed features. MongoDB is optional; its connection is tested with a bounded timeout when configured. Database initialization errors are logged; features requiring an unavailable database may not work.

## Docker

Build and run from this repository directory:

```sh
docker build -t eiva-userbot .
docker run --env-file .env --restart unless-stopped eiva-userbot
```

Provide persistent storage for the Telethon session file if you use file-based sessions. A string session is stored in the environment. Do not bake credentials into the image.

## Railway or another container host

Deploy from the repository using the Dockerfile and configure the same environment variables as `.env`. The platform must support a persistent long-running process and outbound Telegram connections. Database services are optional unless a feature needs them. The old Railway template and Heroku deployment references have been removed because this checkout does not include or validate those deployment definitions.

## Troubleshooting

- **Missing required configuration:** Set `APP_ID`, `API_HASH`, `EivaBOT_SESSION`, and `BOT_TOKEN`.
- **Invalid API credentials or session:** Generate a fresh session with the intended Telegram account and verify credentials at my.telegram.org.
- **Database initialization failed:** Check the URL, network access, and database availability. The app can start without optional database URLs.
- **Plugin failed to load:** Check the logged module name and traceback; other plugins continue loading.
- **Missing system tools:** Media and image commands may require the binaries installed in the Docker image (FFmpeg, ImageMagick, Tesseract, and MediaInfo).

## Tests and verification

Run `python -m unittest discover -s tests` for source-level sanity checks and `python -m compileall -q Eivabot mongo_database` for compilation. Live Telegram authentication and remote database connectivity require configured credentials and services; they are not covered by these local checks.
