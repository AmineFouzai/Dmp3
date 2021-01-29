import sys
sys.path.insert(0,"./src/")
from fastapi.staticfiles import StaticFiles
from api import app
app.mount("/static", StaticFiles(directory="cache"), name="static")
