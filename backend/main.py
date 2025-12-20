from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from yt_dlp import YoutubeDL
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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/testYT")
def process_video(data: Url):
    #url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    # Output folder
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": False,  # DOWNLOAD the file
            "format": "bestaudio/best",
            "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
            "noplaylist": True,

            # Convert to MP3
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)

        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "file_saved_as": info.get("title") + ".mp3",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/testYT2")
def process_video(data: Url):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    try:
        ydl_opts = {
            "quiet": True,
            "format": "bestaudio/best",
            "outtmpl": f"{output_dir}/%(playlist_title|single)s/%(title)s.%(ext)s",
            "noplaylist": False,

            # Convert to MP3
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)

        # Playlist
        if "entries" in info:
            songs = []
            total_duration = 0

            for entry in info["entries"]:
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

    


    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))