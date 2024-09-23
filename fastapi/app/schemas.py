from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class LogoutRequest(BaseModel):
    token: str