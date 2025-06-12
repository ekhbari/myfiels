from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TikTok Downloader API"}

@app.get("/download")
def download_tiktok(url: str = Query(..., description="TikTok video URL")):
    if "tiktok.com" not in url:
        return JSONResponse(content={"error": "Invalid TikTok URL"}, status_code=400)

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': False,
        'extract_flat': False,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url") or info["formats"][0]["url"]
            title = info.get("title", "TikTok Video")
            return {
                "title": title,
                "video_url": video_url,
                "thumbnail": info.get("thumbnail"),
                "uploader": info.get("uploader"),
            }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
