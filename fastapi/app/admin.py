from typing import Union
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import session
from model import User



app = FastAPI()


@app.get("/dateExtraction")
def dateExtraction():
    from main import dateForm
    data: dict = Depends(dateForm)
    print(data+"test")
    # 抽出期間より、データベースに登録したものをAIを介して出力
    #AIデータを受け取る

    return data # 出力データを返す