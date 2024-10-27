import uvicorn
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")


class Post(BaseModel):
    author: str
    text: str


@app.get("/")
def foo_get(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/get-post")
def foo(request: Request, author: str = Form(...), text: str = Form(...)):
    return templates.TemplateResponse(request=request, name="post.html", context={"author": author, "text": text})


@app.get("/feed")
def get_feed():
    ...


@app.get("/authorization")
def authorization_page():
    ...


@app.get("/user-cabinet")
def user_cabinet():
    ...


@app.get("/secret-page")
def casino_page():
    ...


@app.get("detail-seria-info")
def detail_seria_info():
    ...


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
