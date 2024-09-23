from typing import Union
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db import get_db
from schemas import UserLogin
from crud import get_user_by_username

app = FastAPI()

# # `process_login` をスキーマと CRUD を使用するように更新
# def process_login(user: UserLogin, db: Session):
#     username = user.username
#     password = user.password
    
#     # ユーザー名でデータベースからユーザーを取得
#     db_user = get_user_by_username(db, username)
    
#     if db_user and db_user.password == password and db_user.admin:
#         # Adminログイン成功時のリダイレクト
#         return RedirectResponse(url='/admin', status_code=303)
#     elif db_user and db_user.password == password:
#         # 一般ログイン成功時のリダイレクト
#         return RedirectResponse(url='/talk_screen', status_code=303)
#     else:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return process_login(user, db)



# from typing import Union
# from fastapi import FastAPI, Request, Form,Depends
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from db import session
# from model import User
# # from main import login_inf


# app = FastAPI()

# # ユーザー名でユーザー情報を取得する関数
# def get_user_by_username(db, username: str):
#     user=db.query(User).filter(User.name == username).first()
#     print(user)
#     print("ユーザー名でユーザー情報を取得")
#     print(user.name)
#     print(user.password)
#     print(user.admin)
#     return user

# # main.pyからのログイン情報を受け取り、Userテーブルと照合してログイン可否を返す
# def process_login(username: str, password: str, db):
#     # ユーザー名でデータベースからユーザーを取得
#     user = get_user_by_username(db, username)
    
    
#     if user and user.password == password and bool(user.admin) == True:
#         print("管理者ログイン成功")
#         return {"message": "Admin Login successful"}
#     elif user and user.password == password:
#         print("ログイン成功")
#         return {"message": "Login successful"}
#     else:
#         print("ログイン失敗")
#         return {"message": "Login failed"}