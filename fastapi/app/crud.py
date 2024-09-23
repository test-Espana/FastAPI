from sqlalchemy.orm import Session
from model import User

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()

def delete_user_session(db: Session, token: str):
    # トークンに該当するセッションを検索
    session = db.query(User).filter(User.token == token).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False