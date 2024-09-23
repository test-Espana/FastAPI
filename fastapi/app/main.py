from typing import Union
from fastapi import FastAPI, Request, Form, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

from fastapi.responses import HTMLResponse, FileResponse,JSONResponse
# import requests

from db import get_db
from model import User
from login import process_login   # login.pyから関数をインポート
from admin import dateExtraction

# from voice import synthesize_voice
from voice_utils import create_voice_from_text


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():

    return {"こんにちは": "世界"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

#　ユーザー情報一覧取得
@app.get("/users")
def get_user_list():
    users = session.query(User).all()
    return users

# templatesの中にある.htmlファイルを表示する
@app.get("/show")
def show_template(request: Request):
    context = {"request": request, "message": "Hello FastAPI with Jinja2!"}
    return templates.TemplateResponse("index.html", context)

# templatesの中にある.htmlを表示
# @app.get("/test")
# def test():
#     # "こんにちは" を testdatashow に渡して、その戻り値を返す
#     return {"message": testdatashow("こんにちは")}

# templatesの中にある.htmlを表示
###########loginに関する関数##############

# templatesの中にある.htmlを表示
@app.get("/login")
def login(request: Request):
    
    context = {"request": request}
    return templates.TemplateResponse("Login.html", context)

# @app.post("/submit")
# def login_info(username: str = Form(...), password: str = Form(...)):
#     # ログイン処理をここに実装
#     return {"username": username, "password": password}


# POSTでユーザー名とパスワードを受け取って、login.pyで処理する
@app.post("/submit")
def login_check(username: str = Form(...), password: str = Form(...), admin: bool = Form(False),db: Session = Depends(get_db)):
    # ログイン処理をlogin.pyのprocess_loginに移譲
    print("username:",username)
    print("password:",password)
    print("admin:",admin)
    result = process_login(username, password, db)
    return result

# @app.post("/submit")
# def login_info(username: str = Form(...), password: str = Form(...)):
#     # ログイン処理をここに実装
#     return {"username": username, "password": password}


# POSTでユーザー名とパスワードを受け取って、login.pyで処理する
@app.post("/submit")
def login_check(username: str = Form(...), password: str = Form(...), admin: bool = Form(False),db: Session = Depends(get_db)):
    # ログイン処理をlogin.pyのprocess_loginに移譲
    print("username:",username)
    print("password:",password)
    print("admin:",admin)
    result = process_login(username, password, db)
    return result

#バックエンド側で音声処理を行なっていた名残。記録として残しておく
# @app.get("/get_voice", response_class=HTMLResponse)
# async def get_form(request: Request):
#     return templates.TemplateResponse("voice.html", {"request": request})
# @app.post("/create_voice_from_text/")
# async def create_voice_from_text_endpoint(text: str = Form(...)):
#     return await create_voice_from_text(text)


#########admin機能に関する関数############
@app.get("/admin")
def admin(request: Request):
    context = {"request": request, "message": "Hello FastAPI with Jinja2!"}
    return templates.TemplateResponse("admin.html", context)

class DateForm(BaseModel):
    startDate: date
    endDate: date

# POSTリクエストで日付データを受け取るエンドポイント
@app.post("/dateForm")
async def handle_date_form(request: Request):
   form_data = await request.form()
   startDate = form_data.get("startDate")
   endDate = form_data.get("endDate")
   return {"message":"日付範囲が送信されました"}

@app.get("/download_report")
def download_report(startDate: date = Query(...), endDate: date = Query(...)):
    print(startDate)
    print(type(startDate))
    print(endDate)
    print(type(endDate))
    return {"admin": "download_report", "startDate": startDate, "endDate": endDate}

@app.get("/sns_output")
def sns_output(startDate: date = Query(...), endDate: date = Query(...)):
    print(startDate)
    print(type(startDate))
    print(endDate)
    print(type(endDate))
    return {"admin": "sns_output", "startDate": startDate, "endDate": endDate}

@app.get("/delete_history")
def delete_history(startDate: date = Query(...), endDate: date = Query(...)):
    return {"admin": "delete_history", "startDate": startDate, "endDate": endDate}