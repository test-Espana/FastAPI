from typing import Union
from fastapi import FastAPI, Request, Form, Depends, Query,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse, FileResponse,JSONResponse, RedirectResponse
# import requests
from datetime import date
from pydantic import BaseModel
from schemas import UserLogin

from db import get_db
from model import User
# from login import process_login   
from admin import dateExtraction
from typing import Optional, Dict

from sqlalchemy.orm import Session
from db import get_db
from schemas import UserLogin, LogoutRequest
from crud import get_user_by_username,delete_user_session

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
    return templates.TemplateResponse("test.html", context)

def get_user_from_token(token: str):
    # トークンからユーザー情報を取得する（例: トークンが無効であればNoneを返す）
    return tokens.get(token, None)

def require_authentication(request: Request):
    token = request.query_params.get('token')
    if not token or not get_user_from_token(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated"
        )

tokens: Dict[str, dict] = {}

# templatesの中にある.htmlを表示
@app.get("/login")
def login(request: Request):
    
    context = {"request": request}
    return templates.TemplateResponse("login.html", context)

def process_login(user: UserLogin, db: Session, request: Request):
    username = user.username
    password = user.password
    
    # ユーザー名でデータベースからユーザーを取得
    db_user = get_user_by_username(db, username)
    
    if db_user and db_user.password == password and db_user.admin:
        token = "some_unique_token" 
        tokens[token] = {"name": db_user.name, "user_id": db_user.id}
        # Adminログイン成功時のリダイレクト
        return show_admin(request, db_user.name, db_user.id)
    elif db_user and db_user.password == password:
        token = "some_unique_token"  # ユニークなトークンを生成
        tokens[token] = {"name": db_user.name, "user_id": db_user.id}
        # 一般ログイン成功時のリダイレクト
        return talk_screen(request, db_user.name, db_user.id)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    # ログアウト処理（ここではトークン削除など）
    # 省略...

    # ログイン画面にリダイレクト
    return RedirectResponse(url="/login")

# POSTでユーザー名とパスワードを受け取って、login.pyで処理する
@app.post("/submit")
def submit_login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = UserLogin(username=username, password=password)
    result = process_login(user, db, request)
    return result
    

conversations = [
    {"sender": "AI", "message": "こんにちは！今日は晴れていますが、少し風が強いです。"},
    {"sender": "You", "message": "ありがとう、今日の予定にぴったりだ！"},
    {"sender": "AI", "message": "それは良かったです！素敵な一日を過ごしてください。"},
    {"sender": "AI", "message": "今日は気温が高いので熱中症に注意してください。"}
]

@app.get("/talk_screen", response_class=HTMLResponse)
def talk_screen(request: Request, name: str, user_id: int):
    context = {
        "request": request,
        "name": name,
        "user_id": user_id,
        "conversations": conversations
    }
    return templates.TemplateResponse("talk_screen.html", context)

# ここからadmin これプラス admin.js admin.html

# @app.get("/admin", response_class=HTMLResponse)
# def admin(request: Request, name: Optional[str] = None, user_id: Optional[str] = None):
#     return templates.TemplateResponse("admin.html", {"request": request, "name": name, "user_id": user_id})
@app.get("/admin")
def show_admin(request: Request, name:str,user_id:int):
    context = {
        "request": request,
        "name": name,
        "user_id": user_id,
        "message": "Hello FastAPI with Jinja2!"
    }
    return templates.TemplateResponse("admin.html", context)

@app.post("/dateForm")
async def handle_date_form(request: Request):
    form_data = await request.form()
    start_date = form_data.get("startDate")
    end_date = form_data.get("endDate")
    # 期間に基づいた処理を行う
    return {"message": "日付範囲が送信されました"}

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

@app.get("/voiceop")
def show_voice_output(request: Request):
    context = {"request": request, "message": "Hello voice"}
    return templates.TemplateResponse("voiceOP.html", context)