import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv()

print(load_dotenv())

# 環境変数からデータベース接続情報を取得
host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# MySQL のデータベース接続URL
DATABASE = 'mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8' % (
    user,
    password,
    host,
    db_name,
)

ENGINE = create_engine(
    DATABASE,
    echo=True  # デバッグ用にSQLログを表示
)

# セッションの設定
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)


# セッションを生成する関数
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

        
# Base クラスの設定
Base = declarative_base()
Base.query = session.query_property()

