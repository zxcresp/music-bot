# Telegram Music Mini App

A personal music library built as a Telegram Mini App with a Python backend.

> **Work in Progress**
>
> This project is currently under active development. The current version is an MVP, and many planned features have not been implemented yet.

## About

The project allows users to send audio files to a Telegram bot and store information about their music library.

The Telegram Mini App retrieves the user's songs and displays them in a simple web-based music library.

Each user's music library is separated using their Telegram `user_id`.

## Current Features

* Receive audio files through a Telegram bot
* Store music metadata in SQLite
* Separate music libraries for different Telegram users
* Store song title, Telegram `file_id`, duration, and user ID
* View uploaded songs using the `/songs` command
* FastAPI backend
* Telegram Mini App frontend
* Server-side validation of Telegram Web App `initData`
* HTTPS access during development using Cloudflare Tunnel
* Basic music library interface

## Currently in Development

The project is not finished yet.

Planned features include:

* Audio playback
* Play and pause controls
* Seek and progress bar
* Volume control
* Next and previous track
* Shuffle
* Repeat
* Music search
* Track deletion
* Favorites
* Playlists
* Album covers and additional metadata
* Improved UI/UX
* Production deployment
* Stable domain and permanent backend hosting

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* SQLite
* pyTelegramBotAPI
* python-dotenv

### Frontend

* HTML
* CSS
* JavaScript
* Telegram Web Apps API

### Development

* Cloudflare Tunnel
* Git
* GitHub

## Project Structure

```
Music Bot/
├── main.py
├── database.py
├── app.py
├── .env.example
├── .gitignore
├── README.md
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

The SQLite database (`music.db`) is generated automatically and is not included in the repository.

## Installation

### 1. Clone the repository

```
git clone https://github.com/zxcresp/music-bot.git
cd music-bot
```

### 2. Create a virtual environment

```
python -m venv .venv
```

On Windows:

```
.venv\Scripts\activate
```

### 3. Install dependencies

```
pip install pyTelegramBotAPI python-dotenv fastapi uvicorn
```

### 4. Configure environment variables

Paste your Telegram Bot API token into the .env file.

The file should contain your Telegram bot token:

```
BOT_TOKEN=your_telegram_bot_token
```

### 5. Start the Telegram bot

```
python main.py
```

### 6. Start the FastAPI server

In another terminal:

```
uvicorn app:app --reload
```

The application will be available locally at:

```
http://127.0.0.1:8000
```

## Telegram Mini App

During development, the Mini App can be exposed to the internet using Cloudflare Tunnel:

```
.\cloudflared-windows-amd64.exe tunnel --url http://127.0.0.1:8000
```

Cloudflare will provide a temporary HTTPS URL.

This URL can then be configured as the Telegram bot's Menu Button through BotFather.

Cloudflare Quick Tunnels are intended for development and testing. The public URL can change when the tunnel is restarted.

## Security

Telegram Web App `initData` is validated on the server using HMAC-SHA256 before accessing a user's music library.

The bot token is stored only in the local `.env`

## Database

The project currently uses SQLite.

The `songs` table contains:

```
id
user_id
file_id
title
duration
```

The database is created automatically when the bot starts.

## Current Status

The current MVP can:

1. Receive an audio file through Telegram.
2. Extract its filename and duration.
3. Save the song metadata to SQLite.
4. Associate the song with the Telegram user.
5. Open the Telegram Mini App.
6. Authenticate the Telegram user on the backend.
7. Retrieve and display the user's songs.

Actual audio playback is not implemented yet.

## Roadmap

```
[x] Telegram bot
[x] Audio upload
[x] SQLite database
[x] User-specific music library
[x] FastAPI backend
[x] Telegram Web App authentication
[x] Mini App frontend
[x] Cloudflare Tunnel development setup

[ ] Audio playback
[ ] Player controls
[ ] Search
[ ] Favorites
[ ] Playlists
[ ] Track management
[ ] Improved UI
[ ] Stable deployment
[ ] Production-ready storage
```

## License

This project is currently under development. Licensing information may be added later.
