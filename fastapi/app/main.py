from typing import Union
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import json

from fastapi.responses import HTMLResponse, FileResponse
# import requests

from db import get_db
from model import User
from login import process_login   # login.pyから関数をインポート


# from voice import synthesize_voice
from voice_utils import create_voice_from_text

#グローバル変数
global convert_text #AIに渡すテキストをテスト用にグローバル変数に代入している変数。実装時にはこれをAI側に渡すよう変更

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

#バックエンド側で音声処理を行なっていた名残。記録として残しておく
@app.get("/get_voice", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("voice.html", {"request": request})

@app.post("/create_voice_from_text/")
async def create_voice_from_text_endpoint(text: str = Form(...)):
    convert_text = text
    return convert_text

#AIからのコメントを取得してhtml側に渡す（現在はcreate_voice_from_textのテキストを転送しているだけ）
@app.get("/responceAIcomment")
async def responceAIcomment():
    convert_text
    print(convert_text)
    return JSONResponse(content={"comment": convert_text})

#今後の作業：ルーティング（最初のアクセス時にloginへ飛ばし、その後結果に応じて各htmlへ遷移するようにする。管理者のみ要素が多いため、htmlの相互リンクを作る。）