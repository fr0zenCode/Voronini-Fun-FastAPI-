import uvicorn
from fastapi import FastAPI
from modules.user.api import user_router


app = FastAPI()
app.include_router(user_router, prefix="/user")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
