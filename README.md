# Project SoundsOfMusic
A simple project that enables users to download music using the yt-dlp downloader. 

## Tech Stack
- **Frontend:** Angular with TypeScript, HTML and CSS
- **Backend:** FastAPI in Python, served with Uvicorn

## Features
- Download single songs
- Download entire playlists
- Song and playlist info after download
- Library of downloaded songs

## Prerequisites
- **Node.js** (v22+)
- **Angular CLI** (v21+)
- **Python** (v3.13+)
- **FastAPI**
- **Uvicorn**

## Dependencies
- This project uses yt-dlp, a feature-rich command-line audio/video downloader (Link: https://github.com/yt-dlp/yt-dlp). It can be installed using pip: ```python -m pip install yt-dlp```
- To download music in mp3 format FFmpeg is required (Link: https://www.ffmpeg.org/). It can be downloaded [here](https://www.ffmpeg.org/download.html) and needs to be added to PATH (Windows Environment Variables).

## Installation
- In any terminal: ```git clone https://github.com/FilipK19/SoundsOfMusic.git```
- Backend:
  - In project folder:  ```cd backend```
  - To start: ```python -m uvicorn main:app --reload --port 8000```
- Frontend:
  - In project folder: ```cd frontend```
  - Install dependencies: ```npm install```
  - Run the app:  ```ng serve```
