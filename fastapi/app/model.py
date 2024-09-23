from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from db import Base
from db import ENGINE

# テーブル定義
class User(Base):
    __tablename__ = 'users'  # テーブル名と一致させる

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    admin = Column(Boolean, nullable=False,default=False)

# モデル定義 
class TestUser(BaseModel):
    id: int
    name: str
    password: str
    admin: bool