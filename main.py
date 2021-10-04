import os
from fastapi import FastAPI, File, UploadFile, Query
from dedup import splitBlocks
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dedup.userlogin import register_user
from fastapi import APIRouter
from fastapi import Request
from dedup.userlogin import check_user_exist
from Database.base import engine



conn = engine.connect()

app = FastAPI(title="Image_Deduplication", version="1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@app.get("/")
def read_root():
    return {"Hello": "World of Image Deduplication"}


@app.get("/Home/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})


@app.get("/register/")
def user_register(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})


@app.post('/register/')
def register(username: str, email: str, password: str):
    user_exist = check_user_exist(username)
    if user_exist:
        return "username already exist, please choose another"
    else:
        register_user(username, email, password)


@app.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})


@app.post('/login/')
def login(username : str, password:str):
    user_exist = check_user_exist(username)
    if user_exist:
        return {"status","Login Successful Access Granted"}
    else:
        return{"status","Login error Access not Granted"}


@app.get("/updownload/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("updownload.html", {"request": request})


@app.post("/imageDeDuplication/")
async def image_de_duplication(file: UploadFile = File(...)):
    filename = file.filename
    blocks = splitBlocks.split_blocks(await file.read(), filename)
    #print("blocks from input", blocks)
    return blocks


@app.get("/image_download/")
async def image_download(request:Request, _q: str = Query("bird", enum=["bird.jpg","bir.jpg", "bird1.png","bir1.png", "lena.tiff","lena1.tiff", "dedup.jpg","dedup1.jpg", "flower.jpg","flower1.jpg","dedup2.tiff","dolphin.jpg","dolphin1.jpg","sun.jpg","sun1.jpg","wheel.png","wheel1.png"])):
    print("Selected from drop down:", _q)
    splitBlocks.download(_q)



