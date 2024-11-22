from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from modules.user.api import user_router
from modules.feed.api import feed_router

BASE_DIR = Path(__file__).parent
static_folder = "static"

app = FastAPI()
app.mount(f"/static", StaticFiles(directory=static_folder), name="static")

app.include_router(user_router, prefix="/user")
app.include_router(feed_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
