import os
import hmac
import hashlib
import json
import time
import httpx
from urllib.parse import parse_qsl
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from database import get_songs, get_song_by_id

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
app = FastAPI()

class WebAppData(BaseModel):
    init_data: str

class AudioRequest(BaseModel):
    init_data: str
    song_id: int

def validate_init_data(init_data: str):
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not configured")

    data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = data.pop("hash", None)

    if not received_hash:
        raise ValueError("Hash is missing")

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(data.items()))
    secret_key = hmac.new(b"WebAppData",BOT_TOKEN.encode(),hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key,data_check_string.encode(),hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("Invalid Telegram data")

    auth_date = int(data.get("auth_date", 0))

    if time.time() - auth_date > 86400:
        raise ValueError("Telegram data has expired")

    user = json.loads(data["user"])
    return user


@app.post("/songs")
def songs(web_app_data: WebAppData):
    try:
        user = validate_init_data(web_app_data.init_data)
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Invalid Telegram authentication data")

    user_id = user["id"]

    songs = get_songs(user_id)

    return [
        {
            "id": song[0],
            "file_id": song[1],
            "title": song[2],
            "duration": song[3]
        }
        for song in songs
    ]

@app.post("/audio")
async def play_audio(request: AudioRequest):
    try:
        user = validate_init_data(request.init_data)
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(status_code=401,detail="Invalid Telegram authentication data")

    song = get_song_by_id(user["id"], request.song_id)

    if song is None:
        raise HTTPException(status_code=404,detail="Song not found")

    file_id = song[1]

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",params={"file_id": file_id})

    if response.status_code != 200:
        raise HTTPException(status_code=502,detail="Failed to retrieve audio from Telegram")

    result = response.json()

    if not result.get("ok"):
        raise HTTPException(status_code=502,detail="Telegram could not retrieve the audio")

    file_path = result["result"]["file_path"]
    file_url = (f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}")

    async def audio_stream():
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", file_url) as audio_response:
                audio_response.raise_for_status()

                async for chunk in audio_response.aiter_bytes():
                    yield chunk

    return StreamingResponse(audio_stream(),media_type="audio/mpeg")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")import os
import hmac
import hashlib
import json
import time
from urllib.parse import parse_qsl
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from database import get_songs

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
app = FastAPI()

class WebAppData(BaseModel):
    init_data: str

def validate_init_data(init_data: str):
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not configured")

    data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = data.pop("hash", None)

    if not received_hash:
        raise ValueError("Hash is missing")

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(data.items()))
    secret_key = hmac.new(b"WebAppData",BOT_TOKEN.encode(),hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key,data_check_string.encode(),hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("Invalid Telegram data")

    auth_date = int(data.get("auth_date", 0))

    if time.time() - auth_date > 86400:
        raise ValueError("Telegram data has expired")

    user = json.loads(data["user"])
    return user


@app.post("/songs")
def songs(web_app_data: WebAppData):
    try:
        user = validate_init_data(web_app_data.init_data)
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid Telegram authentication data"
        )

    user_id = user["id"]

    songs = get_songs(user_id)

    return [
        {
            "id": song[0],
            "file_id": song[1],
            "title": song[2],
            "duration": song[3]
        }
        for song in songs
    ]


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
