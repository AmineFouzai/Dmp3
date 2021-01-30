from fastapi import FastAPI,Request
from fastapi.responses import FileResponse
from middleware import wrap_middleware
from youtube_dl import DownloadError
import os
from core.dmp3 import DMP3
app=wrap_middleware(FastAPI())
from pydantic import BaseModel

class URL(BaseModel):
    url: str
    format:str

@app.post("/")
async def search(url: URL,request:Request):
    dmp3=DMP3(url.url,url.format)
    meta_data=dmp3.download()
    if type(meta_data) is DownloadError:
        return {
            "error":"cant extract video or audio from url"
        }
    return {
    "url":f"https://dmp3-server.herokuapp.com/?file={meta_data['id']}.mp3"
    }if dmp3.format_type=="mp3"else {
        "url":f"https://dmp3-server.herokuapp.com/?file={meta_data['id']}.mp4" 
    }

@app.get("/")
async def main(file):
    return FileResponse(f"./cache/{file}",media_type='application/octet-stream',filename=file)


    


    
    
