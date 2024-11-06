import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from modules.user.api import user_router

static_folder = "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_folder), name="static")

app.include_router(user_router, prefix="/user")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
