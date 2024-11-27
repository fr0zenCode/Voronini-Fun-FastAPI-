from fastapi import FastAPI

from api import comments_router


app_comments = FastAPI()
app_comments.include_router(comments_router)
