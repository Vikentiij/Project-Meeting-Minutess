from turtle import title
from typing import Union
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates= Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": "id"})


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("index.html",{"request": request, "id": id})

@app.get("/login/notices")
async def notices(limit=10, published: bool = True, sort: Optional [str]=None):
    # only get 10 published blogs
    if published:
        return{"data":f"{limit} published notices from the db"}
    else:
        return{"data":f"{limit} notices from the db"}
@app.get("/login/{id}")
async def login(id: int):
    return {"data": id}

@app.get("/login/{id}/notice")
async def notice(id, limit=10):
    # fetch notice of login with id=id
    return {"data":{"1","2"}}



class Meeting(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/meeting")
async def create_meeting(request: Meeting):    #or meeting: Meeting
    return{"data": f"Meeting is created with title {request.title}"}



@app.get("/about")
async def about():
    return {"data":{"adout page"}}


# if_name_ = "_main_":
#   uvicorn.run(app, host="127.0.0.1", port=9000)   for debgginf porpose (python3 main.py)