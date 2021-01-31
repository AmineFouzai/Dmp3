from youtube_dl import YoutubeDL
import re 
import requests
import urllib.request
from tqdm import tqdm
import os
class TqdmUpTo(tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            return self.update(b * bsize - self.n)

class DMP3(object):
    
    def __init__(self,url,format_type):
        self.url=url
        self.format_type=format_type
        if format_type=="mp3":
            self.ydl=YoutubeDL({
                        'format': 'bestaudio/best',
                        'outtmpl': './cache/%(id)s.%(ext)s',
                        'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }],
                        }) 
        else:
            self.ydl=YoutubeDL({"outtmpl": './cache/%(id)s.%(ext)s','format':'137'})
        

    def download(self):
        try:
            if "facebook" in self.url:
                soup=requests.get(self.url)
                with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,desc=self.url.split('/')[-1]) as tqdm:
                    try:
                        self.url=re.search('hd_src:"(.+?)"',soup.text)[1]
                    except:
                        self.url=re.search('sd_src:"(.+?)"',soup.text)[1]
                    if self.format_type=="mp3":
                        filename="download.mp3"
                        fullfilename = os.path.join(os.getcwd()+"\cache", filename)
                    else:
                        filename="download.mp4"
                        fullfilename = os.path.join(os.getcwd()+"\cache", filename)
                    urllib.request.urlretrieve(self.url,fullfilename,tqdm.update_to,data=None)
                    tqdm.total = tqdm.n
                return {"id":"download"}
            else:
                with self.ydl:
                    result=self.ydl.extract_info(
                        self.url, 
                        download=True)
               
                return  {"id":result['id']}
        except Exception as e:
            return e
