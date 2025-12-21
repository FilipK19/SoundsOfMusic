from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from yt_dlp import YoutubeDL
from typing import Literal
import os

app = FastAPI()


# enables communication with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "noplaylist": is_music,  # 🔥 KEY LINE
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
            "creator": info.get("uploader"),
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


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/testYT")
def process_video(data: Url):
    try:
        return get_music_playlist(data.url, data.mode)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))