from typing import Union
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db
from model import User
from login import process_login   # login.pyから関数をインポート


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