from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from urllib.parse import urlparse

from yt_dlp import YoutubeDL
from typing import Literal
import os

app = FastAPI()

DOWNLOAD_DIR = "downloads"

# enables communication with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

class Url(BaseModel):
    url:str
    mode: Literal["music", "playlist"]


def get_music_playlist(url: str, mode: str) -> dict:
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    is_music = mode == "music"

    ydl_opts = {
        "quiet": True,
        "skip_download": False,
        "format": "bestaudio/best",
        "noplaylist": is_music,
        "outtmpl": (
            f"{output_dir}/%(title)s.%(ext)s"
            if is_music
            else f"{output_dir}/%(playlist_title|single)s/%(title)s.%(ext)s"
        ),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    # MUSIC (single)
    if is_music:
        return {
            "type": "music",
            "title": info.get("title"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "file_saved_as": f"{info.get('title')}.mp3",
        }

    # PLAYLIST
    songs = []
    total_duration = 0

    for entry in info.get("entries", []):
        if not entry:
            continue

        duration = entry.get("duration") or 0
        total_duration += duration

        songs.append({
            "title": entry.get("title"),
            "duration": duration,
        })

    return {
        "type": "playlist",
        "playlist_title": info.get("title"),
        "creator": info.get("uploader"),
        "songs": songs,
        "total_duration": total_duration,
        "videos": len(songs),
    }

def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/testYT")
async def process_video(data: Url):
    if not is_valid_url(data.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:
        result = await run_in_threadpool(
            get_music_playlist,
            data.url,
            data.mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/music")
def list_music():
    files = []

    if os.path.exists(DOWNLOAD_DIR):
        # Walk through all files/folders recursively
        for root, dirs, filenames in os.walk(DOWNLOAD_DIR):
            for file in filenames:
                if file.endswith(".mp3"):
                    rel_dir = os.path.relpath(root, DOWNLOAD_DIR)
                    playlist = None if rel_dir == "." else rel_dir

                    files.append({
                        "name": file,
                        "url": f"/downloads/{rel_dir}/{file}" if playlist else f"/downloads/{file}",
                        "playlist": playlist
                    })
    return files