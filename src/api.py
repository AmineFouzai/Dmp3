from fastapi import FastAPI
from fastapi.responses import FileResponse
from middleware import wrap_middleware
import os
from core.dmp3 import DMP3
app=wrap_middleware(FastAPI())
from pydantic import BaseModel

class URL(BaseModel):
    url: str
    format:str
    
class File(BaseModel):
    filename: str

@app.post("/")
async def search(url: URL):
    dmp3=DMP3(url.url,url.format)
    meat_data=dmp3.download()
    return "type of response"

@app.get("/")
async def main(file):
    return FileResponse(f"./cache/{file}",media_type='application/octet-stream',filename=file)


    


    
    